# sqlalchemy 是数据库映射，且model都是直接从基类Base继承创建的，所以一般是一个表一个model（或py文件），
# User 涉及到用户权限管理，通过 标识符统一管理

from .user import User
from .shcity import ShCity
from .friendcity import FriendCity
from .friendship import Friendship