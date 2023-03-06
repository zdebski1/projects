import mysql.connector
import pandas as pd
import glob
import os 

from sqlalchemy  import create_engine



path = r'C:\Users\Brittany\Desktop\Repos\Python\Budget\Data\march'

# find the latest csv file in a directory
list_of_files = glob.glob(r'C:\Users\Brittany\Desktop\Repos\Python\Budget\Data\march\*')
latest_file = max(list_of_files, key=os.path.getctime)

df=pd.read_csv(latest_file)
df = df.reset_index(drop=True)


mydb = mysql.connector.connect(host='localhost', user='Zdebski', passwd = 'Debski1515')

# truncatequery = "TRUNCATE TABLE stage.ChargesTransactions"
# mycursor = mydb.cursor()
# mycursor.execute(truncatequery)
# mydb.commit()


engine = create_engine("mysql://Zdebski:Debski1515@localhost/stage")
con = engine.connect()

df.to_sql(name='chargestransactions',con=con,if_exists='replace',index=False,schema='stage')

con.commit()


#execute the load into production table


executequery = "CALL dbo.LoadChargesTransactions;"
mycursor = mydb.cursor()
mycursor.execute(executequery)
mydb.commit()



print('Finish Import')