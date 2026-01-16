import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

firebase_json = json.loads(os.environ.get("FIREBASE_KEY"))

cred = credentials.Certificate(firebase_json)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
