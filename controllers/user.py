# coding=utf-8
import bcrypt
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer
from flask import Blueprint, current_app, request, g

from backend_common.controllers.base import BaseController
from backend_common.middlewares.login_required import user_required
from backend_common.models.database import database
from backend_common.models.user import User as UserModel
from backend_common.models.user_token import UserToken as UserTokenModel
import backend_common.constants.user_type as user_type

user_blueprint = Blueprint('user', __name__)


class UserController(BaseController):

    @classmethod
    def register(cls):
        data = request.json or request.form or request.args
        with database.transaction():
            try:
                phone_number = data['phone_number']
                password = data['password']
                verifycode = data['verifycode']
                user = UserModel.select().where(UserModel.phone_number == phone_number).for_update().first()
                if user:
                    raise UserModel.HasExistError()
                else:
                    confirm_verifycode = current_app.cache.get('verifycode:' + str(phone_number))
                    if not confirm_verifycode:
                        raise UserModel.VerifycodeExpiredError()
                    if confirm_verifycode != verifycode:
                        raise UserModel.VerifycodeError()
                    # 加密密码
                    hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    # 注册用户
                    user = UserModel.create(username=phone_number, password=hash_password, phone_number=phone_number, nick=phone_number)
                    # 注册成功顺便登录
                    s = TimedJSONWebSignatureSerializer(current_app.secret_key, expires_in=7*24*60*60)
                    token = s.dumps(user.id)
                    UserTokenModel.create(user_id=user.id, user_type=user_type.USER, token=token)
                    result = user.format('id,username,sex,phone_number,nick,avatar,created_at,register_type')
                    result.update({'token': token})
                    return cls.success_with_result(result)
            except KeyError, e:
                raise UserModel.LackOfFieldError('请传递正确的用户名、密码、验证码')

    @classmethod
    def login(cls):
        data = request.json or request.form or request.args
        try:
            username = data['username']
            password = data['password']
            user = UserModel.get(UserModel.username == username, UserModel.deleted_at == None)
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                s = TimedJSONWebSignatureSerializer(current_app.secret_key, expires_in=7*24*60*60)
                token = s.dumps(user.id)
                UserTokenModel.create(user_id=user.id, user_type=user_type.USER, token=token)
                result = user.format('id,username,sex,phone_number,nick,avatar,created_at,register_type')
                result.update({'token': token})
                return cls.success_with_result(result)
            else:
                raise UserModel.PasswordError()
        except UserModel.DoesNotExist, e:
            raise UserModel.NotFoundError('该用户不存在')
        except KeyError, e:
            raise UserModel.LackOfFieldError('请传递参数用户名和密码')

    @classmethod
    @user_required
    def logout(cls, user):
        data = request.json or request.form or request.args
        token = data.get('token')
        UserTokenModel.delete().where(UserTokenModel.user_id == user.id, UserTokenModel.user_type == user_type.USER, UserTokenModel.token == token).execute()
        return cls.success_with_result(user.format('updated_at'))

    @classmethod
    @user_required
    def reset_password(cls, user):
        data = request.json or request.form or request.args
        try:
            old_password = data['old_password']
            new_password = data['new_password']
            if bcrypt.checkpw(old_password.encode('utf-8'), user.password.encode('utf-8')):
                user.password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                user.updated_at = datetime.now()
                user.save()
                return cls.success_with_result(user.format('updated_at'))
            else:
                raise UserModel.PasswordError()
        except KeyError, e:
            raise UserModel.LackOfFieldError(u'请传递参数旧密码和新密码')

    @classmethod
    def current(cls):
        if g.user:
            result = g.user.format('id,username,sex,phone_number,nick,avatar,created_at,register_type')
            return cls.success_with_result(result)
        else:
            return cls.success_with_result(None)

    @classmethod
    @user_required
    def update(cls, user):
        data = request.json or request.form or request.args
        sex = data.get('sex', 0)
        nick = data.get('nick')
        avatar = data.get('avatar')
        user.sex = sex
        user.nick = nick
        user.avatar = avatar
        user.updated_at = datetime.now()
        user.save()
        return cls.success_with_result(user.format('updated_at'))
