# @Author   : Yang Liu
# @FileName : Dockerfile
# @Software : NANOME project
# @Organization : JAX Li Lab
# @Website  : https://github.com/LabShengLi/nanome

# Set the base image to Ubuntu 18.04 and NVIDIA GPU from https://hub.docker.com/r/nvidia/cuda
# or from https://ngc.nvidia.com/catalog/containers/nvidia:cuda/tags
FROM nvidia/cuda:11.6.2-base-ubuntu18.04

# Author and maintainer
MAINTAINER Yang Liu <yang.liu@jax.org>
LABEL description="Nanome project in Li Lab at The Jackson Laboratory" \
      author="yang.liu@jax.org"

# Guppy version 6.4.x is not support, due to no fast5_out option
# ont-remora 2.x is not support, due to pod5 needs python 3.7+
ARG GUPPY_VERSION=6.4.6
ARG REMORA_VERSION=1.1.1
ARG MEGALODON_VERSION=2.5.0
ARG BUILD_PACKAGES="wget apt-transport-https procps git curl libnvidia-compute-460-server"
ARG DEBIAN_FRONTEND="noninteractive"

# Check version of guppy, ref: wget https://americas.oxfordnanoportal.com/software/analysis/ont-guppy-cpu_6.1.3_linux64.tar.gz --no-check-certificate
# Another way: https://pypi.org/project/ont-pyguppy-client-lib/
# Install guppy-gpu version, ref: https://github.com/GenomicParisCentre/dockerfiles
RUN apt-get -q update && \
    DEBIAN_FRONTEND="noninteractive" apt-get -q install --yes ${BUILD_PACKAGES} && \
    cd /tmp && \
    wget -q https://mirror.oxfordnanoportal.com/software/analysis/ont_guppy_${GUPPY_VERSION}-1~bionic_amd64.deb  --no-check-certificate && \
    DEBIAN_FRONTEND="noninteractive" apt-get -q install --yes /tmp/ont_guppy_${GUPPY_VERSION}-1~bionic_amd64.deb && \
    rm *.deb && \
    apt-get autoremove --purge --yes && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

#Install miniconda
RUN wget -q https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O Miniconda.sh && \
    /bin/bash Miniconda.sh -b -p /opt/conda && \
    rm Miniconda.sh

# Adding conda to PATH
ENV PATH /opt/conda/bin:$PATH

# Create the environment:
COPY environment.yml /
RUN conda env create --name nanome --file=environment.yml && conda clean -a

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "nanome", "/bin/bash", "-c"]

# Install latest version for megalodon, even conflicts with fast5mod, they can work
RUN pip install megalodon==${MEGALODON_VERSION} &&\
	pip install ont-remora==${REMORA_VERSION} &&\
    pip cache purge &&\
    npm install -g inliner && npm cache clean --force

# Set nanome env path into PATH
ENV PATH /opt/conda/envs/nanome/bin:$PATH
USER root
WORKDIR /data/

# Get bigwig conversion tool
RUN cd /data && \
    wget -q http://hgdownload.soe.ucsc.edu/admin/exe/linux.x86_64/bedGraphToBigWig &&\
    chmod +x bedGraphToBigWig &&\
    mv bedGraphToBigWig  /usr/local/bin/

CMD ["bash"]
