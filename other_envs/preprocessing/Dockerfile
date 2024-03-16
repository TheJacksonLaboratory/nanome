# @Author   : Yang Liu
# @FileName : Dockerfile
# @Software : NANOME project
# @Organization : JAX Li Lab
# @Website  : https://github.com/LabShengLi/nanome

FROM ubuntu

# Author and maintainer
MAINTAINER Yang Liu <yang.liu@jax.org>
LABEL description="Nanome project in Li Lab at The Jackson Laboratory" \
      author="yang.liu@jax.org"

ARG BUILD_PACKAGES="wget apt-transport-https procps git curl libnvidia-compute-460-server"
ARG DEBIAN_FRONTEND="noninteractive"

RUN apt-get -q update && \
    DEBIAN_FRONTEND="noninteractive" apt-get -q install --yes ${BUILD_PACKAGES} && \
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
COPY preprocessing_env.yml /
RUN conda env create --name preprocessing --file=preprocessing_env.yml && conda clean -a

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "preprocessing", "/bin/bash", "-c"]

# Set env path into PATH
ENV PATH /opt/conda/envs/preprocessing/bin:$PATH
ENV LD_LIBRARY_PATH /opt/conda/envs/preprocessing/lib:$LD_LIBRARY_PATH
ENV HDF5_PLUGIN_PATH /opt/conda/envs/preprocessing/hdf5/lib/plugin:$HDF5_PLUGIN_PATH

USER root
WORKDIR /data/

CMD ["bash"]
