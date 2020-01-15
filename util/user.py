from util.db_builder import execute
from util.qaf import Qaf

class User:

    def __init__(self, id):
        command = 'SELECT * FROM users WHERE id={}'.format(id)
        data = execute(command).fetchall()
        self.id = int(data[0][0])
        self.username = str(data[0][1])
        self.password = str(data[0][2])
        self.waffles = int(data[0][3])
        self.qafs_joined = str(data[0][4])


    def join_qaf(self, qaf_id):
        qafs = self.qafs_joined.split(',')
        if qaf_id not in qafs:
            command = 'UPDATE users \
                        SET qafs_joined =  qafs_joined || "{}," \
                        WHERE id = {}'.format(qaf_id, self.id)
            execute(command)

    def get_qafs_joined(self):
        qafs_joined = self.qafs_joined.split(',')[:-1]
        qaf_list = [Qaf(qaf_id) for qaf_id in qafs_joined]
        return qaf_list
    def change_password(self, new_pass):
        command = 'UPDATE users \
                    SET password = "{}," \
                    WHERE id = {}'.format(new_pass, self.id)

    # checks if username exists
    @staticmethod
    def username_avaliable(username):
        command = 'SELECT id FROM users WHERE username = "{}"'.format(username)
        data = execute(command).fetchall()
        return len(data) == 0

    # add user into database
    @staticmethod
    def new_user(username, password):
        command = f'INSERT INTO users (username, password, waffles, qafs_joined) VALUES ("{username}", "{password}", 0, "")'
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
