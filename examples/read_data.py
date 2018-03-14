from __future__ import print_function
import h5py
import json
import numpy as np
import sys

filename = sys.argv[1]

data = h5py.File(filename,'r')

print()
print('attrs')
print('----------------------')
for k,v in data.attrs.iteritems():
    print(k,v)


run_param = json.loads(data.attrs['jsonparam'])
print(run_param['num_steps'])
print(data.attrs['datetime'])


print()
print('datasets')
print('----------------------')
for k,v in data.iteritems():
    print(k,v.shape)


t = np.array(data['t'])
x = np.array(data['x'])
a = np.array(data['a'])










