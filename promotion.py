import mysql.connector 
mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root', 
    password = '##kc@##hc@98'
)
mycursor = mydb.cursor()
#mycursor.execute('CREATE DATABASE promotions_db')
mycursor.execute('use promotions_db')
#mycursor.execute('ALTER TABLE promotions ADD COLUMN photo VARCHAR(255)')
#mycursor.execute('CREATE TABLE promotions (id INT AUTO_INCREMENT PRIMARY KEY,business VARCHAR(80) NOT NULL,deal VARCHAR(200) NOT NULL,address VARCHAR(200) NOT NULL)')
#mycursor.execute('CREATE TABLE subscriptions (id INT AUTO_INCREMENT PRIMARY KEY,email VARCHAR(255) NOT NULL,business_name VARCHAR(80) NOT NULL)')
#mycursor.execute('CREATE TABLE reviews (id INT AUTO_INCREMENT PRIMARY KEY,promo_id INT,reviewer_name VARCHAR(255),comment TEXT,FOREIGN KEY (promo_id) REFERENCES promotions(id))')
mycursor.execute('CREATE TABLE users ( id INT AUTO_INCREMENT PRIMARY KEY,username VARCHAR(50) NOT NULL UNIQUE,password VARCHAR(255) NOT NULL)')
