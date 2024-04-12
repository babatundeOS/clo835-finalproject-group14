from flask import Flask, render_template, request
from pymysql import connections
import os
import random
import argparse
import boto3


app = Flask(__name__)

DBHOST = os.environ.get("DBHOST") or "localhost"
DBUSER = os.environ.get("DBUSER") or "root"
DBPWD = os.environ.get("DBPWD") or "password"
DATABASE = os.environ.get("DATABASE") or "employees"
#COLOR_FROM_ENV = os.environ.get('APP_COLOR') or "lime"
DBPORT = int(os.environ.get("DBPORT", "3306"))
#added updates
BGIMG = os.environ.get("BGIMG") or "bg-image.jpg"
BUCKETNAME = os.environ.get("BUCKETNAME") or "finalprojectimagesforgrp14"
GRPNAME = os.environ.get("GRPNAME") or "Group 14"

# Create a connection to the MySQL database
db_conn = connections.Connection(
    host= DBHOST,
    port=DBPORT,
    user= DBUSER,
    password= DBPWD, 
    db= DATABASE
    
)
output = {}
table = 'employee';

# Define the supported color codes
default_bucket = "finalprojectimagesforgrp14"
default_image = "bg-image.jpg"

@app.route("/download", methods=['GET', 'POST'])
def download(bucket = default_bucket, imageName = default_image):
    try:
        imagesDir = "static"
        if not os.path.exists(imagesDir):
            os.makedirs(imagesDir)
        bgImagePath = os.path.join(imagesDir, "background.png")
        
        print(bucket, imageName)
        s3 = boto3.resource('s3')
        s3.Bucket(bucket).download_file(imageName, bgImagePath)
        return os.path.join(imagesDir, "background.png")
    except Exception as e:
        print("Exception occured while fetching the image! Check the log --> ", e)
       

# Create a string of supported colors
#SUPPORTED_COLORS = ",".join(color_codes.keys())

# Generate a random color
#COLOR = random.choice(["red", "green", "blue", "blue2", "darkblue", "pink", "lime"])


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('addemp.html', image=image, group_name=GRPNAME)

# Catch-all route
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    # You can either redirect to the home page
    # return redirect(url_for('home'))

    # Or render the same template as the home page
    return render_template('addemp.html', image=image, group_name=GRPNAME)
    
@app.route("/about", methods=['GET','POST'])
def about():
    return render_template('about.html', image=image, group_name=GRPNAME)
    
@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    primary_skill = request.form['primary_skill']
    location = request.form['location']

  
    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        
        cursor.execute(insert_sql,(emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = "" + first_name + " " + last_name

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('addempoutput.html', name=emp_name, image=image, group_name=GRPNAME)

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    return render_template("getemp.html", image=image, group_name=GRPNAME)


@app.route("/fetchdata", methods=['GET','POST'])
def FetchData():
    emp_id = request.form['emp_id']

    output = {}
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location from employee where emp_id=%s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql,(emp_id))
        result = cursor.fetchone()
        
        # Add No Employee found form
        output["emp_id"] = result[0]
        output["first_name"] = result[1]
        output["last_name"] = result[2]
        output["primary_skills"] = result[3]
        output["location"] = result[4]
        
    except Exception as e:
        print(e)

    finally:
        cursor.close()

    return render_template("getempoutput.html", id=output["emp_id"], fname=output["first_name"],
                           lname=output["last_name"], interest=output["primary_skills"], location=output["location"], image=image, group_name=GRPNAME)

if __name__ == '__main__':
    
    # Check for Command Line Parameters for color
    image = download(BUCKETNAME, BGIMG)
    print(image)
    
    app.run(host='0.0.0.0',port=8080,debug=True)
