import argparse

from sag_parser import Evaluate

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Evaluate a SAGL script on a RUTHEN table')
  parser.add_argument('program', type=argparse.FileType('r'),
                    help='The SAGL program to evaluate')
  parser.add_argument('input_table', type=argparse.FileType('r'),
                    help='The RUTHEN table to use as input')
  parser.add_argument('--output', type=argparse.FileType('w'),
                    default=None,
                    help='The file path to output to')
                    
  args = parser.parse_args()
  sagl = args.program.read()

  Evaluate(sagl, input_table=args.input_table, output_file=args.output)
