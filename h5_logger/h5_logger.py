from __future__ import print_function

import os
import os.path

import h5py
import numpy as np
import arrow
import json


class H5Logger(object):

    Default_Auto_Incr_Format = '{0:06d}'

    def __init__(
            self,
            filename='data.hdf5',
            auto_incr=False, 
            auto_incr_format=Default_Auto_Incr_Format,
            param_attr = None
            ):
        self.auto_incr = auto_incr
        self.auto_incr_format = auto_incr_format
        self.h5file = None
        self.dataset_dict = None 
        self.filename = filename
        self.param_attr = param_attr

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self,value):
        self._filename = value
        self.init_log_count()

    def init_log_count(self):
        self.log_count = 0
        if self.auto_incr:
            dirname, base, ext = fileparts(self.filename)
            file_list = [f for f in os.listdir(dirname) if os.path.isfile(os.path.join(dirname,f))]
            file_list = [os.path.splitext(f)[0] for f in file_list if os.path.splitext(f)[1] == ext]
            file_list = [f for f in file_list if base == f[:len(base)]]
            str_list = [f[len(base):] for f in file_list]
            val_list = []
            for item in str_list:
                try:
                    val_list.append(int(item))
                except ValueError:
                    continue
            if val_list:
                self.log_count = max(val_list)

    def get_next_filename(self):
        next_filename = self.filename
        if self.auto_incr:
            self.log_count += 1
            dirname, base, ext = fileparts(self.filename)
            filename_w_incr = '{0}{1}{2}'.format(base,self.auto_incr_format,ext).format(self.log_count)
            next_filename = os.path.join(dirname, filename_w_incr)
        return next_filename

    def reset(self):
        if self.h5file is not None:
            self.h5file.close()
        self.h5file = None
        self.dataset_dict = None 

    def add(self,data):
        
        if self.h5file is None:
            # Create h5df file and dataset_dict file and add values
            next_filename = self.get_next_filename()
            self.h5file = h5py.File(next_filename,'w')
            self.dataset_dict = {}
            for key,val in data.iteritems():
                if not type(val) == np.ndarray:
                    val_as_np = convert_to_np(val)
                else:
                    val_as_np = np.reshape(val, (1,) + val.shape)
                dtype = val_as_np.dtype
                shape = (1,) + val_as_np.shape[1:]
                maxshape = (None,) + val_as_np.shape[1:]
                self.dataset_dict[key] = self.h5file.create_dataset(key, shape, maxshape=maxshape, dtype=dtype)
                self.dataset_dict[key][0] = val_as_np

            # Add data creation time 
            now = arrow.now()
            self.h5file.attrs['timestamp'] = now.timestamp
            self.h5file.attrs['datetime'] = now.format('YYYY-MM-DD HH:mm:ss')

            # Add parameter attribute is it exists
            if self.param_attr is not None:
                jsonparam = json.dumps(self.param_attr)
                self.h5file.attrs['jsonparam'] = jsonparam

        else:
            # Add data to existing hdf5 file dataset_dict
            if set(data.keys()) != set(self.dataset_dict.keys()):
                raise ValueError('keys in data do not match those is existing dataset')
            for key, val in data.iteritems():
                shape = self.dataset_dict[key].shape
                num_vals = shape[0]
                self.dataset_dict[key].resize((num_vals+1,) + shape[1:])
                if not type(val) == np.ndarray:
                    val_as_np = convert_to_np(val)
                else:
                    val_as_np = np.reshape(val, (1,) + val.shape) 
                self.dataset_dict[key][num_vals] = val_as_np


# Utility functions
# -------------------------------------------------------------------------------------------------

def convert_to_np(val):
    if type(val) != np.ndarray:
        return np.array([val])
    else:
        return val

def fileparts(filename): 
    dirname, filename_only = os.path.split(filename)
    base, ext = os.path.splitext(filename_only)
    if not dirname:
        dirname = os.curdir
    return dirname, base, ext




