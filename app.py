#Eva Stern-Rodriguez and Emily Schron

import MySQLdb
from helproom_dsn import DSN
import dbconn2
import helproom_queries
import os
from flask import Flask, render_template, url_for, request, redirect, url_for, make_response, flash, escape, json, jsonify
from flask import (session, send_from_directory)
from werkzeug import secure_filename
# new
from flask_cas import CAS
import sys
import imghdr
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '/user_photo/'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key='owwbbitf'


#checks if valid file
def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Login page, either login or sign up actions
@app.route('/', methods=['POST','GET'])
def login():
	if request.method == 'POST':
		if request.form['submit'] == 'Login':
			email = request.form['email']
			if email=="":
				flash("Please give a valid input")
			else: #check db for email (user)
				user_info = helproom_queries.search_users(email)
				print user_info
				if user_info==():
					flash("Username not found in database, please sign up.")
				else:
					session['username'] = request.form['email']
					#return redirect(url_for('select_class',email=session['username']))
					return redirect(url_for('select_class'))
		if request.form['submit'] == 'Sign Up!':
			return redirect(url_for('signup'))
	return render_template('login.html')

#File upload and creates new user with form responses. A few error handling checks here
@app.route('/signup/', methods=['POST','GET'])
def signup():
	if request.method == 'POST':
		if request.form['submit'] == "Sign Up!":
			email = request.form['email']
			status = request.form["status"]
			print "THIS STATUS" + status
			user_info = helproom_queries.search_users(email)
			if email=="" or status == "":
				flash("Please give a valid input")
			else:
				if user_info == ():
					file = request.files['file']
					print file
					# check if the post request has the file part
					if 'file' not in request.files:
						flash('No file part')
						return redirect(url_for('signup'))
					# if user does not select file, browser also
					# submit a empty part without filename
					if file.filename == '':
						flash('No selected file')
						return redirect(url_for('signup'))
					if file and allowed_file(file.filename):
						file.filename = request.form['email']+'.jpg'
						file.save("static/user_photo/"+secure_filename(file.filename))
						helproom_queries.add_user(email, status)
						session['username'] = request.form['email']
						return redirect(url_for('select_class'))
				else:
					flash("Username already in database, please log in.")
					return redirect(url_for('login'))
	return render_template('signup.html')

#Ends user's session, logs out
@app.route('/logout/')
def logout():
   # remove the username from the session if it is there
   flash("Thank you for using HelpRoom!")
   session.pop('username', None)
   return render_template('logout.html')

#Displays all CS courses from the database. Allows user to select a course.
@app.route('/class/', methods=['POST','GET'])
def select_class():
	all_courses= helproom_queries.get_courses()
	render = render_template('class.html', courses=all_courses)
	if request.method == 'POST':
		course_num = request.form['course']
		return redirect(url_for('course', cid=course_num))
	return render

#Displays user's profile photo and all questions user has ever posted.
#Able to respond to these questions here.
@app.route('/profile/', methods=['POST','GET'])
def profile():
	#get all questions for a user.
	all_user_qs = helproom_queries.get_user_questions(session['username'])
	all_resp = helproom_queries.get_all_response()
	all_tags= helproom_queries.get_all_tags()
	render = render_template('profile.html',questions=all_user_qs, tags = all_tags, responses= all_resp, user = session['username'])
	if request.method == 'POST':
		if request.form['submit'] == 'Post Response':
			r_text = request.form['response_text']
			tag= request.form['resp_tag']
			qid = request.form['qid']
			cid = request.form['cid']
			print "THIS IS THE CID: " + cid
			helproom_queries.insert_response(qid, session['username'], r_text, tag, cid)
			flash(session['username'] + " your response has been posted")
			return redirect(url_for('profile'))
	return render

#Displays all questions for a specific course (and each question's responses)
#Allows users to post question for this course and respond to existing questions
@app.route('/course/<cid>', methods=['POST','GET'])
def course(cid):
	all_questions= helproom_queries.get_course_questions(cid)
	all_tags= helproom_queries.get_all_tags()
	all_responses=helproom_queries.get_course_responses(cid)
	render = render_template('course.html', course_id = cid, tags = all_tags, questions=all_questions, responses= all_responses)
	if request.method == 'POST':
		if request.form['submit'] == 'Post Question':
			tag= request.form['menu_tag']
			q_text= request.form['post_question']
			helproom_queries.insert_question(cid, session['username'], q_text, tag)
			flash(session['username'] + " your question has been posted")
			return redirect(url_for('course', cid=cid))
		else:
			if request.form['submit'] == 'Post Response':
				r_text = request.form['response_text']
				tag= request.form['resp_tag']
				qid = request.form['qid']
				helproom_queries.insert_response(qid, session['username'], r_text, tag, cid)
				flash(session['username'] + " your response has been posted")
				return redirect(url_for('course', cid=cid))
	return render

#Displays all questions associated with a tag.
#Allows users to respond to tag questions
@app.route('/search/', methods=['POST','GET'])
def search():
	all_tags= helproom_queries.get_all_tags()
	render = render_template('search.html', tags = all_tags)
	if request.method == 'POST':
		if request.form['submit'] == 'Search':
			tag= request.form['menu_tag']
			tag_questions= helproom_queries.get_all_tag_questions(tag)
			#get all responses and find responses that correspond with QID
			resp= helproom_queries.get_all_response()
			return render_template('search.html',questions=tag_questions, user = session['username'], tags = all_tags, responses = resp)
		else:
			if request.form['submit'] == 'Post Response':
				r_text = request.form['response_text']
				tag= request.form['resp_tag']
				qid = request.form['qid']
				cid = request.form['cid']
				resp= helproom_queries.get_all_response()
				helproom_queries.insert_response(qid, session['username'], r_text, tag, cid)
				flash(session['username'] + " your response has been posted")
				return render_template('search.html',user = session['username'], tags = all_tags,responses= resp)
	return render

#Checks if user has already voted on a question
#If they have not, update vote count and add to user action table
@app.route('/like/<cid>/<qid>', methods=['POST'])
def like(cid, qid):
	qid = qid
	user_info= session['username']
	voted= helproom_queries.check_voted(user_info, qid)
	v_count= helproom_queries.get_vote_count(qid)
	vote=v_count[0]['vote_count']
	if voted != ():
		return redirect(url_for('course', cid=cid))
	else:
		helproom_queries.update_vote(user_info,qid)
		helproom_queries.update_question(qid)
		vote = vote +1
		return jsonify(question=qid, vote_count=vote)


# ================================================================
# This starts the ball rolling, *if* the script is run as a script,
# rather than just being imported.

if __name__ == '__main__':
	app.debug = True
	port = os.getuid()
	print('Running on port '+str(port))
	app.run('0.0.0.0',port)
