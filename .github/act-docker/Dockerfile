# Pull base image
FROM ubuntu:22.04

# ALL DEPENDENCIES
# This step installs all of the dependencies needed to build the tooling necessary to build
# compliance environment
# Install tools by apt
ENV DEBIAN_FRONTEND=noninteractive
RUN set -x \
    && apt-get -y update \
    && apt-get -y install \
# essential tools
    apt-utils \
    git \
    wget \
    vim \
    gawk \
    flex \
    bison \
    gperf \
    telnet \
    bc \
    curl \
    zip \
    unzip \
    z3 \
    texinfo \
    sudo \
# python3
    python3.10 \
    python3-pip \
    python3-dev \
# network tools
    iputils-ping \
    net-tools \
    netcat-openbsd \
# building tools
    build-essential \
    make \
    autoconf \
    automake \
    autotools-dev \
    gcc \
    g++ \
    pkg-config \
    libtool \
    device-tree-compiler \
    patchutils \
# qemu
    opensbi \ 
    qemu-system-misc \
    u-boot-qemu \
# gdb dependencies
    libncurses* \
    libncurses5-dev \
# qemu dependencies
    libnuma-dev \
    libcurl4-gnutls-dev \
    libiscsi-dev \
    libaio-dev \
    libnfs-dev \
    librbd-dev \
    libxkbcommon-dev \
    libfdt-dev \
    libpixman-1-dev \
    libepoxy-dev \
    libpng-dev \ 
    libjpeg-turbo8-dev \
    libsnappy-dev \
    liblzo2-dev \
    libsdl2-dev \
    libvdeplug-dev \
    libgtk-3-dev \
    libcacard-dev \
    libbrlapi-dev \
    libcapstone-dev \
    libspice-server-dev \ 
    libpmem-dev \
    libdaxctl-dev \
    libslirp-dev \
    libsdl2-image-dev \
    libvirglrenderer-dev \
    libusbredirhost-dev \
    libfuse3-dev \
# opam dependencies
    opam \
    libmpc-dev \
    libmpfr-dev \
    libgmp-dev \
    zlib1g-dev \
    libexpat-dev \
    libusb-1.0 \
    && apt clean && rm -rf /var/lib/apt/lists \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1 \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 \
    && : # last line

# install packages via pip3
RUN set -x \
    && python3 -m pip install -U pip setuptools \
    && pip3 install -U \
        pexpect \
        PyYAML \
        numpy \
        pytest \
        prettytable \
        colorlog \
        GitPython \
        click \
        Jinja2 \
        pytz \
        riscof \
        riscv-config \
        riscv-isac \
        riscv-ctg \
    && : # last line


# add new user
ENV DOCKER_USER act
RUN useradd -U -m -u 1000 -s /bin/bash -p "$(openssl passwd -1 123)" $DOCKER_USER \
    && usermod -aG sudo $DOCKER_USER \
    && echo '%sudo ALL=(ALL) NOPASSWD: ALL' | EDITOR='tee -a' visudo \
    && : # last line


# Initial Docker User
USER $DOCKER_USER
WORKDIR /home/act

# Install Opam and sail
RUN set -x \
    && opam init --yes --disable-sandboxing \
    && opam install --yes \
        sail \
        herdtools7 \
    && : # last line

# build RISC-v Sail golden model from source code
RUN set -x \
    && eval $(opam env) \
    && git clone https://github.com/rems-project/sail-riscv.git \
    && cd sail-riscv \
    && make ocaml_emulator/riscv_ocaml_sim_RV64 \
    && make c_emulator/riscv_sim_RV64 \
    && ARCH=RV32 make ocaml_emulator/riscv_ocaml_sim_RV32 \
    && ARCH=RV32 make c_emulator/riscv_sim_RV32 \
    && mkdir -p /home/act/sail/bin \
    && mv ./c_emulator/riscv_sim_* /home/act/sail/bin \
    && mv ./ocaml_emulator/riscv_ocaml_sim_* /home/act/sail/bin \
    && cd $HOME \
    && rm -rf sail-riscv \
    && : # last line


# build SPIKE model from source
RUN set -x \
    && git clone https://github.com/riscv/riscv-isa-sim.git -b master \
    && cd riscv-isa-sim \
    && mkdir build \
    && cd build \
    && ../configure --prefix=$RISCV \
    && make -j $(nproc) 1>/dev/null \
    && sudo make install \
    && cd $HOME \
    && rm -rf riscv-isa-sim \
    && : # last line

# Download and install riscv-gnu-toochain 32bit & 64bit
RUN set -x \
    && wget -q https://github.com/riscv-collab/riscv-gnu-toolchain/releases/download/2023.10.06/riscv64-elf-ubuntu-22.04-gcc-nightly-2023.10.06-nightly.tar.gz -O riscv64-elf-gcc.tar.gz \
    && wget -q https://github.com/riscv-collab/riscv-gnu-toolchain/releases/download/2023.10.06/riscv32-elf-ubuntu-22.04-gcc-nightly-2023.10.06-nightly.tar.gz -O riscv32-elf-gcc.tar.gz \
    && tar -xf riscv64-elf-gcc.tar.gz \
    && tar -xf riscv32-elf-gcc.tar.gz \
    && rm -rf riscv64-elf-gcc.gz \
    && rm -rf riscv32-elf-gcc.tar.gz \
    && : # last line


USER root
# Set environment variables
ENV PATH=/home/act/.opam/default/bin:/home/act/riscv/bin:/home/act/sail/bin:$PATH

RUN litmus7 -version
RUN sail -version
RUN riscv32-unknown-elf-gcc --version
RUN riscv64-unknown-elf-gcc --version
RUN qemu-system-riscv64 -cpu help
RUN riscof --version
RUN riscv_sim_RV64 -h
RUN spike --help


CMD ["/bin/bash"]