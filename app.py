from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3

app = Flask(__name__)

# Environment Variables
DBHOST = os.getenv("DBHOST", "localhost")
DBUSER = os.getenv("DBUSER", "root")
DBPWD = os.getenv("DBPWD", "root")
DATABASE = os.getenv("DATABASE", "employees")
DBPORT = int(os.getenv("DBPORT", 3306))
BUCKETNAME = os.getenv("BUCKETNAME", "finalprojectgroup14")
BGIMG = os.getenv("BGIMG", "bg-image.png")
GRPNAME = os.getenv("GRPNAME", "Group 14")

# Image download setup
imagesDir = "static"
bgImagePath = os.path.join(imagesDir, "background.png")
if not os.path.exists(imagesDir):
    os.makedirs(imagesDir)

# Create a connection to the MySQL database
try:
    db_conn = connections.Connection(
        host=DBHOST,
        port=DBPORT,
        user=DBUSER,
        password=DBPWD,
        db=DATABASE
    )
except Exception as e:
    print(f"Database connection failed: {e}")
    exit(1)

@app.route("/download")
def download(bucket=BUCKETNAME, imageName=BGIMG):
    print(f"Attempting to download from {bucket} the image {imageName}")
    try:
        session = boto3.Session(
            aws_access_key_id='ASIAUMNHBPJRGNWB5BNY',
            aws_secret_access_key='5qw+AMolFg31IkP9TGF4LGVZgeFr53UarvoMMwYl',
            aws_session_token='IQoJb3JpZ2luX2VjECwaCXVzLXdlc3QtMiJHMEUCIQCHlWRhxcl9krhF9qK6/25nYPCoq3kFGPU0mOGsKrXt5QIgI/xc90GdPfvXEIZovDNYBSQ0MISn5rihK+J+/mXNykQqpgIIZRAAGgwzMDE1MzQ5MDI4ODIiDC3kCJTK5+fJZaSeiiqDAnZbu1QSCGy+lih7+s+3CCo5sP1R/+d/FhsXexZP0juxhBvA7v+1UqqF87chGVTCCShaTMQWrZknBhR96J+4SQdr5436E5GHvI5XcTWZ1Ij0PdH3DZqMzeKHUvB/G3BSZFwuI3+RRYAHCdTFz7jshIwjMMSYu2yNWCRuTXNVecg7i6zuXk8+opx11S5fwiZx/NjgYWIqYO83voX7MSWBgtXwDCxlvJM9l1ykuz2qdtlD1WzetVrsi82ZMcU/lhyMdUEEW3YceBmZBMOBJmZiaLMaddtomm2uuWLhfq8DEVtnQoZp3S3zDBpioHriJ8kbarxwCQWejSS7tkBz20Ac6F87qG8w1ZfmsAY6nQHL/EmHVSg3aCsR6ok+H0tg/7CqqDyocINJ8eFz4SBU/UCLjvjXcrCEOPrkXOiioSuNFb+dafYJHcnTuRERHNdjp21GFoMHj2AYVzOQ46TNgHqIt6Hs1IpzMCuSiBa8Izxnsi/1GlSSSsLSqL1b/6ngZ8WLiyRIRZKDSRgd2a8AIBGfnrxmNf4ESXItFvvSLfbEj2NUcGYcC88N22kP',  # Replace with your actual session token
            region_name='us-east-1'
        )
        s3 = session.resource('s3')
        s3.Bucket(bucket).download_file(imageName, bgImagePath)
        return "Download successful"
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return "Download failed"

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('addemp.html', image=bgImagePath, group_name=GRPNAME)

@app.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('about.html', group_name=GRPNAME)

@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form.get('emp_id')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    primary_skill = request.form.get('primary_skill')
    location = request.form.get('location')
    insert_sql = "INSERT INTO employee (emp_id, first_name, last_name, primary_skill, location) VALUES (%s, %s, %s, %s, %s)"
    
    with db_conn.cursor() as cursor:
        try:
            cursor.execute(insert_sql, (emp_id, first_name, last_name, primary_skill, location))
            db_conn.commit()
            emp_name = f"{first_name} {last_name}"
            return render_template('addempoutput.html', name=emp_name, group_name=GRPNAME, message='Employee successfully added.')
        except Exception as e:
            db_conn.rollback()
            print(f"Error: {str(e)}")
            return render_template('addempoutput.html', name="", group_name=GRPNAME, message='Failed to add employee.')

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    emp_id = request.form.get('emp_id')
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location FROM employee WHERE emp_id = %s"
    
    with db_conn.cursor() as cursor:
        cursor.execute(select_sql, (emp_id,))
        result = cursor.fetchone()
    
    if result:
        details = {
            "id": result[0],
            "fname": result[1],
            "lname": result[2],
            "interest": result[3],
            "location": result[4]
        }
    else:
        details = {"id": "Not found", "fname": "", "lname": "", "interest": "", "location": ""}
    
    return render_template("getempoutput.html", group_name=GRPNAME, image=bgImagePath, **details)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
