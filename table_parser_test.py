import unittest
import textwrap
import table_parser
from sag_types import Table, Column

class TableParserTest(unittest.TestCase):

  def testFindSeparations(self):
    line = " 123  456  789"
    self.assertEqual(table_parser.FindSeparations(line),
                     [(0,4), (4, 9), (9, 14)])

  def testFindSeparationsNoLeadingSpace(self):
    line = "0123  456  789"
    self.assertEqual(table_parser.FindSeparations(line),
                     [(0,4), (4, 9), (9, 14)])

  def testFindSeparationsNewline(self):
    line = " 123  456  789 \r\n"
    self.assertEqual(table_parser.FindSeparations(line),
                     [(0,4), (4, 9), (9, 14)])
                     
  def testSeparate(self):
    line = " 123  456  789 \r\n"
    separations = [(0,4), (4, 9), (9, 14)]
    self.assertEqual(table_parser.Separate(line, separations),
                     ['123', '456', '789'])
                     
  def testSeparateEmpty(self):
    line = " 123       789 \r\n"
    separations = [(0,4), (4, 9), (9, 14)]
    self.assertEqual(table_parser.Separate(line, separations),
                     ['123', '', '789'])
                     
  def testParseRuthenTable(self):
    table = textwrap.dedent("""\
    RUTHEN header
    Ruthen Model: more header
    Model Run: more header
                               
    Describe
    Description
    BEGIN TABLE
     Age   Foo  Bar
      23  0.25 0.50
      24  0.50 0.75
     Age - Age""")
    expected = Table([Column([23.0, 24.0], name='Age', description='from ruthen'),
                      Column([0.25, 0.50], name='Foo', description='from ruthen'),
                      Column([0.50, 0.75], name='Bar', description='from ruthen'),
                     ],
                     description="Describe\nDescription\n")
    actual = table_parser.ParseRuthenTable(table)
    self.assertEqual(str(actual), str(expected))  # compare strings because == is broken
                      

if __name__ == '__main__':
  unittest.main()
