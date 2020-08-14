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
        
        # select specific rows using boolean selection
        if isinstance(item, DataFrame):
            if item.shape[1] != 1:
                raise ValueError('Can only pass a one column DataFrame for selection')
        
            bool_arr = next(iter(item._data.values()));
            if bool_arr.dtype.kind != 'b':
                raise TypeError('DataFrame must be a boolean')
            
            new_data = {}
            for col, values in self._data.items():
                new_data[col] = values[bool_arr]
            return DataFrame(new_data)
    
        
        if isinstance(item, tuple):
            return self._getitem_tuple(item)
        else:
            raise TypeError('Select with either a string, a list, or a row and column '
                            'simultaneous selection')
        
    
    def _getitem_tuple(self, item):
        # simultaneous selection of rows and cols -> df[rs, cs]
        if len(item) != 2:
            raise ValueError('Pass either a single string or a two-item tuple inside the '
                                'selection operator.')
        
        row_selection = item[0];
        col_selection = item[1]

        if isinstance(row_selection, int):
            row_selection = [row_selection]
        elif isinstance(row_selection, DataFrame):
            if row_selection.shape[1] != 1:
                raise ValueError('Can only pass a one column DataFrame for selection')
            row_selection = next(iter(row_selection._data.values()))
            if row_selection.dtype.kind != 'b':
                raise TypeError('DataFrame must be a boolean')
        elif not isinstance(row_selection, (list, slice)):
            raise TypeError('Row selection must be either an int, slice, list or DataFrame.')

        
        if isinstance(col_selection, int):
            col_selection = [self.columns[col_selection]]
        elif isinstance(col_selection, str):
            col_selection = [col_selection]
        elif isinstance(col_selection, list):
            new_col_selection = []
            for col in col_selection:
                if isinstance(col, int):
                    new_col_selection.append(self.columns[col])
                else:
                    new_col_selection.append(col)
            col_selection = new_col_selection
        elif isinstance(col_selection, slice):
            start = col_selection.start
            stop = col_selection.stop
            step = col_selection.step

            if isinstance(start, str):
                start = self.columns.index(col_selection.start)
            if isinstance(stop, str):
                stop = self.columns.index(col_selection.stop) + 1

            col_selection = self.columns[start:stop:step]
        else:
            raise TypeError('Column selection must be either an int, string, list, or slice')

        new_data = {}
        for col in col_selection:
            new_data[col] = self._data[col][row_selection]
        return DataFrame(new_data)
            


    def _ipython_key_completions_(self):
        # allows for tab completion when doing df['c
        return self.columns

    def __setitem__(self, key, value):
        # adds a new column or a overwrites an old column
        if not isinstance(key, str):
            raise NotImplementedError('Only able to set a single column')
        
        if isinstance(value, np.ndarray):
            if value.ndim != 1:
                raise ValueError('Setting array must be 1D')
            if len(value) != len(self):
                raise ValueError('Setting array must be same length as DataFrame')
        elif isinstance(value, DataFrame):
            if value.shape[1] != 1:
                raise ValueError('Setting DataFrame must be one column')
            if len(value) != len(self):
                raise ValueError('Setting and Calling DataFrames must be the same length')
            value = next(iter(value._data.values()))
        elif isinstance(value,(int, float, bool, str)):
            value = np.repeat(value,len(self))
        else:
            raise TypeError('Setting value must either be a numpy array, '
                            'DataFrame, integer, string, float, or boolean')
        
        if value.dtype.kind == 'U':
            value = value.astype('O')
        
        self._data[key] = value

    def head(self, n=5):
        return self[:n , :]

    def tail(self, n=5):
        return self[-n:,:]

    #### Aggregation Methods ####

    def min(self):
        return self._agg(np.min)

    def max(self):
        return self._agg(np.max)

    def mean(self):
        return self._agg(np.mean)

    def median(self):
        return self._agg(np.median)

    def sum(self):
        return self._agg(np.sum)

    def var(self):
        return self._agg(np.var)

    def std(self):
        return self._agg(np.std)

    def all(self):
        return self._agg(np.all)

    def any(self):
        return self._agg(np.any)

    def argmax(self):
        return self._agg(np.argmax)

    def argmin(self):
        return self._agg(np.argmin)

    def _agg(self, aggfunc):
        
        new_data = {}
        for col, values in self._data.items():
            try:
                val = aggfunc(values)
            except TypeError:
                continue
            new_data[col] = np.array([val])
        return DataFrame(new_data)

    def isna(self):
       
        new_data = {}
        for col, values in self._data.items():
            kind = values.dtype.kind
            if kind == 'O':
                new_data[col] = values == None 
            else:
                new_data[col] = np.isnan(values)
        return DataFrame(new_data)

    def count(self):
        """
        Counts the number of non-missing values per column

        Returns
        -------
        A DataFrame
        """
        new_data = {}
        df = self.isna()
        length = len(self)
        for col, values in df._data.items():
            val = length - values.sum()
            new_data[col] = np.array([val])
        return DataFrame(new_data)

    def unique(self):
        list_df = []             # list of dataframes to be returned
        for col, values in self._data.items():
            val = np.unique(values)
            list_df.append(DataFrame({col:val}))
        if(len(list_df) == 1):
            return list_df[0]
        return list_df 

    def nunique(self):
        # will return count of unique values in each column
        new_data = {}
        for col, values in self._data.items():
            new_data[col] = np.array([len(np.unique(values))])
        return DataFrame(new_data)
        
    def value_counts(self, normalize=False):
        # a list of dataframe is returned. one dataframe for each column
        # each dataframe contains two columns - one of unique values
        # and other the frequency of each value
        list_df = []
        for col, values in self._data.items():
            uniques,freq = np.unique(values, return_counts = True)
            index_order = np.argsort(-freq)       # generating indices in descending order of freq
            sorted_freq = freq[index_order]       # sorting freq acc. to index order
            sorted_uniques = uniques[index_order] # sorting unique values acc. to index order

            # normalize freq
            if normalize:
                sorted_freq = sorted_freq / sorted_freq.sum()

            list_df.append(DataFrame({col:sorted_uniques, 'count':sorted_freq}))
        if (len(list_df) == 1):
            return list_df[0]
        return list_df
        

    def rename(self, columns):
        # renames columns 
        if isinstance(columns, dict):
            new_data = {}
            for col, values in self._data.items():
                new_data[columns.get(col, col)] = values
            return DataFrame(new_data)
        else:
            raise TypeError('`columns` must be a dictionary')

    
    def drop(self, columns):
        if isinstance(columns, str):
            columns = [columns]
        elif not isinstance(columns, list):
            raise TypeError('`columns` must either be a string or a list')
        new_data = {}
        for col, values in self._data.items():
            if col not in columns:
                new_data[col] = values
        
        return DataFrame(new_data)

    #### Non-Aggregation Methods ####

    def abs(self):
        return self._non_agg(np.abs)

    def cummin(self):
        return self._non_agg(np.minimum.accumulate)

    def cummax(self):
        return self._non_agg(np.maximum.accumulate)

    def cumsum(self):
        return self._non_agg(np.cumsum)

    def clip(self, lower=None, upper=None):
        return self._non_agg(np.clip, a_min=lower, a_max=upper)

    def round(self, n):
        return self._non_agg(np.round, kinds= 'if',decimals=n)

    def copy(self):
        return self._non_agg(np.copy)

    def _non_agg(self, funcname, kinds='bif', **kwargs):
        new_data = {}
        for col, values in self._data.items():
            if values.dtype.kind in kinds:
                new_data[col] = funcname(values, **kwargs)
            else:
                new_data[col] = values.copy()
        return DataFrame(new_data) 
            
    def diff(self, n=1):
        """
        Take the difference between the current value and
        the nth value above it.

        Parameters
        ----------
        n: int

        Returns
        -------
        A DataFrame
        """
        def func(values):
            values = values.astype('float')
            values_rolled = np.roll(values, n)
            values = values - values_rolled
            if n>=0:
                values[:n] = np.NAN
            else:
                values[n:] = np.NAN
            return values            
        return self._non_agg(func)

    def pct_change(self, n=1):
        """
        Take the percentage difference between the current value and
        the nth value above it.

        Parameters
        ----------
        n: int

        Returns
        -------
        A DataFrame
        """
        def func(values):
            values = values.astype('float')
            values_rolled = np.roll(values, n)
            values = values - values_rolled
            if n>=0:
                values[:n] = np.NAN
            else:
                values[n:] = np.NAN
            return values/values_rolled
        return self._non_agg(func)

    #### Arithmetic and Comparison Operators ####

    def __add__(self, other):
        return self._oper('__add__', other)

    def __radd__(self, other):
        return self._oper('__radd__', other)

    def __sub__(self, other):
        return self._oper('__sub__', other)

    def __rsub__(self, other):
        return self._oper('__rsub__', other)

    def __mul__(self, other):
        return self._oper('__mul__', other)

    def __rmul__(self, other):
        return self._oper('__rmul__', other)

    def __truediv__(self, other):
        return self._oper('__truediv__', other)

    def __rtruediv__(self, other):
        return self._oper('__rtruediv__', other)

    def __floordiv__(self, other):
        return self._oper('__floordiv__', other)

    def __rfloordiv__(self, other):
        return self._oper('__rfloordiv__', other)

    def __pow__(self, other):
        return self._oper('__pow__', other)

    def __rpow__(self, other):
        return self._oper('__rpow__', other)

    def __gt__(self, other):
        return self._oper('__gt__', other)

    def __lt__(self, other):
        return self._oper('__lt__', other)

    def __ge__(self, other):
        return self._oper('__ge__', other)

    def __le__(self, other):
        return self._oper('__le__', other)

    def __ne__(self, other):
        return self._oper('__ne__', other)

    def __eq__(self, other):
        return self._oper('__eq__', other)

    def _oper(self, op, other):
        """
        Generic operator function

        Parameters
        ----------
        op: str name of special method
        other: the other object being operated on

        Returns
        -------
        A DataFrame
        """
        if isinstance(other, DataFrame):
            if other.shape[1] != 1:
                raise ValueError('`other` must be one column DataFrame')
            other = next(iter(other._data.values()))
        new_data = {}
        for col, values in self._data.items():
            func = getattr(values, op)
            new_data[col] = func(other)
        return DataFrame(new_data)

    def sort_values(self, by, asc=True):
        """
        Sort the DataFrame by one or more values

        Parameters
        ----------
        by: str or list of column names
        asc: boolean of sorting order

        Returns
        -------
        A DataFrame
        """
        if isinstance(by, str):
            order = np.argsort(self._data[by])
        elif isinstance(by, list):
            cols = [self._data[col] for col in by[::-1]]
            order = np.lexsort(cols)
        else:
            raise TypeError('`by` must be a str or a list')
        
        if not asc:
            order = order[::-1]
        return self[order.tolist(), :]

    def sample(self, n=None, frac=None, replace=False, seed=None):
        if seed:
            np.random.seed(seed)
        if frac is not None:
            if frac <= 0:
                raise ValueError('`frac` should be greater than 0')
            n = int(frac * len(self))
        if n is not None:
            if not isinstance(n, int):
                raise TypeError('`n` must a integer')
            sampled_rows = np.random.choice(np.arange(len(self)),size=n,replace=replace).tolist()
        return self[sampled_rows, :]

    