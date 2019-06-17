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

    @property
    def columns(self):
        return list(self._data)
    
    @columns.setter
    def columns(self, columns):
        if not isinstance(columns, list):
            raise TypeError('New columns must be a list')
            
        if len(columns) != len(self.columns):
            raise ValueError(f'New column length must be {len(self._data)}')
        else:
            for col in columns:
                if not isinstance(col, str):
                    raise TypeError('New column names must be strings')
        if len(columns) != len(set(columns)):
            raise ValueError('Column names must be unique')

        new_data = dict(zip(columns, self._data.values()))
        self._data = new_data

    @property
    def shape(self):
        return len(self),len(self.columns)
    
    def _repr_html_(self):
        html = '<table><thead><tr><th></th>'
        for col in self.columns:
            html += f"<th>{col:10}</th>"

        html += '</tr></thead>'
        html += "<tbody>"

        only_head = False
        num_head = 10
        num_tail = 10
        if len(self) <= 20:
            only_head = True
            num_head = len(self)

        for i in range(num_head):
            html += f'<tr><td><strong>{i}</strong></td>'
            for col, values in self._data.items():
                kind = values.dtype.kind
                if kind == 'f':
                    html += f'<td>{values[i]:10.3f}</td>'
                elif kind == 'b':
                    html += f'<td>{values[i]}</td>'
                elif kind == 'O':
                    v = values[i]
                    if v is None:
                        v = 'None'
                    html += f'<td>{v:10}</td>'
                else:
                    html += f'<td>{values[i]:10}</td>'
            html += '</tr>'

        if not only_head:
            html += '<tr><strong><td>...</td></strong>'
            for i in range(len(self.columns)):
                html += '<td>...</td>'
            html += '</tr>'
            for i in range(-num_tail, 0):
                html += f'<tr><td><strong>{len(self) + i}</strong></td>'
                for col, values in self._data.items():
                    kind = values.dtype.kind
                    if kind == 'f':
                        html += f'<td>{values[i]:10.3f}</td>'
                    elif kind == 'b':
                        html += f'<td>{values[i]}</td>'
                    elif kind == 'O':
                        v = values[i]
                        if v is None:
                            v = 'None'
                        html += f'<td>{v:10}</td>'
                    else:
                        html += f'<td>{values[i]:10}</td>'
                html += '</tr>'

        html += '</tbody></table>'
        return html
    
    @property
    def values(self):
        return np.column_stack(self._data.values())

    @property
    def dtypes(self):
        DTYPE_NAME = {'O': 'string', 'i': 'int', 'f': 'float', 'b': 'bool'}
        col_arr = np.array(self.columns)
        dtypes = []
        for values in self._data.values():
            kind = values.dtype.kind
            dtype = DTYPE_NAME[kind]
            dtypes.append(dtype)

        return DataFrame({'Column Name': col_arr, 'Data Type': np.array(dtypes)})

    
    def __getitem__(self, item):
        # select a single column -> df['column']
        if isinstance(item, str):
            return DataFrame({item: self._data[item]})
        
        # select multiple columns -> df[['col1','col2','col3']]
        if isinstance(item, list):
            return DataFrame({col: self._data[col] for col in item})
            
    def StringMethods(self):
        pass

    
    def _add_docs():
        pass

    