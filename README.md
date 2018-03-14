## h5_logger 

Simple HDF5 based data logger designed for saving numerical data in an
experimental setting.  

Data is appended to the hdf5 data file using a simple add  method, e.g.
logger.add(data) where data is a dictionary of data items. The data dictionary
should always have the same keys and the items in the dictionary should always
same shape, e.g. nxm arrays.  


## Installation

Requirements: numpy, arrow, h5py

```bash
$ python setup.py install 

```


## Example

``` python
import h5_logger
import numpy as np

logger = h5_logger.H5Logger('data.hdf5')

for i in range(num_steps):
    data = {'t': 0.01*i, 'x': 2.0*i, 'a': np.random.rand(2,2)}
    logger.add(data)

```




