# fast_zero/storage.py
from fast_zero.firebase import get_storage_bucket

def upload_file(file_path: str, destination_blob_name: str):
    bucket = get_storage_bucket()
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(file_path)
    return blob.public_url

def download_file(source_blob_name: str, destination_file_name: str):
    bucket = get_storage_bucket()
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)


def delete_file(blob_name: str):
    bucket = get_storage_bucket()
    blob = bucket.blob(blob_name)
    blob.delete()