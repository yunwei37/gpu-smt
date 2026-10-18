//! Untrusted arithmetic AST -> polynomial/products -> exact Farkas certificate.
//! Native proof reconstruction remains the authority; no Lean expressions cross back.
use farkas_core::{types::{Hyp,Ineq},race::produce_certificate_hint as produce_certificate_hybrid,verify::verify_cert};
use num_bigint::BigInt;
use num_rational::BigRational as Q;
use num_traits::{Zero,One};
use num_integer::Integer;
use serde_json::{Value,json};
use std::{collections::BTreeMap,io::{BufRead,Write},str::FromStr,time::Instant};
type Poly=BTreeMap<Vec<usize>,Q>;
fn scalar(n:Q)->Poly {if n.is_zero(){Poly::new()}else{BTreeMap::from([(vec![],n)])}}
fn add(mut p:Poly,q:Poly)->Poly {for (k,v) in q {let e=p.entry(k).or_insert_with(Q::zero);*e+=v;}p.retain(|_,v|!v.is_zero());p}
fn scale(p:Poly,q:&Q)->Poly {p.into_iter().filter_map(|(k,v)|{let v=v*q;if v.is_zero(){None}else{Some((k,v))}}).collect()}
fn mul(p:&Poly,q:&Poly)->Poly {let mut r=Poly::new();for(a,x)in p{for(b,y)in q{let mut k=a.clone();k.extend(b);k.sort();*r.entry(k).or_insert_with(Q::zero)+=x*y;}}r.retain(|_,v|!v.is_zero());r}
fn parse(v:&Value)->Result<Poly,String>{
 let a=v.as_array().ok_or("AST array")?;
 let op=a.first().and_then(Value::as_str).ok_or("AST op")?;
 match op{
 "q"=>{let n=BigInt::from_str(a[1].as_str().ok_or("num")?).map_err(|_|"num")?;let d=BigInt::from_str(a[2].as_str().ok_or("den")?).map_err(|_|"den")?;if d.is_zero(){return Err("zero denominator".into())}Ok(scalar(Q::new(n,d)))},
 "a"=>Ok(BTreeMap::from([(vec![a[1].as_u64().ok_or("atom")? as usize],Q::one())])),
 "neg"=>Ok(scale(parse(&a[1])?,&-Q::one())),
 "+"=>Ok(add(parse(&a[1])?,parse(&a[2])?)),
 "-"=>Ok(add(parse(&a[1])?,scale(parse(&a[2])?,&-Q::one()))),
 "*"=>Ok(mul(&parse(&a[1])?,&parse(&a[2])?)),
 _=>Err("unsupported AST".into())}
}
#[derive(Clone)]struct Fact{p:Poly,k:Ineq,origin:Value}
fn solve(v:Value)->Result<Value,String>{
 farkas_core::race::set_context(&v);
 let start=Instant::now();
 if v.get("hello")==Some(&Value::Bool(true)){return Ok(json!({"arithmetic_protocol":1}))}
 let mut facts=Vec::new();
 for(i,h)in v["hyps"].as_array().ok_or("hyps")?.iter().enumerate(){
 let k=match h[0].as_str(){Some("lt")=>Ineq::Lt,Some("le")=>Ineq::Le,Some("eq")=>Ineq::Eq,_=>return Err("ineq".into())};
 facts.push(Fact{p:add(parse(&h[1])?,scale(parse(&h[2])?,&-Q::one())),k,origin:json!(["h",i])});
 }
 let linear_ns=start.elapsed().as_nanos();
 let mut pool=facts.clone();
 if v["nlin"]==true {
 let mut squares=BTreeMap::new();
 for f in &facts{for mon in f.p.keys(){if mon.len()==2&&mon[0]==mon[1]{squares.insert(mon[0],());}}}
 for(a,_)in squares{pool.push(Fact{p:BTreeMap::from([(vec![a,a],-Q::one())]),k:Ineq::Le,origin:json!(["sq",a])});}
 }
 let mut all=vec![Fact{p:scalar(-Q::one()),k:Ineq::Lt,origin:json!(["seed"])}];
 all.extend(pool.clone());
 if v["nlin"]==true {
 for i in 0..pool.len(){for j in i..pool.len(){
 let a=&pool[i];let b=&pool[j];let k=if a.k==Ineq::Eq||b.k==Ineq::Eq{Ineq::Eq}else if a.k==Ineq::Lt&&b.k==Ineq::Lt{Ineq::Lt}else{Ineq::Le};
 all.push(Fact{p:scale(mul(&a.p,&b.p),&if k==Ineq::Eq{Q::one()}else{-Q::one()}),k,origin:json!(["mul",a.origin,b.origin])});
 }}
 }
 let products_ns=start.elapsed().as_nanos()-linear_ns;
 let mut ids=BTreeMap::new();ids.insert(vec![],0usize);
 for f in &all{for mon in f.p.keys(){if !ids.contains_key(mon){let n=ids.len();ids.insert(mon.clone(),n);}}}
 let mut hyps=Vec::new();let mut origins=Vec::new();let mut scales=Vec::new();
 for f in &all {
 let den=f.p.values().fold(BigInt::one(),|d,c|d.lcm(c.denom()));
 let coeffs:Vec<_>=f.p.iter().map(|(m,c)|(ids[m],c.numer()*(&den/c.denom()))).collect();
 hyps.push(Hyp{ineq:f.k,coeffs:coeffs.clone()});origins.push((f.origin.clone(),false));scales.push(den.clone());
 if f.k==Ineq::Eq {hyps.push(Hyp{ineq:Ineq::Eq,coeffs:coeffs.into_iter().map(|(i,c)|(i,-c)).collect()});origins.push((f.origin.clone(),true));scales.push(den);}
 }
 let before_lp=Instant::now();
 let answer=produce_certificate_hybrid(&hyps,ids.len()-1).0;
 let lp_ns=before_lp.elapsed().as_nanos();
 let cert=match answer{
 Some(c)if verify_cert(&hyps,&c)=>Value::Array(c.into_iter().filter(|(_,c)|!c.is_zero()).map(|(i,c)|json!({"origin":origins[i].0,"flip":origins[i].1,"coeff":(c*&scales[i]).to_string()})).collect()),
 _=>Value::Null};
 let exact_nnz:usize=hyps.iter().map(|h|h.coeffs.iter().filter(|(_,c)|!c.is_zero()).count()+usize::from(h.ineq==Ineq::Lt)).sum();
 let product_columns:Vec<bool>=origins.iter().map(|(origin,_)|origin[0]=="mul").collect();
 Ok(json!({"cert":cert,"linear_ns":linear_ns,"products_ns":products_ns,"lp_ns":lp_ns,"facts":all.len(),"atoms":ids.len()-1,
  "exact_certificate_shape":{"rows":ids.len()+1,"cols":hyps.len(),"nnz":exact_nnz},
  "generated_products":all.len()-pool.len()-1,"product_columns":product_columns}))
}
fn main(){
 let stdin=std::io::stdin();let mut out=std::io::BufWriter::new(std::io::stdout().lock());
 for line in stdin.lock().lines(){let Ok(line)=line else{break};if line.trim().is_empty(){continue}
 let answer=std::panic::catch_unwind(||serde_json::from_str(&line).map_err(|e|e.to_string()).and_then(solve));
 let v=match answer{Ok(Ok(v))=>v,Ok(Err(e))=>json!({"error":e}),Err(_)=>json!({"error":"panic"})};
 writeln!(out,"{}",v).unwrap();out.flush().unwrap();
 }}
