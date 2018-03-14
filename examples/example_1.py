from __future__ import print_function
import h5_logger
import numpy as np
import time 


logfile = 'mydata.hdf5'

num_steps = 100

run_param = {
        'num_steps': num_steps,
        '1st_thing': 10, 
        '2nd_thing': 'bob',
        }

logger = h5_logger.H5Logger(logfile,param_attr=run_param)


for i in range(num_steps):

    print(i)

    data = {
            't': 0.01*i, 
            'x': 2.0*i, 
            'a': np.random.rand(2,2),
            }

    logger.add(data)

    time.sleep(0.01)





