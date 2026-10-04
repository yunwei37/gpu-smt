#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>
int main(int argc,char**argv){
  size_t N=1ULL<<27; double *a=malloc(N*8),*b=malloc(N*8),*c=malloc(N*8);
  for(size_t i=0;i<N;i++){a[i]=1;b[i]=2;c[i]=0;}
  int thr=atoi(argv[1]); omp_set_num_threads(thr);
  struct timespec t0,t1; clock_gettime(CLOCK_MONOTONIC,&t0);
  int reps=20;
  #pragma omp parallel for
  for(int r=0;r<reps;r++) for(size_t i=0;i<N;i++) c[i]=a[i]+b[i];
  clock_gettime(CLOCK_MONOTONIC,&t1);
  double dt=(t1.tv_sec-t0.tv_sec)+(t1.tv_nsec-t0.tv_nsec)/1e9;
  printf("threads=%d triad=%.1f GB/s\n",thr,3.0*8*N*reps/dt/1e9);
  return 0;
}
