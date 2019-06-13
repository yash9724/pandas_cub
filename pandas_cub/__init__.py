import numpy as np 

__version__ = '0.0.1'

class DataFrame:

    def __init__(self,data):
        """
        A DataFrame holds two dimensional heterogeneous data. Create it by
        passing a dictionary of NumPy arrays to the values parameter

        Parameters
        ----------
        data: dict
            A dictionary of strings mapped to NumPy arrays. The key will
            become the column name.
        """
        # check for correct input types
        self._check_input_types(data)

        # check for equal array lengths
        self._check_array_lengths(data)

        #convert unicode arrays to object
        self._data = self._convert_unicode_to_object(data)

        # Allow for special methods for strings
        # self.str = StringMethods(self)
        # self._add_docs()

    def _check_input_types(self, data):
        if not isinstance(data, dict):
            raise TypeError("`data` must be a dictionary of 1-D numpy arrays")
        
        for col_name, values in data.items():
            if not isinstance(col_name, str):
                raise TypeError('All column names must be a string')
            if not isinstance(values, np.ndarray):
                raise TypeError("All values must be a 1-D NumPy array")
            if values.ndim != 1:
                raise ValueError('Each value must be a 1-D NumPy array')
    

    
    def _check_array_lengths(self,data):
        for i, value in enumerate(data.values()):
            if i==0:
                length = len(value)
            elif len(value)!=length:
                raise ValueError('All values must be the same length')

    
    def _convert_unicode_to_object(self,data):
        new_data = {}
        for col_name,values in data.items():
            if values.dtype.kind == 'U':
                new_data[col_name] = values.astype('O')
            else:
                new_data[col_name] = values
        return new_data
    
    def __len__(self):
        return len(next(iter(self._data.values())))
    
    def StringMethods(self):
        pass

    
    def _add_docs():
        pass

    