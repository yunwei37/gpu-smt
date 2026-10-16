// SPDX-License-Identifier: Apache-2.0
//! E036 diagnostic: typed native DAG bridge and paid-body observation.
//! Every native check still runs. Host positives are prospective, not trusted
//! replacement checks. This module is an overlay on sokonanoda 7645b1e1fcac.
use crate::checker::{context::ExportFile, env::Declar};
use crate::term::{expr::Expr, hash::FxHashMap, level::Level as NativeLevel,
    name::Name, ptr::{ExprPtr, LevelPtr, NamePtr}};
use std::sync::{OnceLock, atomic::{AtomicU64, Ordering::Relaxed}};
const NONE: u32 = u32::MAX;
#[repr(C)] #[derive(Default, Clone, Copy)]
struct Node { tag:u32,a:u32,b:u32,c:u32,d:u32 }
#[repr(C)] #[derive(Default, Clone, Copy)]
struct Level { tag:u32,a:u32,b:u32 }
#[repr(C)] #[derive(Default, Clone, Copy)]
struct Decl { kind:u32,name:u32,ty:u32,value:u32,po:u32,pn:u32,np:u32,nf:u32,
    ind:u32,ni:u32,nm:u32,minor:u32,ro:u32,rn:u32,flags:u32,ctor:u32 }
#[repr(C)] #[derive(Default, Clone, Copy)]
struct Rule { ctor:u32,nfields:u32,rhs:u32 }
#[repr(C)] #[derive(Default, Clone, Copy)]
struct Answer { verified:u32,reason:u32,steps:u32,terms:u32,frames:u32,envs:u32,levels:u32 }
#[repr(C)]
struct Input { nodes:*const Node,levels:*const Level,decls:*const Decl,
    rules:*const Rule,ulists:*const u32,params:*const u32,nn:u32,nl:u32,nd:u32,
    nr:u32,nat:u32,string_:u32,zero:u32,succ:u32,nu:u32,np:u32 }
unsafe extern "C" { fn arena_support_run(input:Input,answers:*mut Answer,threads:u32);
    fn arena_thread_cpu_ns()->u64; }
struct Diagnostic { answers:Vec<Answer>, body_ns:Vec<AtomicU64> }
static DIAGNOSTIC: OnceLock<Diagnostic> = OnceLock::new();
pub(crate) fn body_begin()->u64 {
    if DIAGNOSTIC.get().is_none() { return 0 }
    unsafe { arena_thread_cpu_ns() }
}
pub(crate) fn body_end(index:u32,begin:u64) {
    if let Some(d)=DIAGNOSTIC.get() {
        if let Some(cell)=d.body_ns.get(index as usize) {
            cell.fetch_add(unsafe {arena_thread_cpu_ns()}.saturating_sub(begin),Relaxed);
        }
    }
}
fn id(n:usize)->u32 { u32::try_from(n).expect("E036 graph exceeds 32-bit representation") }
struct Bridge<'p> {
    expr_ids:FxHashMap<ExprPtr<'p>,u32>, exprs:Vec<ExprPtr<'p>>, nodes:Vec<Node>,
    level_ids:FxHashMap<LevelPtr<'p>,u32>, level_ptrs:Vec<LevelPtr<'p>>, levels:Vec<Level>,
    name_ids:FxHashMap<NamePtr<'p>,u32>, string_ids:FxHashMap<String,u32>,
    ulists:Vec<u32>, params:Vec<u32>, decls:Vec<Decl>, rules:Vec<Rule>,
}
impl<'p> Bridge<'p> {
    fn new()->Self {Self {expr_ids:FxHashMap::default(),exprs:vec![],nodes:vec![],
        level_ids:FxHashMap::default(),level_ptrs:vec![],levels:vec![],
        name_ids:FxHashMap::default(),string_ids:FxHashMap::default(),
        ulists:vec![],params:vec![],decls:vec![],rules:vec![]}}
    fn expr(&mut self,p:ExprPtr<'p>)->u32 {
        if let Some(v)=self.expr_ids.get(&p) {return *v}
        let k=id(self.exprs.len());self.expr_ids.insert(p,k);
        self.exprs.push(p);self.nodes.push(Node::default());k
    }
    fn level(&mut self,p:LevelPtr<'p>)->u32 {
        if let Some(v)=self.level_ids.get(&p) {return *v}
        let k=id(self.level_ptrs.len());self.level_ids.insert(p,k);
        self.level_ptrs.push(p);self.levels.push(Level::default());k
    }
    fn name(&mut self,p:NamePtr<'p>)->u32 {
        let next=id(self.name_ids.len());*self.name_ids.entry(p).or_insert(next)
    }
    fn declaration(&self,e:&ExportFile<'p>,n:NamePtr<'p>)->u32 {
        e.declars.get_index_of(&n).map_or(NONE,id)
    }
    fn flatten(&mut self,e:&ExportFile<'p>) {
        let mut i=0;
        while i<self.exprs.len() {
            let node=match *self.exprs[i] {
                Expr::Var{dbj_idx,..}=>Node{tag:1,a:u32::from(dbj_idx),..Node::default()},
                Expr::Sort{level,..}=>Node{tag:2,a:self.level(level),..Node::default()},
                Expr::Const{name,levels,..}=>{
                    let off=id(self.ulists.len());
                    for &l in levels.iter(){let k=self.level(l);self.ulists.push(k)}
                    Node{tag:3,a:self.declaration(e,name),b:off,c:id(levels.len()),d:0}
                }
                Expr::App{fun,arg,..}=>Node{tag:4,a:self.expr(fun),b:self.expr(arg),..Node::default()},
                Expr::Lambda{binder_type,body,..}=>Node{tag:5,a:self.expr(binder_type),b:self.expr(body),..Node::default()},
                Expr::Pi{binder_type,body,..}=>Node{tag:6,a:self.expr(binder_type),b:self.expr(body),..Node::default()},
                Expr::Let{data,..} if !data.nondep=>Node{tag:7,a:self.expr(data.binder_type),
                    b:self.expr(data.val),c:self.expr(data.body),d:0},
                Expr::NatLit{ptr,..}=>{
                    let digits=ptr.to_u32_digits();
                    if digits.len()<=1 {Node{tag:8,a:digits.first().copied().unwrap_or(0),..Node::default()}}
                    else {Node::default()}
                }
                Expr::StringLit{ptr,..}=>{
                    let text=ptr.as_ref().to_string();let next=id(self.string_ids.len());
                    Node{tag:9,a:*self.string_ids.entry(text).or_insert(next),..Node::default()}
                }
                // Projection semantics and nondependent-let handling are not
                // admitted by this representation. Real execution must fallback.
                Expr::Proj{..}|Expr::Let{..}=>Node::default(),
            };
            self.nodes[i]=node;i+=1;
        }
        let mut i=0;
        while i<self.level_ptrs.len() {
            self.levels[i]=match *self.level_ptrs[i] {
                NativeLevel::Zero=>Level::default(),
                NativeLevel::Succ(a,_)=>Level{tag:1,a:self.level(a),b:0},
                NativeLevel::Max(a,b,_)=>Level{tag:2,a:self.level(a),b:self.level(b)},
                NativeLevel::IMax(a,b,_)=>Level{tag:3,a:self.level(a),b:self.level(b)},
                NativeLevel::Param(n,_)=>Level{tag:4,a:self.name(n),b:0},
            };i+=1;
        }
    }
}
fn display_name(mut name:NamePtr<'_>)->String {
    let mut parts=vec![];
    loop {match name.as_ref().kind {
        Name::Anon=>break,
        Name::Str(parent,s,_)=>{parts.push(s.as_ref().to_string());name=parent},
        Name::Num(parent,n,_)=>{parts.push(n.to_string());name=parent},
    }}
    parts.reverse();parts.join(".")
}
impl<'p> ExportFile<'p> {
    pub fn e036_prepare_host_diagnostic(&self) {
        let begin=std::time::Instant::now();let mut b=Bridge::new();
        let mut nat=NONE;let mut string_=NONE;let mut zero=NONE;let mut succ=NONE;
        for (i,(name,d)) in self.declars.iter().enumerate() {
            match display_name(*name).as_str() {
                "Nat"=>nat=id(i),"String"=>string_=id(i),
                "Nat.zero"=>zero=id(i),"Nat.succ"=>succ=id(i),_=>{}
            }
            let po=id(b.params.len());
            for p in d.info().uparams.iter() {
                if let NativeLevel::Param(n,_)=**p {let k=b.name(n);b.params.push(k)}
                else {panic!("E036 unexpected nonparameter native declaration universe")}
            }
            let mut out=Decl{kind:0,name:id(i),ty:b.expr(d.info().ty),
                value:NONE,po,pn:id(d.info().uparams.len()),ind:NONE,ctor:NONE,..Decl::default()};
            match d {
                Declar::Definition{val,..}=>{out.kind=1;out.value=b.expr(*val)},
                Declar::Theorem{val,..}=>{out.kind=2;out.value=b.expr(*val)},
                Declar::Opaque{val,..}=>{out.kind=3;out.value=b.expr(*val)},
                Declar::Inductive(v)=>{out.kind=4;out.np=u32::from(v.num_params);
                    out.ni=u32::from(v.num_indices);
                    out.ctor=v.all_ctor_names.first().map_or(NONE,|n|b.declaration(self,*n));
                    // Existing projection checker not admitted here.
                    out.flags=if v.is_recursive||v.is_nested {2} else {0};},
                Declar::Constructor(v)=>{out.kind=5;out.np=u32::from(v.num_params);
                    out.nf=u32::from(v.num_fields);out.ind=b.declaration(self,v.inductive_name);},
                Declar::Recursor(v)=>{out.kind=6;out.np=u32::from(v.num_params);
                    out.ni=u32::from(v.num_indices);out.nm=u32::from(v.num_motives);
                    out.minor=u32::from(v.num_minors);out.ro=id(b.rules.len());
                    out.rn=id(v.rec_rules.len());out.flags=u32::from(v.is_k);
                    for rule in v.rec_rules.iter() {
                        let rhs=b.expr(rule.val);b.rules.push(Rule{ctor:b.declaration(self,rule.ctor_name),
                            nfields:u32::from(rule.ctor_telescope_size_wo_params),rhs});
                    }},
                Declar::Axiom{..}|Declar::Quot{..}=>{},
            }
            b.decls.push(out);
        }
        b.flatten(self);
        let bytes=b.nodes.len()*std::mem::size_of::<Node>()+b.levels.len()*std::mem::size_of::<Level>()
            +b.decls.len()*std::mem::size_of::<Decl>()+b.rules.len()*std::mem::size_of::<Rule>()
            +(b.ulists.len()+b.params.len())*4;
        eprintln!("e036 bridge nodes={} levels={} declarations={} rules={} packed_bytes={} wall_s={:.9}",
            b.nodes.len(),b.levels.len(),b.decls.len(),b.rules.len(),bytes,begin.elapsed().as_secs_f64());
        let input=Input{nodes:b.nodes.as_ptr(),levels:b.levels.as_ptr(),decls:b.decls.as_ptr(),
            rules:b.rules.as_ptr(),ulists:b.ulists.as_ptr(),params:b.params.as_ptr(),
            nn:id(b.nodes.len()),nl:id(b.levels.len()),nd:id(b.decls.len()),nr:id(b.rules.len()),
            nat,string_,zero,succ,nu:id(b.ulists.len()),np:id(b.params.len())};
        let mut answers=vec![Answer::default();b.decls.len()];
        let begin=std::time::Instant::now();
        unsafe{arena_support_run(input,answers.as_mut_ptr(),id(self.config.num_threads.max(1)))};
        eprintln!("e036 host_query wall_s={:.9}",begin.elapsed().as_secs_f64());
        assert!(DIAGNOSTIC.set(Diagnostic{body_ns:(0..answers.len()).map(|_|AtomicU64::new(0)).collect(),answers}).is_ok(),
            "E036 supports one export per diagnostic process");
        // Drop bridge allocation before native checking; its cost stays in wall.
    }
    pub fn e036_write_diagnostic(&self,path:&std::path::Path)->std::io::Result<()> {
        use std::io::Write;
        let d=DIAGNOSTIC.get().expect("E036 diagnostic not prepared");
        let mut f=std::io::BufWriter::new(std::fs::File::create(path)?);
        writeln!(f,"declaration_index,kind,host_positive,host_reason,host_steps,native_body_thread_cpu_ns")?;
        for (i,(_,native)) in self.declars.iter().enumerate() {
            let kind=match native {Declar::Definition{..}=>"definition",Declar::Theorem{..}=>"theorem",
                Declar::Opaque{..}=>"opaque",_=>"native-only"};
            let a=d.answers[i];
            writeln!(f,"{i},{kind},{},{},{},{}",a.verified,a.reason,a.steps,d.body_ns[i].load(Relaxed))?;
        }f.flush()
    }
}
