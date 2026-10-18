import sys,json,time,resource,pathlib
resource.setrlimit(resource.RLIMIT_AS,(48*1024**3,48*1024**3));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
sys.path.insert(0,'/tmp/gpu-smt-linarith-oracle-20261017/race-oracle-pooled/cuopt-grpc')
import grpc,cuopt_remote_data_pb2 as d,cuopt_remote_pb2 as c,cuopt_remote_service_pb2 as s,cuopt_remote_service_pb2_grpc as r
q=json.loads(pathlib.Path(__file__).with_name('failed-barrier-LP.json').read_text());n=q['ncols'];rhs=q['rhs']
ch=grpc.insecure_channel(sys.argv[1]+':5001');grpc.channel_ready_future(ch).result(timeout=60);stub=r.CuOptRemoteServiceStub(ch);job=None;t=time.monotonic_ns()
try:
 model=d.OptimizationProblem(A_values=q['values'],A_indices=q['indices'],A_offsets=q['offsets'],c=[0.]*n,b=rhs,variable_lower_bounds=[0.]*n,variable_upper_bounds=[float('inf')]*n,constraint_lower_bounds=rhs,constraint_upper_bounds=rhs,row_types=b'E'*len(rhs),objective_scaling_factor=1.)
 req=c.SolveLPRequest(header=c.RequestHeader(version=1,problem_category=d.LP),problem=model,settings=d.PDLPSolverSettings(method=d.Barrier,crossover=True))
 job=stub.SubmitJob(s.SubmitJobRequest(lp_request=req)).job_id;print(json.dumps({'event':'submitted','job':job}),flush=True)
 stub.WaitForCompletion(s.WaitRequest(job_id=job));v=stub.GetResult(s.GetResultRequest(job_id=job));sol=v.lp_solution
 print(json.dumps({'status':v.status,'message':v.error_message or sol.error_message,'engine':sol.solved_by,'termination':sol.lp_termination_status,'primal_length':len(sol.primal_solution),'solver_seconds':sol.solve_time,'whole_ns':time.monotonic_ns()-t}),flush=True)
finally:
 if job:stub.DeleteResult(s.DeleteRequest(job_id=job))
 ch.close()
