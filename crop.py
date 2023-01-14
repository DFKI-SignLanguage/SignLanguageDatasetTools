"""
@author: Aljoscha Lipski
@mail: aljoscha.lipski@googlemail.com
@license: MIT

Copyright (c) 2023 Aljoscha Lipski
"""

import sys
import os
import subprocess

# global variables
OUTPUT_FOLDER_NAME = 'croppedVideos'


def cropSingleVideo(nameVideo: str, pathVideo: str, cropLeft: int, cropRight: int,
                    cropTop: int, cropBottom: int):
    '''
    crops a video to the given size.

    arguments:
    - name of the video
    - path to the video
    - percentage of cropping left edge
    - percentage of cropping right edge
    - percentage of cropping from the top edge
    - percentage of cropping from the bottom edge
    '''
    # get the video size
    size = subprocess.run(['ffprobe', '-y', 'error', '-show_entries',
                           'stream=width,height', '-of', 'default=noprint_wrappers=1',
                           pathVideo], capture_output=True, text=True)
    width = int((size.stdout.split('=')[1]).split('\n')[0])
    height = int(size.stdout.split('=')[2])

    # calculate the percentages in position and pixels.
    # see: http://ffmpeg.org/ffmpeg-all.html#crop
    left = width * (cropLeft / 100)
    top = width * (cropTop / 100)
    right = width - (width * (cropRight / 100)) - left
    bottom = height - (height * (cropBottom / 100)) - top

    subprocess.run(['ffmpeg', '-i', pathVideo,
                    '-filter:v', 'crop=' + str(right) + ':' + str(bottom) + ':' +
                    str(left) + ':' + str(top),
                    OUTPUT_FOLDER_NAME + '/' + nameVideo])


def cropAllVideos(pathFolder: str, cropLeft: int, cropRight: int, cropTop: int,
                  cropBottom: int):
    '''
    This function iterates through the given folder and crops all .mp4 files.
    Those new files will be written into a new folder.
    Every other content of the original folder will be copied to the new folder.

    arguments:
    - path to the folder with the videos
    - percentage of cropping left edge
    - percentage of cropping right edge
    - percentage of cropping from the top edge
    - percentage of cropping from the bottom edge
    '''
    if os.name == "nt":
        linux = False
        subprocess.run(['lmkdir', OUTPUT_FOLDER_NAME])
    else:
        linux = True
        subprocess.run(['mkdir', OUTPUT_FOLDER_NAME])

    counter = 0

    # iterate through the folder and crop every .mp4 file
    for filename in os.listdir(pathFolder):
        pathFile = os.path.join(pathFolder, filename)

        # checking if it is a file
        if os.path.isfile(pathFile):
            # if it is .mp4 crop the video
            if (filename.endswith('.mp4')):
                cropSingleVideo(filename, pathFile, cropLeft, cropRight,
                                cropTop, cropBottom)
            # otherwise just copy it to the new folder
            else:
                if linux:
                    subprocess.run(
                        ['cp', pathFile, OUTPUT_FOLDER_NAME + '/' + filename])
                else:
                    subprocess.run(
                        ['copy', pathFile, OUTPUT_FOLDER_NAME + '/' + filename])
        print("DONE: " + str(counter))


if __name__ == "__main__":
    helpText = "Please use the script like this:\n\npython3 crop.py path/to/video/folder cropLeft cropRight cropTop cropBottom\n\n\
    Important:\n\
        - Only .mp4 videos will be taken, all other files will be skipped\n\
        - This script is only tested for Linux but should work on Windows as well if ffmpeg is installed\n\
        - cropXY must be an integer between 0 and 100\n\
        - the sum of cropLeft and cropRight must be < 100\n\
        - the sum of cropTop and cropBottom must be < 100\n\n\
    Usage:\n\
        cropXY is given in percentage from the position X.\n\
        So if cropLeft = 10, cropRight = 20, cropTop = 0, cropBottom = 50,\n\
        that means the cropped window is 10% from the left edge, \
        20% from the right edge,\n\
        0% from the top edge (so nothing) and 50% from the bottom edge away,\n\
        The reference is the size of the original video size."
    if len(sys.argv) == 1:
        print(helpText)
        sys.exit(0)

    # check for help
    if (sys.argv[1] == "-h" or sys.argv[1] == "--h" or
            sys.argv[1] == "-help" or sys.argv[1] == "--help"):
        print(helpText)
        sys.exit(0)

    # check for correct amount of arguments
    if len(sys.argv) != 6:
        print("\nThe correct amount of arguments was not given!")
        print(helpText)
        sys.exit(0)

    # test the percentage arguments on being a number
    if (not sys.argv[2].isnumeric() or not sys.argv[3].isnumeric() or
            not sys.argv[4].isnumeric() or not sys.argv[5].isnumeric()):
        print("\nSome percentage arguments are no positive integers!\n\n")
        print(helpText)
        sys.exit(0)

    # test the percentage arguments on the range
    if (int(sys.argv[2]) + int(sys.argv[3]) >= 100 or
            int(sys.argv[4]) + int(sys.argv[5]) >= 100 or
            int(sys.argv[2]) >= 100 or int(sys.argv[3]) >= 100 or
            int(sys.argv[4]) >= 100 or int(sys.argv[5]) >= 100 or
            int(sys.argv[2]) < 0 or int(sys.argv[3]) < 0 or
            int(sys.argv[4]) < 0 or int(sys.argv[5]) < 0
        ):
        print("\nThe sum of some percentages is >= 100 or some percentages are larger than 100!\n\n")
        print(helpText)
        sys.exit(0)

    # check if the path exists
    if not os.path.exists(sys.argv[1]):
        print("\nThe provided path does not exist or is wrong!\n\n")
        print(helpText)
        sys.exit(0)

    cropAllVideos(sys.argv[1], int(sys.argv[2]),
                  int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
