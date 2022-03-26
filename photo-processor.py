#!/usr/bin/env python
"""
This script polls a directory
"""
#Standard imports
from shutil import copy2
from shutil import move
import os
import subprocess
import sys
import time


#Need to do this early, in case import below fails:
REAL_PATH = os.path.dirname(os.path.realpath(__file__))

#Additional Imports
try:
    import yaml
#    from dropbox.files import WriteMode
#    from dropbox.exceptions import ApiError, AuthError, BadInputError
#    import dropbox
#TODO: FIX THE ABOVE, SUCH THAT DROPBOX IMPORTS ARE CONDITIONALLY INCLUDED (ONLY WHEN DB = ENABLED).

except ImportError as missing_module:
    print('--------------------------------------------')
    print('ERROR:')
    print(missing_module)
    print('')
    print(' - Please run the following command(s) to resolve:')
    if sys.version_info < (3,0):
        print('   pip install -r ' + REAL_PATH + '/requirements.txt')
    else:
        print('   python3 -m pip install -r ' + REAL_PATH + '/requirements.txt')
    print('')
    sys.exit()

#############################
### Load config from file ###
#############################
PATH_TO_CONFIG = 'photo-processor-config.yaml'
PATH_TO_CONFIG_EXAMPLE = 'photo-processor-config.example.yaml'

#Check if config file exists
if not os.path.exists(PATH_TO_CONFIG):
    #Create a new config file, using the example file
    print('Config file was not found. Creating:' + PATH_TO_CONFIG)
    copy2(PATH_TO_CONFIG_EXAMPLE, PATH_TO_CONFIG)

#Read config file using YAML interpreter
with open(PATH_TO_CONFIG, 'r') as stream:
    CONFIG = {}
    try:
        CONFIG = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

#Required config
try:
    # Each of the following varibles, is now configured within [photo-processor-config.yaml]:
    INPUT_DIRECTORY            = CONFIG['INPUT_DIRECTORY']
    PROCESSING_DIRECTORY       = CONFIG['PROCESSING_DIRECTORY']
    OUTPUT_DIRECTORY           = CONFIG['OUTPUT_DIRECTORY']
    OUTPUT_OPTIMISED_STILLS    = CONFIG['OUTPUT_OPTIMISED_STILLS']
    OUTPUT_ANIMATED_THUMBNAILS = CONFIG['OUTPUT_ANIMATED_THUMBNAILS']
    OUTPUT_LAYOUTS             = CONFIG['OUTPUT_LAYOUTS']
    IMAGE_QUALITY              = CONFIG['IMAGE_QUALITY']
    DROPBOX_ENABLED            = CONFIG['DROPBOX_ENABLED']
    DROPBOX_TOKEN              = CONFIG['DROPBOX_TOKEN']

except KeyError as exc:
    print('')
    print('ERROR:')
    print(' - Problems exist within configuration file: [' + PATH_TO_CONFIG + '].')
    print(' - The expected configuration item ' + str(exc) + ' was not found.')
    print(' - Please refer to the example file [' + PATH_TO_CONFIG_EXAMPLE + '], for reference.')
    print('')
    sys.exit()

def health_test_required_folders():
    folders_list=[INPUT_DIRECTORY, PROCESSING_DIRECTORY, OUTPUT_DIRECTORY]
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

def health_test_dropbox():
        # Check for an access token
    if (len(DROPBOX_TOKEN) == 0):
        sys.exit("ERROR: Looks like you didn't add your DROPBOX_TOKEN access token.")

    # Create an instance of a Dropbox class, which can make requests to the API.
    print("Creating a Dropbox object...")
    dbx = dropbox.Dropbox(DROPBOX_TOKEN)

    # Check that the access token is valid
    try:
        dbx.users_get_current_account()
    except AuthError as err:
        sys.exit("ERROR: Invalid DROPBOX token, try re-generating an access token from the app console on the web.")
    except BadInputError as err:
        sys.exit("ERROR: Invalid DROPBOX token, try re-generating an access token from the app console on the web.")

    return dbx

def filename_matches_expected_format(f):
    #TODO: Replace the code below with Regex equivalent?
    result = False

    filename_base = os.path.splitext(f)[0]
    filename_ext = os.path.splitext(f)[1]

    # Is the file a '.jpg'?
    if(filename_ext == '.jpg'):

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

def perform_image_optimisation(src_file, dest_file, perform_colour_correction=True, compression_factor='90%', debug=True):

    command=['convert']
    command.extend(['-strip']) #Strip out meta tags
    command.extend(['-interlace','Plane'])
    command.extend(['-gaussian-blur','0.05'])
    command.extend(['-quality',compression_factor])
    
    if perform_colour_correction:
        command.extend([src_file, '-auto-level', dest_file])
    else:
        command.extend([src_file, dest_file])
    
    result = subprocess.call(command)

    if debug and not result == 0:
        print(result)    
    return result

def create_animated_gif(src_folder_path, src_filename_prefix, dest_file, total_pics, size='200x120', duration='100', image_quality='50%', debug=True):

    source_images = src_folder_path + '/' + src_filename_prefix + '_' + '[1-' + str(total_pics) + ']' + 'of' + str(total_pics) +'.jpg'

    command=['convert']
    command.extend(['-quality',image_quality])
    command.extend(['-delay', duration])
    command.extend(['-resize', size])

    command.append(source_images) #source images
    command.append(dest_file) #destination

    result = subprocess.call(command)

    if debug and not result == 0:
        print(result)    

    return dest_file

def create_photo_strip(folder_path, filename_prefix, total_pics, layout='2x', image_size='1920x1152', margin='20', debug=True):

    source_images = folder_path + '/' + filename_prefix + '_' + '[1-' + str(total_pics) + ']' + 'of' + str(total_pics) + '.jpg'
    output_file = folder_path + '/' + filename_prefix + '_layout_' + layout + '.jpg'

    command=['montage']
    command.extend(['-tile',layout])
    command.extend(['-geometry',image_size + '+' + margin + '+' + margin])

    command.append(source_images) #source images
    command.append(output_file) #destination

    #print("Attempting command: " + command)
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

def dropbox_upload(dbx, upload_path, file_path):

    with open(file_path, 'rb') as f:
        # We use WriteMode=overwrite to make sure that the settings in the file are changed on upload
        print("Uploading " + file_path + " to Dropbox as " + upload_path + "...")
        try:
            dbx.files_upload(f.read(), upload_path, mode=WriteMode('overwrite'))
        except ApiError as err:
            # This checks for the specific error where a user doesn't have enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().reason.is_insufficient_space()):
                print("ERROR: Cannot back up; insufficient space.")
                return False
            elif err.user_message_text:
                print(err.user_message_text)
                return False
            else:
                print(err)
                return False

    return True

def main():
    """
    Main program loop
    """
    #Clear the console window
    os.system('cls' if os.name == 'nt' else 'clear')

    #Health checks
    health_test_required_folders()
    if DROPBOX_ENABLED:
        dbx = health_test_dropbox()

    #Begin watching
    print('Watching for new files in: ' + INPUT_DIRECTORY + '...')
    while True:
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
                        continue
                    else:
                        print(' - All ' + str(total_pics) + ' photos found.')

                    #Start processing our group of files
                    for this_file in files_to_process:

                        #Perform image optimisations with Imagemagick
                        print(' - Optimising image size: ' + this_file)
                        src_file  = INPUT_DIRECTORY + '/' + this_file
                        dest_file = PROCESSING_DIRECTORY + '/' + this_file

                        perform_image_optimisation(src_file, dest_file)

                        #Later, we will move this folder to our 'DONE' directory:
                        completed_files.append(this_file)
                        
                        #Later, we will upload this file to dropbox:
                        if DROPBOX_ENABLED:
                            files_to_upload_to_dropbox.append(this_file)


                    if(files_to_process and OUTPUT_ANIMATED_THUMBNAILS):

                        #Create animated gif
                        print(' - Creating animated thumbnail')
                        dest_file = OUTPUT_DIRECTORY + '/thumbnails/' + filename_prefix + '.gif'
                        this_animated_gif = create_animated_gif(PROCESSING_DIRECTORY, filename_prefix, dest_file, total_pics)
                        print(' - Animated thumbnail was created')
                        completed_files.append(this_animated_gif)
                        if DROPBOX_ENABLED:
                            files_to_upload_to_dropbox.append(this_animated_gif)
 

                    if(files_to_process and OUTPUT_ANIMATED_THUMBNAILS):

                        #Create photo strip ( 1x4 layout)
                        print(' - Creating photo strip (1 column layout)')
                        this_photo_strip = create_photo_strip(PROCESSING_DIRECTORY, filename_prefix, total_pics, '1x')
                        completed_files.append(this_photo_strip)
                        if DROPBOX_ENABLED:
                            files_to_upload_to_dropbox.append(this_photo_strip)

                        #Create photo strip ( 2x2 layout)
                        print(' - Creating photo strip (2 column layout)')
                        this_photo_strip = create_photo_strip(PROCESSING_DIRECTORY, filename_prefix, total_pics, '2x')
                        completed_files.append(this_photo_strip)
                        if DROPBOX_ENABLED:
                            files_to_upload_to_dropbox.append(this_photo_strip)

                    for this_file in files_to_upload_to_dropbox:
                        print(' - Uploading to dropbox: ' + this_file)
                        upload_path = '/photo-booth/' + os.path.basename(this_file)
                        dropbox_upload(dbx, upload_path, this_file)

                    for this_file in completed_files:
                        print(' - Clean up: ' + this_file)

                        if os.path.exists(this_file):
                            #If a file with this name already exists in 'Done' folder then we will need to remove it.
                            target_filename = OUTPUT_DIRECTORY + os.path.basename(this_file)
                            if os.path.exists(target_filename):
                                print(' - Overwriting: ' + target_filename)
                                os.remove(target_filename) #If we don't do this then "move" will fail.

                            #Move file to "Done" folder
                            move(this_file, OUTPUT_DIRECTORY)

        time.sleep(10)

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print('Goodbye')

