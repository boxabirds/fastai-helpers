#!/usr/bin/env python3

#fast.ai batch Google image downloader helper
#for the 2018 Lesson 1 that requires test images to be in test/ and train/directories
# execution example:
# training-data-generator vespas "vespa gtv,vespa gts,vespa primavera,vespa sprint,vespa 946"
import sys
import shutil
import random
import os
import pip
import re
import argparse
from google_images_download import google_images_download

VALID_DIR_NAME = "valid"
TRAIN_DIR_NAME = "train"


parser = argparse.ArgumentParser()
parser.add_argument('-d',action="store",dest="dest_dir",default="test-data",help="destination directory path to store the files, inside of which you'll have a test and train directory, inside that will have one directory per search term")
parser.add_argument('-s',action="store",dest="search_terms",default="cats,dogs",help="comma-separated list of terms to search for")
parser.add_argument("-q",action="store",dest="quantity_per_term",type=int,default=100,help="how many images to get for each search term (max 100)")
parser.add_argument("-v",action="store",dest="valid_pct",type=int, default=20,help="how much of the data to set aside for validation set (percentage, e.g. '20')")

def install_and_import(package):
    pass

def download_test_images(dest_dir,search_terms,quantity_per_term):
    response = google_images_download.googleimagesdownload()
    arguments = {
        "keywords":search_terms,
        "limit":quantity_per_term,
        "type":"photo",
        "output_directory":dest_dir
    }

    # get the downloader to download up 100 images inside a folder called <dest_dir>/<search term>
    # one for each search term e.g. "downloads/vespa gtv"
    response.download(arguments)


def get_options():
    results = parser.parse_args()
    print( "destination folder: '%s'" % results.dest_dir )
    print( "search terms: '%s'" % results.search_terms )
    print( "quantity per term: '%s'" % results.quantity_per_term )
    print( f'validation set percentage: {results.valid_pct}%' )
    return results.dest_dir, results.search_terms, results.quantity_per_term, results.valid_pct

def ensure_dir_exists( dest_dir, sub_dir, file_name ):
    path = os.path.join( dest_dir, sub_dir, file_name )
    print ("Ensuring existence of directory '%s'" % path )
    if not os.path.exists(path):
        os.makedirs(path)

# mirror directory structure in valid directories
def prepare_training_data_directories(dest_dir):
    search_term_dirs = os.listdir( dest_dir )
    print( search_term_dirs )
    for dir in search_term_dirs:
        ensure_dir_exists( dest_dir, VALID_DIR_NAME, dir )

# redistribute images between valid and train
def redistribute_images(dest_dir,search_terms,valid_pct):

    # split search terms with commas or commas and whitespace
    # https://stackoverflow.com/questions/4071396/split-by-comma-and-strip-whitespace-in-python
    pattern = re.compile( "^\s+|\s*,\s*|\s+$" )
    search_term_list= [x for x in pattern.split(search_terms) if x]
    print( "Search term list: '%s'" % search_term_list )
    for search_term_dir in search_term_list:
        #print( "search term dir: '%s'" % search_term_dir )
        path = os.path.join( dest_dir, search_term_dir )
        files = os.listdir( path )
        #print( "files: '%s'" % files )
        num_files = len(files)
        validation_set_size = num_files * (valid_pct / 100)
        #print( f'validation set size: {validation_set_size}' )
        if( validation_set_size < 1 ):
            print( "please increase your validation percentage, with only %s files that percentages is less than one file... skipping" % num_files )
        else:
            validation_set_size = int(validation_set_size)
            validation_files = random.choices(population=files,k=validation_set_size)
            #print( f'Randomly chosen validation files: {validation_files}' )
            for validation_file in validation_files:
                src_path = os.path.join( dest_dir, search_term_dir, validation_file )
                #print( f'source: "{src_path}"' );
                dest_path = os.path.join( dest_dir, VALID_DIR_NAME, search_term_dir, validation_file )
                #print( f'dest:   "{dest_path}"' );
                shutil.move( src_path, dest_path )
        # move the downloaded files into the train directory now
        src_path = os.path.join( dest_dir, search_term_dir )
        dest_path = os.path.join( dest_dir, TRAIN_DIR_NAME, search_term_dir )
        print( f'moving {src_path} to {dest_path}' )
        shutil.move( src_path, dest_path )

if __name__ == "__main__":

    # get all the command line options
    dest_dir,search_terms,quantity_per_term,valid_pct = get_options()

    # get the files, then create a structure 
    # compatible with the Jupyter notebook in fast.ai's lesson 1
    download_test_images(dest_dir,search_terms,quantity_per_term)
    prepare_training_data_directories(dest_dir)
    redistribute_images(dest_dir,search_terms,valid_pct)


