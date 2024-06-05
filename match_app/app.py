from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from flask_migrate import Migrate
import logging
from forms import LoginForm  # Import your LoginForm class

app = Flask(__name__)

# Set the secret key for CSRF protection
app.config['SECRET_KEY'] = '4444'

# Configure your database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # SQLite database URI

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)
app.logger.setLevel(logging.DEBUG)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    university = db.Column(db.String(150))
    city = db.Column(db.String(150))
    interests = db.Column(db.String(500))

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return '<User %r>' % self.username

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reported_user_id = db.Column(db.Integer)
    reason = db.Column(db.String(500))

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ProfileForm(FlaskForm):
    university = StringField('University', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    interests = TextAreaField('Interests', validators=[DataRequired()])
    submit = SubmitField('Update Profile')

class ChatForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')

class ReportForm(FlaskForm):
    reason = TextAreaField('Reason', validators=[DataRequired()])
    submit = SubmitField('Submit Report')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Create an instance of the LoginForm
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):  # Assuming you have a method to check the password
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', form=form, error='Invalid email or password.')
    return render_template('login.html', form=form)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = ProfileForm()
    if request.method == 'POST' and form.validate():
        user = User.query.get(session['user_id'])
        user.university = form.university.data
        user.city = form.city.data
        user.interests = form.interests.data
        db.session.commit()
        flash('Profile updated!', 'success')
    return render_template('profile.html', form=form)

@app.route('/match')
def match():
    user = User.query.get(session['user_id'])
    matches = User.query.filter_by(university=user.university, city=user.city, interests=user.interests).all()
    return render_template('match.html', matches=matches)

@app.route('/chat/<int:match_id>', methods=['GET', 'POST'])
def chat(match_id):
    form = ChatForm()
    match = User.query.get(match_id)
    if request.method == 'POST' and form.validate():
        new_message = Chat(sender_id=session['user_id'], receiver_id=match_id, message=form.message.data)
        db.session.add(new_message)
        db.session.commit()
        flash('Message sent!', 'success')
    # Fetch chat history
    user_id = session['user_id']
    chat_history = Chat.query.filter(
        ((Chat.sender_id == user_id) & (Chat.receiver_id == match_id)) | 
        ((Chat.sender_id == match_id) & (Chat.receiver_id == user_id))
    ).order_by(Chat.timestamp).all()
    return render_template('chat.html', form=form, match=match, chat_history=chat_history)

@app.route('/report/<int:match_id>', methods=['GET', 'POST'])
def report(match_id):
    form = ReportForm()
    if form.validate_on_submit():
        new_report = Report(user_id=session['user_id'], reported_user_id=match_id, reason=form.reason.data)
        db.session.add(new_report)
        db.session.commit()
        flash('Report submitted!', 'success')
    return render_template('report.html', form=form)

@app.route('/dashboard')
def dashboard():
    # Add your logic here if needed
    # For example, you might fetch some data from a database or perform some calculations
    # Once you have the data or any other logic, pass it to the template
    # For now, let's assume we don't need any specific data
    
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
