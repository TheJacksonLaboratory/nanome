#!/bin/bash
#SBATCH --job-name=nanome.benchmark.hpc
#SBATCH -p gpu
#SBATCH --gres=gpu:1
#SBATCH -q training
#SBATCH -N 1 # number of nodes
#SBATCH -n 1 # number of cores
#SBATCH --mem=20G # memory pool for all cores
#SBATCH --time=14-00:00:00 # time
#SBATCH -o %x.%j.out # STDOUT
#SBATCH -e %x.%j.err # STDERR
#SBATCH --mail-user=yang.liu@jax.org
#SBATCH --mail-type=END

date; hostname; pwd

baseDir=${1:-/fastscratch/li-lab/nanome}

workDir=${baseDir}/work-benchmark
outputsDir=${baseDir}/outputs-benchmark


########################################
########################################
# Ensure directories
mkdir -p ${baseDir}; chmod ugo+w ${baseDir}
export SINGULARITY_CACHEDIR="${baseDir}/singularity-cache"
mkdir -p  $SINGULARITY_CACHEDIR; chmod ugo+w $SINGULARITY_CACHEDIR


########################################
########################################
# Get nextflow and install it
if [ ! -f "nextflow" ]; then
    curl -s https://get.nextflow.io | bash
fi


########################################
########################################
# Clean old results
rm -rf ${workDir} ${outputsDir}
mkdir -p ${workDir}; chmod ugo+w ${workDir}
mkdir -p ${outputsDir}; chmod ugo+w ${outputsDir}


########################################
########################################
# Running pipeline for benchmark data
set -x
./nextflow run main.nf \
    -profile winter_conda -resume\
    -with-report -with-timeline -with-trace -with-dag \
    -work-dir ${workDir} \
    --outputDir ${outputsDir} \
    -config conf/benchmarking.config \
    --processors 8 \
    --filterGPUTaskRuns true