from util.db_builder import execute
from util.comment import Comment
import util.user

class Post:

    def __init__(self, id):
        command = 'SELECT * FROM posts WHERE id={}'.format(id)
        data = execute(command).fetchall()
        self.id = int(data[0][0])
        self.author_id = str(data[0][1])
        self.title = str(data[0][2])
        self.content = str(data[0][3])
        self.qaf_id = int(data[0][4])
        self.time_created = str(data[0][5])


    def get_comments(self):
        command = f'SELECT id FROM comments WHERE post_id = {self.id}'
        data = execute(command).fetchall()
        comments = []
        for comment_id in data:
            comments.append(Comment(comment_id[0]))
        return comments
    # add post into database
    @staticmethod
    def new_post(author_id, title, content, qaf_id):
        command = 'INSERT INTO posts (author_id, title, content, qaf_id) VALUES ("{}", "{}", "{}", {})'.format(author_id, title, content, qaf_id)
        execute(command)
        util.user.User(author_id).join_qaf(qaf_id)
