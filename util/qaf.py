from util.db_builder import execute
from util.post import Post

class Qaf:

	def __init__(self, id):
		command = 'SELECT * FROM qafs WHERE id={}'.format(id)
		data = execute(command).fetchall()
		self.id = int(data[0][0])
		self.name = str(data[0][1])
		self.owner_id = int(data[0][2])

	def get_posts(self):
		command = 'SELECT id FROM posts WHERE qaf_id = {}'.format(self.id)
		data = execute(command).fetchall()
		posts = []
		for post_id in data:
			posts.append(Post(post_id[0]))
		return posts

	#adds QAF into database
	@staticmethod
	def new_qaf(name, owner_id):
		command = 'INSERT INTO qafs (name, owner_id) VALUES ("{}", "{}")'.format(name, owner_id)
		cursor = execute(command)
		return cursor.lastrowid
