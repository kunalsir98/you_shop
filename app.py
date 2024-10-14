from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

app = Flask(__name__)

# Set the upload folder and allowed extensions
UPLOAD_FOLDER = 'static/uploads'  # Path where you want to save uploaded files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

# Simple question-answer pairs for the chatbot
QA={
    "What is your name?": "I'm a simple chatbot.",
    "How can I contact support?": "You can contact support at support@example.com.",
    "What are your operating hours?": "We are available from 9 AM to 5 PM.",
    "What services do you offer?": "We offer a variety of services including promotions, reviews, and local business information.",
    "How can I submit a promotion?": "You can submit a promotion through the 'Add a Promotion' button on our homepage.",
    "What types of promotions can I find?": "You can find discounts, special offers, and deals from local businesses.",
    "Can I leave a review for a promotion?": "Yes, you can leave a review after selecting a promotion.",
    "How do I update my profile?": "You can update your profile in the account settings section.",
    "Is there a mobile app available?": "Currently, we do not have a mobile app, but our website is mobile-friendly.",
    "How do I reset my password?": "You can reset your password by clicking on the 'Forgot Password' link on the login page.",
    "Can I delete my account?": "Yes, you can delete your account in the account settings.",
    "What payment methods are accepted?": "We accept credit cards, debit cards, and PayPal.",
    "Are there any membership fees?": "No, our services are free to use.",
    "How do I unsubscribe from emails?": "You can unsubscribe from emails by clicking the 'unsubscribe' link at the bottom of any email.",
    "What should I do if I encounter a bug?": "Please report any bugs to our support email.",
    "Can I get a refund for a promotion?": "Refunds are handled on a case-by-case basis, please contact support for assistance.",
    "Do you have a loyalty program?": "Yes, we have a loyalty program that rewards frequent users.",
    "How often do you update promotions?": "We update promotions regularly, so check back often for the latest deals.",
    "Can I recommend a business for a promotion?": "Yes, you can recommend a business by contacting our support team.",
    "What do I do if my promotion isn't listed?": "If your promotion is missing, please contact support to resolve the issue.",
    "Is my personal information safe?": "Yes, we take privacy and security seriously. Your information is protected.",
    "Can I change my review after submitting it?": "Currently, you cannot edit your review after submission, but you can submit a new one.",
    "How do I find local businesses?": "You can find local businesses by browsing our promotion list.",
    "What if I forgot my username?": "If you forget your username, please contact support for assistance.",
    "Can I view past promotions?": "Yes, you can view past promotions in your account history.",
    "Are there any seasonal promotions?": "Yes, we offer seasonal promotions throughout the year.",
    "Can I view promotions in my area?": "Yes, you can filter promotions by your location.",
    "How can I provide feedback about the app?": "You can provide feedback through the feedback form on our website.",
    "Do I need to create an account to use the app?": "Creating an account enhances your experience but is not mandatory.",
    "Can I share promotions with friends?": "Yes, you can share promotions via social media or direct links.",
    "What happens if a promotion expires?": "Expired promotions are removed from the listing.",
    "How do you verify promotions?": "We verify promotions by contacting the businesses directly.",
    "Can I save my favorite promotions?": "Yes, you can save your favorite promotions in your account.",
    "Are there any restrictions on reviews?": "Yes, reviews must be respectful and relevant to the promotion.",
    "How do I report inappropriate content?": "You can report inappropriate content to support for review.",
    "What is the refund policy?": "Our refund policy varies based on the type of promotion.",
    "Can I change my review rating?": "Currently, you cannot change your review rating after submission.",
    "How do I find out about new promotions?": "You can sign up for our newsletter to receive updates on new promotions.",
    "What are the benefits of signing up?": "Signing up allows you to save promotions, leave reviews, and receive personalized offers.",
    "Do you offer any discounts for students?": "Currently, we do not have student discounts, but stay tuned for future promotions.",
    "Can I suggest features for the app?": "Yes, we welcome feature suggestions through our feedback form.",
    "How do I contact the business directly?": "Contact information for businesses is provided in each promotion.",
    "Are there any age restrictions to use the app?": "Yes, you must be at least 13 years old to use our services.",
    "Can I use the app outside my country?": "Yes, you can access the app from anywhere, but promotions may vary by location.",
    "How do I check the status of my promotion submission?": "You can check the status in your account under the submission history.",
    "What types of businesses can submit promotions?": "Any local business can submit promotions for consideration.",
    "Is there a limit to how many promotions I can submit?": "There is currently no limit to the number of promotions you can submit.",
    "How can I learn more about a promotion?": "Click on the promotion to view more details and terms.",
    "What if I receive a promotion that I did not sign up for?": "Please report this issue to support for investigation.",
    "Can I interact with other users?": "Currently, we do not have a social interaction feature, but it may be added in the future.",
    "How do I keep track of my reviews?": "You can view all your reviews in your account profile.",
    "Are there any hidden fees for promotions?": "No, there are no hidden fees associated with promotions.",
    "How do I know if my promotion is active?": "You will receive a notification once your promotion is approved and active.",
    "What kind of support is available?": "You can reach our support team via email for any questions or concerns.",
    "Can I ask for personalized promotions?": "Yes, you can ask for personalized promotions by contacting support.",
    "What if I have multiple businesses?": "You can submit promotions for each business individually.",
    "How often do you check for fraudulent promotions?": "We regularly monitor promotions to prevent fraud.",
    "Can I unsubscribe from notifications?": "Yes, you can manage your notification preferences in your account settings.",
    "Are there any community guidelines?": "Yes, we have community guidelines that all users must follow.",
    "How do I appeal a rejected promotion?": "You can appeal a rejected promotion by contacting support with your reasons.",
    "Can I see reviews before I submit mine?": "Yes, you can read existing reviews before submitting your own.",
    "Is there a feature for live chat?": "Currently, we do not have a live chat feature, but it may be added in the future.",
    "How do I find the best deals?": "You can sort promotions by popularity or rating to find the best deals.",
    "Can I change my email address?": "Yes, you can change your email address in your account settings.",
    "What if I encounter an error while using the app?": "Please report any errors to our support team for assistance.",
    "How do I clear my search history?": "You can clear your search history in your account settings.",
    "Can I switch my account to a business account?": "Yes, you can switch your account type by contacting support.",
    "How long does it take to approve a promotion?": "Promotion approval typically takes 1-3 business days.",
    "What if I don't receive my verification email?": "Please check your spam folder and contact support if you still don't receive it.",
    "Is there a referral program?": "Yes, we have a referral program that rewards users for inviting others.",
    "How do I leave feedback on my experience?": "You can leave feedback through the feedback form on our website.",
    "Can I view promotions for specific categories?": "Yes, you can filter promotions by categories on our website.",
    "What is the best way to stay updated?": "Sign up for our newsletter to stay informed about the latest promotions.",
    "Can I access the app offline?": "No, you need an internet connection to access the app.",
    "Are there any tutorials available?": "Yes, we provide tutorials on how to use the app effectively.",
    "What languages is the app available in?": "Currently, the app is available in English.",
    "Can I change my password from the app?": "Yes, you can change your password in the account settings.",
    "How do I report a scam promotion?": "You can report scams directly to our support team.",
    "Can I see my promotion performance?": "Yes, you can view your promotion performance in your account dashboard.",
    "Are promotions available in multiple locations?": "Promotions are typically location-based, but you can check for variations.",
    "What if I find a duplicate promotion?": "Please report duplicate promotions to our support team for review.",
    "How do I manage my notifications?": "You can manage notifications in your account settings.",
    "What if I encounter difficulties while submitting a review?": "Please contact support for help with submitting a review.",
    "Can I request a specific promotion?": "Yes, you can request specific promotions through our feedback form.",
    "How often should I check for new promotions?": "We recommend checking regularly, as promotions are updated frequently."
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

# Route for chatbot question answering
@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json.get("question")
    answer = QA.get(user_question, "I'm sorry, I don't understand that question.")
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)
