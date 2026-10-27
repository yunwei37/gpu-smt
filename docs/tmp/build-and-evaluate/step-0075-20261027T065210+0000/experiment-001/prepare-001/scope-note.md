The reused support runner receipt carries the inherited label
rust_support_test_only:true. In this cell its retained command executes only
the offline input-preparation script. No Rust test or native candidate ran.
Keep the original receipt/source unchanged;the command/native-count fields
and this scope note define actual preparation. Release-001 is a Rust build,
not a Rust test or native candidate execution either.
