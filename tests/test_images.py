import os
import io

import pytest
from PIL import Image

from flaskr.models.post import Post
from flaskr.models.comment import Comment
from flaskr.blueprints.blog.comment import get_comment
from flaskr.blueprints.blog.post import upload_photo, update_photo


class TestPhoto():
    filename = 'input.jpg'

    def read(self):
        i = Image.open('tests/img/input.jpg')
        bytes_ = io.BytesIO()
        i.save(bytes_, 'jpeg')
        return bytes_.getvalue()
    
    
def test_upload_photo(app):
        
    fp= TestPhoto()
    name = upload_photo(fp)
    assert name is not None


def test_update_without_new_photo(app):
    # first if at line 202 of post.py
    old_photo = TestPhoto()
    new_photo = None
    result = update_photo(old_photo, new_photo, False)
    assert result == old_photo


def test_update_with_remove_old_photo(app):
    # second if at line 205 of post.py
    old_photo = TestPhoto()
    new_photo = TestPhoto()
    result = update_photo(old_photo.filename, new_photo, False)
    assert result is not None


def test_remove_photo(app):
    # second if at line 205 without 212 of post.py
    old_photo = TestPhoto()
    new_photo = None
    result = update_photo(old_photo.filename, new_photo, True)
    assert result is None  

def test_remove_photo_without_old_photo(app):
    # third if at line 212 of post.py
    old_photo = None
    new_photo = None
    result = update_photo(old_photo, new_photo, True)
    assert result is None  

# @pytest.mark.parametrize(
#     ('old_photo', 'new_photo', 'remove_photo', 'expected_output'), (
#     (None, None, True, None),
#     (None, TestPhoto(), True, None),
# ))
# def test_remove_photo(app, old_photo, new_photo, remove_photo, expected_output):
#     # test update_photo with remove_photo = True

#     class TestOldPhoto():
#         filename = old_photo

#         def read():
#             fp = 'tests/img/' + TestOldPhoto.filename
#             i = Image.open(fp)
#             bytes_ = io.BytesIO()
#             i.save(bytes_, 'jpeg')
#             return bytes_.getvalue()
        
#     old_photo = TestOldPhoto()
#     new_photo = new_photo
#     filename = update_photo(old_photo.filename, new_photo, remove_photo)

#     assert filename == expected_output


# def test_update_photo_with_old_photo(app):
#     # Test update new photo with removal of old photo.
#     class TestOldPhoto():
#         filename = 'notfound.jpeg'

#         def read():
#             fp = 'tests/img/' + TestOldPhoto.filename
#             i = Image.open(fp)
#             bytes_ = io.BytesIO()
#             i.save(bytes_, 'jpeg')
#             return bytes_.getvalue()
        

#     old_photo = TestOldPhoto()
#     new_photo = TestPhoto()
#     filename = update_photo(old_photo.filename, new_photo, False)

#     assert filename is not None

# # def test_update_photo_without_old_photo(app):
# #     # Test upload photo where old_photo = None

# #     old_photo = None
# #     new_photo = TestPhoto()
# #     filename = update_photo(old_photo, new_photo, False)

# #     assert filename is not None

