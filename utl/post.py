from db_builder import execute

class Post:

    def __init__(self, id):
        command = 'SELECT * FROM posts WHERE id={}'.format(id)
        data = execute(command).fetchall()
        self.id = int(data[0][0])
        self.author_id = str(data[0][1])
        self.title = str(data[0][2])
        self.content = int(data[0][3])
        self.qaf_id = int(data[0][4])
        self.time_created = int(data[0][5])


    @staticmethod
    def new_post(author_id, title, content, qaf_id):
        command = 'INSERT INTO posts (author_id, title, content, qaf_id) VALUES ("{}", "{}", "{}", {})'.format(author_id, title, content, qaf_id)
        execute(command)
