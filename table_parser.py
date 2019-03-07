import csv
import io
from sag_types import Table, Column


def ParseCSVTable(table_str):
  """Parses a csv table to a SAG Table.
  
  This is temporary while the RUTHEN table parser is written."""
  r = csv.reader(io.StringIO(table_str))
  return Table([Column([float(e.replace(',', '')) for e in col[1:]], name = col[0], description='from csv')
                for col in zip(*r)])
  
  
