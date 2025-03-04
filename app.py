from flask import Flask, request,jsonify,render_template, redirect,session, url_for
import razorpay
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import numpy as np
import pickle
from datetime import datetime
from mailjet_rest import Client
import requests
import sqlite3



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'jobmeup'

client = razorpay.Client(auth=("rzp_test_Hw4sQn2Wrbsw8u", "FzZKveveEpe47blpGKe9Ssgq"))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    number = db.Column(db.String(100), unique=True)
    dob=db.Column(db.Date(),unique=False)
    payment = db.Column(db.Boolean, default=False)

    def __init__(self, name,email,password,number,dob,payment):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.number = number
        self.dob = dob
        self.payment = payment
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
with app.app_context():
     db.create_all()

@app.route('/signin')
def index():
    return render_template('signup.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle request
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        number = request.form['number']
        dob_str = request.form['dob']
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        payment = request.form.get('payment', False)

        new_user = User(name=name, email=email, password=password, number=number, dob=dob,payment=payment)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['email'] = user.email
            return redirect('/2')
        else:
            return render_template('login.html', error='Invalid user')

    return render_template('login.html')

@app.route("/")
def landing_page():
    return render_template('landing-page1.html')

#   careers

@app.route("/careers")
def careers():
    return render_template('main-sunburst.html')

@app.route('/chiropractor')
def chiropractor():
    return render_template('chiropractor.html')

@app.route('/astronomer')
def astronomer():
    return render_template('astronomer.html')

@app.route('/software-developer')
def software_developer():
    return render_template('software-developer.html')

@app.route('/data-analyst')
def data_analyst():
    return render_template('data-analyst.html')


@app.route('/job_posting')
def jon_posting():
    return render_template('index.html')


@app.route("/quiz")
def quiz():
    return render_template('quiz2.html')


@app.route('/logout')
def logout():
    session.pop('login_email',None)
    return redirect('/login')


model = pickle.load(open('model.pkl', 'rb'))


@app.route('/submit', methods=['POST'])
def submit():
    hcaptcha_response = request.form['h-captcha-response']
    
    secret_key = "ES_5141b751dc3d4680a278485ff4a813b3"  # Replace with your actual secret key
    verify_url = "https://hcaptcha.com/siteverify"

    payload = {
        'secret': secret_key,
        'response': hcaptcha_response
    }

    # Send the POST request to verify the captcha
    response = requests.post(verify_url, data=payload)
    verification_result = response.json()

    if verification_result['success']:
        # Store form values in session
        session['form_data'] = request.form.to_dict() 
        del session['form_data']['g-recaptcha-response']
        del session['form_data']['h-captcha-response'] # Save all form data in the session
        print(session['form_data'])
        return redirect(url_for('predict'))
    else:
        return "hCaptcha validation failed!", 400

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    # Retrieve form data from session
    form_data = session.get('form_data', {})
    if not form_data:
        return "No form data found!", 400

    try:
        int_features = [float(x) for x in form_data.values()]
        final_features = [np.array(int_features)]
        prediction = model.predict(final_features)

        output = round(prediction[0], 9)

        # Redirect based on prediction output
        if output == 0:
            return redirect('/healthcare-and-medical.html')
        elif output == 1:
            return redirect('/science-and-research.html')
        elif output == 2:
            return redirect('/engineering-and-technology.html')
        elif output == 3:
            return redirect('/design-and-creative-arts.html')
        elif output == 4:
            return redirect('/education.html')
        elif output == 5:
            return redirect('/business-and-finance.html')
        elif output == 6:
            return redirect('/law-and-public-service.html')
        elif output == 7:
            return redirect('/media-and-communication.html')
        else:
            return redirect('/webrtc.html')
    except ValueError:
        return "Error processing input data!", 400
    
# @app.route('/communication')
# def payment_form():
#     return render_template('communication.html')


@app.route('/payment_form')
def payment_form():
    return render_template('form.html')

mailjet = Client(auth=('51e9cd9c523e12637bef00832c5f00ab', 'b2cd0d4bc0f7e8f3debe72f25ac50a9d'), version='v3.1')

@app.route('/pay', methods=["GET", "POST"])
def pay():
    emaill = request.form.get("emaill")
    session['emaill'] = emaill
    if request.form.get("amount") != "":
        amount = request.form.get("amt")
        data = { "amount": amount, "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data)
        pdata = [amount, payment["id"]]

        return render_template("payment.html", pdata=pdata)
    return redirect("/2")

@app.route('/success', methods=["POST"])
def success():
    emaill = session.get('emaill') 
    pid = request.form.get("razorpay_payment_id")
    ordid = request.form.get("razorpay_order_id")
    sign = request.form.get("razorpay_signature")
    print(f"The payment id : {pid}, order id : {ordid} and signature : {sign}")
    
    params = {
        'razorpay_order_id': ordid,
        'razorpay_payment_id': pid,
        'razorpay_signature': sign
    }
    
    final = client.utility.verify_payment_signature(params)
    
    if final == True:
        finalans = User.query.filter_by(email=emaill).first()
        if finalans:
            finalans.payment = True  # Set payment column to True
            db.session.commit()  # Commit the changes to the database

            # Prepare and send the email
            send_payment_email(emaill, pid, ordid)

        return redirect("/3", code=301)
    
    return "Something Went Wrong Please Try Again"

def send_payment_email(email, payment_id, order_id):
    subject = "Payment Successful"
    text = f"""
    Your payment has been successfully processed!
    
    Payment ID: {payment_id}
    Order ID: {order_id}
    
    Thank you for your payment!
    """
    
    # Create email payload
    payload = {
        'Messages': [
            {
                'From': {
                    'Email': 'carrerforgebusiness@gmail.com',  # Replace with your sender email
                    'Name': 'Manan Upmanyu'  # Replace with your name
                },
                'To': [
                    {
                        'Email': email,
                        'Name': 'Recipient Name'  # Optional
                    }
                ],
                'Subject': subject,
                'TextPart': text
            }
        ]
    }
    
    # Send email
    result = mailjet.send.create(data=payload)
    if result.status_code != 200:
        print(f"Failed to send email: {result.json()}")


    #------------------------------------- forum db ------------------------------------

def init_db():
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
   
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            likes INTEGER DEFAULT 0,
            dislikes INTEGER DEFAULT 0
        )
    ''')
  
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS replies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            reply TEXT NOT NULL,
            FOREIGN KEY (question_id) REFERENCES questions(id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/submit_question', methods=['POST'])
def submit_question():
    question = request.form['question'].strip()
    
    if len(question) < 5:
        return "Invalid question. It must contain at least 5 characters.", 400
    
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO questions (question) VALUES (?)', (question,))
    conn.commit()
    conn.close()
    return redirect(url_for('forum'))


@app.route('/submit_reply/<int:question_id>', methods=['POST'])
def submit_reply(question_id):
    reply = request.form['reply']
    if len(reply) < 3:
        return "Invalid reply. It must contain at least 3 characters.", 400

    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO replies (question_id, reply) VALUES (?, ?)', (question_id, reply))
    conn.commit()
    conn.close()
    return 'Reply submitted successfully!'

@app.route('/vote/<int:question_id>/<action>', methods=['POST'])
def vote(question_id, action):
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    if action == 'like':
        cursor.execute('UPDATE questions SET likes = likes + 1 WHERE id = ?', (question_id,))
    elif action == 'dislike':
        cursor.execute('UPDATE questions SET dislikes = dislikes + 1 WHERE id = ?', (question_id,))
    conn.commit()
    conn.close()
    return 'Vote submitted!'


@app.route('/get_questions_with_replies', methods=['GET'])
def get_questions_with_replies():
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM questions')
    questions = cursor.fetchall()
    
    result = []
    for question in questions:
        cursor.execute('SELECT * FROM replies WHERE question_id = ?', (question[0],))
        replies = cursor.fetchall()
        result.append({'question': question, 'replies': replies})
    
    conn.close()
    return jsonify(result)


@app.route('/delete_question/<int:id>', methods=['POST'])
def delete_question(id):
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM replies WHERE question_id = ?', (id,))
    cursor.execute('DELETE FROM questions WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return 'Question deleted successfully!'


app.run(debug=True)

