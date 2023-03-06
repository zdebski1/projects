import pandas as pd
import mysql.connector
import webbrowser

## CONNECTING TO MYSQL DB ##
mydb = mysql.connector.connect(host='localhost', user='Zdebski', passwd = 'Debski1515')
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM dbo.vw_chargestransactions")


table_rows = mycursor.fetchall()

df = pd.DataFrame(table_rows)
#keeping only the first 7 columns
df = df[[0,1,2,3,4,5,6,7]]

#renaming columns
df.rename(columns={0:'date', 1: 'description', 2: 'amount', 3: 'status', 4:'isActive',5:'validFmTs',6: 'validToTs',7:'category'}, inplace=True)

#creating year and month from date
df['year'] = pd.DatetimeIndex(df['date']).year
df['month'] = pd.DatetimeIndex(df['date']).month

#creating just a year month variable 
df['yearMonth'] = pd.to_datetime(df[['year', 'month']].assign(DAY=1))

#categorising charge types
def categorise(row):
        if row['category'] in (['Mortgage Payment','Internet Bill','Water Bill','Golf Cart Payment','Gas Bill','Electric Bill','Pet','Personal Loan','Phone Bill','Car Insurance','ADT Bill','Truck Payment','Car Payment']):
            return 'Bill'
        if row['category'] not in (['Income','Mortgage Payment','Internet Bill','Water Bill','Golf Cart Payment','Gas Bill','Electric Bill','Pet','Personal Loan','Phone Bill','Car Insurance','ADT Bill','Truck Payment','Car Payment']):
            return 'Spending'
        
        return row['category']

# applying new charge types and creating a new variable called newCategory
df['newCategory'] = df.apply(lambda row: categorise(row), axis=1)


#grouping and transposing by sum of amount
df2 = df.groupby(['yearMonth','newCategory'],sort=True)['amount'].agg('sum').unstack()


df2['Bill'] = df2['Bill'].apply(lambda x: x*-1)
df2['Spending'] = df2['Spending'].apply(lambda x: x*-1)

df2 = df2.fillna(0)



#df2 = df2[['Income','Bill','Fast Food','Food & Dining','Gas','Groceries','Home Improvement','Subscriptions','Coffee Shops']]
df2['Net'] = df2['Income'] - df2['Bill'] - df2['Spending']
df2 = df2[['Income','Bill','Spending','Net']]


df2.to_csv(r'C:\Users\Brittany\Desktop\Repos\Python\Budget\Data\ChargesTransactions.csv',index=True)
#print (df2)


# fig, ax = plt.subplots()

# sns.countplot(ax = ax, data = df, x = 'yearMonth', hue = 'amount')

# plt.show()
#print(df2[['Income','Bill','Gas']])



def generate_html(dataframe: pd.DataFrame):
    # get the table HTML from the dataframe
    table_html = dataframe.to_html(table_id="table")
    # construct the complete HTML with jQuery Data tables
    # You can disable paging or enable y scrolling on lines 20 and 21 respectively
    html = f"""
    <html>
    <header>
        <link href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css" rel="stylesheet">
    </header>
    <body>
    {table_html}
    <script src="https://code.jquery.com/jquery-3.6.0.slim.min.js" integrity="sha256-u7e5khyithlIdTpu22PHhENmPcRdFiHRjhAuHcs05RI=" crossorigin="anonymous"></script>
    <script type="text/javascript" src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
    <script>
        $(document).ready( function () {{
            $('#table').DataTable({{
                 paging: false,    
                // scrollY: 400,
            }});
        }});
    </script>
    </body>
    </html>
    """
    # return the html
    return html

if __name__ == "__main__":
    # read the dataframe dataset
    df = pd.read_csv(r'C:\Users\Brittany\Desktop\Repos\Python\Budget\Data\ChargesTransactions.csv')
    # take only first 1000, otherwise it'll generate a large html file
    df = df.iloc[:1000]
    # generate the HTML from the dataframe
    html = generate_html(df)
    # write the HTML content to an HTML file
    open("index.html", "w").write(html)
    # open the new HTML file with the default browser
    webbrowser.open("index.html")

print('finish')