import bcrypt
from flask import Blueprint, flash, render_template
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from werkzeug.security import generate_password_hash, check_password_hash



user = Blueprint('user', __name__, url_prefix='/user', template_folder='templates')

@user.route('/profile', methods=['GET'])
def profile():
    flash("Welcome to your profile!", "success")  # Example flash message
    return render_template('profile.html')


@user.route('/settings', methods=['GET'])
@login_required
def settings():
    flash("View your settings!", "success")  # Example flash message
    return render_template('settings.html')

@user.route('/update_settings', methods=['POST'])
@login_required
def update_settings():
    new_email = request.form.get('email')
    new_password = request.form.get('password')

    if new_email and new_password:
        # Update user info (assuming `User` model exists)
        current_user.email = new_email
        current_user.set_password(generate_password_hash(new_password))  # Hash password
        db.session.commit()  # Save changes
        flash("Settings updated successfully!", "success")
    else:
        flash("Please fill in all fields.", "danger")

    return redirect(url_for('user.settings'))

 