import os, io

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

@pytest.mark.parametrize(
    ('old_photo', 'new_photo', 'remove_photo', 'expected_output'), (
    (None, None, True, None),
    ('not_existing.jpg', None, True, None),
    # ('None', 'input.jpg', False, 'old_photo'),
))
def test_update_photo(app, old_photo, new_photo, remove_photo, expected_output):

    class TestOldPhoto():
        filename = old_photo

        def read():
            fp = 'tests/img/' + TestOldPhoto.filename
            i = Image.open(fp)
            bytes_ = io.BytesIO()
            i.save(bytes_, 'jpeg')
            return bytes_.getvalue()
        
    class TestNewPhoto():
        filename = new_photo

        def read():
            fp = 'tests/img/' + TestNewPhoto.filename
            i = Image.open(fp)
            bytes_ = io.BytesIO()
            i.save(bytes_, 'jpeg')
            return bytes_.getvalue()
        
    old_photo = TestOldPhoto()
    new_photo = TestNewPhoto()
    filename = update_photo(old_photo.filename, new_photo, remove_photo)

    assert filename == expected_output


def test_update_photo_with_new_photo(app):

    class TestOldPhoto():
        filename = 'old_photo.jpeg'

        def read():
            fp = 'tests/img/old_photo'
            i = Image.open(fp)
            bytes_ = io.BytesIO()
            i.save(bytes_, 'jpeg')
            return bytes_.getvalue()
    class TestNewPhoto():
        filename = 'input.jpg'

        def read(self):
            fp = 'tests/img/' + TestNewPhoto.filename
            i = Image.open(fp)
            bytes_ = io.BytesIO()
            i.save(bytes_, 'jpeg')
            return bytes_.getvalue()

    old_photo = TestOldPhoto()
    new_photo = TestNewPhoto()
    filename = update_photo(old_photo.filename, new_photo, False)

    assert filename is not None

def test_update_photo_with_new_photo2(app):

    class TestOldPhoto():
        filename = 'old_photo.jpeg'

        def read():
            fp = 'tests/img/old_photo'
            i = Image.open(fp)
            bytes_ = io.BytesIO()
            i.save(bytes_, 'jpeg')
            return bytes_.getvalue()
    class TestNewPhoto():
        filename = 'input.jpg'

        def read(self):
            fp = 'tests/img/' + TestNewPhoto.filename
            i = Image.open(fp)
            bytes_ = io.BytesIO()
            i.save(bytes_, 'jpeg')
            return bytes_.getvalue()

    old_photo = TestOldPhoto()
    new_photo = TestNewPhoto()
    filename = update_photo(None, new_photo, False)

    assert filename is not None

# def test_update_photo3():

#     class TestOldPhoto():
#         filename = 'input.jpg'

#         def read():
#             fp = 'tests/img/input.jpg'
#             i = Image.open(fp)
#             bytes_ = io.BytesIO()
#             i.save(bytes_, 'jpeg')
#             return bytes_.getvalue()
        
#     class TestNewPhoto():
#         filename = 'input.jpg'

#         def read():
#             fp = 'tests/img/input.jpg'
#             i = Image.open(fp)
#             bytes_ = io.BytesIO()
#             i.save(bytes_, 'jpeg')
#             return bytes_.getvalue()
        
#     old_photo = TestOldPhoto()
#     new_photo = TestNewPhoto()
#     filename = update_photo(old_photo.filename, new_photo.filename, False)

#     assert filename is not None