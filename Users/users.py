from flask import Flask, render_template,jsonify,request,abort,redirect,url_for 
import requests
from flask_cors import CORS
import json
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'cloud'

mysql = MySQL(app)
CORS(app)

ride_no = 1001
users = {}
rides = {}
password_check = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

method = ["GET", "PUT", "POST", "HEAD", "DELETE"]

@app.route('/api/v1/users', methods = method)	
def add_user():
	temp2 = {"type":5, 'items':['call number update']}
	resp2 = requests.post('http://34.231.57.195:80/api/v1/db/write', json = temp2)
	d2 = resp2.json()['ans']
	if(d2 == 400):
		return jsonify(['count prob'])

	if(request.method == 'PUT'):
		details = request.get_json()
		username = details["username"]
		password = details["password"]

		temp = {"type":2, 'items':[]}
		resp = requests.post('http://34.231.57.195:80/api/v1/db/write', json = temp)

		print(username, password)
		if(len(password) == 40):
			check = set(password)
			for i in check:
				if i not in password_check:
					abort(400)
			temp = {"type":1, 'items':[username,password]}
			resp = requests.post('http://34.231.57.195:80/api/v1/db/write', json = temp)
			d = resp.json()
			if(d['ret'] == 400):
				abort(400)
			else:
				temp = {"type":1, 'items':[username,password]}
				resp = requests.post('http://ccassignment-1982451452.us-east-1.elb.amazonaws.com/api/v1/db/write', headers={'Origin':'http://52.21.234.168'}, json = temp)
				d = resp.json()
				if(d['ret'] == 400):
					return jsonify(['cros']), 400
				return jsonify({}),201
		else:
			abort(400)

	if(request.method == 'GET'):
		
		temp = {"type":2, 'items':[]}
		resp = requests.post('http://34.231.57.195:80/api/v1/db/read', json = temp)
		d = resp.json()['ans']
		if(len(d) == 0):
			abort(204)
		else:
			return jsonify(d),200
	else:
		abort(405)

@app.route('/api/v1/users/<username>', methods = method)
def delete_user(username):
	temp2 = {"type":5, 'items':['call number update']}
	resp2 = requests.post('http://34.231.57.195:80/api/v1/db/write', json = temp2)
	d2 = resp2.json()['ans']
	if(d2 == 400):
		return jsonify(['count prob'])

	if(request.method == "DELETE"):
		
		temp = {'type':1, 'name':username}
		user_list = requests.post('http://34.231.57.195:80/api/v1/db/read', json = temp)
		ans = user_list.json()['ans']

		if(ans == 'no'):
			abort(400)

		temp = {"type":2, 'items':[username]}
		resp = requests.post('http://34.231.57.195:80/api/v1/db/write', json = temp)
		d = resp.json()

		if(d['ret'] == 400):
			abort(400)
		else:
			temp = {"type":2, 'items':[username]}
			resp = requests.post('http://ccassignment-1982451452.us-east-1.elb.amazonaws.com/api/v1/db/write', headers={'Origin':'http://52.21.234.168'}, json = temp)
			d = resp.json()
			if(d['ret'] == 400):
				return jsonify(['cros']), 400
			return jsonify({}), 200
	else:
		abort(405)
	

@app.route('/api/v1/db/clear', methods=["POST"])
def clear_db():
	if(request.method == 'POST'):
		temp = {"type":3, 'items':[]}
		resp = requests.post('http://34.231.57.195:80/api/v1/db/write', json = temp)
		d = resp.json()['ans']
		if(d == 400):
			abort(400)
		else:
			return jsonify({}),200
	else:
		abort(405)


@app.route('/api/v1/_count', methods=["GET"])
def http_count():
	if(request.method == 'GET'):
		temp = {"type":3, 'items':[]}
		resp = requests.post('http://34.231.57.195:80/api/v1/db/read', json = temp)
		d = resp.json()['ans']
		if(len(d) == 0):
			abort(204)
		else:
			return jsonify(d),200
	else:
		abort(405)

@app.route('/api/v1/_count', methods=["DELETE"])
def reset_count():
	temp2 = {"type":5, 'items':['call number update']}
	resp2 = requests.post('http://34.231.57.195:80/api/v1/db/write', json = temp2)
	d2 = resp2.json()['ans']
	if(d2 == 400):
		return jsonify(['count prob'])

	if(request.method == 'DELETE'):
		temp = {"type":4, 'items':[]}
		resp = requests.post('http://34.231.57.195:80/api/v1/db/write', json = temp)
		d = resp.json()['ans']
		if(d == 400):
			abort(400)
		else:
			return jsonify({}), 200
	else:
		abort(405)

@app.route('/api/v1/db/read', methods = ["POST"])
def read_db():
	if(request.method == 'POST'):
		l = request.get_json()
		if(l["type"] == 1):
			u_handle = mysql.connection.cursor()
			u_handle.execute("SELECT username FROM users WHERE username = %s", (l['name'],))
			ret = u_handle.fetchall()
			mysql.connection.commit()  
			u_handle.close()
			print(ret)
			if(len(ret) == 0):
				return {'ans':'no'}
			else:
				return {'ans':'yes'}

		if(l["type"] == 2):
			u_handle = mysql.connection.cursor()
			u_handle.execute("SELECT username FROM users")
			ret = u_handle.fetchall()
	
			tl = []
			for item in ret:
				tl.append(item[0])
			mysql.connection.commit()  
			u_handle.close()
			return {'ans': tl}

		if(l["type"] == 3):
			u_handle = mysql.connection.cursor()
			u_handle.execute("SELECT req FROM calls")
			ret = u_handle.fetchall()
	
			tl = []
			for item in ret:
				tl.append(item[0])
				break

			mysql.connection.commit()  
			u_handle.close()
			return {'ans': tl}
		

@app.route('/api/v1/db/write', methods = ["POST"])
def write_db():
	if(request.method == 'POST'):
		l = request.get_json()

		if(l["type"] == 1):
			u_handle = mysql.connection.cursor()
			try:
				u_handle.execute("INSERT INTO users values(%s, %s)",(l['items'][0], l['items'][1]))
			except:
				return {'ret':400}
			mysql.connection.commit()  
			u_handle.close()
			return {'ret':200}

		if(l["type"] == 2):
			u_handle = mysql.connection.cursor()
			try:
				u_handle.execute("DELETE FROM users WHERE username = %s",(l['items'][0],))
			except Exception as e:
				print(e)
				return {'ret':400}
			mysql.connection.commit()  
			u_handle.close()
			return {'ret':200}

		if(l["type"] == 3):
			u_handle = mysql.connection.cursor()
			try:
				u_handle.execute("DELETE FROM users")
				u_handle.execute("DELETE FROM riders_list")
				u_handle.execute("DELETE FROM rides")
			except Exception as e:
				print(e)
				return {'ans':400}
			mysql.connection.commit()  
			u_handle.close()
			return {'ans':200}

		if(l["type"] == 4):
			u_handle = mysql.connection.cursor()
			try:
				u_handle.execute("UPDATE calls SET req = 0")
			except Exception as e:
				print(e)
				return {'ans':400}
			mysql.connection.commit()  
			u_handle.close()
			return {'ans': 200}

		if(l["type"] == 5):
			u_handle = mysql.connection.cursor()
			try:
				u_handle.execute("UPDATE calls SET req = req + 1")
			except Exception as e:
				print(e)
				return {'ans':400}
			mysql.connection.commit()  
			u_handle.close()
			return {'ans': 200}
	else:
		return {'ret':400}


if __name__ == '__main__':	
	app.debug=True
	app.run(host='0.0.0.0', port = 80)

