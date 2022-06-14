from flask_login import UserMixin
import database as db


class UserLogin(UserMixin):
    def get(self, userid):
        self.__user = db.get_user(userid)
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user.id)
