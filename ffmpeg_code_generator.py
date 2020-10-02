''' This utility reads from a file called video_filenames.csv that consists of input video filenames,
    input caption filenames, and output video filenames in order to combine video and caption files
    for web use.

    A sample command for an individual captioning command is:
    ffmpeg -i infile.mp4 -i infile.srt -c copy -c:s mov_text outfile.mp4

    Output from this utility will create those individual commands and then concatenate them, e.g.

    ffmpeg -i video1.mp4 -i video1.srt -c copy -c:s mov_text video1_c.mp4
    && ffmpeg -i video2.mp4 -i video2.srt -c copy -c:s mov_text video2_c.mp4
    && ffmpeg -i video3.mp4 -i video3.srt -c copy -c:s mov_text video3_c.mp4

    ffmpeg can be installed via homebrew.'''

import csv, os

# Defining global constant for input and output file name. 
INPUT = 'video_filenames.csv'

def main():
    with open(INPUT, newline='') as csvfile:
        reader = csv.reader(csvfile)
        items = list(reader)
        csvfile.close()
        concatenated_command = ''
        num_loops = len(items)
        for i,item in enumerate(items):
            line_command = ('ffmpeg -i ' + item[0] + ' -i ' + item[1] + ' -c copy -c:s mov_text ' + item[2])
            concatenated_command += line_command
            if i != (num_loops - 1):
                concatenated_command += ' && '
            
        cmd = concatenated_command
        os.system(cmd)

main()

