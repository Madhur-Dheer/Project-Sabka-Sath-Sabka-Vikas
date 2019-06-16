from flask import Flask, redirect , url_for, request, session, render_template,flash
import json
import smtplib
import pandas as pd
import numpy as np
from csv import reader,writer
import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders

#from twilio.rest import Client
#from flask import CURSE
app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'Oh So Secret'


def send_an_email():
    toaddr = 'swayamdheer2910@gmail.com'    
    me = 'madhurdheer09@gmail.com' 
    subject = "Query Successfully Submitted"

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = toaddr
    msg.preamble = "test "
    text='''
            Your query has been successfully submitted.
            Hereby Attached the pdf of the query recorded by the system.
        '''
    msg.attach(MIMEText(text))

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open("query_letter.pdf", "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="query_letter.pdf"')
    msg.attach(part)

    
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(user = 'madhurdheer09@gmail.com', password = 'urd291174')
       #s.send_message(msg)
    s.sendmail(me, toaddr, msg.as_string())
    s.quit()
    #except:
    #   print ("Error: unable to send email")


def validate(filename):
    open_file=open(filename,encoding="UTF-8")
    read_file=reader(open_file)
    list_file=list(read_file)
    print(list_file)
    keyset={}
    for row in list_file:
        if row!=[]:
            print('row is',row)
            user=row[0]
            passw=row[1]
            type1=row[2]
            if user not in keyset:
                keyset[user]=[passw,type1]
    return keyset
def getlist(filename):
    open_file=open(filename,encoding="UTF-8")
    read_file=reader(open_file)
    list_file=list(read_file)
    alist={}
    for row in list_file:
        if row!=[]:
            name=row[0]
            if name not in alist:
                alist[name]=[row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]]
    return alist
def getuid(filename):
    open_file=open(filename,encoding="UTF-8")
    read_file=reader(open_file)
    list_file=list(read_file)
    alist=[]
    for row in list_file:
        if row!=[]:
            alist.append(row[0])
    return alist
@app.route('/')
def launcher():
    return render_template('newlogin.html')


#Login System using Aadhar UID
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        uid = request.form['uid']
        password=request.form['pass']
        dataset=validate('data.csv')
        if(uid in dataset):
            alist=dataset[uid]                       ### alist[0]--> Password    alist[1]---> type
            if(password==alist[0]):
                if(alist[1]=='Doctor'):
                    return redirect(url_for('input'))   ### link for doctor.html
                else:
                    return redirect(url_for('input2'))  ### link for municipal.html
            else:
                flash("You have Entered Wrong Id or Password")
                return render_template('newlogin.html')
        else:
            flash("You have Entered Wrong Id or Password")
            return render_template('newlogin.html')
            
    else:
        uid = request.get.args['uid']
        password=request.get.args['pass']
        dataset=validate('data.csv')
        if(uid in dataset):
            if(password==dataset[uid][0]):
                return redirect(url_for('input'))
            else:
                flash("You have Entered Wrong Id or Password")
                return render_template('newlogin.html')
        else:
            flash("You have Entered Wrong Id or Password")
            return render_template('newlogin.html')

@app.route('/newid')
def newid():
    return render_template('newid.html')
@app.route('/forgotpass')
def forgotpass():
    return render_template('changepass.html')


@app.route('/changepassw')
def changepassw():
    if request.method=='POST':
        print("Post")
    else:
        uid1=request.args.get('uid')
        password=request.args.get('psw')
        password_repeat=request.args.get('psw-repeat')
        checklist=getuid("data.csv")
        if uid1 in checklist:
            if(password==password_repeat):
                df = pd.read_csv("data.csv")
                df.set_value(checklist.index(uid1)-1, "Password",int(password))
                df.to_csv("data.csv",index=False)
                flash('Password Successfully Changed')
                return render_template('changepass.html')
            else:
                flash('Password Does not match Re-enter the Details')
                return render_template('changepass.html')
        else:
            flash('Enter Aadhar Number Does Not Exist/Not in the Database')
            return render_template('changepass.html')

@app.route('/makeid')
def makeid():
    if request.method=='POST':
        uid1=request.form['aadhar']
        password=request.form['psw']
        password_repeat=request.form['psw-repeat']
        flash('Added Successfully Return to login page')
        return render_template('newid.html')
    else:
        uid1=request.args.get('aadhar')
        mobile=request.args.get('mobile')
        data=request.args.get('country')
        password=request.args.get('psw')
        password_repeat=request.args.get('psw-repeat')
        if(password==password_repeat):
            alist1=[int(uid1),int(password),data,mobile]
            with open('data.csv', 'a') as writeFile:
                writer11 = writer(writeFile)
                writer11.writerow(alist1)
            flash('Added Successfully to the Database!! Please Return to login page')
            return render_template('newid.html')
        else:
            flash('Password Does not match Re-enter the Details')
            return render_template('newid.html')
        

@app.route('/success/<uID>')
def success(uID):
    return ("Registered UID : %s" % uID)

@app.route('/input2')
def input2():
    return render_template('municipal.html')

@app.route('/query')
def query():
    return render_template('query.html')


@app.route('/querynode')
def querynode():
    if request.method=='POST':
        print("This here")
    else:
        uid=request.args.get('fname')
        name=request.args.get('lname')
        typeofquery=request.args.get('country')
        issue=request.args.get('subject')

        doc = SimpleDocTemplate("query_letter.pdf",pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)
        Story=[]
        formatted_time = time.ctime()

        logo='python_logo.png'
 
        im = Image(logo, 2*inch, 2*inch)     #### Adding Image here
        Story.append(im)
 
        styles=getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        ptext = '<font size=12>Time of Submission :- %s</font>' % formatted_time
 
        Story.append(Paragraph(ptext, styles["Normal"]))     ### Adding time here
        Story.append(Spacer(1, 12))
        Story.append(Spacer(1, 12))
        ptext = '<font size=12>Dear %s:</font>' % name.strip()
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
 
        ptext = '<font size=12>The type of Qeury Submitted is :- %s.</font>' % (typeofquery)
        Story.append(Paragraph(ptext, styles["Justify"]))
        Story.append(Spacer(1, 12))
        Story.append(Spacer(1, 12))
        ptext = '<font size=12>Description :- %s.</font>' % (issue)
        Story.append(Paragraph(ptext, styles["Justify"]))
        Story.append(Spacer(1, 12))
        Story.append(Spacer(1, 12))
        
        ptext = '<font size=12><b>Thank you very much and we look forward to serving you.</b></font>'
        Story.append(Paragraph(ptext, styles["Justify"]))
        Story.append(Spacer(1, 12))
        ptext = '<font size=12>Sincerely,</font>'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1,12))
        ptext = '<font size=12>Swayam Dheer/Malay Bladha/Karthik Kishore</font>'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
        doc.build(Story)
        send_an_email()
        print("Get here")
    return "Your Query is Submitted"

# Data Collector Node
@app.route('/input')
def input():
    return render_template('doctor.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/datatx', methods = ['POST', 'GET'])
def data_tx():
    if request.method == 'POST':
        c=request.form['search']
        return render_template("login.html")

    else:
        data= request.args.get('search')
        list_name=getlist('ud.csv')
        if data in list_name:
            return render_template('result.html',var1=data,var2=list_name[data][0],var3=list_name[data][1],var4=list_name[data][2],var5=list_name[data][3],var6=list_name[data][4],var7=list_name[data][5],var8=list_name[data][6],var9=list_name[data][7],var10=list_name[data][8])
        else:
            flash('The Given Name is Not in the Database')
            return redirect(url_for('input'))

@app.route('/fta', methods = ['POST', 'GET'])
def fta_tx1():
    toaddr = 'swayamdheer2910@gmail.com'    
    me = 'madhurdheer09@gmail.com' 
    subject = "Appointment Scheduled for a Specialist"

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = toaddr
    msg.preamble = "test "
    text='''
        Respected Sir/Maam,
        
            Your Appointment has been scheduled.
            Date of Appointment=17th-June-2019
            Location-Reliance Greens,Motikhavadi
            Time of Appointment-9:30am

        PS:- Please be avaialable prior 30minutes the given time of appointment.

    '''


    msg.attach(MIMEText(text))
    s=smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login("madhurdheer09@gmail.com","urd291174")
    s.sendmail("madhurdheer09@gmail.com","swayamdheer2910@gmail.com",msg.as_string())
    s.quit()
    return "The Appointment is Scheduled"


if __name__=='__main__':
    app.run(debug=True)
