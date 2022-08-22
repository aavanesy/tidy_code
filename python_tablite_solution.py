from tablite import Table, GroupBy
from datetime import datetime,date
Table.reset_storage()

# 1. Import the data
df = Table.import_file('data.csv', import_as='csv')

# 2. create the joined month-year field by adding datetime str.
df['date'] = [datetime.strptime(f"{m} {y}", '%b %Y').date() for m,y in zip(df['Month'], df['Year'])]  

# 3. add zeros for blanks.
var_order = ['Salary','Bonus', 'Taxes']
for month in range(1,12+1):  
    for variable in var_order:
        dt = date(2022,month,1)
        df.add_rows("John Henry", dt.strftime('%b'), 2022, variable, 0, dt)  

# 4. sort by date (not in reverse order), as the tablite pivot keeps the order.
df = df.sort(date=False)  

# 5. create the pivot.
pivot = df.pivot(rows=['Variable'], columns=['date'], functions=[('Amount', GroupBy.sum)])  

# 6. remove extra column
del pivot['function']  

# 7. rename the columns from (date=2022-01-01) to 2022-01
for column_name in pivot.columns[1:]:  
    new_name = column_name[6:13]
    pivot[new_name] = pivot[column_name][:]
    del pivot[column_name]

# 8. reindex so that taxes are at the bottom.
sorted_pivot = pivot.reindex(index=[var_order.index(v) for v in list(pivot['Variable'])])  

# 9. create the YearTotal column
sorted_pivot['YearTotal'] = [sum(r[1:]) for r in sorted_pivot.rows] 

# 10. Add TotalBrutto.
sorted_pivot.add_rows(["TotalBrutto"] + [sum(sorted_pivot[c]) for c in sorted_pivot.columns[1:]])  

sorted_pivot  # show it.
