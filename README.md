Objectives

Overall objective is to build a library similar to pandas
1. Have a DataFrame class with data stored in numpy arrays
2. Read in data from a comma-separated value file.
3. have a nicely formatted display of DataFrame in the notebook
4. Select subsets of data with brackets operator
5. Use special methods defined in python data model.
6. Implement aggregation methods - sum, min, max, median, etc.
7. Implement non-aggregation methods - isna, unique, rename ,drop
8. Group by one or two columns
9. Have methods specific to string columns - aggregation methods don't make any sense in string columns like sum

methods ---> in readme file give on example of each of them
1. read_csv --> to read file data

2. head() --> return first 5 rows

3. Selecting data using brackets operator. There are many features 
provided by brackets operator. Some are
    a. selecting single column - df['col_name']
    b. selecting multiple column - df[list of columns]
    c. selecting rows and columns simultaneously --> df[list of rows, list of columns]
    d. selcting using slices --> df[2:5, 3:5]
    e. boolean selection --> df[boolean condition or boolean mask]

4. Using special methods defined in the python data model
    a. How to make len() applicable on our DataFrame
    b. Using special methods too implement ops like +, - etc
            ex: df['salary'] + 10000  --> pointwise addition

5. Aggregation methods -- summarises a sequences of values using a single value
    ex: mean(), median(), sum() etc

6. Non-Aggregation methods
    Ex: unique()  --> returns a list of dataframes each for one column
                    containing unique values in that column

7. Group by one or two columns only --> pandas can group by any no of columns
    ex: df.pivot_table(rows='dept', column='race', values='salary' , aggfunc='mean')

8. Have methods specific for columns
    ex: 1. df.str.count(col_name, 'a') --> count no of a's in each value in dept column.
    
        