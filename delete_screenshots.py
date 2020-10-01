'''Deletes screenshots from directory based on user input.'''

import os, glob

print('Please enter the directory from which you would like to delete screenshots.')
print('Starting from the home directory - ~ - is assumed.')
    
my_dir = os.path.expanduser('~')
directory = input()

path = my_dir + '/' + directory + "/Screen Shot*"
for filename in glob.glob(path):
    os.remove(filename) 
