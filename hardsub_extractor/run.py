from videocr import save_subtitles_to_file
from tqdm.auto import tqdm
import multiprocessing as mp
import parmap
import os
import json    
# from functools import partial
# from itertools import repeat

import warnings
warnings.filterwarnings("ignore")


def get_config():
    with open('config.json', 'r') as f:  
        config = json.load(f)
    return config

def get_videopaths(config):
    DIR_PATH = config['DIR_PATH']
    VIDEO_TYPE = config['VIDEO_TYPE']
    files = os.listdir(DIR_PATH)
    files = [file for file in files if file.endswith(VIDEO_TYPE)]
    print(f"=== List of videos: {files}===")
    return files

def process_B(conf,files): # deprecated
    num_cores = mp.cpu_count()
    pool = Pool(num_cores)
    arg1 = (conf,files)
    #M = pool.starmap(func, zip(a_args, repeat(second_arg)))
    pool.starmap(save_subtitles,zip(repeat(conf),repeat(files),range(len(files))))

def multiprocessing(conf,files):
    num_cores = mp.cpu_count()
    print(f"\n=== Multiprocessing Started with the number of Cores: {num_cores}===\n")
    parmap.map(save_subtitles, 
               list(range(len(files))),
               conf=conf,
               files=files,
               pm_pbar={"desc": "TOTAL:",
                        "position":0,
                        "leave": True},
               pm_processes=num_cores)
    return



def save_subtitles(idx:int,
                   conf: dict,
                   files:list):

    # set input file path
    input_file_path = conf['DIR_PATH'] + '/' + str(files[idx])
    
    # set output file path
    output_file_path = conf['DIR_PATH'] + '/' + str(files[idx]).split('.')[:-1][0] + '.srt'
    # output_file_path = (conf['DIR_PATH'] + '/' + str(files[0])).split('.')[:-1]
    # output_file_path.extend(['.srt'])
    # output_file_path = ''.join(output_file_path)
    
    # check if srt file exists
    if os.path.exists(output_file_path):
        if not os.path.getsize(output_file_path):
            pass
        else:
            print(f"Subtitle Exists: {files[idx]}")
            return

    # run
    print(f"Processing: {str(files[idx])}\n")
    save_subtitles_to_file(idx,
                           input_file_path,
                           output_file_path,
                           lang=conf['language_code'],
                           use_gpu=conf['use_gpu'],
                           time_start=conf['start_time'],
                           time_end=conf['end_time'], 
                           conf_threshold=conf['confidence_threshold'],
                           sim_threshold=conf['similarity_threshold'],
                           use_fullframe=conf['use_fullframe'], # note: videocr just assumes horizontal lines of text. vertical text scenario hasn't been implemented yet
                           frames_to_skip=conf['frames_to_skip'], # can skip inference for some frames to speed up the process
                           crop_x=conf['crop_x'],
                           crop_y=conf['crop_y'],
                           crop_width=conf['crop_width'],
                           crop_height=conf['crop_height'],
                           similar_image_threshold = conf['similar_image_threshold'],
                           similar_pixel_threshold = conf['similar_pixel_threshold'],
                          )
    return



if __name__ == '__main__':
    conf = get_config()
    files= get_videopaths(conf)
    multiprocessing(conf,files)