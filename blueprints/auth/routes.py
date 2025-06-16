from flask import Blueprint, render_template, redirect, url_for, flash, session, request, make_response
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from urllib.parse import urlparse
from app import db, bcrypt, mail
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SelectField, BooleanField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from models.models import User
from flask_mail import Message, Mail
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app

auth = Blueprint('auth', __name__, template_folder='../templates')

# Security decorator to prevent logged-in users from accessing auth pages
def anonymous_required(f):
    """Decorator to redirect logged-in users away from auth pages"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash('You are already logged in.', 'info')
            return redirect(url_for('quiz.quiz_home'))
        return f(*args, **kwargs)
    return decorated_function

def add_no_cache_headers(response):
    """Add headers to prevent page caching - stops back button access"""
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    response.headers['Last-Modified'] = '0'
    return response

# Define the Register Form
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        InputRequired(message='Username is required'), 
        Length(min=4, max=100, message='Username must be between 4 and 100 characters')
    ])
    email = EmailField('Email address', validators=[
        InputRequired(message='Email is required'), 
        Email(message='Invalid email address')
    ])
    password = PasswordField('Password', validators=[
        InputRequired(message='Password is required'), 
        Length(min=6, max=100, message='Password must be at least 6 characters')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        InputRequired(message='Please confirm your password'), 
        EqualTo('password', message='Passwords must match')
    ])
    role = SelectField('Role', choices=[('user', 'User'), ('admin', 'Admin')], validators=[
        InputRequired(message='Please select a role')
    ])

# Define the Login Form
class LoginForm(FlaskForm):
    email = EmailField('Email address', validators=[
        InputRequired(message='Email is required'), 
        Email(message='Invalid email address')
    ])
    password = PasswordField('Password', validators=[
        InputRequired(message='Password is required')
    ])
    remember_me = BooleanField('Remember Me')

# Forgot Password Form
class ForgotPasswordForm(FlaskForm):
    email = EmailField('Email address', validators=[
        InputRequired(message='Email is required'), 
        Email(message='Invalid email address')
    ])

# Reset Password Form
class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[
        InputRequired(message='Password is required'), 
        Length(min=6, max=100, message='Password must be at least 6 characters')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        InputRequired(message='Please confirm your password'), 
        EqualTo('password', message='Passwords must match')
    ])

@auth.route('/login', methods=['GET', 'POST'])
@anonymous_required
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=form.remember_me.data)
            
            # Get the next page from URL parameters
            next_page = request.args.get('next')
            
            # Validate next_page to prevent open redirect attacks
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('quiz.quiz_home')
            
            session.permanent = True
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(next_page)
        else:
            flash('Invalid email or password. Please try again.', 'danger')
    
    # Render template with no-cache headers
    response = make_response(render_template('login.html', form=form))
    return add_no_cache_headers(response)

@auth.route('/register', methods=['GET', 'POST'])
@anonymous_required
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.lower().strip()
        password = form.password.data
        role = form.role.data

        # Check if user already exists
        existing_user = User.query.filter(
            (User.email == email) | (User.username == username)
        ).first()
        
        if existing_user:
            if existing_user.email == email:
                flash('Email address already registered. Please use a different email.', 'danger')
            else:
                flash('Username already taken. Please choose a different username.', 'danger')
            response = make_response(render_template('register.html', form=form))
            return add_no_cache_headers(response)

        if role not in ['user', 'admin']:
            flash('Invalid role selected', 'danger')
            response = make_response(render_template('register.html', form=form))
            return add_no_cache_headers(response)
        
        # Hash password and create new user
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password, role=role)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating your account. Please try again.', 'danger')
            current_app.logger.error(f'Registration error: {str(e)}')

    # Render template with no-cache headers
    response = make_response(render_template('register.html', form=form))
    return add_no_cache_headers(response)

@auth.route('/forgot_password', methods=['GET', 'POST'])
@anonymous_required
def forgot_password():
    form = ForgotPasswordForm()
    
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        user = User.query.filter_by(email=email).first()
        
        flash('If an account with that email exists, a password reset link has been sent.', 'info')
        
        if user:
            try:
                token = user.get_reset_token()
                reset_url = url_for('auth.reset_password', token=token, _external=True)

                msg = Message(
                    'QuizMaster - Password Reset Request',
                    sender='noreply@quizmaster.com',
                    recipients=[user.email]
                )
                msg.body = f'''Hello {user.username},

A password reset was requested for your QuizMaster account.

Click the link below to reset your password:
{reset_url}

This link will expire in 1 hour for security reasons.

If you did not request this reset, please ignore this email.

Best regards,
The QuizMaster Team
'''
                mail.send(msg)
                current_app.logger.info(f'Password reset email sent to {email}')
                
            except Exception as e:
                current_app.logger.error(f'Failed to send reset email: {str(e)}')
        
        return redirect(url_for('auth.login'))

    # Render template with no-cache headers
    response = make_response(render_template('forgot_password.html', form=form))
    return add_no_cache_headers(response)

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
@anonymous_required
def reset_password(token):
    user = User.verify_reset_token(token)
    
    if user is None:
        flash('Invalid or expired reset link. Please request a new password reset.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    form = ResetPasswordForm()
    
    if form.validate_on_submit():
        try:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            
            flash('Your password has been updated successfully! You can now log in.', 'success')
            current_app.logger.info(f'Password reset successful for user: {user.email}')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating your password. Please try again.', 'danger')
            current_app.logger.error(f'Password reset error: {str(e)}')

    # Render template with no-cache headers
    response = make_response(render_template('reset_password.html', form=form, token=token))
    return add_no_cache_headers(response)

@auth.route('/logout')
@login_required
def logout():
    # Log the logout action
    if current_user.is_authenticated:
        username = current_user.username
        current_app.logger.info(f'User {username} logged out')
    
    # Clear the user session
    logout_user()
    
    # Clear all session data
    session.clear()
    
    # Create response that redirects to home page
    response = make_response(redirect(url_for('main.home')))
    
    # Strong no-cache headers to prevent back button access
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0, private'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    response.headers['Last-Modified'] = '0'
    
    # Clear authentication cookies completely
    response.set_cookie('session', '', expires=0, path='/')
    response.set_cookie('remember_token', '', expires=0, path='/')
    
    flash('You have been logged out successfully.', 'info')
    return response
