from util.db_builder import execute

class Comment:
	
	def __init__(self, id):
		command = 'SELECT * FROM comments WHERE id={}'.format(id)
		data = execute(command).fetchall()
		self.id = int(data[0][0])
		self.author_id = int(data[0][1])
		self.content = str(data[0][2])
		self.post_id = int(data[0][3])
		self.qaf_id = int(data[0][4])
		self.time_created = str(data[0][5])

	# add comment into database
	@staticmethod
	def new_comment(author_id, content, post_id, qaf_id):
		command = f'INSERT INTO comments (author_id, content, post_id, qaf_id) VALUES ("{author_id}", "{content}","{post_id}","{qaf_id}")'
		execute(command)

			