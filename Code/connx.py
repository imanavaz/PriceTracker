import mysql.connector
import datetime
from mysql.connector import errorcode

def connectDB():
    """ Connect to the PostgreSQL database server """
    try:
        # read connection parameters
        #params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the MySQL database...')
        cnx = mysql.connector.connect(
                            user='vhost1011', 
                            password='AgVipx8Rv0C0NK0A',
                            host='shared-db.its.deakin.edu.au',
                            database='vhost1011')

 
        # create a cursor
        cur = cnx.cursor()
        
        
        # execute a statement
        print('List of tables available in database:')
        cur.execute('SELECT table_name FROM information_schema.tables where table_schema=\'vhost1011\';')

        #t = datetime.datetime.now(datetime.timezone.utc)
        # cur.execute('INSERT INTO public."Product"("UID", "Source", "Date_of_insertion", "Date_of_data_extraction", "Brand", "Product_name", "Category", "Pack_size", "Serving_size", "Servings_per_Pack", "Product_code", "Energy_per_100g_or_100ml", "Protein_per_100g_or_100ml", "Total_fat_per_100g_or_100ml", "Saturated_fat_per_100g_or_100ml", "Carbohydrate_per_100g_or_100ml", "Sugars_per_100g_or_100ml", "Sodium_per_100g_or_100ml", "Price_at_insertion") VALUES (%s)', 
        #                                        ('test5678', 'Coles', t, t, '100 Plus', 'Isotonic Drink', 'International Foods', '325mL', '325ml', '1', '6800779P', '113kJ', '0g', '0g', '0g', '6.8g', '6.8', '48mg', 1.25,))
        # cur.execute('SELECT * FROM public."Product"')

        # display the PostgreSQL database server version
        tableList = cur.fetchall()
        print(tableList)
       
        # close the communication with the PostgreSQL
        #cur.close()

        return cnx

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Could not recognise your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        cnx.close()
         


def disconnectDB(con):
    con.close()
    print('Database connection closed.')
 

if __name__ == '__main__':
    connectDB()

