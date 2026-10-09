import Cache.Requests
open Cache IO Hashing Requests System
-- Official hash/download/unpack path on archive-extracted sources.
-- Optional browser-widget release download requires absent Git metadata;
-- skipping that download leaves exact cached native OLeans unchanged.
def main : IO Unit := do
  CacheM.run do
    let roots ← parseArgs ["Mathlib"]
    let memo ← getHashMemo roots
    let goodCurl ← validateCurl
    validateLeanTar
    downloadFiles MATHLIBREPO memo.hashMap false goodCurl true
    unpackCache memo.hashMap false
