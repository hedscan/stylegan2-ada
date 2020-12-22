import glob
import os
import re

from pathlib import Path

def get_parent_dir(run_dir):
    out_dir = Path(run_dir).parent

    return out_dir

def locate_latest_pkl(out_dir):
    all_pickle_names = sorted(glob.glob(os.path.join(out_dir, '0*', 'network-*.pkl')))

    try:
        latest_pickle_name = all_pickle_names[-1]
    except IndexError:
        latest_pickle_name = None

    return latest_pickle_name

def parse_kimg_from_network_name(network_pickle_name):

    if network_pickle_name is not None:
        resume_run_id = os.path.basename(os.path.dirname(network_pickle_name))
        RE_KIMG = re.compile(r'network-snapshot-(\d+).pkl')
        try:
            kimg = int(RE_KIMG.match(os.path.basename(network_pickle_name)).group(1))
        except AttributeError:
            kimg = 0.0
    else:
        kimg = 0.0

    return float(kimg)

def locate_latest_log_file(out_dir):
    all_log_files = sorted(glob.glob(os.path.join(out_dir, '0*', 'log.txt')))

    try:
        latest_log_file = all_log_files[-1]
    except IndexError:
        latest_log_file = None
    return latest_log_file

def parse_resume_augment_val_from_log_file(logfile, kimg):
    # Open log file
    with open(logfile) as f:
        # read training tick summaries from log file into list
        ticklines = [line.rstrip('\n') for line in f if 'tick' in line]
    # Create a dict of param: value pairs per tick
    ticks = [
        {j.split(maxsplit=1)[0]: j.split(maxsplit=1)[1].strip()
         for j in splitline}
         # Regex splits on whitespace followed by char a-z
        for splitline in [re.split(r'\s(?=[a-z])', line) for line in ticklines]]
    # Get actual tick we are resuming from (not necessarily last)
    resume_tick = next(tick for tick in ticks if float(tick['kimg']) == kimg)
    return float(resume_tick['augment'])
