from flask import Flask, request, render_template, jsonify
import mysql.connector
app = Flask(__name__)
app.config['MYSQL_USER'] = "task"
app.config['MYSQL-HOST'] = "localhost"
app.config['MYSQL_PASSWORD'] = "password123"
app.config['MYSQL-DB'] = 'nba'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mydb = mysql.connector.connect(host=app.config['MYSQL-HOST'] , database = app.config['MYSQL-DB'] ,user=app.config['MYSQL_USER'], password=app.config['MYSQL_PASSWORD'], auth_plugin='mysql_native_password')

@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('home.html')

@app.route('/<string:firstname>/<string:lastname>/<int:second_message>',methods=['GET'])
def multi(firstname, lastname, second_message):
	name = firstname + " " + lastname
	mycursor = mydb.cursor(buffered=True) 
	if second_message == 1:
		mycursor.execute("select seasons_stats.Year from seasons_stats where player = \'" + name + "\'")
		year = ""
		for row in mycursor:
			year += (str(*row) + " ")
		return jsonify({name: year})
	elif (second_message == 2):
		my_points = 0
		mycursor.execute("select seasons_stats.pts from seasons_stats where player = \'" + name + "\'")
		for row in mycursor:	
			integer = str(*row)  # a tuble cannot be converted to a int but can with string so i covert it to string and then to int with int() function
			if (int(integer) > my_points):
				my_points = int(integer)
		return jsonify({"Most points in a season by " + name : my_points})
	elif (second_message == 4):
		line_count = 0
		team_list = []
		team = " "
		mycursor.execute("select seasons_stats.tm from seasons_stats where player = \'" + name + "\'")
		for row in mycursor:
			if (line_count == 0):
				team_list.append(str(*row))
			else:
				if str(*row) not in team_list:
					team_list.append(str(*row))
				line_count += 1
		for t in team_list:
			team += " " + t
		return jsonify({"The team(s) " + name + " has played for are/is": team})

if __name__ == '__main__':
	app.run(debug=False)

    
