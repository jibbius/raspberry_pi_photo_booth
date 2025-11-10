#!/usr/bin/env bash

# Before running this script, I:
# - Created a set of .jpgs (i.e. 800x480):
#     Photo group 1:
#         2017-04-15_14-09-29_1.jpg
#         2017-04-15_14-09-29_2.jpg
#         2017-04-15_14-09-29_3.jpg
#     Photo group 2:
#         2017-04-15_14-10-15_1.jpg
#         2017-04-15_14-10-15_2.jpg
#         2017-04-15_14-10-15_3.jpg
# - Created thumbnail versions of each image (i.e. 200x120)
# - Ran this command, looping over each thumbnail:
#     GM convert -delay 100 2017-04-15_14-09-29*.jpg 2017-04-15_14-09-29.gif
# - This created some small animated gifs, in the format:
#     2017-04-15_14-09-29.gif
# - I put all of the full size images, and animated gifs, (not the thumbnail jpgs),
#   in the same directory as this script
# - Ensure that the script is made executable:
#   `chmod +x script-1.sh`


this_group=""
prev_group=""
for jpg_file in *.jpg;
do
    if [ $jpg_file != "*.jpg" ]; then
        filename_no_ext="${jpg_file%.*}" # Example: 2017-04-15_15-07-08_1of4
        filename_no_inc="${filename_no_ext::${#filename_no_ext}-5}" # Example: 2017-04-15_15-07-08
        this_group=$filename_no_inc

        if [ "$this_group" != "$prev_group" ]; then
           
            #Close previous HTML
            if [[ ! -z $prev_group ]]; then
                cat _footer.html >> "../${prev_group}.html"
            fi

            echo "Creating page: ${filename_no_inc}.html"
            cat _header.html > "../${filename_no_inc}.html"
        fi

        #Append image
        echo "      <img src='photo_booth/${jpg_file}' width='820px' height='616px'></img>" >> "../${filename_no_inc}.html"

        prev_group=$filename_no_inc
    else
        echo "No JPGs found"
    fi
done

if [[ ! -z $prev_group ]]; then
    cat _footer.html >> "../${prev_group}.html"
fi