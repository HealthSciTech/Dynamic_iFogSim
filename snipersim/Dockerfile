FROM ubuntu:18.04
MAINTAINER Dongjoo Seo <dseo3@uci.edu>

# Add i386 support for support for Pin
RUN dpkg --add-architecture i386
RUN apt-get update && apt-get install -y \
    python \
    screen \
    tmux \
    binutils \
    libc6:i386 \
    libncurses5:i386 \
    libstdc++6:i386 \
 && rm -rf /var/lib/apt/lists/*
# For building Sniper
RUN apt-get update && apt-get install -y \
    automake \
    build-essential \
    curl \
    wget \
    libboost-dev \
    libsqlite3-dev \
    zlib1g-dev \
    libbz2-dev \
    g++-4.8 \
 && rm -rf /var/lib/apt/lists/*
# For building RISC-V Tools
RUN apt-get update && apt-get install -y \
    autoconf \
    automake \
    autotools-dev \
    bc \
    bison \
    curl \
    device-tree-compiler \
    flex \
    gawk \
    gperf \
    libexpat-dev \
    libgmp-dev \
    libmpc-dev \
    libmpfr-dev \
    libtool \
    libusb-1.0-0-dev \
    patchutils \
    pkg-config \
    texinfo \
    zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*
# Helper utilities
RUN apt-get update
RUN apt-get install -y software-properties-common 
RUN apt-get update && apt-get install -y \
    gdb \
    git \
 && rm -rf /var/lib/apt/lists/*

RUN add-apt-repository 'deb http://security.ubuntu.com/ubuntu xenial-security main'
RUN apt update
RUN apt install -y libjasper1 libjasper-dev && rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
        apt-get install -y \
        build-essential \
        cmake \
        git \
        wget \
        unzip \
        yasm \
        pkg-config \
        libswscale-dev \
        libtbb2 \
        libtbb-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libavformat-dev \
        libpq-dev \
	python-pip \
        python2.7 \
        python2.7-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV DEBIAN_FRONTEND="noninteractive"
RUN apt-get install -y python-opencv


ENV PIN_NAME pin-3.11-97998-g7ecce2dac-gcc-linux
WORKDIR /usr/local/bin
RUN wget https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.11-97998-g7ecce2dac-gcc-linux.tar.gz
RUN chmod ugo+x $PIN_NAME.tar.gz
RUN tar -xvzf $PIN_NAME.tar.gz
RUN rm /usr/local/bin/$PIN_NAME.tar.gz
RUN chmod 777 ./$PIN_NAME -R
ENV PIN_HOME /usr/local/bin/$PIN_NAME

RUN mkdir /usr/local/src/sniper
WORKDIR /usr/local/src/sniper
COPY sniper-7.2.tgz ./
RUN tar xvf sniper-7.2.tgz
ENV SNIPER_PATH=/usr/local/src/sniper/sniper-7.2
WORKDIR $SNIPER_PATH
RUN make -j2

RUN pip uninstall -y numpy
RUN pip install pyinstaller==3.5

USER root
WORKDIR /root

SHELL [ "/bin/bash", "-c" ]


# Existing lsb_release causes issues with modern installations of Python3
# https://github.com/pypa/pip/issues/4924#issuecomment-435825490
# Set (temporarily) DEBIAN_FRONTEND to avoid interacting with tzdata
RUN apt-get -qq -y update && \
    apt-get -qq -y upgrade && \
    DEBIAN_FRONTEND=noninteractive apt-get -qq -y install \
        gcc \
        g++ \
        zlibc \
        zlib1g-dev \
        libssl-dev \
        libbz2-dev \
        libsqlite3-dev \
        libncurses5-dev \
        libgdbm-dev \
        libgdbm-compat-dev \
        liblzma-dev \
        libreadline-dev \
        uuid-dev \
        libffi-dev \
        tk-dev \
        wget \
        curl \
        git \
        make \
        sudo \
        bash-completion \
        tree \
        vim \
	libsndfile1 \
        software-properties-common && \
    mv /usr/bin/lsb_release /usr/bin/lsb_release.bak && \
    apt-get -y autoclean && \
    apt-get -y autoremove && \
    rm -rf /var/lib/apt-get/lists/*

RUN apt-get install -y python3.6 python3-pip
# Use C.UTF-8 locale to avoid issues with ASCII encoding
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

USER root

RUN update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
WORKDIR /usr/local/src/sniper/sniper-7.2
RUN wget https://cmake.org/files/v3.16/cmake-3.16.2.tar.gz
RUN tar -xvzf cmake-3.16.2.tar.gz
WORKDIR /usr/local/src/sniper/sniper-7.2/cmake-3.16.2
RUN ./bootstrap --prefix=/usr/local
RUN make -j4
RUN make install

COPY sniper/* /usr/local/src/sniper/sniper-7.2/
WORKDIR /usr/local/src/sniper/sniper-7.2

RUN git clone --recurse-submodules https://github.com/rpreen/xcsf.git
WORKDIR /usr/local/src/sniper/sniper-7.2/xcsf/build
RUN cmake -DCMAKE_BUILD_TYPE=Release -DXCSF_PYLIB=ON -DENABLE_TESTS=ON ..
RUN make -j4

WORKDIR /usr/local/src/sniper/sniper-7.2
COPY default.ini /usr/local/src/sniper/sniper-7.2/
COPY edge.cfg /usr/local/src/sniper/sniper-7.2/
COPY fog.cfg /usr/local/src/sniper/sniper-7.2/
COPY cloud.cfg /usr/local/src/sniper/sniper-7.2/
COPY nehalem.cfg /usr/local/src/sniper/sniper-7.2/

RUN pip3 install numpy scipy pandas cython
RUN pip3 install sklearn

CMD [ "/bin/bash" ]
