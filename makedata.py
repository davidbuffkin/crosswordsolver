#David Buffkin

#Takes a crossword in JSON and outputs a txt file containing clue answer pairs.
#Usage: python makedata.py <inputfile> [outputfile]

import json
import sys
import os.path

filename, extension = os.path.splitext(sys.argv[1])

if extension != ".json":
    print("Not a JSON file, exiting.")
    sys.exit

file_raw = None
with open(filename + extension) as reader:
    file_raw = reader.read()

cross = json.loads(file_raw)

writeName = filename + "_pairs.txt" if len(sys.argv) < 3 else sys.argv[2]

def getClue(clue_raw):
    return clue_raw[clue_raw.find(" ") + 1:]

with open(writeName, "w") as writer:
    acrossClues = cross['clues']['across']
    acrossAnswers = cross['answers']['across']
    if len(acrossAnswers) != len(acrossClues):
        print("Puzzle is corrupted, exiting.")
        sys.exit()
    for i in range(len(acrossAnswers)):
        if i != 0:
            writer.write("\n")
        writer.writelines(f"{getClue(acrossClues[i])}\n{acrossAnswers[i]}")
    downClues = cross['clues']['down']
    downAnswers = cross['answers']['down']
    if len(downAnswers) != len(downClues):
        print("Puzzle is corrupted, exiting.")
        sys.exit()
    for i in range(len(downAnswers)):
        writer.write(f"\n{getClue(downClues[i])}\n{downAnswers[i]}")
