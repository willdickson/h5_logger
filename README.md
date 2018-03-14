## h5_logger 

Simple HDF5 data logger. 



## Installation

Requirements: numpy, arrow, h5py

```bash
$ python setup.py install 

```


## Example

``` python
import h5_logger
import numpy as np

logger = h5_logger.H5Logger(logfile,param_attr=run_param)

for i in range(num_steps):
    data = {'t': 0.01*i, 'x': 2.0*i, 'a': np.random.rand(2,2)}
    logger.add(data)

```




