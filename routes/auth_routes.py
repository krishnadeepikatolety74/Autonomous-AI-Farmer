from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user_model import UserModel
from utils.validators import validate_email, validate_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Please enter email and password.', 'error')
            return render_template('signin.html')

        user = UserModel.find_by_email(email)
        if user and UserModel.verify_password(user['password_hash'], password):
            session.clear()
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            return redirect(url_for('dashboard.overview'))
        else:
            flash('Invalid email or password.', 'error')
            return render_template('signin.html')

    return render_template('signin.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        # Validate inputs
        if not name or not email or not password:
            flash('All fields are required.', 'error')
            return render_template('signup.html')

        if not validate_email(email):
            flash('Please enter a valid email address.', 'error')
            return render_template('signup.html')

        if not validate_password(password):
            flash('Password must be at least 6 characters.', 'error')
            return render_template('signup.html')

        if password != confirm:
            flash('Passwords do not match.', 'error')
            return render_template('signup.html')

        # Check if email already exists
        if UserModel.find_by_email(email):
            flash('An account with this email already exists.', 'error')
            return render_template('signup.html')

        # Create user
        user_id = UserModel.create(name, email, password)
        if user_id:
            session.clear()
            session['user_id'] = user_id
            session['user_name'] = name
            return redirect(url_for('dashboard.overview'))
        else:
            flash('Registration failed. Please try again.', 'error')
            return render_template('signup.html')

    return render_template('signup.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.signin'))
