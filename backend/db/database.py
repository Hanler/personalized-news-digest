import firebase_admin.firestore
import firebase_admin
from firebase_admin import credentials
from config.settings import FIREBASE_KEY_PATH


class Database(object):
    def __init__(self):
        """
        Init the database connection
        """
        cred = credentials.Certificate(FIREBASE_KEY_PATH)
        firebase_admin.initialize_app(cred)

        self.db = firebase_admin.firestore.client()

    def send_to_db(self, data):
        """
        Send the write query to DB
        """
        doc_ref = self.db.collection('news').document()

        # Set an unique id
        data["id"] = doc_ref.id 

        doc_ref.set(data)
        print("Send was succesful")

database_instance = Database()
