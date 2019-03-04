import sys

from sly import Lexer, Parser
from sag_types import Table, Column

class SAGLLexer(Lexer):

  tokens = {
    EOL,
    NAME,
    STRING, NUMBER,
    PLUS, MINUS, TIMES, DIVIDE, EQUALS,
    LPAREN, RPAREN,
    IMPORT, COLUMNS, BY,
    DESCRIBE,
    DEFINE, TABLE,
    LIMIT, BETWEEN,
    OUTPUT,
  }
  

  # Ignored characters
  ignore = " \t\r"
  ignore_comment = r'//[^\n]*'

  @_(r'\n+')
  def ignore_newline(self, t):
    self.lineno += len(t.value)

  # Mathematical operators
  PLUS    = r'\+'
  MINUS   = r'-'
  TIMES   = r'\*'
  DIVIDE  = r'/'
  EQUALS  = r'='
  LPAREN  = r'\('
  RPAREN  = r'\)'
  EOL     = r';'
  
  # Variable naming
  NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
  
  # Keyword remapping
  NAME['IMPORT'] = IMPORT
  NAME['COLUMNS'] = COLUMNS
  NAME['BY'] = BY
  NAME['DESCRIBE'] = DESCRIBE
  NAME['DEFINE'] = DEFINE 
  NAME['TABLE'] = TABLE
  NAME['LIMIT'] = LIMIT 
  NAME['BETWEEN'] = BETWEEN
  NAME['OUTPUT'] = OUTPUT

  def NAME(self, t):
    """Ensures variable names are case insensitive"""
    t.value = t.value.lower()
    return t
  

  @_(r'"[^"]*"')
  def STRING(self, t):
   t.value = t.value.strip('"')
   return t
    
  @_(r'\d+(\.\d+)?')
  def NUMBER(self, t):
    t.value = float(t.value)
    return t

  def error(self, t):
      print("Illegal character '%s' on line %d" % (t.value[0], self.lineno))
      self.index += 1


# Program state manager
class SAGLParser(Parser):

  tokens = SAGLLexer.tokens
  
  def __init__(self, input_table, output_file):
    super().__init__()
    self.names = {}  # for storing variables
    self.column_len = None  # TODO initialize this from input_table
    self.output_file = output_file
    
  def import_table(self, column_names):
    # This should be replaced by importing the data from input_table
    self.column_len = 2
    for name in column_names:
      self.names[name] = Column([1., 2.], name=name, description='fake')

  precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
    )

  # Top level rule, a program is a sequence of statements
  @_('program statement',
     'statement')
  def program(self, p):
    pass

  # Statements are all terminated by semicolons
  @_('import_ EOL',
     'assignment EOL',
     'describe EOL',
     'define EOL',
     'limit EOL',
     'output EOL')
  def statement(self, p):
    pass
  
  # Resychronize on semicolons after finding syntax errors
  @_('error EOL')
  def statement(self, p):
    pass

  @_('namelist NAME')
  def namelist(self, p):
    return p.namelist + [p.NAME]
      
  @_('NAME')
  def namelist(self, p):
    return [p.NAME]

  @_('IMPORT COLUMNS BY namelist')
  def import_(self, p):
    self.import_table(p.namelist)
  
  @_('NAME EQUALS expression')
  def assignment(self, p):
    p.expression.name = p.NAME
    self.names[p.NAME] = p.expression

  @_('expression PLUS expression',
     'expression MINUS expression',
     'expression TIMES expression',
     'expression DIVIDE expression')
  def expression(self, p):
    if   p[1] == '+': return p.expression0 + p.expression1
    elif p[1] == '-': return p.expression0 - p.expression1
    elif p[1] == '*': return p.expression0 * p.expression1
    elif p[1] == '/': return p.expression0 / p.expression1

  @_('MINUS expression %prec UMINUS')
  def expression(self, p):
    return -p.expression

  @_('LPAREN expression RPAREN')
  def expression(self, p):
    return p.expression

  @_('NUMBER')
  def expression(self, p):
    return Column([p.NUMBER] * self.column_len)

  @_('NAME')
  def expression(self, p):
    try:
      return self.names[p.NAME]
    except LookupError:
      print("Undefined name '%s'" % p.NAME)

  @_('DESCRIBE NAME STRING')
  def describe(self, p):
    try:
      self.names[p.NAME].description = p.STRING
    except LookupError:
      print("Undefined name '%s'" % p.NAME)

  @_('DEFINE TABLE namelist')
  def define(self, p):
    table_name = p.namelist[0]
    try:
      # TODO Check that all names refer to columns
      columns = [self.names[column] for column in p.namelist[1:]]
      self.names[table_name] = Table(columns)
    except LookupError:
      print("Undefined column while defining table '%s'" % table_name)

  @_('LIMIT NAME BETWEEN NUMBER NUMBER')
  def limit(self, p):
    try:
      table = self.names[p.NAME]
    except LookupError:
      print("Undefined name '%s'" % p.NAME)
      return
      
    if not isinstance(table, Table):
      print("%s is not a table, cannot set limits" % p.NAME)
      return
    table.lower_bound = p.NUMBER0
    table.upper_bound = p.NUMBER1
      
  @_('OUTPUT NAME')
  def output(self, p):
    try:
      table = self.names[p.NAME]
    except LookupError:
      print("Undefined name '%s'" % p.NAME)
      return
      
    if not isinstance(table, Table):
      print("%s is not a table, cannot output" % p.NAME)
      return
    
    print(str(table), file=self.output_file)
    # TODO Output legend after the table


def Evaluate(program, input_table, output_file=None):
  """Evaluates a SAGL program on an input table and outputs to a file.
  
  Args:
    program: A string containing the SAGL program to evaluate
    input_table: The parsed Ruthen table to use as a data source
    output_file: A file-like object to write the output to
  """
  output_file = sys.stdout if output_file is None else output_file
  lexer = SAGLLexer()
  parser = SAGLParser(input_table, output_file)
  parser.parse(lexer.tokenize(program))
