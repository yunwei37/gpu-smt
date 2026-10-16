from pathlib import Path
import subprocess,json,datetime
r=Path('/workspaces/repository')
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
p=r/'bench/lean-gpu/closure-reclaiming.cu'
assert not p.exists()
s=(r/'bench/lean-gpu/closure-canonical.cu').read_text()
s=s.replace('// E037 canonical worker variant; original closure-checker.cu is preserved.','// E040 quiescent-step reclamation; original canonical and frozen engines are preserved.')
s=s.replace('struct Scratch {',"""struct GCItem {U kind,id;};
struct GCState {
 unsigned char *ta,*ea,*la; U *tn,*en,*ln; GCItem* queue;
 U th,eh,lh; bool enabled;
 uint64_t passes,freed_t,freed_e,freed_l,retry_failures;
};
struct Scratch {""")
s=s.replace('U epoch;bool canonical;};','U epoch;bool canonical;GCState* gc;};')
s=s.replace(' HD U mix(U h,U v)',""" HD U alloc(U kind,U& top){
  GCState* g=z.gc;U* head=kind==0?&g->th:kind==1?&g->eh:&g->lh;
  U* next=kind==0?g->tn:kind==1?g->en:g->ln;
  unsigned char* flags=kind==0?g->ta:kind==1?g->ea:g->la;
  U id;
  if(*head!=N){id=*head;*head=next[id];}
  else {if(top>=z.cap){fail(CAPACITY);return N;}id=top++;}
  flags[id]=1;return id;
 }
 HD void mark(U kind,U id,U& count){
  GCState* g=z.gc;U top=kind==0?nt:kind==1?ne:nl;
  unsigned char* flags=kind==0?g->ta:kind==1?g->ea:g->la;
  if(id>=top||flags[id]!=1)return;
  flags[id]=2;g->queue[count++]={kind,id};
 }
 HD void roots(U value,U& count){mark(0,value,count);mark(1,value,count);mark(2,value,count);}
 HD U collect(){
  GCState* g=z.gc;U count=0,scan=0;
  roots(ret,count);
  for(U k=0;k<sp;k++){
   Frame f=z.frames[k];
   U values[]={f.op,f.pc,f.x,f.y,f.mode,f.a,f.b,f.c,f.d,f.i,f.j,f.k,f.ox,f.oy};
   for(U j=0;j<14;j++)roots(values[j],count);
  }
  while(scan<count){
   GCItem q=g->queue[scan++];
   if(q.kind==0){
    Term t=z.terms[q.id];
    mark(1,t.e,count);mark(1,t.u,count);mark(1,t.s,count);
    switch(t.tag){
     case LOCAL:mark(0,t.b,count);break;
     case SORT:if(t.b==1)mark(2,t.a,count);break;
     case APP:case LAM:case PI:mark(0,t.a,count);mark(0,t.b,count);break;
     case LET:mark(0,t.a,count);mark(0,t.b,count);mark(0,t.c,count);break;
     case PROJ:mark(0,t.c,count);break;
     default:break;
    }
   }else if(q.kind==1){
    Env e=z.envs[q.id];mark(0,e.value,count);mark(1,e.next,count);
   }else{
    LVal v=z.levels[q.id];
    if(v.tag==1||v.tag==2||v.tag==3)mark(2,v.a,count);
    if(v.tag==2||v.tag==3)mark(2,v.b,count);
   }
  }
  U freed=0;
  g->th=g->eh=g->lh=N;
  for(U kind=0;kind<3;kind++){
   U top=kind==0?nt:kind==1?ne:nl;
   unsigned char* flags=kind==0?g->ta:kind==1?g->ea:g->la;
   U* next=kind==0?g->tn:kind==1?g->en:g->ln;
   U* head=kind==0?&g->th:kind==1?&g->eh:&g->lh;
   uint64_t* counter=kind==0?&g->freed_t:kind==1?&g->freed_e:&g->freed_l;
   for(U k=0;k<top;k++){
    if(flags[k]==2){flags[k]=1;continue;}
    if(flags[k]==1){++freed;++*counter;}
    flags[k]=0;next[k]=*head;*head=k;
   }
  }
  // Cached answers/intern keys are weak; no stale object ID survives reuse.
  for(U k=0;k<z.cap*2;k++){z.ts[k]={0,0};z.es[k]={0,0};z.ls[k]={0,0};z.memo[k]={0,0,0,0,0,0};}
  for(U k=0;k<nt;k++)if(g->ta[k]){
   Term t=z.terms[k];U h=mix(mix(mix(mix(mix(mix(t.tag,t.a),t.b),t.c),t.e),t.u),t.s);
   U slot=h&(z.cap*2-1);while(z.ts[slot].epoch==z.epoch)slot=(slot+1)&(z.cap*2-1);
   z.ts[slot]={z.epoch,k};
  }
  for(U k=0;k<ne;k++)if(g->ea[k]){
   Env e=z.envs[k];U slot=mix(mix(e.key,e.value),e.next)&(z.cap*2-1);
   while(z.es[slot].epoch==z.epoch)slot=(slot+1)&(z.cap*2-1);z.es[slot]={z.epoch,k};
  }
  for(U k=0;k<nl;k++)if(g->la[k]){
   LVal v=z.levels[k];U slot=mix(mix(v.tag,v.a),v.b)&(z.cap*2-1);
   while(z.ls[slot].epoch==z.epoch)slot=(slot+1)&(z.cap*2-1);z.ls[slot]={z.epoch,k};
  }
  ++g->passes;return freed;
 }
 HD U mix(U h,U v)""")
a='if(nt>=z.cap){fail(CAPACITY);return 0;}U id=nt++;z.terms[id]={tag,a,b,c,e,u,s};'
b='U id=alloc(0,nt);if(id==N)return 0;z.terms[id]={tag,a,b,c,e,u,s};'
assert s.count(a)==1;s=s.replace(a,b)
a='if(ne>=z.cap){fail(CAPACITY);return N;}U id=ne++;z.envs[id]={key,val,next};'
b='U id=alloc(1,ne);if(id==N)return N;z.envs[id]={key,val,next};'
assert s.count(a)==1;s=s.replace(a,b)
a='if(nl>=z.cap){fail(CAPACITY);return 0;}U id=nl++;z.levels[id]={tag,a,b};'
b='U id=alloc(2,nl);if(id==N)return 0;z.levels[id]={tag,a,b};'
assert s.count(a)==1;s=s.replace(a,b)
a='HD void run(U op,U x,U y=0){push(op,x,y);while(sp&&!error){'
b='HD void step(){do{'
assert s.count(a)==1;s=s.replace(a,b)
a=' } }\n};\nHD Answer execute'
b=""" }while(false); }
 HD void run(U op,U x,U y=0){
  push(op,x,y);bool retrying=false;
  while(sp&&!error){
   U saved_sp=sp,saved_ret=ret,saved_fresh=fresh;Frame saved=z.frames[sp-1];
   step();
   if(error==CAPACITY&&z.gc->enabled&&!retrying){
    sp=saved_sp;ret=saved_ret;fresh=saved_fresh;z.frames[sp-1]=saved;
    U freed=collect();
    if(freed){error=0;retrying=true;continue;}
   }else if(error==CAPACITY&&retrying){++z.gc->retry_failures;}
   if(!error)retrying=false;
  }
 }
};
HD Answer execute"""
assert s.count(a)==1;s=s.replace(a,b)
p.write_text(s)
print('wrote',str(p),len(s))
