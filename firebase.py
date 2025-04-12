import pyrebase

firebaseConfig = {
  'apiKey': "AIzaSyBBxq5O8rN12uBa1lQvJgqghkTefO4T8LY",
  'authDomain': "pushnotification-d7fac.firebaseapp.com",
  'projectId': "pushnotification-d7fac",
  'storageBucket': "pushnotification-d7fac.firebasestorage.app",
  'messagingSenderId': "372000880894",
  'appId': "1:372000880894:web:669b0d2e83ca334d514daf",
  'measurementId': "G-VG38XD35F5",
  "databaseURL": "https://pushnotification-d7fac-default-rtdb.firebaseio.com/"
}

fb = pyrebase.initialize_app(firebaseConfig)
auth = fb.auth()