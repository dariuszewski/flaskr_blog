from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES
from flask_ckeditor import CKEditor

db = SQLAlchemy()
photos = UploadSet("photos", IMAGES)
ckeditor = CKEditor()