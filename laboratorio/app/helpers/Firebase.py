import pyrebase
import os

from pyrebase.pyrebase import Storage 

config = {
    'apiKey': os.getenv('API_KEY'),
    'authDomain': os.getenv('AUTH_DOMAIN'),
    'databaseURL': os.getenv('DATABASE_URL_FIREBASE'),
    'projectId': os.getenv('PROJECT_ID'),
    'storageBucket': os.getenv('STORAGE_BUCKET'),
    'messagingSenderId': os.getenv('MESSAGING_SENDER_ID'),
    'appId': os.getenv('APP_ID')
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()