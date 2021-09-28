# DNA methylation-calling tools for Oxford Nanopore sequencing: a survey and human epigenome-wide evaluation
## --NANOME(Nanopore methylation) pipeline for evaluation of DNA methylation calling tools for Oxford Nanopore sequencing 

## Methodology of NANOME pipeline

**Background:** Nanopore long-read sequencing technology greatly expands the capacity of long-range, single-molecule DNA-modification detection. A growing number of analytical tools have been developed to detect DNA methylation from nanopore sequencing reads. Here, we assess the performance of different methylation calling tools to provide a systematic evaluation to guide researchers performing human epigenome-wide studies.


![Figure1A](https://github.com/TheJacksonLaboratory/nanome/blob/master/docs/Fig1A.jpg)

**Fig. 1A. Survey of methylation calling tools .**  Timeline of publication and technological developments of Oxford Nanopore Technologies (ONT) methylation calling tools to detect DNA cytosine modifications. 


![Figure1B](https://github.com/TheJacksonLaboratory/nanome/blob/master/docs/Fig1B.jpg)
**Fig. 1B. Workflow for 5-methylcytosine (5mC) detection for nanopore sequencing.** 


**Results:** We compared seven analytic tools for detecting DNA modifications from nanopore long-read sequencing data. We evaluated the CpG methylation-detection accuracy, CpG site coverage, and running time using nanopore sequencing data across different genomic contexts, using natural human DNA. Furthermore, we provide an online DNA methylation database (https://nanome.jax.org) with which to display the DNA methylation levels detected by nanopore sequencing and bisulfite sequencing data across different genomic contexts.


**Conclusions:** Our study is the first benchmark of computational methods for detection of mammalian whole-genome DNA-modifications in nanopore sequencing. We provide a broad foundation for cross-platform standardization, and an evaluation of analytical tools designed for genome-scale modified-base detection using nanopore sequencing. 

## System Requirements

### Hardware requirements

The NANOME is based on Nextflow pipeline framework, and start with raw fast5 nanopore sequencing input data with a reference genome. The pipeline can be configured with different RAM, number of processors, GPU resources schema to parallel run all methylation calling tools. For optimal usage, we recommend using NANOME pipeline on HPC:
* GPU or CPU with 2+ cores. 
* RAM: 7+ GB per cpu.
* Storage using HDD or SSD. Please ensure your storage before running the pipeline.


### Software requirements

We provide conda, docker and singularity environments which depend on below well-known open-source packages for methylation calling for nanopore sequencing data:

[nanopolish](https://github.com/jts/nanopolish) >=0.13.2  
[ont-tombo](https://github.com/nanoporetech/tombo) >=1.5.1  
[deepsignal](https://github.com/bioinfomaticsCSU/deepsignal) >=0.1.8  
[deepmod](https://github.com/WGLab/DeepMod) >=0.1.3  
[megalodon](https://github.com/nanoporetech/megalodon) >=2.2.9  
[METEORE](https://github.com/comprna/METEORE) >=1.0.0  
[ont-pyguppy-client-lib](https://github.com/nanoporetech/pyguppyclient) >=4.2.2  
[fast5mod](https://github.com/nanoporetech/fast5mod) >=1.0.5

Guppy software >= 4.2.2 from [ONT (Oxford Nanopore Technologies) website](https://nanoporetech.com)


## Installation
Users only need to install **Nextflow** by `curl -fsSL get.nextflow.io | bash`, execution environment will be automatically configured.

NANOME pipeline support running with various ways in different platforms:
* Conda
    1. Create conda enviroment: `conda env create -f environment.yml`
* Docker
    1. Docker container name from [Docker Hub](https://hub.docker.com/repository/docker/liuyangzzu/nanome): `liuyangzzu/nanome:latest`, you can also build docker image by `docker build -t liuyangzzu/nanome:latest .`
* Singularity
    1. Pull image from [Docker Hub](https://hub.docker.com/repository/docker/liuyangzzu/nanome): `singularity pull docker://liuyangzzu/nanome:latest`
* HPC clusters with **SLURM** support
* Google Cloud platform with **google-lifesciences** support

Therefore, NANOME pipeline can be easily executed without any installation steps:
```angular2html
./nextflow run https://github.com/TheJacksonLaboratory/nanome.git \
    -profile ci,singularity,hpc
```

For running on CloudOS platform (such as google cloud), please check [Usage](https://github.com/TheJacksonLaboratory/nanome/blob/master/docs/Usage.md#4-running-pipeline-on-cloud-computing-platform). 

[comment]: <> (We will update more information within a short time.)

## Usage

Please refer to [Usage](https://github.com/TheJacksonLaboratory/nanome/blob/master/docs/Usage.md) for how to use NANOME pipeline.

## Pipeline reports
### Benchmarking reports on our HPC using [Nextflow](https://www.nextflow.io/)

We constructed a set of benchmarking datasets that contain reads from 800 to 8,000 reads for NA19240, and monitored job running timeline and resource usage on our HPC, reports generated by **Nextflow** workflows are: [Trace file](https://github.com/TheJacksonLaboratory/nanome/blob/master/docs/resources/trace_benchmark.txt.tsv), [Report](https://github.com/TheJacksonLaboratory/nanome/blob/master/docs/resources/report_benchmark.pdf)  and [Timeline](https://github.com/TheJacksonLaboratory/nanome/blob/master/docs/resources/timeline_benchmark.pdf). 

Our HPC hardware specifications are as follows:
* CPU: Intel(R) Xeon(R) Gold 6136 CPU @ 3.00GHz
* GPU: Tesla V100-SXM2-32GB 
* RAM: 300 GB
* Slurm manager version: 19.05.5

### Pipeline DAG
<img src="https://github.com/TheJacksonLaboratory/nanome/blob/mini_docker/docs/resources/trace_benchmark.txt.tsv), [Report](https://github.com/TheJacksonLaboratory/nanome/blob/master/docs/nanome_dag.png" width="600"/>


![NanomeDag](https://github.com/TheJacksonLaboratory/nanome/blob/mini_docker/docs/resources/trace_benchmark.txt.tsv), [Report](https://github.com/TheJacksonLaboratory/nanome/blob/master/docs/nanome_dag.png)

## Revision History

For release history, please visit [here](https://github.com/TheJacksonLaboratory/nanome/releases). For details, please go [here](https://github.com/TheJacksonLaboratory/nanome/blob/master/README.md).

## Contact

If you have any questions/issues/bugs, please post them on [GitHub](https://github.com/TheJacksonLaboratory/nanome/issues). We will regularly update the Github to support more methylation calling tools.

## Reference
Detailed results can be found in our preprint. Please cite our preprint below if you are interested in our code repository:

 **DNA methylation calling tools for Oxford Nanopore sequencing: a survey and human epigenome-wide evaluation.** bioRxiv, 2021. Online at https://doi.org/10.1101/2021.05.05.442849.
