"""
Construct the benchmarking data for resource usage evaluation
"""
import glob
import os
import random
from shutil import copy

import numpy as np
import pandas as pd

from nanocompare.global_config import set_log_debug_level, logger, pic_base_dir

base_input = '/projects/li-lab/Nanopore_compare/nanopore_fast5/NA19240-N300-sept/10'
out_dir = os.path.join(pic_base_dir, 'BenchmarkingData')

trace_fn = '/projects/li-lab/Nanopore_compare/suppdata/benchmarking/benchmarking-trace.txt'

# sizes = [int(x) for x in np.linspace(1000, 10000, 10)]

sample_sizes = [int(x) for x in np.linspace(800, 8000, 10)]

random.seed(688)


def gen_benchmarking_data():
    logger.info(f'gen_benchmarking_data for sample size={sample_sizes}')
    fnlist = glob.glob(os.path.join(base_input, '*.fast5'))

    logger.info(len(fnlist))
    os.makedirs(out_dir, exist_ok=True)

    for t in sample_sizes:
        retfnlist = random.sample(fnlist, k=t)

        benchDir = os.path.join(out_dir, f'MB{t:02n}K')
        os.makedirs(benchDir, exist_ok=True)

        for fn in retfnlist:
            # copy fn into benchDir
            copy(fn, benchDir)
        logger.info(f'Copy done for t={t}, benchDir={benchDir}')


def parse_mem_str_to_gbsize(strmem):
    """
    String like 845 MB	677.8 MB to GB size
    :param strtime:
    :return:
    """
    strmem = strmem.strip()

    if strmem.endswith('MB'):
        memgb = float(strmem[:-2]) / 1024
    elif strmem.endswith('GB'):
        memgb = float(strmem[:-2])
    elif strmem.endswith('KB'):
        memgb = float(strmem[:-2]) / 1024 / 1024
    else:
        raise Exception(f'Not recognized strmem={strmem}')
    return memgb

    pass


def parse_string_time_to_seconds(strtime):
    """
    String like 1h 52m 55s to seconds
    :param strtime:
    :return:
    """
    strlist = strtime.strip().split(' ')
    secs = float(0)
    for strk in strlist:

        if strk.endswith('h'):
            num = int(float(strk[:-1]))
            secs += 60 * 60 * num
        elif strk.endswith('m'):
            num = int(float(strk[:-1]))
            secs += 60 * num
        elif strk.endswith('ms'):
            num = int(float(strk[:-2]))
            secs += num / 1000
        elif strk.endswith('s'):
            num = int(float(strk[:-1]))
            secs += num
        else:
            raise Exception(f"not recognized format strtime={strtime}")
    return secs


def extract_tool_and_dsname_from_name(row):
    """
    Extract Basecall (MB1.6K) into Basecall and MB1.6K, and 1600 three fields
    :param instr:
    :return:
    """
    try:
        toolname, dsname = row['name'].strip().split(' ')
        dsname = dsname[1:-1]
    except:  # No tag process
        toolname = row['name'].strip()
        dsname = 'None'
    if not dsname.startswith('MB'):  # not tagged with MB
        dsname = 'None'
        reads = 0
    else:
        reads = float(dsname[2:-1])

    duration = parse_string_time_to_seconds(row['duration'])
    realtime = parse_string_time_to_seconds(row['realtime'])

    cpu = float(row['%cpu'][:-1])
    peak_rss = parse_mem_str_to_gbsize(row['peak_rss'])
    peak_vmem = parse_mem_str_to_gbsize(row['peak_vmem'])
    rchar = parse_mem_str_to_gbsize(row['rchar'])
    wchar = parse_mem_str_to_gbsize(row['wchar'])

    return toolname, dsname, reads, duration, realtime, cpu, peak_rss, peak_vmem, rchar, wchar


def analyse_trace():
    df = pd.read_csv(trace_fn, sep='\t')
    logger.info(df)

    ## Extract all meaning fields into raw format
    # return toolname, dsname, reads, duration, realtime, cpu, peak_rss, peak_vmem, rchar, wchar
    df[['tool', 'dsname', 'reads', 'duration', 'realtime', '%cpu', 'peak_rss', 'peak_vmem', 'rchar', 'wchar']] = df.apply(extract_tool_and_dsname_from_name, axis=1, result_type="expand")
    logger.info(df)

    outfn = os.path.join(pic_base_dir, 'benchmarking.log.formated.table.all.steps.csv')
    df.to_csv(outfn, sep=',')

    ## Recalculate the time and memory for each tools


    pass


if __name__ == '__main__':
    set_log_debug_level()
    # gen_benchmarking_data()
    analyse_trace()
