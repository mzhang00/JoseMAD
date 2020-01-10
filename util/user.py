from util.db_builder import execute

class User:

    def __init__(self, id):
        command = 'SELECT * FROM users WHERE id={}'.format(id)
        data = execute(command).fetchall()
        self.id = int(data[0][0])
        self.username = str(data[0][1])
        self.password = str(data[0][2])
        self.waffles = int(data[0][3])
        self.qafs_joined = str(data[0][4])

    # checks if username exists
    @staticmethod
    def username_avaliable(username):
        command = 'SELECT id FROM users WHERE username = "{}"'.format(username)
        data = execute(command).fetchall()
        return len(data) == 0

    # add user into database
    @staticmethod
    def new_user(username, password):
        command = 'INSERT INTO users (username, password, waffles) VALUES ("{}", "{}", 0)'.format(username, password)
        execute(command)

    # get user object by username
    @staticmethod
    def get_user(username):
        command = 'SELECT id from users WHERE username = "{}"'.format(username)
        data = execute(command).fetchall()
        if len(data) == 0: # if no user exists with the username then return None
            return None
        else:
            return User(data[0][0]) #returns user object
