import csv
import io
from sag_types import Table, Column


def ParseCSVTable(table_str):
  """Parses a csv table to a SAG Table.
  
  This is temporary while the RUTHEN table parser is written."""
  r = csv.reader(io.StringIO(table_str))
  return Table([Column([float(e.replace(',', '')) for e in col[1:]], name = col[0], description='from csv')
                for col in zip(*r)])
  
def FindSeparations(line):
  """Finds the separations in a fixed width line.
  
  Columns are assumed to be right-aligned and space padded, with at least one
  space between each column and no internal spaces.
  
  Returns:
    A sequence of (begin, end) tuples, where begin is the first character index
    in a column and end is one past the last index so that line[begin:end] is
    the cell contents.
  """
  separations = []
  cell_begin=0
  space_previous=True
  for i in range(len(line)):
    if line[i].isspace() and not space_previous:
      separations.append((cell_begin, i))
      cell_begin = i
    space_previous = line[i].isspace()
  else:
    if not space_previous:
      separations.append((cell_begin, len(line)))
  return separations
  
def Separate(line, separations):
  """Separates a line into its fixed-width cells and trims whitespace."""
  return [line[b:e].lstrip() for (b, e) in separations]
  
def ParseRuthenTable(table_str):
  """Parses a RUTHEN table to a SAG table."""
  if table_str[:6] != "RUTHEN":
    raise ValueError("Table doesn't have a RUTHEN header")

  description_lines = []
  table_rows = []
  table_begun=False
  separations = None
  table_width = None
  with io.StringIO(table_str) as lines:
    for line_num, line in enumerate(lines):
      if line_num < 4:
        continue  # Skip the header
      if line.startswith('BEGIN TABLE'):
        table_begun=True
        continue
        
      if table_begun:
        if not separations:  # are we reading the table headers
          separations = FindSeparations(line)
          table_width = len(line)
        if len(line) != table_width:
          break  # Done parsing the table
          # TODO parse the column descriptions
        table_rows.append(Separate(line, separations))
      else:
        description_lines.append(line)
        
  return Table([Column([float(e.replace(',', '')) for e in col[1:]],
                        name = col[0], description='from RUTHEN')
                for col in zip(*table_rows)],
                description=''.join(description_lines))
