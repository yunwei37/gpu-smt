// Declared Linux runtime extension, not a stock Lean shutdown API.
// Startup is identical to Lean4.21 initialize_libuv except that the thread
// is joinable and retained. Stop refuses every other handle/request.
#include <lean/lean.h>
#include "runtime/uv/event_loop.h"
#include "runtime/thread.h"
#include "runtime/stack_overflow.h"
#include <pthread.h>
#include <cerrno>

namespace lean {
void initialize_libuv_timer();
void initialize_libuv_tcp_socket();
void initialize_libuv_udp_socket();
size_t get_max_heartbeat();
void set_max_heartbeat(size_t);
}

static pthread_t event_thread;
static bool event_thread_live = false;
static size_t event_heartbeat;

static void *event_main(void *) {
    // Same thread entry obligations as pinned runtime/thread.cpp.
    lean::stack_guard guard;
    lean::lean_initialize_thread();
    lean::set_max_heartbeat(event_heartbeat);
    lean::event_loop_run_loop(&lean::global_ev);
    lean::lean_finalize_thread();
    return nullptr;
}

static int start_event_thread() {
    pthread_attr_t attr;
    int error = pthread_attr_init(&attr);
    if (error) return error;
    error = pthread_attr_setstacksize(&attr, lean::lthread::get_thread_stack_size());
    if (!error) {
        event_heartbeat = lean::get_max_heartbeat();
        error = pthread_create(&event_thread, &attr, event_main, nullptr);
    }
    pthread_attr_destroy(&attr);
    if (!error) event_thread_live = true;
    return error;
}

extern "C" void __wrap_initialize_libuv() {
    lean::initialize_libuv_timer();
    lean::initialize_libuv_tcp_socket();
    lean::initialize_libuv_udp_socket();
    lean::initialize_libuv_loop();
    if (start_event_thread()) lean_internal_panic("prepared native UV thread initialization failed");
}

struct HandleCount { unsigned own = 0; unsigned other = 0; };
static void count_handles(uv_handle_t *handle, void *data) {
    auto *counts = static_cast<HandleCount *>(data);
    if (handle == reinterpret_cast<uv_handle_t *>(&lean::global_ev.async)) ++counts->own;
    else ++counts->other;
}

int prepared_uv_stop() {
    if (!event_thread_live) return EINVAL;
    auto &ev = lean::global_ev;
    // Task manager is still present through UV callback/TLS cleanup.
    lean::event_loop_lock(&ev);
    HandleCount count;
    uv_walk(ev.loop, count_handles, &count);
    auto *async = reinterpret_cast<uv_handle_t *>(&ev.async);
    if (count.own != 1 || count.other || uv_is_closing(async)) {
        lean::event_loop_unlock(&ev);
        return EBUSY;
    }
    uv_unref(async);
    bool other_work = uv_loop_alive(ev.loop);
    uv_ref(async);
    if (other_work) {
        lean::event_loop_unlock(&ev);
        return EBUSY;
    }
    // Closing the only idle handle lets the stock outer loop terminate.
    // No callback containing Lean values is fabricated or discarded.
    uv_close(async, nullptr);
    lean::event_loop_unlock(&ev);
    int error = pthread_join(event_thread, nullptr);
    if (!error) event_thread_live = false;
    return error;
}

int prepared_uv_restart(bool child) {
    if (event_thread_live) return EINVAL;
    auto &ev = lean::global_ev;
    // Official libuv requires this before ANY child loop API after fork.
    if (child) {
        int error = uv_loop_fork(ev.loop);
        if (error) return -error;
    }
    int error = uv_async_init(ev.loop, &ev.async, nullptr);
    if (error) return -error;
    return start_event_thread();
}
