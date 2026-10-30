# syntax=docker/dockerfile:1
FROM rust:1.98.1-bookworm AS engine
WORKDIR /src
ENV CARGO_BUILD_JOBS=1
COPY Cargo.toml Cargo.lock ./
COPY crates ./crates
RUN cargo build --release --locked -p proofserve

FROM debian:bookworm-slim AS lean
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl git zstd python3 build-essential binutils libgmp-dev \
    && rm -rf /var/lib/apt/lists/*
ENV PATH="/opt/lean/bin:${PATH}"
RUN mkdir -p /opt/lean /opt/repl /opt/mathlib && \
    curl -fL https://github.com/leanprover/lean4/releases/download/v4.18.0/lean-4.18.0-linux.tar.zst \
    | tar --zstd -x --strip-components=1 -C /opt/lean
RUN curl -fL https://codeload.github.com/leanprover-community/repl/tar.gz/2f0a3cb876b045cc0fe550ca3a625bc479816739 \
    | tar -xz --strip-components=1 -C /opt/repl
WORKDIR /opt/repl
RUN lake build
RUN curl -fL https://codeload.github.com/leanprover-community/mathlib4/tar.gz/aa936c36e8484abd300577139faf8e945850831a \
    | tar -xz --strip-components=1 -C /opt/mathlib
WORKDIR /opt/mathlib
RUN lake exe cache get
COPY native/lean /opt/native-source
RUN python3 /opt/native-source/build.py --project /opt/repl --sysroot /opt/lean --out /opt/prepared

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates libgmp10 libstdc++6 python3 git && rm -rf /var/lib/apt/lists/*
ENV PATH="/opt/lean/bin:${PATH}"
COPY --from=engine /src/target/release/proofserve /usr/local/bin/proofserve
COPY --from=lean /opt/lean /opt/lean
COPY --from=lean /opt/repl /opt/repl
COPY --from=lean /opt/mathlib /opt/mathlib
COPY --from=lean /opt/prepared /opt/prepared
COPY packaging/start-proofserve /usr/local/bin/start-proofserve
COPY packaging/container_smoke.py /opt/container_smoke.py
COPY clients/python/proofserve /opt/client/proofserve
ENV PYTHONPATH="/opt/client"
WORKDIR /opt/mathlib
EXPOSE 3000
ENTRYPOINT ["/bin/sh", "/usr/local/bin/start-proofserve"]
CMD ["serve", "--listen", "0.0.0.0:3000"]
RUN --network=none python3 /opt/container_smoke.py --self-test
