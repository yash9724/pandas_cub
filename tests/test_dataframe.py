import numpy as np
from numpy.testing import assert_array_equal
import pytest

import pandas_cub as pdc
from tests import assert_df_equals

pytestmark = pytest.mark.filterwarnings("ignore")

a = np.array(['a', 'b', 'c'])
b = np.array(['c', 'd', None])
c = np.random.rand(3)
d = np.array([True, False, True])
e = np.array([1, 2, 3])
df = pdc.DataFrame({'a': a, 'b': b, 'c': c, 'd': d, 'e': e})

"""
This class holds tests responsible for methods required
for valid dataframe creation 
"""

class TestDataFrameCreation:

    def test_input_types(self):
        with pytest.raises(TypeError):
            pdc.DataFrame([1, 2, 3])

        with pytest.raises(TypeError):
            pdc.DataFrame({1: 5, 'b': 10})

        with pytest.raises(TypeError):
            pdc.DataFrame({'a': np.array([1]), 'b': 10})

        with pytest.raises(ValueError):
            pdc.DataFrame({'a': np.array([1]), 
                           'b': np.array([[1]])})

        # correct construction. no error
        pdc.DataFrame({'a': np.array([1]), 
                       'b': np.array([1])})

    def test_array_length(self):
        with pytest.raises(ValueError):
            pdc.DataFrame({'a': np.array([1, 2]), 
                           'b': np.array([1])})
        # correct construction. no error                           
        pdc.DataFrame({'a': np.array([1, 2]), 
                        'b': np.array([5, 10])})

    def test_unicode_to_object(self):
        a_object = a.astype('O')
        assert_array_equal(df._data['a'], a_object)
        assert_array_equal(df._data['b'], b)
        assert_array_equal(df._data['c'], c)
        assert_array_equal(df._data['d'], d)
        assert_array_equal(df._data['e'], e)

    def test_len(self):
        assert len(df) == 3

    def test_columns(self):
        assert df.columns == ['a', 'b', 'c', 'd', 'e']

    def test_set_columns(self):
        with pytest.raises(TypeError):
            df.columns = 5

        with pytest.raises(ValueError):
            df.columns = ['a', 'b']

        with pytest.raises(TypeError):
            df.columns = [1, 2, 3, 4, 5]

        with pytest.raises(ValueError):
            df.columns = ['f', 'f', 'g', 'h', 'i']

        df.columns = ['f', 'g', 'h', 'i', 'j']
        assert df.columns == ['f', 'g', 'h', 'i', 'j']

        # set it back
        df.columns = ['a', 'b', 'c', 'd', 'e']
        assert df.columns == ['a', 'b', 'c', 'd', 'e']

    def test_shape(self):
        assert df.shape == (3, 5)

    def test_values(self):
        values = np.column_stack((a, b, c, d, e))
        assert_array_equal(df.values, values)

    def test_dtypes(self):
        cols = np.array(['a', 'b', 'c', 'd', 'e'], dtype='O')
        dtypes = np.array(['string', 'string', 'float', 'bool', 'int'], dtype='O')

        df_result = df.dtypes
        df_answer = pdc.DataFrame({'Column Name': cols,
                                   'Data Type': dtypes})
        assert_df_equals(df_result, df_answer)


"""
This class holds tests responsible for methods required
for selection of data from dataframe
"""
class TestSelection:

    def test_one_column(self):
        assert_array_equal(df['a'].values[:, 0], a)
        assert_array_equal(df['c'].values[:, 0], c)

    def test_multiple_columns(self):
        cols = ['a', 'c']
        df_result = df[cols]
        df_answer = pdc.DataFrame({'a': a, 'c': c})
        assert_df_equals(df_result, df_answer)


