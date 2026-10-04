#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>
#include <omp.h>

using u32 = uint32_t;
struct Node { u32 kind, a, b, c, imm; };
static_assert(sizeof(Node)==20);
template<class T> void read(std::ifstream& f, std::vector<T>& v, size_t n) {
  v.resize(n); f.read(reinterpret_cast<char*>(v.data()), n*sizeof(T));
  if (!f) throw std::runtime_error("truncated input");
}
u32 eval(const Node& n, const std::vector<u32>& out) {
  switch(n.kind) {
    case 0: return 0;
    case 1: return n.imm+1;
    case 2: return std::max(out[n.a],out[n.b]);
    case 3: return std::max(out[n.a],out[n.b] ? out[n.b]-1 : 0);
    case 4: return std::max({out[n.a],out[n.b],out[n.c] ? out[n.c]-1 : 0});
    case 5: return out[n.a];
    default: throw std::runtime_error("invalid expression kind");
  }
}
int main(int argc, char** argv) {
  if(argc!=6) { std::cerr<<"input reference serial|wave threads repeats\n"; return 2; }
  std::ifstream f(argv[1],std::ios::binary);
  char magic[8]; f.read(magic,8);
  if(std::string(magic,8)!=std::string("LBVDAG1\0",8)) throw std::runtime_error("bad magic");
  std::vector<u32> header; read(f,header,4);
  u32 n=header[0], waves=header[1];
  std::vector<Node> nodes; read(f,nodes,n);
  std::vector<u32> order, offsets, roots, reference, out(n);
  read(f,order,n); read(f,offsets,waves+1); read(f,roots,header[2]);
  std::ifstream rf(argv[2],std::ios::binary); read(rf,reference,n);
  const bool wave=std::string(argv[3])=="wave";
  const int threads=std::stoi(argv[4]), repeats=std::stoi(argv[5]);
  if(threads<1 || repeats<1) throw std::runtime_error("positive threads/repeats required");
  omp_set_num_threads(threads);
  std::vector<double> times;
  for(int rep=0;rep<repeats;++rep) {
    auto start=std::chrono::steady_clock::now();
    if(!wave) {
      for(u32 i=0;i<n;++i) out[i]=eval(nodes[i],out);
    } else {
      #pragma omp parallel
      {
        for(u32 l=0;l<waves;++l) {
          #pragma omp for schedule(static)
          for(u32 p=offsets[l];p<offsets[l+1];++p) {
            u32 i=order[p]; out[i]=eval(nodes[i],out);
          }
        }
      }
    }
    double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
    times.push_back(seconds);
    if(out!=reference) { std::cerr<<"metadata mismatch\n"; return 1; }
  }
  std::cout<<"{\"mode\":\""<<(wave?"wave":"serial")<<"\",\"threads\":"<<threads
    <<",\"expressions\":"<<n<<",\"waves\":"<<waves<<",\"matches\":true,\"seconds\":[";
  for(size_t i=0;i<times.size();++i) std::cout<<(i?",":"")<<times[i];
  std::cout<<"]}\n";
}
