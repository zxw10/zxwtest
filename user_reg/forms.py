
from django.forms import ModelForm
from django.forms import CharField
from django.forms import ValidationError


from user_reg.models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'password', 'icon', 'sex', 'age']

    password2 = CharField(max_length=128)

    #  调用is_valid方法就自动调用cleaned__方法
    def clean_password3(self):  #清洗后的数据里的密码,在一个字典里
        cleaned_data = super().clean()  # 继承父类的clean方法,不需要调用ls_valid,返回清洗后的数据
        if cleaned_data['password'] != cleaned_data['password2']:
            raise ValidationError('两次密码不一致')  #错误类