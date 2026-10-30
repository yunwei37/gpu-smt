#define _POSIX_C_SOURCE 200809L
#include <stdint.h>
#include <stdio.h>
#include <time.h>
static double now(void){struct timespec t;clock_gettime(CLOCK_PROCESS_CPUTIME_ID,&t);return t.tv_sec+t.tv_nsec/1e9;}
static int eligible(uint64_t n){if(n<1000||n>9999||n%5)return 0;for(int k=0;k<4;k++,n/=10)if(n%10%2)return 0;return 1;}
int main(void){
 double a=now();uint64_t count=0,sum=0;for(uint64_t n=0;n<10000;n++)if(eligible(n)){count++;sum+=n;}
 double b=now();uint64_t lattice=0;for(uint64_t m=2;m<=2005;m++)for(uint64_t n=2;n<=2005;n++)if(m*n==2005){printf("solution=%lu,%lu\n",m,n);lattice++;}
 double c=now();
 printf("digits_count=%lu digits_sum=%lu digits_CPU_seconds=%.9f lattice_cells=4016016 lattice_count=%lu lattice_CPU_seconds=%.9f\n",count,sum,b-a,lattice,c-b);
 return count==100&&lattice==2?0:1;
}
