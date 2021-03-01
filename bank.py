"""
bank.py

Builds a problem bank based on the topics directory. The bank is returned as a .csv file.
"""

USAGE = """
usage: 
python {0} 
python {0} TOPICFOLDER
python {0} TOPICFOLDER OUTPUT

Creates a problem bank .csv from the topic folder.
"""

import os
import csv
import re
from pathlib import Path

def explore(folder="topics", out="bank.csv"):
    """Returns the contents of a dependency file.

    PARAMETERS:
    target       -- str; Makefile target that requires dependencies.
    dependencies -- list of str; list of dependencies.
    assets       -- dict; keys are target names for assets, values
                    are actual asset locations on the filesystem.
    phony        -- str or None; if str, this denotes a convenient
                    phony target that depends on assets. If None,
                    the phony target is omitted from the dependency
                    file.

    RETURNS:
    str; the contents to write to a dependency file.
    """
    # out file
    with open(out, 'w') as f:
        # create writer
        wtr = csv.writer(f, lineterminator='\n')
        # write header
        wtr.writerow(["Topic", "Difficulty", "Problem", "Env?", "WWPD?", "Link"])
        # iterate through directories
        for root, dirs, files in os.walk(folder):
            # iterate through files
            for filename in files:
                # problem name
                problem = filename.split('.')[0]
                # topic
                subfolders = root.split("\\")
                topic = re.sub('[_-]', ' ', subfolders[1]).title()
                if topic.lower() in ['sql', 'oop', 'hof']:
                    topic = topic.upper()
                # difficulty
                difficulty = ''
                if len(subfolders) > 2:
                    difficulty = subfolders[2].capitalize()
                # wwsd/env
                wwpd = ""
                env = ""
                if len(subfolders) > 3:
                    if subfolders[3] == 'wwsd':
                        wwpd = "x"
                    if subfolders[3] == 'env':
                        env = "x"
                # build url
                link = "/".join(["https://github.com/csmberkeley/csm-61a/master",root.replace("\\", "/"), filename])
                # write row
                wtr.writerow([topic, difficulty, problem, env, wwpd, link])

def main(args):
    if len(args) > 3:
        print(USAGE.format(args[0]))
        exit(1)
    explore(*args[1:])

if __name__ == '__main__':
    import sys
    main(sys.argv)
