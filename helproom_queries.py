import MySQLdb
from helproom_dsn import DSN
import dbconn2
import os

# Searches user table for an already existing user given the login_nm
def search_users(login_nm):
	DSN['db'] = 'helproom_db'
	conn = dbconn2.connect(DSN)
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT username FROM user WHERE username=%s;',(login_nm,))
	return curs.fetchall()

#Returns all CS courses in the database
def get_courses():
	DSN['db'] = 'helproom_db'
	conn = dbconn2.connect(DSN)
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT cid,name FROM course;')
	all_course = curs.fetchall()
	return all_course

#returns all questions related to given course id
def get_course_questions(cid):
	DSN['db'] = 'helproom_db'
	conn = dbconn2.connect(DSN)
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT * from question where courseid= %s;', (cid,))
	return curs.fetchall()

#returns all questions posted by the user currently logged in
def get_user_questions(username):
	DSN['db'] = 'helproom_db'
	conn = dbconn2.connect(DSN)
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT * from question where user_id= %s;', (username,))
	return curs.fetchall()

#returns all tags in the database
def get_all_tags():
	DSN['db'] = 'helproom_db'
	conn = dbconn2.connect(DSN)
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT * FROM tag;')
	all_tags = curs.fetchall()
	return all_tags

#Adds a question to the database after user posts with all required fields
def insert_question(course_id, email, text_input, tag):
	DSN['db'] = 'helproom_db'
	conn = dbconn2.connect(DSN)
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('INSERT into question (qid, vote_count, courseid, user_id, text_input, tag) values(%s, %s, %s, %s, %s, %s);', ('cid', '0', course_id, email, text_input, tag))

#returns all of the responses for a specific question
#given the question id
def get_question_responses(question_id):
	DSN['db'] = 'helproom_db'
	conn = dbconn2.connect(DSN)
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT * FROM response where qid = %s;', (question_id,))
	all_responses = curs.fetchall()
	return all_responses

#returns all the informaiton associated with specific question
#takes question id as parameter
def get_question_info(question_id):
	DSN['db'] = 'helproom_db'
	conn = dbconn2.connect(DSN)
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT * FROM question where qid = %s;', (question_id,))
	return curs.fetchall()

#gives all of the responses associated with a specific course
def get_course_responses(cid):
	DSN['db'] = 'helproom_db'
	conn = dbconn2.connect(DSN)
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT * from response where course_num=%s;',(cid,))
	return curs.fetchall()

#Adds a response to the database after user posts with all required fields
def insert_response(qid, email, text_input, tag, course_id):
	DSN['db'] = 'helproom_db'
	conn = dbconn2.connect(DSN)
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute ('INSERT into response (response_id, qid, vote_count, user_id, text_input, tag, course_num) values (%s, %s, %s, %s, %s, %s, %s);', ('rid', qid, '0', email, text_input, tag, course_id));
	return curs.fetchall()

#adds a new user to the database
def add_user(username, status):
	DSN['db'] = 'helproom_db'
	conn = dbconn2.connect(DSN)
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('INSERT into user (username, status) values(%s, %s);', (username, status))

#returns all of the responses in the database
def get_all_response():
	DSN['db'] = 'helproom_db'
	conn = dbconn2.connect(DSN)
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT * from response;')
	return curs.fetchall()

#returns all of the questions in the database associated with a specific tag
def get_all_tag_questions(tag):
	DSN['db'] = 'helproom_db'
	conn = dbconn2.connect(DSN)
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT * FROM question where tag = %s;', (tag,))
	return curs.fetchall()

#checks to see if a user has voted on a question
def check_voted(user, qid):
	DSN['db'] = 'helproom_db'
	conn = dbconn2.connect(DSN)
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT * FROM vote where user_id= %s and comment_id = %s;', (user, qid))
	return curs.fetchall()

#returns the current vote count for a specific question given the question id
def get_vote_count(qid):
	DSN['db'] = 'helproom_db'
	conn = dbconn2.connect(DSN)
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT vote_count FROM question where qid= %s;', (qid,))
	return curs.fetchall()

#adds to database of actions whether a user has voted on a question
def update_vote(user,qid):
	DSN['db'] = 'helproom_db'
	conn = dbconn2.connect(DSN)
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('INSERT into vote(user_id, comment_type, comment_id) values (%s,%s,%s);', (user, 'question', qid))
	return curs.fetchall()

#updates the votecount number after user has voted
def update_question(qid):
	DSN['db'] = 'helproom_db'
	conn = dbconn2.connect(DSN)
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('UPDATE question set vote_count = vote_count+1 where qid=%s;', (qid, ))
	return curs.fetchall()

#returns course description for a specific course
def get_course_info(cid):
	DSN['db'] = 'helproom_db'
	conn = dbconn2.connect(DSN)
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT name FROM course where cid= %s;', (cid,))
	return curs.fetchall()
