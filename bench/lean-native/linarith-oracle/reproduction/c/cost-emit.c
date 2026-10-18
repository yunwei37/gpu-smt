
#include <lean/lean.h>
extern char *getenv(const char *);
extern int open(const char *, int, ...);
extern long write(int, const void *, unsigned long);
extern int flock(int,int);
extern int close(int);
extern void abort(void);
extern void perror(const char *);
typedef void *gzFile;
extern gzFile gzopen(const char *,const char *);
extern int gzwrite(gzFile,const void *,unsigned);
extern int gzclose(gzFile);
#define O_WRONLY 1
#define O_CREAT 64
#define O_APPEND 1024
#define LOCK_EX 2
#define LOCK_UN 8
LEAN_EXPORT lean_obj_res gpu_smt_cost_emit(b_lean_obj_arg s,lean_obj_arg world){
 const char *path=getenv("FARKAS_CORPUS_FILE");
 if(path){
  int fd=open(path,O_WRONLY|O_CREAT|O_APPEND,0644);
  if(fd<0||flock(fd,LOCK_EX)<0){perror("cost telemetry lock");abort();}
  const char *text=lean_string_cstr(s);size_t left=lean_string_size(s)-1;
  size_t length=0;while(path[length])++length;
  int zipped=length>=3&&path[length-3]=='.'&&path[length-2]=='g'&&path[length-1]=='z';
  if(zipped){
   gzFile output=gzopen(path,"ab");if(!output){perror("cost gzip open");abort();}
   while(left){unsigned chunk=left>2147483647u?2147483647u:(unsigned)left;
    int n=gzwrite(output,text,chunk);if(n<=0){perror("cost gzip write");abort();}
    text+=n;left-=n;
   }
   if(gzwrite(output,"\n",1)!=1||gzclose(output)!=0){perror("cost gzip finish");abort();}
  }else{
   while(left){long n=write(fd,text,left);if(n<=0){perror("cost write");abort();}text+=n;left-=n;}
   if(write(fd,"\n",1)!=1){perror("cost newline");abort();}
  }
  flock(fd,LOCK_UN);close(fd);
 }
 return lean_io_result_mk_ok(lean_box(0));
}
