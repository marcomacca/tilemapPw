import pyodbc

server = 'pwsmartcross.database.windows.net'
database = 'smartcross'
username ='its2020'
password = 'Projectwork2020'
driver= '{ODBC Driver 17 for SQL Server}'

#DateCreated DATETIME NOT NULL DEFAULT(GETDATE()) x campo data?

cnxn = pyodbc.connect('DRIVER='+driver+
                      ';SERVER='+server+
                      ';PORT=1433;DATABASE='+database+
                      ';UID='+username+
                      ';PWD='+ password)

cursor = cnxn.cursor()
cursor.execute("SELECT * FROM dbo.Traffico")
row = cursor.fetchone()
while row:
    print (str(row))
    row = cursor.fetchone()