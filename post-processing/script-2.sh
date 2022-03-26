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

cat _header.html > index.html

for html_file in 20*.html;
do
    if [ $html_file != "20*.html" ]; then
        # Example: 2022-03-12_21-51-45.html
        filename_no_ext="${html_file%.*}"
        echo ${filename_no_ext}
        echo "<a href='${filename_no_ext}.html'><img alt='${filename_no_ext}' width='205px' height='154px'  src='photo_booth/${filename_no_ext}.gif'></img></a>" >> index.html

    fi
done

cat _footer.html >> index.html