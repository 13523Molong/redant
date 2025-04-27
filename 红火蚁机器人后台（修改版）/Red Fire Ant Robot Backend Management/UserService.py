import hashlib,base64,random,string

class UserService():
    # 用户密码的加密规则
    @staticmethod
    def genePwd(pwd, salt):
        m = hashlib.md5()
        str = "%s-%s" % (base64.encodebytes(pwd.encode("utf-8")), salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    # 产生用户授权码,对用户uid进行加密,存在cookies中
    @staticmethod
    def geneAuthCode(user_info):
        m = hashlib.md5()
        str = "%s-%s-%s-%s" % (user_info['uid'], user_info['login_name'], user_info['login_pwd'], user_info['login_salt'])
        m.update(str.encode("utf-8"))
        return m.hexdigest()


    # 产生salt随机码
    @staticmethod
    def geneSalt(length=16):
        keylist = [random.choice((string.ascii_letters + string.digits)) for i in range(length)]
        return ("".join(keylist))