import pyrebase 

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

path_on_cloud="images/foo.jpg"


path_local="Encrypted/Enc.tiff"
storage.child(path_on_cloud).put(path_local)