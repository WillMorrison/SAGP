import csv
import io

class Column(object):

  def __init__(self, value, name=None, description=None):
    self.name = name
    self.value = value
    self.description = description
    
  def __len__(self):
    return len(self.value)
    
  def __getitem__(self, key):
    return self.value[key]
    
  def __iter__(self):
    return iter(self.value)
    
  def __add__(self, other):
    return Column([a+b for a, b in zip(self.value, other.value)])
    
  def __sub__(self, other):
    return Column([a-b for a, b in zip(self.value, other.value)])
    
  def __mul__(self, other):
    return Column([a*b for a, b in zip(self.value, other.value)])
    
  def __truediv__(self, other):
    return Column([a/b for a, b in zip(self.value, other.value)])
    
  def __neg__(self):
    return Column([-a for a in self.value], self.description)
    
  def __repr__(self):
    return 'Column(%r, name=%r, description=%r)' % (self.value, self.name, self.description)
    
  def __eq__(self, other):
    return (self.value == other.value
            and self.name == other.name
            and self.description == other.description)


class Table(object):

  def __init__(self, columns,
               lower_bound=None, upper_bound=None, index_column=None,
               description=None):
    self.columns = tuple(columns)
    self.lower_bound = lower_bound
    self.upper_bound = upper_bound
    if index_column is not None:
      self.index_column = index_column
    elif columns:
      self.index_column = self.columns[0]
    else:
      raise ValueError("Table has no columns")
    self.description = description
    
  def __str__(self):
    f = io.StringIO()
    if self.description:
      print(self.description, file=f)

    w = csv.writer(f)
    w.writerow([c.name for c in self.columns])

    for index, row in zip(self.index_column, zip(*self.columns)):
      if ((self.lower_bound is None or index >= self.lower_bound)
          and (self.upper_bound is None or index <= self.upper_bound)):
        w.writerow(row)
    return f.getvalue()
    
  def __eq__(self, other):
    return ((self.columns, self.index_column, self.description, self.lower_bound, self.upper_bound) ==
            (other.columns, other.index_column, other.description, other.lower_bound, other.upper_bound))
            
