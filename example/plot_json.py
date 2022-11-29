import pypact as pp
import matplotlib.pyplot as plt
time = []
data = []
output = pp.Output()
with open('inventory.json') as f:
  output.json_deserialize(f.read())
for t in output.inventory_data:
  if not t.isirradiation:
    time.append(t.currenttime)
    data.append(t.gamma_heat)


plt.plot(time, data)

plt.xscale('log')
plt.yscale('log')
plt.show()
