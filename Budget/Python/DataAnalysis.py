import pandas as pd
import mysql.connector
import matplotlib

from pandas import DataFrame
## CONNECTING TO MYSQL DB ##
mydb = mysql.connector.connect(host='localhost', user='Zdebski', passwd = 'Debski1515@')
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM dbo.vw_chargestransactions")


table_rows = mycursor.fetchall()

df = pd.DataFrame(table_rows)
#keeping only the first 7 columns
df = df[[0,1,2,3,4,5,6,7]]

#renaming columns
df.rename(columns={0:'date', 1: 'description', 2: 'amount', 3: 'status', 4:'isActive',5:'validFmTs',6: 'validToTs',7:'category'}, inplace=True)

df['year'] = pd.DatetimeIndex(df['date']).year
df['month'] = pd.DatetimeIndex(df['date']).month

df2 = df.groupby(['year','month','category'])['amount'].agg('sum')


df2 = df2[['year','month','category','amount']]
print(df2)

#df2.groupby(['year','month','category']).sum().plot(y='sum', kind='bar')
#df.groupby('year').sum().plot(y='amount', kind='bar')
#print(df2)




# csv_data=csv_data[['Description','Amount','Status']]