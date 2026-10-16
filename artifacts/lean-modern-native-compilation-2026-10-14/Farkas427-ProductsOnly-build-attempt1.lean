import Farkas.Products

open Lean Elab Tactic Meta
open Mathlib.Tactic.Linarith

namespace Farkas427.ProductsOnly

-- Keep the stock parser, configuration and certificate oracle. Only the
-- product-preprocessor implementation changes; the native kernel remains.
elab_rules : tactic
  | `(tactic| nlinarith $[!%$bang]? $cfg:optConfig $[only%$o]? $[[$args,*]]?) =>
    withMainContext do
      let args ← ((args.map (TSepArray.getElems)).getD {}).mapM
        (elabTermWithoutNewMVars `nlinarith)
      let cfg := (← Mathlib.Tactic.elabLinarithConfig cfg).updateReducibility bang.isSome
      let cfg := { cfg with preprocessors := cfg.preprocessors.concat Farkas427.Products.extras }
      commitIfNoEx do
        liftMetaFinishingTactic <| Mathlib.Tactic.Linarith.linarith o.isSome args.toList cfg

end Farkas427.ProductsOnly
