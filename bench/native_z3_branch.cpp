// Thin stock-Z3 SMT-LIB adapter; no added solver scopes or assertion rewriting.
// Input/output files are raw experimental streams, not orchestration state.
#include <z3.h>
#include <chrono>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <sys/wait.h>
#include <unistd.h>

static std::string read(const std::string& path) {
    std::ifstream in(path);
    if (!in) throw std::runtime_error("Cannot read " + path);
    return {std::istreambuf_iterator<char>(in), std::istreambuf_iterator<char>()};
}
static void write(const std::string& path, const std::string& value) {
    std::ofstream out(path);
    if (!out) throw std::runtime_error("Cannot write " + path);
    out << value;
    out.close();
    if (!out) throw std::runtime_error("Write failed " + path);
}
static unsigned threads() {
    unsigned n = 0;
    for ([[maybe_unused]] const auto& p : std::filesystem::directory_iterator("/proc/self/task")) ++n;
    return n;
}
static std::string evaluate(Z3_context c, const std::string& input) {
    const char* raw = Z3_eval_smtlib2_string(c, input.c_str());
    std::string output = raw ? raw : "";
    Z3_error_code error = Z3_get_error_code(c);
    if (error != Z3_OK) {
        std::cerr << "API_ERROR " << error << " " << Z3_get_error_msg(c, error) << "\n";
    }
    return output;
}
static Z3_context context() {
    Z3_config cfg = Z3_mk_config();
    Z3_context c = Z3_mk_context(cfg);
    Z3_del_config(cfg);
    Z3_set_error_handler(c, nullptr);
    return c;
}
static double seconds(std::chrono::steady_clock::time_point begin) {
    return std::chrono::duration<double>(std::chrono::steady_clock::now() - begin).count();
}
int main(int argc, char** argv) {
    try {
        if (argc < 4) throw std::runtime_error("fresh INPUT OUTPUT | split PREFIX SUFFIX OUTPUT | branch PREFIX OUTPUTDIR SUFFIX...");
        std::string mode = argv[1];
        Z3_context c = context();
        if (mode == "fresh") {
            if (argc != 4) throw std::runtime_error("fresh argument count");
            write(argv[3], evaluate(c, read(argv[2])));
            return Z3_get_error_code(c) == Z3_OK ? 0 : 2;
        }
        auto begin = std::chrono::steady_clock::now();
        std::string prefix_output = evaluate(c, read(argv[2]));
        double setup = seconds(begin);
        if (Z3_get_error_code(c) != Z3_OK) return 2;
        if (mode == "split") {
            if (argc != 5) throw std::runtime_error("split argument count");
            write(argv[4], prefix_output + evaluate(c, read(argv[3])));
            return Z3_get_error_code(c) == Z3_OK ? 0 : 2;
        }
        if (mode != "branch" || argc < 5) throw std::runtime_error("branch argument count");
        std::filesystem::path out = argv[3];
        std::filesystem::create_directories(out);
        write((out / "prefix.stdout").string(), prefix_output);
        write((out / "parent.smaps").string(), read("/proc/self/smaps_rollup"));
        std::cout << "setup\t" << setup << "\tthreads\t" << threads() << std::endl;
        if (threads() != 1) throw std::runtime_error("Refusing to fork a multithreaded prepared parent");
        for (int i = 4; i < argc; ++i) {
            std::string suffix = read(argv[i]);
            auto branch_start = std::chrono::steady_clock::now();
            pid_t pid = fork();
            if (pid < 0) throw std::runtime_error("fork failed");
            if (pid == 0) {
                try {
                    std::string name = (out / std::to_string(i - 4)).string();
                    write(name + ".stdout", prefix_output + evaluate(c, suffix));
                    write(name + ".smaps", read("/proc/self/smaps_rollup"));
                    _exit(Z3_get_error_code(c) == Z3_OK ? 0 : 2);
                } catch (const std::exception& error) {
                    std::cerr << error.what() << std::endl;
                    _exit(3);
                }
            }
            int status;
            if (waitpid(pid, &status, 0) != pid) throw std::runtime_error("waitpid failed");
            std::cout << "child\t" << i - 4 << "\tstatus\t" << status
                      << "\tseconds\t" << seconds(branch_start) << std::endl;
        }
        return 0;
    } catch (const std::exception& error) {
        std::cerr << error.what() << std::endl;
        return 3;
    }
}
