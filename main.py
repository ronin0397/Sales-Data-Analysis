import sqlite3
import csv
import pandas as pd

# Prompt
print("Your Manager received the sales data for the last 2 years and wants you to analyze it.\n"
      "\nShareholders want to identify:\n"
      "1) which countries/regions have the most sales\n"
      "2) each year's profits/losses\n"
      "3) what is the best selling item\n"
      "\nGood Luck.\n")

#Load the Data
sales_file_path = "online_retail_sales_dataset.csv"
sales_data = pd.read_csv(sales_file_path)
#print('This is the sales data:\n', sales_data)
print('Set up is complete')

#Clean the Data

#load the data into SQLite
connection_obj = sqlite3.connect('sales_data.db')
cursor_obj = connection_obj
cursor_obj.execute('DROP TABLE IF EXISTS SALES_DATA')
sales_table = """
    CREATE TABLE SALES_DATA(
        Invoice_Number INT,
        time_stamp FLOAT,
        Customer_ID INT, 
        Product_ID INT,
        Product_Category CHAR(25) NOT NULL, 
        Quantity_Sold INT, 
        Unit_Price INT,
        Discount INT, 
        Payment_Method CHAR(25) NOT NULL, 
        Customer_Age INT, 
        Customer_Gender CHAR(8) NOT NULL, 
        Customer_Location CHAR(25) NOT NULL,
        Total_Amount INT
    );
    """
cursor_obj.execute(sales_table)
cursor_obj = connection_obj.cursor()
with open("online_retail_sales_dataset.csv", 'r') as file:
      csvreader = csv.reader(file)
      for row1 in csvreader:
            print(row1)
            Invoice_Number = row1[0]
            time_stamp = row1[1]
            Customer_ID = row1[2]
            Product_ID = row1[3]
            Product_Category = row1[4]
            Quantity_Sold = row1[5]
            Unit_Price = row1[6]
            Discount = row1[7]
            Payment_Method = row1[8]
            Customer_Age = row1[9]
            Customer_Gender = row1[10]
            Customer_Location = row1[11]
            Total_Amount = row1[12]
            cursor_obj.execute("INSERT INTO SALES_DATA (""Invoice_Number, time_stamp, Customer_ID, Product_ID, Product_Category, Quantity_Sold, Unit_Price, Discount, "
                               "Payment_Method, Customer_Age, Customer_Gender, Customer_Location, Total_Amount)"
                               "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                               (Invoice_Number, time_stamp, Customer_ID, Product_ID, Product_Category, Quantity_Sold, Unit_Price, Discount,
                               Payment_Method, Customer_Age, Customer_Gender, Customer_Location, Total_Amount))
connection_obj.commit()
print('Sales Data Table is ready')


#prompt 1 Which Country has the most Sales
cursor_obj.execute("SELECT Customer_Location, "
                   "       SUM(Total_Amount) as total "
                   "FROM SALES_DATA "
                   "group by Customer_Location "
                   "ORDER BY total DESC")
rows = cursor_obj.fetchall()
print('Here are the sales data totals for each country: \n')
print(*rows, sep='\n')
print(str(rows[0][0]) + ' has the most sales!\n')

#prompt 2 What is each year's revenue?
cursor_obj.execute("SELECT strftime('%Y', time_stamp) as year,"
                   "       SUM(Total_Amount) as total "
                   "FROM SALES_DATA "  
                   "GROUP BY year "
                   "Order BY total ASC ")
rows_2 = cursor_obj.fetchall()
print('Here are the sales data totals by year: \n')
print(*rows_2, sep='\n')

#prompt 3 What is the bestselling item?
cursor_obj.execute("SELECT Product_Category, "
                   "       SUM(Total_Amount) as total "
                   "FROM SALES_DATA "
                   "group by Product_Category "
                   "ORDER BY total DESC")
rows_3 = cursor_obj.fetchall()
print('Here are the totals for best selling items: \n')
print(*rows_3, sep='\n')
print(str(rows_3[0][0]) + ' has the most sales!\n')
connection_obj.close()
