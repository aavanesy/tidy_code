from tablite import Table, GroupBy
from datetime import datetime,date

# 1. Import the data
df = Table.import_file('data.csv', import_as='csv')

# 2. create the joined month-year field.
df['date'] = [datetime.strptime(f"{m} {y}", '%b %Y').date() for m,y in zip(df['Month'], df['Year'])]  # add datetime str.

# 3. add zeros for blanks.
for month in range(1,12+1):  
    for variable in set(df['Variable']):
        dt = date(2022,month,1)
        df.add_rows("John Henry", dt.strftime('%b'), 2022, variable, 0, dt)

# 4. sort by date (not in reverse order), as the tablite pivot keeps the order.
df = df.sort(date=False)

# 5. create the pivot.
pivot = df.pivot(rows=['Variable'], columns=['date'], functions=[('Amount', GroupBy.sum)])  # do the pivot

# 6. create the year total column
pivot['YearTotal'] = [sum(r[2:]) for r in pivot.rows]
# 7. remove extra columns
del pivot['function']
# 8. Add total brutton.
pivot.add_rows(["TotalBrutto"] + [sum(pivot[c]) for c in pivot.columns[1:]])