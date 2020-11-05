# **Data Analysis Library in Python**

This is a basic data analysis library based on pandas. It was build after taking tutorials from [Ted Petrou][1].

## **Features of this library**

1. Have a DataFrame class with data stored in numpy arrays.
2. Read in data from a comma-separated value files.
3. Have a nicely formatted display of DataFrame in the notebook.
4. Select subsets of data with brackets operator.
5. Use special methods defined in python data model.
6. Implement aggregation methods - sum, min, max, median, etc.
7. Implement non-aggregation methods - isna, unique, rename ,drop.
8. Have methods specific to string columns - aggregation methods don't make any sense in string columns like sum.

## **DataFrame, Methods and Properties**
For usage of these features see [Examples.ipynb][2]

### **DataFrame**

DataFrame(data)  
1. data should be python dict.   
2. keys should be string. They will form column names.  
3. values must be one dimensional numpy array.  
4. Length of all numpy arrays must be same.  
5. All unicode numpy arrays will be converted to object type to provide more flexibility.  

Note: Unlike pandas accessing columns using `.` operator is not supported.  
        
            >>> emps.salary      # will give error  
            >>> emps['salary']   # will work
            

### **Basic Properties**

* `columns`: This property can be used to retrive columns as a list and to set a column.
* `shape`: Returns shape of DataFrame as a tuple.
* `values`: Returns list of all column values as numpy arrays.
* `dtypes`: Returns a two-column DataFrame containing type of each column.

### **Basic Methods**

* `read_csv`:  &nbsp;To read csv file data.
* `head`: Returns first n rows of DataFrame.
* `tail`: Returns last n rows of DataFrame.
* `isna`: Returns a boolean DataFrame with each cell either `True` or `False`. `True` means value in that cell is not missing, `False` means missing.
* `count`: The `count` method returns a single-row DataFrame with the number of non-missing values for each column.
* `unique`: This method will return the unique values for each column in the DataFrame. Specifically, it will return a list of one-column DataFrames of unique values in each column.
* `nunique` : Returns a single-row DataFrame with the number of unique values for each column.
* `value_counts`: Returns frequency of unique values in DataFrame.
* `rename`: The `rename` method renames one or more column names.
* `drop`: Accept a single string or a list of column names as strings. Return a DataFrame without those columns.
* `sort_values` : Sorts the dataframe rows according to one or more columns.
* `sample`: Returns a randomly selected sample of rows.
    
### **Using brackets operator**

Selecting data using brackets operator. There are many features provided by brackets operator. Some are:  
* Select single column: &nbsp;`df['col_name']`
* Select multiple column: &nbsp;`df[list of columns]`
* Select rows and columns simultaneously: &nbsp;`df[list of rows, list of columns]`
* Select using slices: &nbsp;`df[2:5, 3:5]`
* Boolean selection: &nbsp;`df[boolean condition or boolean mask]`

### **Implementation of special methods of python data model**

Using special methods defined in the python data model
* Provided support for pointwise operations like +, - etc:  
    Example: `df[col_name]` + 1000 will add 1000 to each value in column `col_name`.
* Implemented `__len__` special method to provide support for `len()`. It will return number of rows in DataFrame.

### **Arithmetic and Comparison operators**

* Used special methods to implement arithmetic and comparison operators.
+, -, *, %(modulus), //(floor division), /(true division), <, >, ==, !=, <=, >=

### **Aggregation methods**

To summarize a sequences of values using a single value.  
* `min`
* `max`
* `mean`
* `median`
* `sum`
* `var`
* `std`
* `all`
* `any`
* `argmax` - index of the maximum
* `argmin` - index of the minimum

### **Non-Aggregation methods**

* `abs`
* `cummin`
* `cummax`
* `cumsum`
* `clip`
* `round`
* `copy`
* `diff` 
* `pct_change` 

### **String Methods**

All the string methods present in python are implemented here. They have same syntax as in python except that here they return DataFrame.

* `capitailize`
* `count`
* `endswith` 
* `startswith` 
* `find` 
* `len` 
* `get` 
* `index` 
* `isalnum` 
* `isaplha` 
* `isdecimal` 
* `islower` 
* `isnumeric` 
* `isspace` 
* `istitle` 
* `isupper` 
* `lstrip` 
* `rstrip` 
* `strip` 
* `replace`,
* `swapcase` 
* `title` 
* `lower` 
* `upper`
* `zfill`
* `encode`

### TODO

- [] Simultaneously adding or overwriting multiple rows and columns in DataFrame. Current support is only for adding one column at a time.
- [] `Generic Aggregation methods`: Support for columnwise aggregation is provided. Pandas provides both row and column aggregation. Implement row aggregation as well. 
- [] Add support to access columns using . operator. 
`df.salary` is not supported
only df['salary'] is supported.
- [] Add `groupby()` method. 


[1]: https://www.youtube.com/channel/UCaJkwcpaePY_kYryKLIfu4A
[2]: https://github.com/yash9724/pandas_cub/blob/master/Examples.ipynb
