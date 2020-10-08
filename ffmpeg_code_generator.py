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
INPUT = 'video_filenames.csv'        # place this file in the same directory as this script

def main():
    with open(INPUT) as csvfile: 
        
        reader = csv.reader(csvfile)
        items = list(csv.reader(csvfile)) # adding csv rows to a list
        csvfile.close()
        
        commands = []      # all commands based on each spreadsheet row 

        for item in items: # adding the command to caption the individual videos
            line_command = ('ffmpeg -i ' + item[0] + ' -i ' + item[1] + ' -c copy -c:s mov_text ' + item[2])
            commands.append(line_command)
            
        cmd = ' && '.join(commands)
        print(cmd)
        
        os.system(cmd)               #output commands to command line 

main()

