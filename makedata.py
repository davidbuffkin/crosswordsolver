#David Buffkin

#Takes a directory or file containing crossword(s) in JSON and outputs a txt file containing clue answer pairs.
#Usage: python makedata.py <input> <outputfile>

import json
import sys
from os.path import splitext
from os import walk


if len(sys.argv) < 2:
    print("No file or directory supplied, exiting.")
    sys.exit()
if len(sys.argv) < 3:
    print("No output file specified, exiting.")
    sys.exit()

#Get all files in directory
f = []
for (dirpath, dirnames, filenames) in walk(sys.argv[1]):
    f += [dirpath + "/" + name for name in  filenames]

if len(f) == 0:
    f = [sys.argv[1]]



def getClue(clue_raw):
    return clue_raw[clue_raw.find(" ") + 1:]

def writeCross(cross, writer):
    acrossClues = cross['clues']['across']
    acrossAnswers = cross['answers']['across']
    if len(acrossAnswers) != len(acrossClues):
        print("Puzzle is corrupted, exiting")
        sys.exit()
    for i in range(len(acrossAnswers)):
        if i != 0:
            writer.write("\n")
        clue = getClue(acrossClues[i]).replace("|", " ")
        answer = acrossAnswers[i].replace("|", " ")
        writer.write(f"{clue}|{answer}")
    downClues = cross['clues']['down']
    downAnswers = cross['answers']['down']
    if len(downAnswers) != len(downClues):
        print("Puzzle is corrupted, exiting.")
        sys.exit()
    for i in range(len(downAnswers)):
        clue = getClue(downClues[i]).replace("|", " ")
        answer = downAnswers[i].replace("|", " ")
        writer.write(f"\n{clue}|{answer}")

first = True
with open(sys.argv[2], "w") as writer:
    for filename in f:
        if not first:
            writer.write("\n")
        first = False
        if splitext(filename)[1] != ".json":
            continue
        try:
            file_raw = None
            with open(filename) as reader:
                file_raw = reader.read()

            cross = json.loads(file_raw)
            
            writeCross(cross, writer)
        except:
            continue
