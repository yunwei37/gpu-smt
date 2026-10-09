// Explicit runtime extension for pinned Lean4.21 Linux lthread workers.
// Retain requested-detached owned workers until their original callback AND
// pthread TLS cleanup can be joined. Foreign callbacks/attributes are untouched.
#include <lean/lean.h>
#include <pthread.h>
#include <cerrno>
#include <cstdlib>

extern "C" int __real_pthread_create(pthread_t *, const pthread_attr_t *, void *(*)(void *), void *);
extern "C" int __real_pthread_detach(pthread_t);
extern "C" int __real_pthread_join(pthread_t, void **);
// Exact source-native callback symbol verified in the pinned runtime archive.
extern "C" void *lean_worker_entry(void *) asm("_ZN4lean7lthread3imp5_mainEPv");

struct Worker {
    Worker *next;
    pthread_t thread;
    void *(*entry)(void *);
    void *argument;
    bool published, detached_requested, returned, claimed;
};
static pthread_mutex_t registry_mutex = PTHREAD_MUTEX_INITIALIZER;
static Worker *workers = nullptr;

static Worker *find_worker(pthread_t thread) {
    for (Worker *r = workers; r; r = r->next)
        if (r->published && pthread_equal(r->thread, thread)) return r;
    return nullptr;
}

static void remove_worker(Worker *record) {
    Worker **p = &workers;
    while (*p && *p != record) p = &(*p)->next;
    if (*p) *p = record->next;
}

static void *worker_main(void *data) {
    Worker *record = static_cast<Worker *>(data);
    // Forward ORIGINAL callback/argument; it retains Lean's stack/TLS/heartbeat
    // setup and cleanup. No registry lock or Lean allocation in this trampoline.
    void *value = record->entry(record->argument);
    pthread_mutex_lock(&registry_mutex);
    record->returned = true;
    pthread_mutex_unlock(&registry_mutex);
    return value;
}

extern "C" int __wrap_pthread_create(pthread_t *thread, const pthread_attr_t *attr,
                                      void *(*entry)(void *), void *argument) {
    int detached = PTHREAD_CREATE_JOINABLE;
    if (entry != lean_worker_entry ||
        (attr && pthread_attr_getdetachstate(attr, &detached)) || detached != PTHREAD_CREATE_JOINABLE)
        return __real_pthread_create(thread, attr, entry, argument);
    Worker *record = static_cast<Worker *>(std::calloc(1, sizeof(Worker)));
    if (!record) return ENOMEM;
    record->entry = entry;
    record->argument = argument;
    pthread_mutex_lock(&registry_mutex);
    record->next = workers;
    workers = record;
    pthread_mutex_unlock(&registry_mutex);
    int error = __real_pthread_create(thread, attr, worker_main, record);
    pthread_mutex_lock(&registry_mutex);
    if (error) remove_worker(record);
    else {
        record->thread = *thread;
        record->published = true;
    }
    pthread_mutex_unlock(&registry_mutex);
    if (error) std::free(record);
    return error;
}

extern "C" int __wrap_pthread_detach(pthread_t thread) {
    pthread_mutex_lock(&registry_mutex);
    Worker *record = find_worker(thread);
    if (record && !record->claimed) record->detached_requested = true;
    bool owned = record != nullptr;
    pthread_mutex_unlock(&registry_mutex);
    return owned ? 0 : __real_pthread_detach(thread);
}

static int join_record(Worker *record, void **value) {
    int error = __real_pthread_join(record->thread, value);
    pthread_mutex_lock(&registry_mutex);
    if (!error) remove_worker(record);
    else record->claimed = false;
    pthread_mutex_unlock(&registry_mutex);
    if (!error) std::free(record);
    return error;
}

extern "C" int __wrap_pthread_join(pthread_t thread, void **value) {
    pthread_mutex_lock(&registry_mutex);
    Worker *record = find_worker(thread);
    bool claimed = record && record->claimed;
    if (record && !claimed) record->claimed = true;
    pthread_mutex_unlock(&registry_mutex);
    if (claimed) return EINVAL;
    return record ? join_record(record, value) : __real_pthread_join(thread, value);
}

static int reap_workers(bool all) {
    while (true) {
        pthread_mutex_lock(&registry_mutex);
        Worker *record = workers;
        while (record && (!record->published || !record->detached_requested || record->claimed ||
                          (!all && !record->returned))) record = record->next;
        if (record) record->claimed = true;
        pthread_mutex_unlock(&registry_mutex);
        if (!record) return 0;
        int error = join_record(record, nullptr);
        if (error) return error;
    }
}

int prepared_join_detached() { return reap_workers(true); }

unsigned prepared_unjoined_workers() {
    pthread_mutex_lock(&registry_mutex);
    unsigned count = 0;
    for (Worker *record = workers; record; record = record->next) ++count;
    pthread_mutex_unlock(&registry_mutex);
    return count;
}

extern "C" lean_obj_res gpu_smt_reap_detached(lean_obj_arg) {
    return lean_io_result_mk_ok(lean_box_uint32(reap_workers(false)));
}

extern "C" lean_obj_res gpu_smt_join_detached(lean_obj_arg) {
    return lean_io_result_mk_ok(lean_box_uint32(prepared_join_detached()));
}
