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
        self.tags = str(data[0][5]).split(',')
        self.time_created = str(data[0][6])
        self.net_vote = int(data[0][7])


    def get_comments(self):
        command = f'SELECT id FROM comments WHERE post_id = {self.id}'
        data = execute(command).fetchall()
        comments = []
        for comment_id in data:
            comments.append(Comment(comment_id[0]))

    def upvoted(self):
        command = 'UPDATE posts \
                    SET net_vote = "{}" \
                    WHERE id = {}'.format(self.net_vote + 1, self.id)
        execute(command)

    def downvoted(self):
        command = 'UPDATE posts \
                    SET net_vote = "{}" \
                    WHERE id = {}'.format(self.net_vote - 1, self.id)
        execute(command)

    # add post into database
    @staticmethod
    def new_post(author_id, title, content, qaf_id, tags):
        command = f'INSERT INTO posts (author_id, title, content, qaf_id, tags, net_vote) VALUES ("{author_id}", "{title}", "{content}", {qaf_id}, "{tags}", 0)'
        execute(command)
        util.user.User(author_id).join_qaf(qaf_id)
