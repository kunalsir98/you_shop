from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables from .env file in development
load_dotenv()

app = Flask(__name__)

# Set the upload folder and allowed extensions
UPLOAD_FOLDER = 'static/uploads'  # Path where you want to save uploaded files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# MySQL Configuration using environment variables
db_config = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),  # Fetch from environment
    'database': os.getenv('MYSQL_DB', 'promotions_db')
}

# Function to add review to a promotion
def add_review_to_promo(promo_id, reviewer_name, comment):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO reviews (promo_id, reviewer_name, comment) VALUES (%s, %s, %s)", 
                   (promo_id, reviewer_name, comment))
    connection.commit()
    cursor.close()
    connection.close()

# Route for the homepage
@app.route('/')
def home():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    
    # Fetch promotions from the database
    cursor.execute("SELECT * FROM promotions")
    promotions = cursor.fetchall()
    
    # Fetch reviews for each promotion
    for promo in promotions:
        cursor.execute("SELECT * FROM reviews WHERE promo_id = %s", (promo['id'],))
        promo['reviews'] = cursor.fetchall()  # Add reviews to each promotion

    cursor.close()
    connection.close()
    return render_template('home.html', promotions=promotions)

# Route to add a promotion
@app.route('/add', methods=['GET', 'POST'])
def add_promotion():
    if request.method == 'POST':
        business = request.form['business']
        deal = request.form['deal']
        address = request.form['address']
        
        # Handle file upload
        file = request.files['photo']  # Retrieve the file from the request
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # Sanitize the filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # Save the file
            
            # Construct the photo URL for database storage
            photo_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)  
            
            # Insert new promotion into the database
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO promotions (business, deal, address, photo) VALUES (%s, %s, %s, %s)", 
                           (business, deal, address, photo_url))
            connection.commit()
            cursor.close()
            connection.close()

            return redirect(url_for('home'))  # Redirect to home after adding promotion

    return render_template('add.html')

# Route to subscribe to promotions
@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    if request.method == 'POST':
        email = request.form['email']
        business_name = request.form['business_name']

        # Insert subscription into the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO subscriptions (email, business_name) VALUES (%s, %s)", (email, business_name))
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('home'))

    return render_template('subscribe.html')

# Route for adding reviews
@app.route('/add_review/<int:promo_id>', methods=['POST'])
def add_review(promo_id):
    reviewer_name = request.form['reviewer_name']
    comment = request.form['comment']

    # Save the review to the database
    add_review_to_promo(promo_id, reviewer_name, comment)

    return redirect(url_for('home'))  # Redirect back to the home page or the appropriate page

if __name__ == '__main__':
    app.run(debug=True)
