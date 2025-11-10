#!/usr/bin/env bash

# Before running this script, I:
# sudo apt-get update
# sudo apt install imagemagick
# sudo apt install graphicsmagick

# - Created a set of .jpgs (i.e. 800x480):
#     Photo group 1:
#         2017-04-15_14-09-29_1.jpg
#         2017-04-15_14-09-29_2.jpg
#         2017-04-15_14-09-29_3.jpg
#     Photo group 2:
#         2017-04-15_14-10-15_1.jpg
#         2017-04-15_14-10-15_2.jpg
#         2017-04-15_14-10-15_3.jpg


for jpg_file in *.jpg;
do
    if [ $jpg_file != "*.jpg" ]; then
        filename_no_ext="${jpg_file%.*}" # Example: 2017-04-15_15-07-08_1of4
        filename_no_inc="${filename_no_ext::${#filename_no_ext}-5}" # Example: 2017-04-15_15-07-08

        if [ "$filename_no_inc" != "$prev_filename_no_inc" ]; then

            #Output filename prefix
            echo "${filename_no_inc}"

            #Create Gif
            gm convert -size 205x154 -delay 100 ${filename_no_inc}*.jpg ${filename_no_inc}-before-compression.gif

            #Compress gif
            gifsicle --colors 256 --lossy=80 -O3 -o ${filename_no_inc}.gif ${filename_no_inc}-before-compression.gif

            #Delete uncompressed version
            rm ${filename_no_inc}-before-compression.gif

            #Set prev filename, to prevent re-execution.
            prev_filename_no_inc="${filename_no_inc}"
        fi
    else
        echo "No JPGs found"
    fi
done