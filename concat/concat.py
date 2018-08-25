__author__ = 'Jan Bogaerts'
__copyright__ = "Copyright 2018, Elastetic"
__credits__ = []
__maintainer__ = "Jan Bogaerts"
__email__ = "jb@elastetic.com"
__status__ = "Development"  # "Prototype", or "Production"


import os

if __name__ == "__main__":
    # execute only if run as a script
    print("start")
    output_path = './output/'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    start_point = '../sonar_to_raw/output/'
    for entry in os.scandir(start_point):
        if entry.is_dir():
            print("processing: " + entry.path)
            with open(output_path + entry.name + '.txt', 'w') as outfile:
                for sub in os.scandir(entry.path):
                    if sub.is_dir():
                        print("processing sub: " + sub.path)
                        for sub2 in os.scandir(sub.path):
                            if sub2.is_file():
                                with open(sub2.path) as infile:
                                    outfile.write(infile.read())
                                    outfile.write('\n')
                    elif sub.is_file():
                        with open(sub.path) as infile:
                            outfile.write(infile.read())
                            outfile.write('\n')