import pyrebase
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.config["IMAGE_UPLOADS"] = "C:\python-firebase-authApp\profilee"
app.config["IMAGE_UPLOADS2"] = "C:\python-firebase-authApp"

config = {
    "apiKey": "AIzaSyA5BN7LM7pA5edWjsHIQ_C9mPTKXBxtA0o",
    "authDomain": "fypproject-b1650.firebaseapp.com",
    "databaseURL": "https://fypproject-b1650.firebaseio.com",
    "projectId": "fypproject-b1650",
    "storageBucket": "fypproject-b1650.appspot.com",
    "messagingSenderId": "1084397066040",
    "appId": "1:1084397066040:web:2ade1e2f8b945ea3a953cd"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
storage = firebase.storage()

path_on_cloud="images/Encrypted.tiff"



@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    if (request.method == 'POST'):
            email = request.form['name']
            password = request.form['password']
            try:
                auth.sign_in_with_email_and_password(email, password)
                #user_id = auth.get_account_info(user['idToken'])
                #session['usr'] = user_id
                return render_template('home.html')
            except:
                unsuccessful = 'Please check your credentials'
                return render_template('index.html', umessage=unsuccessful)
    return render_template('index.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if (request.method == 'POST'):
            email = request.form['name']
            password = request.form['password']
            auth.create_user_with_email_and_password(email, password)
            return render_template('index.html')
    return render_template('create_account.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if (request.method == 'POST'):
            email = request.form['name']
            auth.send_password_reset_email(email)
            return render_template('index.html')
    return render_template('forgot_password.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":

        if request.files:
            assets_dir = os.path.join(
                os.path.dirname(app.instance_path), ''
            )

            img1 = request.files["image1"]
            img2 = request.files["image2"]

            image1 = secure_filename(img1.filename)

            image2 = secure_filename(img2.filename)

            img1.save(os.path.join(assets_dir, 'C:\python-firebase-authApp\profilee', image1))

            img2.save(os.path.join(assets_dir,'C:\python-firebase-authApp', image2))



            os.rename(image2, 'test.jpg')

            print("Images saved")

            os.system('python EncryptInDirectory.py')

            return redirect(request.url)

    return render_template('home.html')

@app.route('/my-link/', methods=["GET", "POST"])
def my_link():
  print ('I got clicked!')
  os.system('python DecryptInDirectory.py')
  return render_template('home.html')

@app.route('/cloud/', methods=["GET", "POST"])
def mylink():
  print ('clouddd')
  path_local = "Encrypted/Encrypted.tiff"
  storage.child(path_on_cloud).put(path_local)
  return render_template('home.html')

@app.route('/download/', methods=["GET", "POST"])
def download():
  print ('download')
  storage.child(path_on_cloud).download("Encrypted.tiff")
  return render_template('home.html')



if __name__ == '__main__':
    app.run()
