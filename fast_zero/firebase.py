import firebase_admin
from firebase_admin import credentials, storage

# Inicialize o Firebase Admin SDK
cred = credentials.Certificate("firebase-credentials.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'packphotos-7d247.appspot.com'
})

def get_storage_bucket():
    return storage.bucket()

