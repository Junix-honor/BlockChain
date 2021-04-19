from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import *
from flask_wtf.file import FileField, FileAllowed, FileRequired
from ..models import User
from .. import avatars


class EditProfileForm(FlaskForm):
    avatar = FileField('头像', validators=[FileAllowed(avatars, '文件格式不对')])
    location = StringField('住址', validators=[Length(0, 64)])
    signature = StringField('个性签名', validators=[Length(0, 64)])
    about_me = TextAreaField('个人简介')
    submit1 = SubmitField('更新信息')


class EditPasswordForm(FlaskForm):
    old = PasswordField('原密码', validators=[DataRequired()])
    password = PasswordField('新密码', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit2 = SubmitField('修改密码')

    def validate_old(self, field):
        if field.data != current_user.password:
            raise ValidationError('原密码错误！')


class CertificationForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired(), Length(1, 64)])
    phone = StringField('手机', validators=[DataRequired(),
                                          Regexp(r'1(3[0-9]|4[579]|5[0-3,5-9]|6[6]|7[0135678]|8[0-9]|9[89])\d{8}',
                                                 message="手机号格式不正确")])
    id = StringField('身份证', validators=[DataRequired(), regexp(
        r'^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$',
        message="身份证格式不正确")])
    pay_password = PasswordField('支付密码', validators=[
        DataRequired(), EqualTo('pay_password2', message='两次密码不一致'), length(6, 6, '请输入六位支付密码')])
    pay_password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit3 = SubmitField('提交')
