import mysql.connector
import csv

mydb = mysql.connector.connect(host='localhost', user='Zdebski', passwd = 'Debski1515@')
with open(r'C:\Users\Brittany\Desktop\Repos\Python\Budget\Data\march\bk_download.csv') as csv_file:
        csvfile = csv.reader(csv_file, delimiter = ',')
        all_value =[]
        for row in csvfile:
                value = (row[0],row[1],row[2],row[3],row[4],row[5])
                all_value.append(value)
#csv_data = pd.read_csv(r'C:\Users\Brittany\Desktop\Repos\Python\Budget\Data\bk_download.csv')

#truncate the staging table before inserting more data... 
#the data lives in files that are always available so no need to kee staging data forever

truncatequery = "TRUNCATE TABLE stage.ChargesTransactions"
insertQuery =  "Insert Into stage.ChargesTransactions (date, description, originalDescription,category,amount, status) VALUE (%s,%s,%s,%s,%s,%s)"
mycursor = mydb.cursor()

mycursor.execute(truncatequery)
mycursor.executemany(insertQuery,all_value)

mydb.commit()