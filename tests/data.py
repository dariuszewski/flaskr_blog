# INSERT INTO user (username, password)
# VALUES
#   ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
#   ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');

# INSERT INTO post (title, body, author_id, created)
# VALUES
#   ('test title', 'test' || x'0a' || 'body', 1, '2018-01-01 00:00:00');

from flaskr.models import User, Post

user1 = User(username='test', password='pbkdf2:sha256:260000$5nA3Qw0INBKctANp$d02abb7c77f46bf38708c97a0fb8b3067c5944e85f04fb2b8e31164cf9562d62')
user2 = User(username='other', password='pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79')
post1 = Post(title='test title', body='body', author_id=1)

test_data = [user1, user2, post1]

