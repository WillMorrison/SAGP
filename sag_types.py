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
    
  def __div__(self, other):
    return Column([a/b for a, b in zip(self.value, other.value)])
    
  def __neg__(self):
    return Column([-a for a in self.value], self.description)
    
  def __repr__(self):
    return 'Column(%r, %r)' % (self.value, self.description)


class Table(object):

  def __init__(self, columns, lower_bound=None, upper_bound=None, description=None):
    self.columns = columns
    self.lower_bound = lower_bound
    self.upper_bound = upper_bound
    self.description = description
    
  def __str__(self):
    f = io.StringIO()
    if self.description:
      print(self.description, file=f)

    w = csv.writer(f)
    w.writerow([c.name for c in self.columns])

    # TODO Filter by limits if present
    for row in zip(*self.columns):
      w.writerow(row)
    return f.getvalue()
