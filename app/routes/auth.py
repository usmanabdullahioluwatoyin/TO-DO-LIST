from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.helpers.model import User
from app import db
from app.forms.auth_forms import SigninForm, SignupForm
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email Already Registered', "error")
            return redirect(url_for('auth.signup'))

        hashed_password = generate_password_hash(form.password.data)

        # ✅ THE TRY BLOCK MUST BE INDENTED HERE (Inside the if)
        try:
            new_user = User(
                username=form.username.data,
                email=form.email.data,
                password=hashed_password
            )
        
            db.session.add(new_user)
            db.session.commit()
            flash("Account Created Successfully", "success")
            return redirect(url_for('auth.signin'))

        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            flash("Server Error", "error")

    # This runs only if it's a GET request or validation failed
    return render_template('auth.html', modal='Signup', form=form)
@auth_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()

    if current_user.is_authenticated:
        flash('Already logged in', 'info')
        return redirect(url_for('tasks.user_dashboard'))
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
    
        # 1. Check if user exists AND password matches
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)

            try:
                
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                current_app.logger.exception(e)
                flash('Server Error, Please try again', 'error')
                return redirect(url_for('auth.signin'))

            flash('Login Successful', 'success')

            # 2. Handle the 'next' page redirect safely
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            return redirect(url_for('tasks.user_dashboard'))

        # 3. IF LOGIN FAILS: Flash the error here
        else:
            flash('Invalid email or password', 'error')

    # Render the template if it's a GET request or validation failed
    return render_template('auth.html', modal='Signin', form=form)
@auth_bp.route('/confirmation')
@login_required
def confirmation():
    return render_template('auth.html', modal='Signout', referrer=request.referrer)

@auth_bp.route('/signout')
@login_required
def signout():
    user = User.query.get(current_user.id)

    if user:
        try:
            user.login_status = False
            db.session.commit()
            logout_user()
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)

            flash('Server Error', 'error')

        flash('Logout Successful', 'success')

        return redirect(url_for('tasks.user_dashboard'))

