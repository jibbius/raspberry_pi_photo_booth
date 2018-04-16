#!/usr/bin/env python
"""
This script polls a directory
"""
import os
import subprocess
import sys
# import argparse
# import dropbox
from shutil import copy2
from shutil import move
from time import sleep

REAL_PATH = os.path.dirname(os.path.realpath(__file__))
INPUT_DIRECTORY      = REAL_PATH + "/photos/"             # Files will be taken from here.
BACKUP_DIRECTORY     = REAL_PATH + "/photos-raw/"         # A backup of the file will be saved here.
PROCESSING_DIRECTORY = REAL_PATH + "/photos-processing/"  # Files will temporarily occupy this folder, whilst being processed.
OUTPUT_DIRECTORY     = REAL_PATH + "/photos-done/"        # Files will be placed in this folder, once all processing is complete.
COMPRESSION_FACTOR = 90
FILE_EXT = '.jpg'

def required_folders_health_test():
    folders_list=[INPUT_DIRECTORY, BACKUP_DIRECTORY, PROCESSING_DIRECTORY, OUTPUT_DIRECTORY]
    folders_checked=[]

    for folder in folders_list:
        if folder not in folders_checked:
            folders_checked.append(folder)
        else:
            print('ERROR: Cannot use same folder path ('+folder+') twice. Refer config file.')

        #Create folder if doesn't exist
        if not os.path.exists(folder):
            print('Creating folder: ' + folder)
            os.makedirs(folder)

def filename_matches_expected_format(f):
    #TODO: Replace the code below with Regex equivalent
    result = False

    filename_base = os.path.splitext(f)[0]
    filename_ext = os.path.splitext(f)[1]

    # Is the file a '.jpg'?
    if(filename_ext == FILE_EXT):

        # Does the filename have two '_' chars?
        if(filename_base.count('_') == 2):
            result = True

    return result

def get_filename_components(f):
    filename_base = os.path.splitext(f)[0]
    filename_ext = os.path.splitext(f)[1]

    #Break filename into its respective components:
    date_stamp, time_stamp, x_of_y = filename_base.split('_')
    x, y = x_of_y.split('of')

    # Return values  
    filename_prefix = date_stamp + '_' + time_stamp
    photo_number = int(x)
    total_pics   = int(y)
    
    return (filename_prefix, photo_number, total_pics, filename_ext)

def construct_filename_from_components(filename_prefix, photo_number, total_pics, ext):
    filename = filename_prefix + '_' + str(photo_number) + 'of'+ str(total_pics) + ext
    return filename

def do_all_expected_files_matching_this_prefix_exist(filename_prefix, total_pics, ext, list_of_files):
    all_files_exist = True

    for photo_number in range(1, total_pics + 1 ):
        filename_to_test = construct_filename_from_components(filename_prefix, photo_number, total_pics, ext)

        if(filename_to_test not in list_of_files):
            all_files_exist = False
            print('File not found : ' + filename_to_test)

    return all_files_exist

def perform_image_optimisation(this_file, perform_colour_correction=True, compression_factor='90%', debug=True):
    output_file = this_file

    command=['magick','convert']
    command.extend(['-strip']) #Strip out meta tags
    command.extend(['-interlace','Plane'])
    command.extend(['-gaussian-blur','0.05'])
    command.extend(['-quality',compression_factor])
    
    if perform_colour_correction:
        command.extend([this_file, '-auto-level', output_file])
    else:
        command.extend([this_file, output_file])
    
    result = subprocess.call(command)

    if debug and not result == 0:
        print(result)    
    return result

def create_animated_gif(folder_path, filename_prefix, total_pics, size='200x120', duration='100', compression_factor='50%', debug=True):

    source_images = folder_path + filename_prefix + '_' + '[1-' + str(total_pics) + ']' + 'of' + str(total_pics) +'.jpg'
    output_file = folder_path + filename_prefix + '_thumbnail.gif'

    command=['magick','convert']
    command.extend(['-quality',compression_factor])
    command.extend(['-delay', duration])
    command.extend(['-resize', size])

    command.append(source_images) #source images
    command.append(output_file) #destination

    result = subprocess.call(command)

    if debug and not result == 0:
        print(result)    

    return output_file

def create_photo_strip(folder_path, filename_prefix, total_pics, layout='2x',image_size='1920x1152', margin='20', debug=True):

    source_images = folder_path + filename_prefix + '_' + '[1-' + str(total_pics) + ']' + 'of' + str(total_pics) + '.jpg'
    output_file = folder_path + filename_prefix + '_layout_' + layout + '.jpg'

    command=['magick','montage']
    command.extend(['-tile',layout])
    command.extend(['-geometry',image_size + '+' + margin + '+' + margin])

    command.append(source_images) #source images
    command.append(output_file) #destination

    result = subprocess.call(command)

    if debug and result != 0:
        print(result)    

    return output_file

def stopwatch(message):
    """Context manager to print how long a block of code took."""
    t0 = time.time()
    try:
        yield
    finally:
        t1 = time.time()
        print('Total elapsed time for %s: %.3f' % (message, t1 - t0))

def dropbox_upload(file_path):
    print('Function is not yet implemented [dropbox_upload]')

# def upload(dbx, fullname, folder, subfolder, name, overwrite=False):
#     """Upload a file.
#     Return the request response, or None in case of error.
#     """
#     path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'), name)
#     while '//' in path:
#         path = path.replace('//', '/')
#     mode = (dropbox.files.WriteMode.overwrite
#             if overwrite
#             else dropbox.files.WriteMode.add)
#     mtime = os.path.getmtime(fullname)
#     with open(fullname, 'rb') as f:
#         data = f.read()
#     with stopwatch('upload %d bytes' % len(data)):
#         try:
#             res = dbx.files_upload(
#                 data, path, mode,
#                 client_modified=datetime.datetime(*time.gmtime(mtime)[:6]),
#                 mute=True)
#         except dropbox.exceptions.ApiError as err:
#             print('*** API error', err)
#             return None
#     print('uploaded as', res.name.encode('utf8'))
#     return res

def main():
    """
    Main program loop
    """
    required_folders_health_test()

    while True:
        print('---------------')
        list_of_known_input_files = os.listdir(INPUT_DIRECTORY)

        for file in list_of_known_input_files:

            #Check to see if filename matches our expected format (e.g. 2018-04-11_15-39-29_1of4.jpg )
            if(filename_matches_expected_format(file)):

                #Break filename into its respective components:
                filename_prefix, photo_number, total_pics, ext = get_filename_components(file)

                #If this is the last file in the set, then lets confirm that all the other files are present;
                if(photo_number == total_pics):
                    print('')
                    print('Found photo group [' + filename_prefix + ']:')

                    files_to_process = []
                    files_to_upload_to_dropbox = []
                    completed_files = []
                    missing_files = False

                    for photo_number in range(1, total_pics + 1 ):
                        expected_file = construct_filename_from_components(filename_prefix, photo_number, total_pics, ext)

                        if expected_file not in(list_of_known_input_files):
                            print('The following file is missing: ' + expected_file)
                            missing_files = True
                        else:
                            files_to_process.append(expected_file)

                    # If there were any missing files, we won't process anything right now
                    if(missing_files):
                        files_to_process = []
                    else:
                        print(' - All ' + str(total_pics) + ' photos found.')

                    #Move/copy of each processing "files for processing"
                    for this_file in files_to_process:

                        #Backup the file:
                        print(' - Creating image backup: ' + this_file)
                        copy2(INPUT_DIRECTORY + this_file, BACKUP_DIRECTORY + this_file)

                        #Move file into processing directory
                        print(' - Moving image into \'processing\' directory: ' + this_file)
                        move(INPUT_DIRECTORY + this_file, PROCESSING_DIRECTORY + this_file)

                    #Start processing our group of files
                    for this_file in files_to_process:

                        #Perform image optimisations with Imagemagick
                        print(' - Optimising image size: ' + this_file)
                        perform_image_optimisation(PROCESSING_DIRECTORY + this_file)

                        #Later, we will upload this file to dropbox:
                        files_to_upload_to_dropbox.append(PROCESSING_DIRECTORY + this_file)

                        #Later, we will move this folder to our 'DONE' directory:
                        completed_files.append(PROCESSING_DIRECTORY + this_file)

                    if(files_to_process):

                        #Create animated gif
                        print(' - Creating animated thumbnail')
                        this_animated_gif = create_animated_gif(PROCESSING_DIRECTORY, filename_prefix, total_pics)
                        files_to_upload_to_dropbox.append(this_animated_gif)
                        completed_files.append(this_animated_gif)

                        #Create photo strip ( 1x4 layout)
                        print(' - Creating photo strip (1 column layout)')
                        this_photo_strip = create_photo_strip(PROCESSING_DIRECTORY, filename_prefix, total_pics, '1x')
                        files_to_upload_to_dropbox.append(this_photo_strip)
                        completed_files.append(this_photo_strip)

                        #Create photo strip ( 2x2 layout)
                        print(' - Creating photo strip (2 column layout)')
                        this_photo_strip = create_photo_strip(PROCESSING_DIRECTORY, filename_prefix, total_pics, '2x')
                        files_to_upload_to_dropbox.append(this_photo_strip)
                        completed_files.append(this_photo_strip)

                    for this_file in files_to_upload_to_dropbox:
                        print(' - Uploading to dropbox: ' + this_file)
                        dropbox_upload(this_file)

                    for this_file in completed_files:
                        print(' - Clean up: ' + this_file)

                        if os.path.exists(this_file):
                            #If a file with this name already exists in 'Done' folder then we will need to remove it.
                            target_filename = OUTPUT_DIRECTORY + os.path.basename(this_file)
                            if(os.path.exists(target_filename)):
                                print(' - Overwriting: ' + target_filename)
                                os.remove(target_filename) #If we don't do this then "move" will fail.

                            #Move file to "Done" folder
                            move(this_file, OUTPUT_DIRECTORY)

        sleep(10)

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print('Goodbye')

