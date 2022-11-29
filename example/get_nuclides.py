import pypact as pp

# the standard output file from FISPACT-II
# test files exist in 'references' directory
filename = './data/EC/WCLL/inventory_10.out'

time = 5
print(f'time = {time}')
with pp.Reader(filename) as output:
   nuclides = output[time].nuclides
   Nnuc = len(nuclides)
   for nuc in nuclides:
      print(f"{nuc.name} = {nuc.atoms:.3e} atoms")
print(f'total number {Nnuc+1}')
