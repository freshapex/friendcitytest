# crud 是直接操作数据库的表的，因此，crud 是跟着表走的，所以也是跟着model走的，
# 一般有多少个model ，对应有 多少张表，对应有多少个crud文件
from .crud_user import user
from .crud_shcity import shcity
from .crud_friendcity import friendcity
from .crud_friendship import friendship