import json,smtplib
from cv2 import trace
from flask import Flask,render_template,request,session#,redirect
from flask_sqlalchemy import SQLAlchemy
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import redis

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///trkr.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key="nine_eleven"
redis_cache = redis.StrictRedis()
db=SQLAlchemy(app)
db.create_all()

@app.route("/",methods=["GET","POST"])
def login():
	if request.method=="POST":
		k=db.engine.table_names()
		result=db.engine.execute("select * from user")
		usnms=[i[0] for i in result]
		# print(usnms)

		#login is clicked
		if request.form['formpurpose']=='loginval':
			username=request.form["logusername"]
			password=request.form["logpassword"]
			result=db.engine.execute("select * from user")
			session["username"]=username
			for user in result:
				if user[0]==username:
					if user[4]==password:
						session['tables']=user[5]
						session['naam']=user[2]
						session['upnaam']=user[3]
						return render_template("user.html",name=session['naam']+" "+session['upnaam'],tables=session['tables'])
			return render_template("login.html",msg="INVALID CREDENTIALS!!!")

		#signup is clicked
		elif request.form['formpurpose']=='signupval':
			naam=request.form["naam"]
			upnaam=request.form["upnaam"]
			email=request.form["email"]
			sgnusername=request.form["sgnusername"]
			sgnpassword=request.form["sgnpassword"]
			if sgnusername in usnms:
				return render_template("login.html",msg="Username already in use!!!")
			db.engine.execute(f"INSERT INTO user VALUES ('{sgnusername}', '{email}', '{naam}', '{upnaam}', '{sgnpassword}', '');")
			session['username']=sgnusername
			session['naam']=naam
			session['upnaam']=upnaam
			return render_template("user.html",name=naam+" "+upnaam)
	return render_template("login.html")

@app.route("/newtracker",methods=["GET","POST"])
def newtracker():
	if request.method=="POST":
		username=session["username"]
		tables=session["tables"]
		# print("session data => ",username,tables)
		tname=request.form["tname"]	
		tdescr=request.form["tdescr"]
		tselect=request.form["tselect"]
		tset=request.form["tset"]
		# print("form data => ",tname,tdescr,tselect,tset)	#prints data
		if tables=="":
			tables+=tname
		else:
			tables+=","+tname
		session['tables']=tables
		modname=tname+"_"+username
		db.engine.execute(f"UPDATE user SET trackers=trackers||','||'{tname}' where username='{username}';")
		db.engine.execute(f"INSERT INTO alltables VALUES ('{username}','{tname}','{tdescr}','{tselect}');")
		if tselect=="1":db.engine.execute(f'CREATE TABLE "{modname}" ("time"TEXT,"value"INTEGER,"desc"TEXT DEFAULT "{tdescr}",PRIMARY KEY("time"));')
		if tselect=="2":db.engine.execute(f'CREATE TABLE "{modname}" ("time"TEXT,"value"TEXT,"choices"TEXT DEFAULT "{tset}","desc"TEXT DEFAULT "{tdescr}",PRIMARY KEY("time"));')
		if tselect=="3":db.engine.execute(f'CREATE TABLE "{modname}" ("time"TEXT,"value"TEXT,"desc"TEXT DEFAULT "{tdescr}",PRIMARY KEY("time"));')
		return render_template("user.html",name=session["naam"]+" "+session["upnaam"],username=session["username"],tables=session["tables"])
	return render_template("newtracker.html",name=session["naam"]+" "+session["upnaam"])

@app.route("/delete/<table>",methods=["GET","POST"])
def deleter(table):
	if request.method=="POST":
		if "yesbtn" in request.form:
			tables=session['tables']
			username=session['username']
			tables=tables.split(",")
			tables.remove(table)
			tables=",".join(tables)
			session['tables']=tables
			modname=table+"_"+username
			# print(session['tables'],modname)
			db.engine.execute(f'DELETE FROM alltables')
			db.engine.execute(f"UPDATE user SET trackers='{tables}' where username='{username}';")
			db.engine.execute(f'DROP TABLE {modname}')
			return render_template("user.html",name=session["naam"]+" "+session["upnaam"],tables=tables)
		else:
			return render_template("user.html",name=session["naam"]+" "+session["upnaam"],tables=session['tables'])
	return render_template("deleter.html",name=session["naam"]+" "+session["upnaam"],table=table)

@app.route("/export/<table>",methods=["GET","POST"])
def exporter(table):
	dnld=None
	username=session['username']
	result=db.engine.execute(f'select * from alltables WHERE tabname="{table}" and username="{username}";')
	for i in result:dnld=i
	print(table,session['username'])
	# if request.method=="POST":
		# return render_template("user.html",name=session["naam"]+" "+session["upnaam"],username=session["username"],tables=session["tables"])
	return render_template("exporter.html",name=session["naam"]+" "+session["upnaam"],table=table,dnld=dnld)

@app.route("/import",methods=["GET","POST"])
def importer():
	# username=session['username']
	if request.method=="POST":
		tra=request.form["trackerinfo"]
		k=eval("["+tra[1:-1]+"]")
		# for i in k:print(i)

		username=k[0]
		tables=session["tables"]
		# print("session data => ",username,tables)
		tname=k[1]
		tdescr=k[2]
		tselect=k[3]
		tset="tset"
		# print("form data => ",tname,tdescr,tselect,tset)	#prints data
		if tables=="":
			tables+=tname
		else:
			tables+=","+tname
		session['tables']=tables
		modname=tname+"_"+username
		db.engine.execute(f"UPDATE user SET trackers=trackers||','||'{tname}' where username='{username}';")
		db.engine.execute(f"INSERT INTO alltables VALUES ('{username}','{tname}','{tdescr}','{tselect}');")
		if tselect==1:db.engine.execute(f'CREATE TABLE "{modname}" ("time"TEXT,"value"INTEGER,"desc"TEXT DEFAULT "{tdescr}",PRIMARY KEY("time"));')
		if tselect==2:db.engine.execute(f'CREATE TABLE "{modname}" ("time"TEXT,"value"TEXT,"choices"TEXT DEFAULT "{tset}","desc"TEXT DEFAULT "{tdescr}",PRIMARY KEY("time"));')
		if tselect==3:db.engine.execute(f'CREATE TABLE "{modname}" ("time"TEXT,"value"TEXT,"desc"TEXT DEFAULT "{tdescr}",PRIMARY KEY("time"));')
		return render_template("user.html",name=session["naam"]+" "+session["upnaam"],username=session["username"],tables=session["tables"])

	return render_template("importer.html",name=session["naam"]+" "+session["upnaam"])

@app.route("/edit/<table>",methods=["GET","POST"])
def editor(table):
	if request.method=="POST":
		newdesc=request.form["newdesc"]
		username=session['username']
		db.engine.execute(f'UPDATE alltables SET desc="{newdesc}" WHERE tabname="{table}" and username="{username}";')
		if "," in newdesc or ";" in newdesc:return render_template("forofor.html")
		return render_template("user.html",name=session["naam"]+" "+session["upnaam"],tables=session["tables"])
	return render_template("editrack.html",name=session["naam"]+" "+session["upnaam"],table=table)

@app.route("/remind/<table>",methods=["GET","POST"])
def reminder(table):
	print(table)
	if request.method=="POST":
		alertime=request.form["alertime"]
	return render_template("reminder.html",name=session["naam"]+" "+session["upnaam"],table=table)

@app.route("/add_data/<table>",methods=["GET","POST"])
def adder(table):
	if request.method=="POST":
		username=session['username']
		when=request.form["when"]
		value=request.form["value"]
		notes=request.form["notes"]
		modname=table+"_"+username
		if "," in when or ";" in when:return render_template("forofor.html")
		if "," in value or ";" in value:return render_template("forofor.html")
		if "," in notes or ";" in notes:return render_template("forofor.html")
		db.engine.execute(f'INSERT INTO {modname} VALUES ("{when}","{value}","{notes}")')
	return render_template("adder.html",name=session["naam"]+" "+session["upnaam"],table=table)

@app.route("/view/<table>",methods=["GET","POST"])
def datashape(table):
	#if generate button is clicked
	username=session['username']
	modname=table+"_"+username
	result=db.engine.execute(f"select * from {modname}")

	if request.method=="POST":
		me = "h1m4n3hu5on1@outlook.com"
		you = "himanshusoni2708@gmail.com"
		msg = MIMEMultipart('alternative')
		msg['Subject'] = "Mail experiment"
		msg['From'] = me
		msg['To'] = you
		res=""
		for i in result:res+=str(i)+"\n"
		print(res)
		html = """
		<html>
		<head></head>
		<body>
		<center>
			<h1 style="color:red">Hi """ + username + """ !<br><br></h1>
			<h3>This is your """ + table + """ tracker!</h3>
			
			<img src="https://i.ibb.co/R2dhgRL/image.png">
		</center>
		</body>
		</html>
		"""
		part2 = MIMEText(html, 'html')
		msg.attach(part2)
		mail = smtplib.SMTP('smtp.outlook.com', 587)
		mail.ehlo()
		mail.starttls()
		mail.login('h1m4n3hu5on1@outlook.com', 'nokia123')
		mail.sendmail(me, you, msg.as_string())
		mail.quit()

		# server=smtplib.SMTP('smtp.outlook.com',587)
		# server.starttls()
		# server.login('h1m4n3hu5on1@outlook.com','password')
		# server.sendmail('h1m4n3hu5on1@outlook.com','himanshusoni2708@gmail.com','Subject:'+"sssubject"+'\n\n'+"cccontent")
	l1=[]
	l2=[]
	l3=[]
	for i in result:
		l1+=[i[0]]
		l2+=[i[1]]
		l3+=[i[2]]
	# print(l1,l2,l3)
	return render_template("chart.html",name=session["naam"]+" "+session["upnaam"],table=table,l1=json.dumps(l1),l2=json.dumps(l2),l3=json.dumps(l3))

if __name__=='__main__':
	app.debug=True
	app.run()