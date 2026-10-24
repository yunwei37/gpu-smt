// Floating proposals only. CPU exact checking remains mandatory.
// Each grid row is one goal; each thread evaluates one candidate assignment.
extern "C" __global__ void arithmetic_points(
 const int* code, const double* constants, const long long* meta,
 const int* domains, const double* points, unsigned char* hits) {
 int g=blockIdx.y;
 const long long* m=meta+7*g;
 long long sample=(long long)blockIdx.x*blockDim.x+threadIdx.x;
 if(sample>=m[5]) return;
 long long result=m[6]+sample;
 hits[result]=0;
 const double* x=points+m[4]+sample*m[3];
 for(int j=0;j<m[3];j++) {
  double v=x[j];
  if(!(v==v) || v>1.7976931348623157e308 || v< -1.7976931348623157e308) return;
  int d=domains[m[2]+j];
  if(d && floor(v)!=v) return;
  if(d==2 && v<0) return;
 }
 double stack[64]; int sp=0;
 for(long long pc=m[0];pc<m[1];pc++) {
  int op=code[2*pc], arg=code[2*pc+1];
  if(op==0) { stack[sp++]=constants[pc]; continue; }
  if(op==1) { stack[sp++]=x[arg]; continue; }
  if(op==8 || op==9) { stack[sp++]=(op==8); continue; }
  if(op==6) { stack[sp-1]=-stack[sp-1]; continue; }
  if(op==7) {
   double base=stack[sp-1], value=1;
   for(int k=0;k<arg;k++) value*=base;
   stack[sp-1]=value; continue;
  }
  if(op==12) { stack[sp-1]=!stack[sp-1]; continue; }
  double b=stack[--sp], a=stack[sp-1], value=0;
  switch(op) {
   case 2:value=a+b;break;
   case 3:value=a-b;break;
   case 4:value=(a>b?a-b:0);break;
   case 5:value=a*b;break;
   case 10:value=(a!=0 && b!=0);break;
   case 11:value=(a!=0 || b!=0);break;
   case 13:value=(a==b);break;
   case 14:value=(a!=b);break;
   case 15:value=(a<b);break;
   case 16:value=(a<=b);break;
  }
  stack[sp-1]=value;
 }
 if(sp==1 && stack[0]!=0) hits[result]=1;
}
