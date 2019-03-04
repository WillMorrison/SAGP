from sag_parser import Evaluate

# A small test program
sagl = '''// Some comments and stuff
IMPORT COLUMNS BY Age
 asseTs DeBt;

StUFf = assets - DEBT + 2.5;
stuff = -Stuff * assets;
DESCRIBE Stuff "Some stuff";

DEFINE TABLE beans stuff assets debt;
DESCRIBE beans "Some beans";
LIMIT beans BETWEEN 4 9;
OUTPUT beans;
'''

if __name__ == '__main__':
  Evaluate(sagl, input_table=None, output_file=None)
