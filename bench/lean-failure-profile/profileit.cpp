// Diagnostic link wrapper around stock Lean profileitM/profileit boundaries.
// Original native objects and source inputs are unchanged. No Lean allocations.
#include <lean/lean.h>
#include <zlib.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/syscall.h>
#include <time.h>
#include <atomic>
#include <fstream>
#include <map>
#include <mutex>
#include <sstream>
#include <string>
#include <thread>
#include <vector>
#include <chrono>
#include <cstdlib>
extern "C" lean_object* __real_lean_profileit(lean_object*,lean_object*,lean_object*,lean_object*);
static uint64_t ns(clockid_t c) { timespec t{};clock_gettime(c,&t);return uint64_t(t.tv_sec)*1000000000+t.tv_nsec; }
static std::string quoted(const std::string& s) {
 std::string o="\"";for(unsigned char c:s){if(c=='"'||c=='\\'){o+='\\';o+=c;}else if(c<32)o+='?';else o+=c;}return o+"\"";
}
static std::string name_string(lean_object* n) {
 if(lean_is_scalar(n))return "";
 std::string p=name_string(lean_ctor_get(n,0));
 std::string q=lean_obj_tag(n)==1?lean_string_cstr(lean_ctor_get(n,1)):"#";
 return p.empty()?q:p+"."+q;
}
struct Bucket {uint64_t calls=0,wall=0,cpu=0,exclusive_cpu=0;};
struct Frame {std::string key;uint64_t wall,cpu,children=0;};
struct State {
 std::mutex mu;clockid_t clock;long tid;std::string source="unknown",phase="unknown";
 std::vector<Frame> stack;std::map<std::string,Bucket> totals;
 State():tid(syscall(SYS_gettid)){pthread_getcpuclockid(pthread_self(),&clock);}
};
struct Recorder {
 std::mutex mu;std::vector<State*> threads;gzFile out=nullptr;std::atomic<bool> alive{true};
 Recorder() {
  const char* d=getenv("GPU_SMT_NATIVE_PROFILE_DIRECTORY");
  if(d){std::string p=std::string(d)+"/"+std::to_string(getpid())+".jsonl.gz";out=gzopen(p.c_str(),"wb1");}
  if(!out) return;
  std::thread([this]{while(alive.load()){std::this_thread::sleep_for(std::chrono::seconds(1));snapshot("sample");}}).detach();
 }
 void snapshot(const char* event) {
  std::lock_guard<std::mutex> lock(mu);if(!out)return;
  std::ostringstream o;o<<"{\"event\":"<<quoted(event)<<",\"pid\":"<<getpid()<<",\"time_ns\":"<<ns(CLOCK_MONOTONIC)<<",\"threads\":[";
  bool first=true;for(State* s:threads){
   std::lock_guard<std::mutex> sl(s->mu);
   if(!first)o<<",";first=false;
   uint64_t cpu=ns(s->clock);o<<"{\"tid\":"<<s->tid<<",\"source_id\":"<<quoted(s->source)<<",\"phase\":"<<quoted(s->phase)<<",\"thread_cpu_ns\":"<<cpu<<",\"totals\":{";
   bool f=true;for(auto& it:s->totals){
    if(!f)o<<",";f=false;o<<quoted(it.first)<<":["<<it.second.calls<<","<<it.second.wall<<","<<it.second.cpu<<","<<it.second.exclusive_cpu<<"]";
   }
   o<<"},\"active\":[";f=true;for(auto& x:s->stack){if(!f)o<<",";f=false;
    o<<"{\"key\":"<<quoted(x.key)<<",\"start_ns\":"<<x.wall<<",\"start_cpu_ns\":"<<x.cpu<<",\"completed_child_cpu_ns\":"<<x.children<<"}";}
   o<<"]}";
  }
  o<<"]}\n";std::string text=o.str();gzwrite(out,text.data(),text.size());gzflush(out,Z_SYNC_FLUSH);
 }
};
static Recorder& recorder(){static Recorder* r=new Recorder();return *r;}
static State& state(){thread_local State* s=[](){State* s=new State();auto& r=recorder();std::lock_guard<std::mutex> l(r.mu);r.threads.push_back(s);return s;}();return *s;}
static std::string field(const std::string& text,const char* key) {
 auto p=text.find(std::string("\"")+key+"\"");if(p==std::string::npos)return "unknown";p=text.find(':',p);if(p==std::string::npos)return "unknown";
 p=text.find_first_not_of(" \t",p+1);if(p==std::string::npos||text[p]!='"')return "unknown";
 auto e=text.find('"',p+1);return e==std::string::npos?"unknown":text.substr(p+1,e-p-1);
}
static std::pair<std::string,std::string> ownership() {
 const char* d=getenv("GPU_SMT_MEMORY_DIRECTORY");if(!d)return {"unknown","unknown"};
 for(int pid:{int(getpid()),int(getppid())}){
  std::ifstream f(std::string(d)+"/activity/"+std::to_string(pid)+".json");if(!f)continue;
  std::ostringstream t;t<<f.rdbuf();return {field(t.str(),"source_id"),field(t.str(),"phase")};
 }
 return {"unknown","unknown"};
}
extern "C" lean_object* __wrap_lean_profileit(lean_object* category,lean_object* opts,lean_object* fn,lean_object* decl) {
 if(!getenv("GPU_SMT_NATIVE_PROFILE_DIRECTORY"))return __real_lean_profileit(category,opts,fn,decl);
 auto& s=state();std::string key=std::string(lean_string_cstr(category))+"|"+name_string(decl);
 bool outer;
 {std::lock_guard<std::mutex> l(s.mu);outer=s.stack.empty();}
 if(outer){
  auto owner=ownership();bool changed;
  {std::lock_guard<std::mutex> l(s.mu);changed=s.source!=owner.first||s.phase!=owner.second;}
  if(changed){
   recorder().snapshot("source_boundary");
   std::lock_guard<std::mutex> l(s.mu);s.source=owner.first;s.phase=owner.second;s.totals.clear();
  }
 }
 {std::lock_guard<std::mutex> l(s.mu);s.stack.push_back({key,ns(CLOCK_MONOTONIC),ns(CLOCK_THREAD_CPUTIME_ID),0});}
 lean_object* result=__real_lean_profileit(category,opts,fn,decl);
 {uint64_t cpu=ns(CLOCK_THREAD_CPUTIME_ID),wall=ns(CLOCK_MONOTONIC);std::lock_guard<std::mutex> l(s.mu);
  Frame f=s.stack.back();s.stack.pop_back();uint64_t c=cpu-f.cpu;auto& b=s.totals[f.key];
  b.calls++;b.wall+=wall-f.wall;b.cpu+=c;b.exclusive_cpu+=c>=f.children?c-f.children:0;
  if(!s.stack.empty())s.stack.back().children+=c;
 }
 if(outer)recorder().snapshot("outer_return");
 return result;
}
