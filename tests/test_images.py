import os, io

import pytest
from PIL import Image

from flaskr.models.post import Post
from flaskr.models.comment import Comment

from flaskr.blueprints.blog.comment import get_comment

from flaskr.blueprints.blog.post import upload_photo, update_photo


# @pytest.mark.parametrize(
#     ('path', 'title', 'body', 'tags', 'photo', 'message'), (
#     ('/create','', '', '', '', 'Title is required.'),
#     ('/create', 'Title', '', '', '', 'Body is required.'),
#     ('/create', 'Title', 'Body', '', '', 'At least 1 tag is required.'),
#     # ('/create', 'Title', 'Body', 'Tag', (io.BytesIO(b"abcdef"), 'test'*1000), 'Request Entity Too Large'),
#     ('/1/update', '', '', '', '', 'Title is required.'),
#     ('/1/update', 'Title', '', '','', 'Body is required.'),
#     ('/1/update', 'Title', 'Body', '', '', 'At least 1 tag is required.'),
#     # ('/1/update', 'Title', 'Body', 'Tag', (io.BytesIO(b"abcdef"), 'test'*1000), 'Request Entity Too Large'),
# ))
# def test_create_update_validate(client, auth, database, path, title, body, tags, photo, message):
#     # Test if validation of input works.
#     auth.login()
#     if not photo:
#         photo = (io.BytesIO(b"abcdef"), '')
#     response = client.post(path, data={'title': title, 'body': body, 'tags': tags, 'photo': photo},
#                            content_type='multipart/form-data')
#     assert bytes(message, encoding='utf-8') in response.data


# def test_upload_photo(client, auth):
#     # photo = os. #tests\img\input.jpg
#     # photo = Image.new(mode='RGB', size=(500, 500))
#     # photo.show()
#     # filename = upload_photo(photo)
#     # assert filename is not None
#     auth.login()
#     photo = (io.BytesIO(b"abcdef"), 'test.jpg')
#     data = {'title': 'PhotoPost', 'body': 'PhotoBody', 'tags': 'photo'}
#     data['photo'] = (io.BytesIO(b"abcdef"), 'test.jpg')
#     content_type='multipart/form-data'
#     client.post('/create', data=data, content_type=content_type)
#     response = client.get('/')
#     assert b"abcdef" in response.data
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
def test_update_photo(old_photo, new_photo, remove_photo, expected_output):

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


def test_update_photo2():

    class TestOldPhoto():
        filename = 'old_photo.jpeg'

        def read():
            fp = 'tests/img/old_photo'
            i = Image.open(fp)
            bytes_ = io.BytesIO()
            i.save(bytes_, 'jpeg')
            return bytes_.getvalue()
        

    old_photo = TestOldPhoto()
    new_photo = None
    filename = update_photo(old_photo.filename, new_photo, False)

    assert filename == old_photo.filename


def test_update_photo3():

    class TestOldPhoto():
        filename = 'input.jpg'

        def read():
            fp = 'tests/img/input.jpg'
            i = Image.open(fp)
            bytes_ = io.BytesIO()
            i.save(bytes_, 'jpeg')
            return bytes_.getvalue()
        
    class TestNewPhoto():
        filename = 'input.jpg'

        def read():
            fp = 'tests/img/input.jpg'
            i = Image.open(fp)
            bytes_ = io.BytesIO()
            i.save(bytes_, 'jpeg')
            return bytes_.getvalue()
        
    old_photo = TestOldPhoto()
    new_photo = TestNewPhoto()
    filename = update_photo(old_photo.filename, new_photo.filename, False)

    assert filename is not None