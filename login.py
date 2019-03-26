from flask import Flask, render_template,url_for,request,session,redirect
from flask_pymongo import PyMongo
import bcrypt
import NGO
import json

app = Flask(__name__)

app.config['MONGO_DBNAME']='mongologinexample'
app.config['MONGO_URI']='mongodb://localhost:27017/mongologinexample'
#app.config['MONGO_URI']='mongodb+srv://arpitkubadia:arpit%40123@cluster0-rpcm0.mongodb.net/admin'


mongo=PyMongo(app)

@app.route('/')
def index():
	if 'username' in session:
		users=mongo.db.users
		details=users.find_one({'name':session['username']})
		if details['type']=='NGO':
			return redirect(url_for('ngo_page'))
		elif details['type']=='Volunteer':
			return redirect(url_for('volunteer_page'))
	return render_template('index.html')


@app.route('/login',methods=['POST'])
def login():
	users=mongo.db.users
	login_user=users.find_one({'name': request.form['username']})

	if login_user:
		if bcrypt.hashpw(request.form['pass'].encode('utf-8'),login_user['password']) == login_user['password']:
			session['username']	= request.form['username']

			if login_user['type']=='NGO':
				return redirect(url_for('ngo_page'))
			elif login_user['type']=='Volunteer':
				return redirect(url_for('volunteer_page'))

			#return redirect(url_for('index'))

		return 'Invalid username/password'

	return 'Invalid username/password'

			
@app.route('/NGO',methods=['POST','GET'])
def ngo_page():
	jobs=mongo.db.jobs
	ngo_jobs=jobs.find({"owner":session['username']})
	all_jobs=[]
	for job in ngo_jobs:
		all_jobs.append(job)
	return render_template('ngo.html',name=session['username'],all_jobs=all_jobs)


@app.route('/Volunteer')
def volunteer_page():

	return render_template('volunteer.html',name=session['username'])


@app.route('/new_job',methods=['POST'])
def new_job():
	jobs=mongo.db.jobs
	existing_job=jobs.find_one({'title':request.form['title']})
	if existing_job is None:
		title=request.form['title']
		owner=session['username']
		description=request.form['description']
		location=request.form['location']
		duration=request.form['duration']

		jobs.insert({'title':title,'owner':owner,'description':description,'location':location,'duration':duration,'applications':[]})
		return 'Job has been created'
	else:	
		return 'Job Exists'



@app.route('/register',methods=['POST','GET'])
def register():
	if request.method=='POST':
		users=mongo.db.users
		existing_user=users.find_one({'name':request.form['username']})

		if existing_user is None:
			hashpass=bcrypt.hashpw(request.form['pass'].encode('utf-8'),bcrypt.gensalt())
			users.insert({'name':request.form['username'],'password':hashpass,'type':request.form['category']})
			session['username']=request.form['username']

			if request.form['category']=='NGO':
				return redirect(url_for('ngo_page'))
			else:
				return redirect(url_for('volunteer_page'))

		else:
			return 'Username already exists!'

	else:
		return render_template('register.html')


if __name__ == '__main__':
	app.secret_key='mysecret'
	app.run(debug=True)

