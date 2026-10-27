The inherited native_body_elaboration:false field refers only to absent
original generated-workload candidates. This cell did execute one native Lean
compiler and elaborate/check the generic contract module,including its theorem.
It is a build/unit dependency,not zero native computation. Raw receipt/source
are retained. Later cells use explicit contract-versus-original-workload fields.
