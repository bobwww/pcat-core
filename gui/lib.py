from typing import Sequence, Union
import bcrypt
from bson import ObjectId
import re
from pymongo import MongoClient
import json

#############
# Permissions
#############
PERM_ADMIN = 'ADMIN'        # Can do anything. Only one admin is allowed at any given time.
PERM_POWER = 'POWER'        #Be poweruser - Has every perm except admin
PERM_VIEW_PACKETS = 'VIEWPKTS'  #View packets collection
PERM_VIEW_LOGS = 'VIEWLOG'         #View logs
PERM_EXPORT_PACKETS = 'EXPPKTS'    #Export packets collection
PERM_EXPORT_LOGS = 'EXPLOG'   #Export logs
PERM_REGISTER = 'REG'      #Create other users
PERM_LOGIN = 'LOGIN'         #Login to own user (Can be used for disabling certain users)
PERM_EDIT_OWN = 'EDITOWN'      #Edit own user's credentials
PERM_EDIT_OTHER = 'EDIT'    #Edit other user's credentials
PERM_DELETE_OWN = 'DELOWN'    #Delete own user
PERM_DELETE_OTHER = 'DEL'  #Delete other users


############
# Exceptions
############

class UserNotFound(Exception):
    
    def __init__(self, msg='Username or password are incorrent!') -> None:
        super().__init__(msg)

class WrongPassword(Exception):
    
    def __init__(self, msg='Username or password are incorrent!') -> None:
        super().__init__(msg)

class UserAlreadyExists(Exception):
    
    def __init__(self, msg='The user cannot be registered since it already exists.') -> None:
        super().__init__(msg)

class BadUsername(Exception):
    
    def __init__(self, msg='A username must be between 5-32 characters and contain alphanumeric characters only.') -> None:
        super().__init__(msg)

class BadEmail(Exception):
    
    def __init__(self, msg='The email address is invalid!') -> None:
        super().__init__(msg)

class BadPassword(Exception):

    def __init__(self, msg='Password must be between 5-64 characters and contain non-whitespace characters.') -> None:
        super().__init__(msg)


class User:

    def __init__(self, uuid: ObjectId, username: str, email: str, perms: set) -> None:
        self.uuid = uuid
        self.username = username
        self.email = email
        self.perms = perms

    def check_perms(self, required_perms: Sequence) -> bool:
        """Check if the user has all required permisions.

        Args:
            required_perms (list): list of strings

        Returns:
            bool: True if user has all required perms, False otherwise
        """
        for perm in required_perms:
            if perm not in self.perms:
                return False
        return True

    def to_json(self):
        return {
            'uuid': str(self.uuid),
            'username': self.username,
            'email': self.email,
            'perms': tuple(self.perms)
        }

    def __str__(self) -> str:
        return f"UUID: {self.uuid}\nUsername: {self.username}\nEmail: {self.email}\nPerms: {self.perms}"

class PowerUser(User):
    
    def __init__(self, uuid: ObjectId, username: str, email: str, perms: set) -> None:
        super().__init__(uuid, username, email, perms)
        # Perms is ignored when user is a power user
    
    def check_perms(self, required_perms: Sequence) -> bool:
        return PERM_ADMIN not in required_perms
        # Has any perm except the admin perm

class Administrator(PowerUser):

    def __init__(self, uuid: ObjectId, username: str, email: str, perms: set) -> None:
        super().__init__(uuid, username, email, perms=(PERM_ADMIN,))

    def check_perms(self, required_perms: Sequence) -> bool:
        return True


class UserSystem:
    USERNAME_PATTERN = re.compile('[A-Za-z][A-Za-z0-9]{4,16}')
    EMAIL_PATTERN = re.compile('([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    PASSWD_PATTERN = re.compile('\S{5,64}')


    def __init__(self, uri: str) -> None:
        self.client = MongoClient(uri)
        self.coll = self.client.pcat.users

        admin = self.coll.find_one({'perms': PERM_ADMIN})
        if not admin: 
            self.__insert_default_admin()
            admin = self.coll.find_one({'perms': PERM_ADMIN})
        self.admin = Administrator(admin['_id'], admin['username'], admin['email'], set(admin['perms']))



        # if len(admins) != 1: #Shouldnt ever happen
        #     #Too many admins
        #     pass

    # def __reset_default_admin(self):
        
    #     self.coll.update_many({ }, { '$pull': {'perms': PERM_ADMIN} })
    #     self.__insert_default_admin()

    def __insert_default_admin(self):
        self.coll.insert_one(
            {'username': 'admin',
            'email': None,
            'password': self.__hash_passwd('admin'),
            'perms': [PERM_ADMIN]}
        )


    def login(self, username: str, passwd: str) -> User:
        user = self.coll.find_one({'username': username})
        if not user: raise UserNotFound

        if self.__validate_passwd(passwd, user['password']):
            # Password correct
            if PERM_ADMIN in user['perms']:
                return self.admin
            if PERM_POWER in user['perms']:
                return PowerUser(user['_id'], user['username'], user['email'], set(user['perms']))
            else:
                return User(user['_id'], user['username'], user['email'], set(user['perms']))
        else:
            raise WrongPassword

    def register(self, username: str, email: str, passwd: str, perms: set) -> User:
        if self.coll.find_one({'username': username}): 
            raise UserAlreadyExists
        
        self.__validate_credentials(username, passwd, email)

        _id = self.coll.insert_one({
            'username': username,
            'email': email,
            'password': self.__hash_passwd(passwd),
            'perms': tuple(perms)
        }).inserted_id

        return User(_id, username, email, perms)


    def from_json(self, user):
        if PERM_ADMIN in user['perms']:
            return self.admin
        if PERM_POWER in user['perms']:
            return PowerUser(user['uuid'], user['username'], user['email'], set(user['perms']))
        else:
            return User(user['uuid'], user['username'], user['email'], set(user['perms']))

    @classmethod
    def __validate_credentials(cls, username, passwd, email):
        if not re.fullmatch(cls.USERNAME_PATTERN, username):
            raise BadUsername
        if not re.fullmatch(cls.EMAIL_PATTERN, email):
            raise BadEmail
        if not re.fullmatch(cls.PASSWD_PATTERN, passwd):
            raise BadPassword

    @staticmethod
    def __hash_passwd(passwd: Union[bytes, str]):
        
        if isinstance(passwd, str):
            passwd = passwd.encode('utf-8')

        salt = bcrypt.gensalt()
        return bcrypt.hashpw(passwd, salt)

    @staticmethod
    def __validate_passwd(passwd, hashed_passwd):

        if isinstance(passwd, str):
            passwd = passwd.encode('utf-8')

        return bcrypt.checkpw(passwd, hashed_passwd)

u = User(ObjectId(b'123456789012'), 'hello', '', {'VIEW'})