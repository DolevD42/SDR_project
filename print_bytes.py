import numpy as np
import matplotlib.pyplot as plt

# Assuming a binary file 'data.bin' with float32 data
bin_array = np.fromfile('data.bin', dtype=np.float32)

print(bin_array)
plt.figure()

plt.plot(bin_array[20000:40000])
plt.show()