from util.db_builder import execute
import util.user

class Comment:

	def __init__(self, id):
		command = 'SELECT * FROM comments WHERE id={}'.format(id)
		data = execute(command).fetchall()
		self.id = int(data[0][0])
		self.author_id = int(data[0][1])
		self.author = util.user.User(self.author_id).username
		self.content = str(data[0][2])
		self.post_id = int(data[0][3])
		self.qaf_id = int(data[0][4])
		self.time_created = str(data[0][5])
		self.net_vote = int(data[0][6])

	def upvoted(self):
        command = 'UPDATE comments \
                    SET net_vote = "{}" \
                    WHERE id = {}'.format(self.net_vote + 1, self.id)
        execute(command)

	def downvoted(self):
        command = 'UPDATE comments \
                    SET net_vote = "{}" \
                    WHERE id = {}'.format(self.net_vote - 1, self.id)
        execute(command)

	# add comment into database
	@staticmethod
	def new_comment(author_id, content, post_id, qaf_id):
		command = f'INSERT INTO comments (author_id, content, post_id, qaf_id, net_vote) VALUES ("{author_id}", "{content}","{post_id}","{qaf_id}", 0)'
		execute(command)
		util.user.User(author_id).join_qaf(qaf_id)
