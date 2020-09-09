from flask import Blueprint, redirect, url_for,render_template, flash, session
from flask_login import login_user, current_user, logout_user, login_required
from mywords.users.forms import LoginForm,RegisterForm
from werkzeug.security import generate_password_hash,check_password_hash
from mywords import db,app
from mywords.models import User
from datetime import date


users = Blueprint("users",__name__)

@users.route("/login", methods=['GET', 'POST'])
def login():
	session["page"] = "login"	
	form = LoginForm()

	if form.validate_on_submit():

		if form.register.data:
			return redirect(url_for('register'))			
		
		if form.submit.data:
			userdata = User.query.filter_by(email=form.email.data).first()	
			if userdata == None:
				flash("Email address not found! Please register to use the application.")
				return render_template("login.html",form=form)
			login_user(userdata)
			if check_password_hash(userdata.password_hash,form.password.data) and userdata.email == form.email.data:
				flash("Login Successful!!")
				session["wordofday"]=""
				return redirect(url_for('users.user'))
	if form.email.errors:
		for error in form.email.errors:
			flash(error)
	return render_template("login.html",form=form)

@users.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	session["page"] = "register"
	if form.validate_on_submit():
		email = User.query.filter_by(email=form.email.data).first()
		if email:
			flash("Email already registered please login!")
			return redirect(url_for('users.login'))
		if len(form.password.data) < 6:
			flash("password length should be greater than 6 characters!")
			return render_template("register.html", form=form)
		user = User(email=form.email.data,first_name=form.first_name.data,last_name=form.last_name.data,password=form.password.data)
		db.session.add(user)
		db.session.commit()
		flash("Thanks for registering!! You can login now.")
		return redirect(url_for('users.login'))
	if form.password.errors:
		flash("password not matching!")
	if form.email.errors:
		for error in form.email.errors:
			flash(error)
		for error in form.password.errors:
			flash(error)

	return render_template("register.html", form=form)

@users.route('/Welcome')
@login_required
def user():
	#print(url_for("\static\mywordslist.txt"))
	test = User.query.filter_by(email="test@test.com").first()
	#print(test.id)
	with app.open_resource("static/mywordslist.txt","r") as filedata:	
		filedata=filedata.readlines()
		#print(filedata[0])
		main_date=filedata[0].split(",")
		main_date=date(int(main_date[0]),int(main_date[1]),int(main_date[2]))	
		today = date.today()
		no_of_days = (today-main_date).days
		word_of_day =filedata[no_of_days+1] 	
		#print(no_of_days ,word_of_day )
	session["page"] = "user"

	return render_template("user.html", word_of_day=word_of_day)

@users.route('/logout')
def logout():
	session.clear()
	logout_user()
	flash("Logged out successfully!!")
	return redirect(url_for("users.login"))

@users.route('/about')
def about():
	session["page"] = "about"
	return render_template("about.html")

@users.route("/")
def main_page():
	session["page"] = "login"
	return redirect(url_for("users.login"))