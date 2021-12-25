#!/bin/bash
#SBATCH --job-name=nanome.google_demo
#SBATCH -p compute
#SBATCH -q batch
#SBATCH -N 1 # number of nodes
#SBATCH -n 2 # number of cores
#SBATCH --mem=6G # memory pool for all cores
#SBATCH --time=3-00:00:00 # time
#SBATCH --output=log/%x.%j.log # STDOUT & STDERR
#SBATCH --mail-user=yang.liu@jax.org
#SBATCH --mail-type=END
set -e
baseDir=${1:-/fastscratch/$USER/nanome}
gcpProjectName=${2:-"jax-nanopore-01"}
WORK_DIR_BUCKET=${3:-"gs://jax-nanopore-01-project-data/NANOME-TestData-work"}
OUTPUT_DIR_BUCKET=${4:-"gs://jax-nanopore-01-export-bucket/NANOME-TestData-ouputs"}

pipelineName="gcp_nanome_demo"

rm -rf $baseDir/$pipelineName
mkdir -p $baseDir/$pipelineName
cd $baseDir/$pipelineName

set -ex
date;hostname;pwd

###########################################
###########################################
###########################################
### Run Test pipeline on google cloud
set +x
source $(conda info --base)/etc/profile.d/conda.sh
conda activate py39
gsutil -m rm -rf ${WORK_DIR_BUCKET}  ${OUTPUT_DIR_BUCKET} >/dev/null 2>&1 || true
set -x

## Run test demo on google cloud
echo "### NANOME pipeline for demo data on google START"
nextflow run ${NANOME_DIR}/main.nf\
    -profile docker,google \
	-w ${WORK_DIR_BUCKET} \
	--outdir ${OUTPUT_DIR_BUCKET} \
	--googleProjectName ${gcpProjectName}\
	--dsname TestData \
	--input https://raw.githubusercontent.com/TheJacksonLaboratory/nanome/master/inputs/test.demo.filelist.txt
echo "### NANOME pipeline for demo data on google DONE"

exit 0
###########################################
###########################################
###########################################
### Run Test pipeline on google 12878
## working and outputs dir
WORK_DIR_BUCKET=${1:-"gs://jax-nanopore-01-project-data/NANOME-na12878_chr17_p6-work"}
OUTPUT_DIR_BUCKET=${2:-"gs://jax-nanopore-01-export-bucket/NANOME-na12878_chr17_p6-ouputs"}

gsutil -m rm -rf ${WORK_DIR_BUCKET}  ${OUTPUT_DIR_BUCKET} >/dev/null 2>&1 || true

## Run test demo on google cloud
echo "### nanome pipeline for NA12878 some chr and part file on google START"
nextflow run main.nf\
    -profile docker,google -resume\
	-w ${WORK_DIR_BUCKET} \
	--outdir ${OUTPUT_DIR_BUCKET} \
	--dsname na12878_chr17_p6 \
	--input 'http://s3.amazonaws.com/nanopore-human-wgs/rel3-fast5-chr17.part06.tar'\
	--cleanAnalyses true\
	--tomboResquiggleOptions '--signal-length-range 0 500000  --sequence-length-range 0 50000'

echo "### nanome pipeline for NA12878 some chr and part file on google DONE"
exit 0