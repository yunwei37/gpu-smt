# Fresh request EOF repair and native24 qualification — root self-review

First qualification(003152Z) was interrupted after74.292420s with four actual
native processes stuck after their initial work. Pinned upstream4.9repl prints
JSON+blank delimiter but does not explicitly flush before reading another
input. It blocked on pipe read while the fresh backend kept input open and
waited for buffered stdout. No native logical rejection or candidate timeout
is inferred from the manually interrupted records.24partial rows,queued20,
four actual attempts,rawlogs,RSS and pre-repair source retained;allpidsretired.

Repair:after submitting exactly one fresh request,close its input. EOF makes
this upstream loop exit/flush. This matches raw-native differential input
lifetime;no proofsource,timeout,upstream algorithm,process cap or nativeparser
decision changes. Regression fixture withholds reply untilEOF,then returns
normally;the existing process/retirement checks now exercise that case.
Fmt/Clippy/fullordinarytests/docs/CLI pass. Existing native tests remain
explicitly ignored in that generic check;real24source run follows.
Release build succeeds;source/logs retained.

Actual003542Z rerun:24original sources execute through native and prepared
conditions at48GiB totalRSS,CPU8–11,onecorelease,nofixedAS. Both return21accepted/
3rejected,exactaccepted sets/allstatusesequal and match the same24historical
native labels. No cache/coalescing/freshfallback. One prepared parent loads
5,545modules once and serves these24branches;allparent/child/rootpidsretired.
Actual fresh-native samples showfourpositiveRSSleaders withaffinities8/9/10/11.
Prepared1sretained snapshots do not establishfoursustainedbusychildren;terminal
maxregisteredleaders includes transient admission observations,not CPUbusyproof.
Allsamplings are observations,not hardkernelRSSquotas.
Native/prepared externalclocks17.730862198/3.931333937s are rawqualification,
not7808population,sustainedspeedup or strongestwarmservice comparison.
Terminals peak14,515,625,984/5,313,019,904B acrossallmonitorcalls;retained1srows
may have lowermaxima. Resource/asymmetricmeasurementdefinitions preserved.

Old scheduling group complete/pushed. Newfullpair uses this corrected source
and exact7808inputs after this boundary iscommitted. Ownenginefresh/prepared
resource support,not workloadnovelty. Fourroutes/RQs remainopen.
Rootself-review,noindependentaudit or agentdelegation.
