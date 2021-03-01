"""
bank.py

Builds a problem bank based on the topics directory. The bank is returned as a .csv file.
"""

USAGE = """
usage: 
python {0} 
python {0} TOPICFOLDER
python {0} TOPICFOLDER SOURCEFOLDER
python {0} TOPICFOLDER SOURCEFOLDER OUTPUT

Creates a problem bank .csv from the topic folder.
"""

import os
import csv
import re
from pathlib import Path

def explore(topicfolder="topics", srcfolder="src", out="bank.csv"):
    """Explores the topic folder and writes problem descriptions to bank.

    PARAMETERS:
    folder       -- str; Name of the topic folder
    out          -- str; Name of the output file

    RETURNS:
    str; none
    """
    print("Reading", srcfolder)
    published = {}
    for root, dirs, files in os.walk(srcfolder):
        # iterate through files
        for filename in files:
            if filename.split('.')[1] == 'tex' and filename[:4] == 'week':
                # store text
                published[root.split("\\")[1]+"-"+filename.split('.')[0]] = open(root+"/"+filename, 'r', encoding="UTF-8").read()
    print("Reading", topicfolder)
    # out file
    with open(out, 'w') as f:
        # create writer
        wtr = csv.writer(f, lineterminator='\n')
        # write header
        wtr.writerow(["Topic", "Difficulty", "Problem", "Type", "Link", "Guide?", "Published"])
        # iterate through directories
        for root, dirs, files in os.walk(topicfolder):
            # iterate through files
            for filename in files:
                if filename.split('.')[1] == 'tex':
                    # problem name
                    problem = filename.split('.')[0]
                    # topic
                    root = root.replace("\\", "/")
                    subfolders = root.split("/")
                    topic = re.sub('[_-]', ' ', subfolders[1]).title()
                    if topic.lower() in ['sql', 'oop', 'hof', ]:
                        topic = topic.upper()
                    # difficulty
                    difficulty = ''
                    if len(subfolders) > 2:
                        difficulty = subfolders[2].capitalize()
                    # type
                    if len(subfolders) > 3 and subfolders[3] in ['env', 'env-diagram', 'wwpd', 'wwsd']:
                        ptype = subfolders[3]
                    else:
                        ptype = "coding"

                    # has guide
                    with open(root+"/"+filename, 'r', encoding="UTF-8") as pfile:
                        text = pfile.read()
                        has_guide = "guide" in text

                    # build url
                    link = "/".join(["https://raw.githubusercontent.com/csmberkeley/csm-61a/org", root, filename])

                    # find past published
                    past_published = ",".join(reversed([p for p in published if problem in published[p]]))

                    # write row
                    wtr.writerow([topic, difficulty, problem, ptype, link, has_guide, past_published])
        print("Saved at", out)

def main(args):
    if len(args) > 4:
        print(USAGE.format(args[0]))
        exit(1)
    explore(*args[1:])

if __name__ == '__main__':
    import sys
    main(sys.argv)
