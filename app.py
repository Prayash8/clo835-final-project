from flask import Flask, render_template, request, redirect, url_for
import pymysql
import boto3
import os

app = Flask(__name__)

# Configuration
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME', 'employees')
db_host = os.environ.get('DB_HOST')

s3_bucket = os.environ.get('S3_BUCKET')
s3_image_filename = os.environ.get('S3_IMAGE_FILENAME')
student_name = os.environ.get('STUDENT_NAME', 'Student')

def download_background_image():
    if not s3_bucket or not s3_image_filename:
        print("Log: S3 Environment variables not set.")
        return None

    local_image_path = os.path.join('static', s3_image_filename)
    
    if not os.path.exists(local_image_path):
        print(f"Log: Downloading {s3_image_filename} from bucket {s3_bucket}...")
        try:
            s3 = boto3.client('s3', region_name='us-east-1')
            s3.download_file(s3_bucket, s3_image_filename, local_image_path)
            print(f"Log: Successfully downloaded background image to {local_image_path}")
        except Exception as e:
            print(f"Log: Error downloading from S3: {e}")
            return None
    return s3_image_filename

@app.route('/')
def home():
    image_file = download_background_image()
    return render_template('home.html', student_name=student_name, background_image=image_file)

@app.route('/health')
def health():
    return "Healthy", 200

if __name__ == '__main__':
    print("Log: Starting Flask app on port 81")
    app.run(host='0.0.0.0', port=81)
