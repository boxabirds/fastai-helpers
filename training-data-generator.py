#!/usr/bin/env python3

#fast.ai batch Google image downloader helper
#for the 2018 Lesson 1 that requires test images to be in test/ and train/directories
# execution example:
# training-data-generator vespas "vespa gtv,vespa gts,vespa primavera,vespa sprint,vespa 946"
import sys
import random
import os
import pip
import re
import argparse
from google_images_download import google_images_download

TEST_DIR_NAME = "test"
TRAIN_DIR_NAME = "train"


parser = argparse.ArgumentParser()
parser.add_argument('-d',action="store",dest="dest_dir",default="test-data",help="destination directory path to store the files, inside of which you'll have a test and train directory, inside that will have one directory per search term")
parser.add_argument('-s',action="store",dest="search_terms",default="cats,dogs",help="comma-separate list of terms to search for")
parser.add_argument("-q",action="store",dest="quantity_per_term",type=int,default=100,help="how many images to get for each search term (max 100)")
parser.add_argument("-t",action="store",dest="test_set_size_percentage",type=int, default=20,help="how much of the data to set aside to test set (percentage, e.g. '20')")

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
    return results.dest_dir, results.search_terms, results.quantity_per_term, results.test_set_size_percentage

def ensure_dir_exists( dest_dir, sub_dir, file_name ):
    path = os.path.join( dest_dir, sub_dir, file_name )
    print ("Ensuring existence of directory '%s'" % path )
    if not os.path.exists(path):
        os.makedirs(path)

# mirror directory structure in test and train directories
def prepare_training_data_directories(dest_dir):
    search_term_dirs = os.listdir( dest_dir )
    print( search_term_dirs )
    for dir in search_term_dirs:
        ensure_dir_exists( dest_dir, TEST_DIR_NAME, dir )
        ensure_dir_exists( dest_dir, TRAIN_DIR_NAME, dir )

# redistribute images between test and train
def redistribute_images(dest_dir,search_terms,test_set_size_percentage):

    # split search terms with commas or commas and whitespace
    # https://stackoverflow.com/questions/4071396/split-by-comma-and-strip-whitespace-in-python
    pattern = re.compile( "^\s+|\s*,\s*|\s+$" )
    search_term_list= [x for x in pattern.split(search_terms) if x]
    print( "Search term list: '%s'" % search_term_list )
    for search_term_dir in search_term_list:
        print( "search term dir: '%s'" % search_term_dir )
        path = os.path.join( dest_dir, search_term_dir )
        files = os.listdir( path )
        print( "files: '%s'" % files )
        num_files = len(files)
        test_set_size = num_files * (test_set_size_percentage / 100)
        print( f'test set size: {test_set_size}' )
        if( test_set_size < 1 ):
            print( "please increase your test percentage, with only %s files that percentages is less than one file" % num_files )
        else:
            test_set_size = int(test_set_size)
            test_files = random.choices(population=files,k=test_set_size)
            print( f'Test files: {test_files}' )


if __name__ == "__main__":

    # get all the command line options
    dest_dir,search_terms,quantity_per_term,test_set_size_percentage = get_options()

    # get the files, then create a structure 
    # compatible with the Jupyter notebook in fast.ai's lesson 1
    download_test_images(dest_dir,search_terms,quantity_per_term)
    prepare_training_data_directories(dest_dir)
    redistribute_images(dest_dir,search_terms,test_set_size_percentage)


