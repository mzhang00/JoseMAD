from db_builder import execute

class QAF:
	
	def __init__(self, id):
		command = 'SELECT * FROM qafs WHERE id={}'.format(id)
		data = execute(command).fetchall()
		self.id = int(data[0][0])
		self.name = str(data[0][1])
		self.owner_id = int(data[0][2])
