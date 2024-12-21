# Use an ARM64-compatible Debian image
FROM arm64v8/debian:buster

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget build-essential m4 gcc make ocaml-nox

# download and install ocaml
RUN wget https://caml.inria.fr/pub/distrib/ocaml-3.08/ocaml-3.08.3.tar.gz && \
    tar -xvf ocaml-3.08.3.tar.gz && \
    cd ocaml-3.08.3 && \
    ./configure && \
    make world && \
    make opt && \
    make install

# working directory

WORKDIR /gramm-ecc-reductions