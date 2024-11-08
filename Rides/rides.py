from flask import Flask, render_template,jsonify,request,abort,redirect,url_for 
import requests
from flask_cors import CORS
import json
from flask_mysqldb import MySQL
from datetime import datetime
import csv

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'cloud'

mysql=MySQL(app)
CORS(app)

ride_no = 1001
users = {}
rides = {}
password_check = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

method = ["GET", "PUT", "POST", "HEAD", "DELETE"]

@app.route('/api/v1/rides', methods = method)
def create_ride():
	temp2 = {"type":8, 'items':['call number update']}
	resp2 = requests.post('http://127.0.0.1:80/api/v1/db/write', json = temp2)
	d2 = resp2.json()['ans']
	if(d2 == 400):
		return jsonify(['count prob'])

	if(request.method == 'POST'):
		details = request.get_json()
		username = details["created_by"]

		user_list = requests.get('http://ccassignment-1982451452.us-east-1.elb.amazonaws.com/api/v1/users', headers={'Origin':'http://3.231.123.96'})
		ans = user_list.text
		if(username not in ans):
			return jsonify({}), 400

		stamp = details["timestamp"]
		s = stamp.split(':')
		n1 = s[0].split('-')
		n2 = s[1].split('-')
		n = n1[2]+'-'+n1[1]+'-'+n1[0]+':'+n2[2]+'-'+n2[1]+'-'+n2[0]

		source = str(details["source"])
		destination = str(details["destination"])

		if(len(source) == 0 or len(destination) == 0 or source == destination):
			return jsonify(['s and d prob']), 400

		with open('AreaNameEnum.csv', 'r') as file:
		    reader = csv.reader(file)
		    check_l = []
		    check_d = {}
		    for row in reader:
		        check_l.append(row[0])
		        check_d[row[0]] = row[1]

		if(source not in check_l or destination not in check_l):
			return jsonify(['csv']), 400

		source = int(details["source"])
		destination = int(details["destination"])

		t1 = (username, n, source, destination)
		temp = {'type':3, 'items':t1}
		resp = requests.post('http://127.0.0.1:80/api/v1/db/write', json = temp)

		if(resp.json()['ret'] == 200):
			return jsonify({}), 201
		else:
			return jsonify({}), 400

	if(request.method == 'GET'):
		source = request.args.get('source')
		destination = request.args.get('destination')

		with open('AreaNameEnum.csv', 'r') as file:
		    reader = csv.reader(file)
		    check_l = []
		    check_d = {}
		    for row in reader:
		        check_l.append(row[0])
		        check_d[row[0]] = row[1]

		if(source not in check_l or destination not in check_l):
			return jsonify({}), 400

		source = int(source)
		destination = int(destination)

		temp = {'type':2, 'items':(source, destination)}
		user_list = requests.post('http://127.0.0.1:80/api/v1/db/read', json = temp)
		ans = user_list.json()['ans']
		if(ans == 'no'):
			return jsonify({}), 204
		else:
			return jsonify(ans), 200
	

@app.route('/api/v1/rides/<rideID>', methods = method)
def ride_details(rideID):
	temp2 = {"type":8, 'items':['call number update']}
	resp2 = requests.post('http://127.0.0.1:80/api/v1/db/write', json = temp2)
	d2 = resp2.json()['ans']
	if(d2 == 400):
		return jsonify(['count prob'])

	if(request.method == "GET"):
		temp = {'type':4, 'name':int(rideID)}
		user_list = requests.post('http://127.0.0.1:80/api/v1/db/read', json = temp)
		ans = user_list.json()['ans']
		if(ans == 'no'):
			return jsonify({}), 204
		else:
			return jsonify(ans), 200
	
	if(request.method == 'POST'):
		details = request.get_json()
		username = details["username"]
		temp = {'type':3, 'name':int(rideID)}
		user_list = requests.post('http://127.0.0.1:80/api/v1/db/read', json = temp)
		ans = user_list.json()['ans']
		if(ans == 'no'):
			return jsonify({}), 400

		temp = {'type':1, 'name':username}
		user_list = requests.post('http://127.0.0.1:80/api/v1/db/read', json = temp)
		ans = user_list.json()['ans']
		if(ans == 'no'):
			return jsonify({}), 400

		t1 = (rideID, username)
		temp = {'type':4, 'items':t1}
		resp = requests.post('http://127.0.0.1:80/api/v1/db/write', json = temp)
		ans = resp.json()['ret']
		if(ans == 400):
			return jsonify({}), 400
		else:
			return jsonify({}), 200

	if(request.method == "DELETE"):
		temp = {'type':3, 'name':int(rideID)}
		user_list = requests.post('http://127.0.0.1:80/api/v1/db/read', json = temp)
		ans = user_list.json()['ans']
		if(ans == 'no'):
			return jsonify({}), 400

		temp = {"type":5, 'items':[rideID]}
		resp = requests.post('http://127.0.0.1:80/api/v1/db/write', json = temp)
		d = resp.json()

		if(d['ret'] == 400):
			return jsonify({}), 400
		else:
			return jsonify({}), 200
		
	else:
		abort(405)
	

@app.route('/api/v1/db/clear', methods=["POST"])
def clear_db():
        if(request.method == 'POST'):
                temp = {"type":6, 'items':[]}
                resp = requests.post('http://127.0.0.1:80/api/v1/db/write', json = temp)
                d = resp.json()['ans']
                if(d == 400):
                        return jsonify({}), 400
                else:
                        return jsonify({}),200
        else:
                abort(405)


@app.route('/api/v1/_count', methods=["GET"])
def http_count():
	if(request.method == 'GET'):
		temp = {"type":5, 'items':[]}
		resp = requests.post('http://127.0.0.1:80/api/v1/db/read', json = temp)
		d = resp.json()['ans']
		if(len(d) == 0):
			abort(204)
		else:
			return jsonify(d),200
	else:
		abort(405)

@app.route('/api/v1/_count', methods=["DELETE"])
def reset_count():
	temp2 = {"type":8, 'items':['call number update']}
	resp2 = requests.post('http://127.0.0.1:80/api/v1/db/write', json = temp2)
	d2 = resp2.json()['ans']
	if(d2 == 400):
		return jsonify(['count prob'])

	if(request.method == 'DELETE'):
		temp = {"type":7, 'items':[]}
		resp = requests.post('http://127.0.0.1:80/api/v1/db/write', json = temp)
		d = resp.json()['ans']
		if(d == 400):
			return jsonify({}), 400
		else:
			return jsonify({}), 200
	else:
		abort(405)

@app.route('/api/v1/rides/count', methods=method)
def ride_count():
	temp2 = {"type":8, 'items':['call number update']}
	resp2 = requests.post('http://127.0.0.1:80/api/v1/db/write', json = temp2)
	d2 = resp2.json()['ans']
	if(d2 == 400):
		return jsonify(['count prob'])

	if(request.method == 'GET'):
		temp = {"type":6, 'items':[]}
		resp = requests.post('http://127.0.0.1:80/api/v1/db/read', json = temp)
		d = resp.json()['ans']
		if(len(d) == 0):
			abort(204)
		else:
			return jsonify(d),200
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
			print(ret)
			if(len(ret) == 0):
				return {'ans':'no'}
			else:
				return {'ans':'yes'}

		if(l["type"] == 2):
			u_handle = mysql.connection.cursor()
			cur_time = datetime.now()
			print(cur_time)
			print(l['items'])
			send = tuple(l["items"])+(cur_time,)
			u_handle.execute("SELECT ride_id, created_by, time_stamp FROM rides WHERE source_loc = %s AND destination_loc = %s AND time_stamp > %s", send)
			ret = u_handle.fetchall()
			print(ret)
			if(len(ret) == 0):
				return {'ans':'no'}

			tl = []
			for item in ret:
				dat = item[2]
				tim = dat.strftime('%d-%m-%Y:%S-%M-%H')
				td = {}
				td['rideId'] = item[0]
				td['username'] = item[1]
				td['timestamp'] = tim
				tl.append(td)
			
			return {'ans': tl}

		if(l["type"] == 3):
			u_handle = mysql.connection.cursor()
			u_handle.execute("SELECT ride_id FROM rides WHERE ride_id = %s", (l['name'],))
			ret = u_handle.fetchall()
			print(ret)
			if(len(ret) == 0):
				return {'ans':'no'}
			else:
				return {'ans':'yes'}

		if(l["type"] == 4):
			u_handle = mysql.connection.cursor()
			u_handle.execute("SELECT * FROM rides WHERE ride_id = %s", (l['name'],))
			ret = u_handle.fetchall()
			if(len(ret) == 0):
				return {'ans':'no'}
			
			u_handle2 = mysql.connection.cursor()
			u_handle2.execute("SELECT username FROM riders_list WHERE ride_id = %s", (l['name'],))
			ret2 = u_handle2.fetchall()

			tl = []
			for i in ret2:
				tl.append(i[0])

			universal = ['rideId', 'created_by', 'users', 'timestamp', 'source', 'destination']

			with open('AreaNameEnum.csv', 'r') as file:
			    reader = csv.reader(file)
			    check_l = []
			    check_d = {}
			    for row in reader:
			        check_l.append(row[0])
			        check_d[row[0]] = row[1]

			td = {}
			td[universal[0]] = ret[0][0]
			td[universal[1]] = ret[0][1]
			td[universal[2]] = tl
			td[universal[3]] = ret[0][2]
			td[universal[4]] = str(ret[0][3])
			td[universal[5]] = str(ret[0][4])

			return {'ans':td}

		if(l["type"] == 5):
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

		if(l["type"] == 6):
			u_handle = mysql.connection.cursor()
			u_handle.execute("SELECT COUNT(*) FROM rides")
			ret = u_handle.fetchall()
			tl = []
			for item in ret:
				tl.append(item[0])
			mysql.connection.commit()  
			u_handle.close()
			return {'ans': tl}

	else:
		return {'ret':400}

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
			date_obj = datetime.strptime(l['items'][1], '%Y-%m-%d:%H-%M-%S')
			l['items'][1] = date_obj

			try:
				u_handle.execute("INSERT INTO rides(created_by,time_stamp,source_loc,destination_loc)  values(%s, %s, %s, %s)",l['items'])
			except Exception as e:
				return {'ret':400}
			mysql.connection.commit()  
			u_handle.close()
			return {'ret':200}

		if(l["type"] == 4):
			u_handle = mysql.connection.cursor()
			try:
				u_handle.execute("INSERT INTO riders_list values(%s, %s)",(l['items'][1], l['items'][0]))
			except:
				return {'ret':400}
			mysql.connection.commit()  
			u_handle.close()
			return {'ret':200}

		if(l["type"] == 5):
			u_handle = mysql.connection.cursor()
			try:
				u_handle.execute("DELETE FROM rides WHERE ride_id = %s",(l['items'][0],))
			except Exception as e:
				print(e)
				return {'ret':400}
			mysql.connection.commit()  
			u_handle.close()
			return {'ret':200}

		if(l["type"] == 6):
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

		if(l["type"] == 7):
			u_handle = mysql.connection.cursor()
			try:
				u_handle.execute("UPDATE calls SET req = 0")
			except Exception as e:
				print(e)
				return {'ans':400}
			mysql.connection.commit()  
			u_handle.close()
			return {'ans': 200}

		if(l["type"] == 8):
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
	app.run(host="0.0.0.0", port=80)

