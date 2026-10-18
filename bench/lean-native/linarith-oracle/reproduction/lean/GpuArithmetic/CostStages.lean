/- gpu-smt reproduction snapshot; local Lean4.27 adaptation/reduced diagnostic implementation. See ../../PROVENANCE.md. -/
import GpuArithmetic.CostTelemetry
import Mathlib.Tactic.Linarith.Frontend
import Farkas.Native
import Farkas.Fast
open Lean Meta Elab Tactic Mathlib.Tactic.Linarith
namespace GpuArithmetic.CostStages
@[extern "gpu_smt_thread_cpu_ns"] opaque threadCpuNs : IO UInt64
structure Costs where
  times : Std.HashMap String (Nat × Nat) := {}
  products : Std.HashSet Expr := {}
def Costs.getD (s : Costs) (key : String) (fallback : Nat × Nat) : Nat × Nat :=
  s.times.getD key fallback
def Costs.insert (s : Costs) (key : String) (value : Nat × Nat) : Costs :=
  {s with times := s.times.insert key value}
def Costs.toList (s : Costs) : List (String × (Nat × Nat)) := s.times.toList
def registerProducts (_ref : IO.Ref Costs) (_proofs : List Expr) : IO Unit := pure ()
def productColumns (_ref : IO.Ref Costs) (_inputs : List Expr) : IO String := pure "null"

def timed (_ref : IO.Ref Costs) (_name : String) (act : MetaM α) : MetaM α := act

def proveFalseByLinarith (cost : IO.Ref Costs) (transparency : TransparencyMode) (oracle : CertificateOracle)
    (discharger : TacticM Unit) : MVarId → List Expr → MetaM (Expr × List Nat)
  | _, [] => throwError "no args to linarith"
  | g, l@(h::_) => do
      Lean.Core.checkSystem decl_name%.toString
      -- for the elimination to work properly, we must add a proof of `-1 < 0` to the list,
      -- along with negated equality proofs.
      let lidx := l.zipIdx
      let l' ← timed cost "linearize" <| detailTrace "addNegEqProofs" <| addNegEqProofsIdx lidx
      let inputsTagged : List (Expr × Option Nat) ←
        timed cost "linearize" <| detailTrace "mkNegOneLtZeroProof" <|
          return ((← mkNegOneLtZeroProof (← typeOfIneqProof h)), none) ::
            (l'.reverse.map fun ⟨e, i⟩ => (e, some i))
      let inputs := inputsTagged.map Prod.fst
      trace[linarith.detail] "inputs:{indentD <| toMessageData (← inputs.mapM inferType)}"
      let (comps, max_var) ← timed cost "linearize" <| detailTrace "linearFormsAndMaxVar" <|
        linearFormsAndMaxVar transparency inputs
      trace[linarith.detail] "comps:{indentD <| toMessageData comps}"
      -- perform the elimination and fail if no contradiction is found.
      pure ()
      let certificate : Std.HashMap Nat Nat ←
        timed cost "lp" <| withTraceNode `linarith (return m!"{exceptEmoji ·} Invoking oracle") do
          let certificate ←
            try
              let flags ← productColumns cost inputs
              withOptions (fun opts => opts.setString `gpuSmtCostProductColumns flags) do
                oracle.produceCertificate comps max_var
            catch e =>
              trace[linarith] e.toMessageData
              throwError "linarith failed to find a contradiction"
          trace[linarith] "found a contradiction: {certificate.toList}"
          return certificate
      timed cost "certificate" do
        let (sm, zip, idxs) ←
          withTraceNode `linarith (return m!"{exceptEmoji ·} Building final expression") do
            let enum_inputs := inputsTagged.zipIdx
            -- construct a list pairing nonzero coeffs with the proof of their corresponding
            -- comparison and track the original index
            let used := enum_inputs.filterMap fun ⟨⟨e, orig?⟩, n⟩ =>
              (certificate[n]?).map fun c => (e, c, orig?)
            let zip := used.map fun ⟨e, c, _⟩ => (e, c)
            let mls ← used.mapM fun ⟨e, c, _⟩ => do mulExpr c (← leftOfIneqProof e)
            -- `sm` is the sum of input terms, scaled to cancel out all variables.
            let sm ← addExprs mls
            -- let sm ← instantiateMVars sm
            trace[linarith] "{indentD sm}\nshould be both 0 and negative"
            let idxs :=
              (used.foldl (fun acc (_, _, orig?) =>
                  match orig? with
                  | some i => i :: acc
                  | none => acc) []).eraseDups
            return (sm, zip, idxs)
        -- we prove that `sm = 0`, typically with `ring`.
        let sm_eq_zero ← detailTrace "proveEqZeroUsing" <| proveEqZeroUsing discharger sm
        -- we also prove that `sm < 0`
        let sm_lt_zero ← detailTrace "mkLTZeroProof" <| mkLTZeroProof zip
        let pf ← detailTrace "Linarith.lt_irrefl" do
          -- this is a contradiction.
          let pftp ← inferType sm_lt_zero
          let ⟨_, nep, _⟩ ← g.rewrite pftp sm_eq_zero
          let pf' ← mkAppM ``Eq.mp #[nep, sm_lt_zero]
          mkAppM ``Mathlib.Tactic.Linarith.lt_irrefl #[pf']
        return (pf, idxs)
where
  /-- Log `f` under `linarith.detail`, with exception emojis and the provided name. -/
  detailTrace {α} (s : String) (f : MetaM α) : MetaM α :=
    withTraceNode `linarith.detail (return m!"{exceptEmoji ·} {s}") f

def findLinarithContradiction (cost : IO.Ref Costs) (cfg : LinarithConfig) (g : MVarId)
    (ls : List (Expr × List (Expr × Nat))) : MetaM (Expr × List Nat) :=
  try
    ls.firstM (fun ⟨α, L⟩ =>
      withTraceNode `linarith (return m!"{exceptEmoji ·} running on type {α}") do
        let (pf, idxs) ←
          GpuArithmetic.CostStages.proveFalseByLinarith cost cfg.transparency cfg.oracle cfg.discharger g (L.map Prod.fst)
        let idxs := idxs.map fun i => L[i]!.2
        return (pf, idxs))
  catch e => throwError "linarith failed to find a contradiction\n{g}\n{e.toMessageData}"

/--
Given a list `hyps` of proofs of comparisons, `runLinarith cfg prefType g hyps` preprocesses
`hyps` according to the list of preprocessors in `cfg`. This results in a list of branches
(typically only one), each of which must succeed in order to close the goal.

In each branch, the hypotheses are partitioned by type and `linarith` is run on each class in
turn; one of these must succeed in order for `linarith` to succeed on the branch. If `prefType`
is provided, the corresponding class is tried first.

On success, the metavariable `g` is assigned and the function returns the indices of the
original hypotheses that were used with nonzero coefficient in the final proof.
-/
-- If it succeeds, the passed metavariable should have been assigned.
def runLinarith (cost : IO.Ref Costs) (cfg : LinarithConfig) (prefType : Option Expr) (g : MVarId)
    (hyps : List Expr) : MetaM (List Nat) := do
  let singleProcess (g : MVarId) (hyps : List (Expr × Nat)) : MetaM (Expr × List Nat) :=
    g.withContext do
      linarithTraceProofs
        s!"after preprocessing, linarith has {hyps.length} facts:" (hyps.map Prod.fst)
      let mut hyp_set ← partitionByTypeIdx hyps
      trace[linarith] "hypotheses appear in {hyp_set.size} different types"
      -- If we have a preferred type, strip it from `hyp_set` and prepare a handler with a custom
      -- trace message
      let pref : MetaM _ ← do
        if let some t := prefType then
          let (i, vs) ← hyp_set.find t
          hyp_set := hyp_set.eraseIdxIfInBounds i
          pure <|
            withTraceNode `linarith (return m!"{exceptEmoji ·} running on preferred type {t}") do
              let (pf, idxs) ←
                GpuArithmetic.CostStages.proveFalseByLinarith cost cfg.transparency cfg.oracle cfg.discharger g (vs.map Prod.fst)
              let idxs := idxs.map fun j => vs[j]!.2
              return (pf, idxs)
        else
          pure failure
      pref <|> GpuArithmetic.CostStages.findLinarithContradiction cost cfg g hyp_set.toList
  let mut preprocessors := cfg.preprocessors
  if cfg.splitNe then
    preprocessors := Mathlib.Tactic.Linarith.removeNe :: preprocessors
  if cfg.splitHypotheses then
    preprocessors := Mathlib.Tactic.Linarith.splitConjunctions.globalize.branching :: preprocessors
  preprocessors := preprocessors.map fun pp =>
    { pp with transform := fun g hs => timed cost (if pp.description == "nonlinear arithmetic extras" then "products" else "preprocess") (pp.transform g hs) }
  let branches ← preprocess preprocessors g hyps
  let mut used : List Nat := []
  for (g, es) in branches do
    let esIdx := es.zipIdx
    let (r, idxs) ← singleProcess g esIdx
    g.assign r
    used := idxs ++ used
  -- Verify that we closed the goal. Failure here should only result from a bad `Preprocessor`.
  (Expr.mvar g).ensureHasNoMVars
  return used.eraseDups

-- /--
-- `filterHyps restr_type hyps` takes a list of proofs of comparisons `hyps`, and filters it
-- to only those that are comparisons over the type `restr_type`.
-- -/
-- def filterHyps (restr_type : Expr) (hyps : List Expr) : MetaM (List Expr) :=
--   hyps.filterM (fun h => do
--     let ht ← inferType h
--     match getContrLemma ht with
--     | some (_, htype) => isDefEq htype restr_type
--     | none => return false)

/--
`GpuArithmetic.CostStages.linarithUsedHyps cost only_on hyps cfg g` runs `linarith` with the supplied hypotheses. It
fails if the goal cannot be closed. When successful, it returns the subset of `hyps` that
were actually used (i.e. had a nonzero coefficient) in the final certificate.

* `hyps` is a list of proofs of comparisons to include in the search.
* If `only_on` is true, the search will be restricted to `hyps`. Otherwise it will use all
  comparisons in the local context.
* If `cfg.transparency := semireducible`,
  it will unfold semireducible definitions when trying to match atomic expressions.
-/
partial def linarithUsedHyps (cost : IO.Ref Costs) (only_on : Bool) (hyps : List Expr)
    (cfg : LinarithConfig := {}) (g : MVarId) : MetaM (List Expr) := g.withContext do
  -- if the target is an equality, we run `linarith` twice, to prove ≤ and ≥.
  if (← whnfR (← instantiateMVars (← g.getType))).isEq then
    trace[linarith] "target is an equality: splitting"
    if let some [g₁, g₂] ← try? (g.apply (← mkConst' ``eq_of_not_lt_of_not_gt)) then
      let h₁ ← withTraceNode `linarith (return m!"{exceptEmoji ·} proving ≥") <|
        GpuArithmetic.CostStages.linarithUsedHyps cost only_on hyps cfg g₁
      let h₂ ← withTraceNode `linarith (return m!"{exceptEmoji ·} proving ≤") <|
        GpuArithmetic.CostStages.linarithUsedHyps cost only_on hyps cfg g₂
      return h₁ ++ h₂

  /- If we are proving a comparison goal (and not just `False`), we consider the type of the
    elements in the comparison to be the "preferred" type. That is, if we find comparison
    hypotheses in multiple types, we will run `linarith` on the goal type first.
    In this case we also receive a new variable from moving the goal to a hypothesis.
    Otherwise, there is no preferred type and no new variable; we simply change the goal to `False`.
  -/

  let (g, target_type, new_var) ← match ← applyContrLemma g with
  | (none, g) =>
    if cfg.exfalso then
      trace[linarith] "using exfalso"
      pure (← g.exfalso, none, none)
    else
      pure (g, none, none)
  | (some (t, v), g) => pure (g, some t, some v)

  g.withContext do
    -- set up the list of hypotheses, considering the `only_on` and `restrict_type` options
    let hyps ←
      (if only_on then return new_var.toList ++ hyps
        else return (← getLocalHyps).toList ++ hyps)

    -- TODO in mathlib3 we could specify a restriction to a single type.
    -- I haven't done that here because I don't know how to store a `Type` in `LinarithConfig`.
    -- There's only one use of the `restrict_type` configuration option in mathlib3,
    -- and it can be avoided just by using `linarith only`.

    linarithTraceProofs "linarith is running on the following hypotheses:" hyps
    let usedIdxs ← GpuArithmetic.CostStages.runLinarith cost cfg target_type g hyps
    let used := usedIdxs.filterMap (hyps[·]?)
    let used := match new_var with
      | some nv => used.filter (fun h => !(h == nv))
      | none => used
    return used

/--
Run the core `linarith` procedure on the goal `g` using the hypotheses `hyps`.
If `only_on` is true, the search is restricted to `hyps`; otherwise all suitable
local hypotheses are considered. This is the workhorse behind the user-facing
`linarith` tactic.
-/
partial def linarith (cost : IO.Ref Costs) (only_on : Bool) (hyps : List Expr) (cfg : LinarithConfig := {})
    (g : MVarId) : MetaM Unit := do
  discard <| GpuArithmetic.CostStages.linarithUsedHyps cost only_on hyps cfg g

def run (nlin onlyOn : Bool) (args : List Expr) (cfg : LinarithConfig) : TacticM Unit := do
  if (← IO.getEnv "GPU_ARITHMETIC_PROFILE").isNone then throwUnsupportedSyntax
  let cost ← IO.mkRef ({} : Costs)
  let w ← IO.monoNanosNow
  let c ← threadCpuNs
  let cfg := if nlin then { cfg with preprocessors := cfg.preprocessors.concat nlinarithExtras } else cfg
  try
    commitIfNoEx do liftMetaFinishingTactic <| GpuArithmetic.CostStages.linarith cost onlyOn args cfg
  finally
    let dc := (← threadCpuNs).toNat - c.toNat
    let dw := (← IO.monoNanosNow) - w
    if (← IO.getEnv "GPU_ARITHMETIC_PROFILE").isSome then
      let stats ← cost.get
      let source := (← getFileMap).source
      let fields := [("ty","\"arithmetic-stages\""),("source",Farkas.Telemetry.jstrEsc source),
        ("nlin",if nlin then "true" else "false"),("cpu_ns",toString dc),("wall_ns",toString dw),
        ("stages","{" ++ ",".intercalate (stats.toList.map fun (k,v) =>
          Farkas.Telemetry.jstrEsc k ++ ":[" ++ toString v.1 ++ "," ++ toString v.2 ++ "]") ++ "}")]
      pure ()
elab_rules : tactic
  | `(tactic| linarith $[!%$bang]? $cfg:optConfig $[only%$o]? $[[$args,*]]?) => withMainContext do
    let args ← ((args.map (Syntax.TSepArray.getElems)).getD {}).mapM (elabTermWithoutNewMVars `linarith)
    let cfg := (← Mathlib.Tactic.elabLinarithConfig cfg).updateReducibility bang.isSome
    run false o.isSome args.toList cfg

elab_rules : tactic
  | `(tactic| nlinarith $[!%$bang]? $cfg:optConfig $[only%$o]? $[[$args,*]]?) => withMainContext do
    let args ← ((args.map (Syntax.TSepArray.getElems)).getD {}).mapM (elabTermWithoutNewMVars `nlinarith)
    let cfg := (← Mathlib.Tactic.elabLinarithConfig cfg).updateReducibility bang.isSome
    run true o.isSome args.toList cfg
end GpuArithmetic.CostStages
