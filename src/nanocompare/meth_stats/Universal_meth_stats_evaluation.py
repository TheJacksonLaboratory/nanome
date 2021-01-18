"""

Evaluation based on methylation calls of four tools, compute the performance results(F1, accuracy, etc.)

/projects/li-lab/NanoporeData/WR_ONT_analyses/NanoCompare/automated_DeepSignal_runs/NA19240/NA19240_DeepSignal.MethCalls.Joined.tsv /projects/li-lab/NanoporeData/WR_ONT_analyses/NanoCompare/automated_Tombo_runs/NA19240/NA19240_Tombo.batch_all.batch_0.perReadsStats.bed /projects/li-lab/NanoporeData/WR_ONT_analyses/NA19240_nanopolish/NA19240.methylation_calls.tsv /projects/li-lab/NanoporeData/WR_ONT_analyses/NanoCompare/automated_DeepMod_runs/NA19240/NA19240.C.combined.bed /projects/li-lab/NanoporeData/WR_ONT_analyses/NanoCompare/EncodeMethyl/joined_reps/RRBS/extractBismark/NA19240_joined_RRBS.Read_R1.Rep_1_trimmed_bismark_bt2.bismark.cov.gz NA19240_RRBS_joined/NA19240_RRBS_joined bismark 10 Tombo


"""
"""
   This script will generate all performance results, bed files of singleton, non-singleton, based on results by DL call tool related to BGTruth results
"""

import argparse

from nanocompare.global_settings import rename_coordinate_name, perf_report_columns
from nanocompare.global_settings import singletonsFile, narrowCoord, nonsingletonsFile
from nanocompare.meth_stats.meth_stats_common import *


def parse_arguments():
    """
    :return:
    """
    parser = argparse.ArgumentParser(description='Performance evaluation task')
    parser.add_argument('--min-bgtruth-cov', type=int, help="min bg-truth coverage cutoff", default=5)
    parser.add_argument('--min-tool-cov', type=int, help="min tool coverage cutoff", default=3)
    parser.add_argument('--dsname', type=str, help="dataset name", default='DS')
    parser.add_argument('--runid', type=str, help="running prefix", required=True)
    parser.add_argument('--report-joined', action='store_true', help="True if report on only joined sets")
    parser.add_argument('--test', action='store_true', help="True if only test for short time running")
    parser.add_argument('--calls', nargs='+', help='all ONT call results <tool-name>:<file-name>', required=True)
    parser.add_argument('--bgtruth', type=str, help="background truth file <encode-type>:<file-name>", required=True)
    parser.add_argument('-o', type=str, help="output dir", default=pic_base_dir)
    return parser.parse_args()


if __name__ == '__main__':
    set_log_debug_level()

    args = parse_arguments()

    dsname = args.dsname
    bgtruth_cov_cutoff = args.min_bgtruth_cov
    tool_cov_cutoff = args.min_tool_cov
    report_joined = args.report_joined

    RunPrefix = args.runid.replace('MethPerf-', '')

    out_dir = os.path.join(args.o, args.runid)
    os.makedirs(out_dir, exist_ok=True)
    logger.info(f'Output to dir:{out_dir}')

    # Add logging files also to result output dir
    add_logging_file(os.path.join(out_dir, 'run-results.log'))

    logger.debug(args)

    # Note: all bed files (Singleton and NonSingleton) are 1-based start, even for "chr1  123  124" (This will conform for + or - strand).
    # So we must import as 1-based format for our tool or bgtruth, DO NOT USE baseFormat=0
    baseFormat = 1

    callfn_dict = defaultdict()  # callname -> filename
    callresult_dict = defaultdict()  # name->call
    callname_list = []  # [DeepSignal, DeepMod, etc.]

    # with Pool(processes=args.processors) as pool:
    for callstr in args.calls:
        callname, callfn = callstr.split(':')
        callname_list.append(callname)
        callfn_dict[callname] = callfn
        callresult_dict[callname] = import_call(callfn, callname, baseFormat=baseFormat)
        # callresult_dict[callname] = pool.apply_async(import_call, (callfn, callname,))

    logger.debug(callfn_dict)
    encode, fn = args.bgtruth.split(':')
    logger.debug(f'BGTruth fn={fn}, encode={encode}')

    bgTruth = import_bgtruth(fn, encode, cov=bgtruth_cov_cutoff, baseFormat=baseFormat, includeCov=True)

    relateCoord = list(narrowCoord)  # copy the basic coordinate

    ## add missing region files:
    singletonsFilePrefix = singletonsFile.replace(".bed", '')
    # relateCoord.append("{}/{}.{}.mixed.bed".format(out_dir, RunPrefix, singletonsFilePrefix))
    relateCoord.append(f"{out_dir}/{RunPrefix}.{singletonsFilePrefix}.absolute.bed")

    nonsingletonsFilePrefix = nonsingletonsFile.replace(".bed", '')
    # relateCoord.append("{}/{}.{}.other.bed".format(out_dir, RunPrefix, nonsingletonsFilePrefix))
    # relateCoord.append("{}/{}.{}.fullyMixed.bed".format(out_dir, RunPrefix, nonsingletonsFilePrefix))
    relateCoord.append(f"{out_dir}/{RunPrefix}.{nonsingletonsFilePrefix}.discordant.bed")
    relateCoord.append(f"{out_dir}/{RunPrefix}.{nonsingletonsFilePrefix}.concordant.bed")

    logger.debug(list(enumerate(relateCoord)))  # all coordinate generated

    if not args.test:
        ret = singletonsPostprocessing(bgTruth, singletonsFile, RunPrefix, outdir=out_dir)
        ret.update(nonSingletonsPostprocessing(bgTruth, nonsingletonsFile, RunPrefix, outdir=out_dir))
        df = pd.DataFrame([ret], index=[f'{dsname}'])
        outfn = os.path.join(out_dir, f'{RunPrefix}.summary.singleton.nonsingleton.csv')
        df.to_csv(outfn)
        logger.info(f'save to {outfn}')

    logger.info("\n\n############\n\n")

    # this file is the all tool joined together sites
    bedfn_tool_join_bgtruth = f"{out_dir}/{RunPrefix}.Tools_BGTruth_Joined.bed"

    # this file is used for all coverage > 4 for correlation analysis
    fn_secondFilterBed_4Corr = f"{out_dir}/{RunPrefix}.Tools_BGTruth_Joined.4Corr.bed"

    joinedCPG = set(bgTruth.keys())
    for toolname in callresult_dict:
        joinedCPG = joinedCPG.intersection(set(callresult_dict[toolname].keys()))
    save_keys_to_single_site_bed(joinedCPG, outfn=bedfn_tool_join_bgtruth, callBaseFormat=baseFormat, outBaseFormat=1)

    logger.info(f"Data points for joined all tools with bg-truth (cov>={bgtruth_cov_cutoff}) stats: {len(joinedCPG):,}\n\n")

    joinedCPG4Corr = combine2programsCalls_4Corr(bgTruth, None, cutt=tool_cov_cutoff, only_bgtruth=True)
    for toolname in callresult_dict:
        joinedCPG4Corr = combine2programsCalls_4Corr(joinedCPG4Corr, callresult_dict[toolname], cutt=tool_cov_cutoff)

    joinedCPG4CorrSet = set(joinedCPG4Corr.keys())
    save_keys_to_single_site_bed(joinedCPG4CorrSet, outfn=fn_secondFilterBed_4Corr, callBaseFormat=baseFormat, outBaseFormat=1)

    logger.info(f"Data points for correlation tools(cov>={tool_cov_cutoff}) with bg-truth(cov>={bgtruth_cov_cutoff}): {len(joinedCPG4CorrSet):,}\n\n")
    logger.info("\n\n############\n\n")

    if report_joined:  # Joined together evaluation
        perf_dir = os.path.join(out_dir, 'performance-results')
        os.makedirs(perf_dir, exist_ok=True)
    else:  # only based on bgtruth
        perf_dir = os.path.join(out_dir, 'performance-results-nojoined')
        os.makedirs(perf_dir, exist_ok=True)

    for tool in callresult_dict:
        tmpPrefix = f'{RunPrefix}.{tool}'
        logger.info(f'Evaluating: {tmpPrefix}')

        # Note: relateCoord - all singleton (absolute and mixed) and non-singleton generated bed. ranges
        #       secondFilterBed - joined sites of four tools and bg-truth. points
        if report_joined:  # step: with joined results of all tools
            df = report_per_read_performance(callresult_dict[tool], bgTruth, tmpPrefix, narrowedCoordinatesList=relateCoord, secondFilterBed=bedfn_tool_join_bgtruth, secondFilterBed_4Corr=fn_secondFilterBed_4Corr, outdir=perf_dir, tagname=tmpPrefix, test=args.test)
        else:  # step: no joined results
            df = report_per_read_performance(callresult_dict[tool], bgTruth, tmpPrefix, narrowedCoordinatesList=relateCoord, secondFilterBed=None, secondFilterBed_4Corr=fn_secondFilterBed_4Corr, outdir=perf_dir, tagname=tmpPrefix, test=args.test)

        df['Tool'] = tool
        df['Dataset'] = dsname
        df = rename_coordinate_name(df)

        # logger.debug(df)
        # logger.debug(df.columns)

        # Select columns to save
        df = df[perf_report_columns]

        outfn = os.path.join(perf_dir, f"{RunPrefix}.{tool}.performance.report.csv")
        df.to_csv(outfn)
        logger.info(f"save to {outfn}")

        # This file will always report intermediate results
        tmpfn = os.path.join(perf_dir, 'performance.report.tmp.csv')
        os.remove(tmpfn)

        if args.test:
            break
    logger.info("Meth stats performance data generation DONE.")
