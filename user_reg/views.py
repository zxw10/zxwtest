from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password,check_password

# from

from user_reg.models import User

from user_reg.forms import UserForm
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES)  # post包含普通字段,文件是FILES字段
        if form.is_valid():
            # 如果验证成功,则创建用户,生成密码
            user = form.save(commit=False)  # 将form表单的数据保存到映射的表中,但先不连接数据库,先不提交
            user.password = make_password(user.password)  # 将密码加密,重新传入
            user.save() # 进行保存到数据库中

            #登陆
            request.session['uid'] = user.id
            request.session['nickname'] = user.nickname
            return redirect('/user/info/')  # 不用get传参,可以直接从session里拿
        else:
            return render(request, 'register.html', {'error': form.errors})
    else:
        return render(request, 'register.html')
        # return HttpResponse('调试专用HTTP')
def login(request):
   if request.method == 'POST':
       nickname = request.POST.get('nickname')
       password = request.POST.get('password')
       try:
           user = User.objects.get(nickname=nickname)
       except User.DoesNotExist:  # 可以不加User.DoesNotExist
           return render(request, 'login.html', {'error': '用户不存在'})

       if check_password(password, user.password):
           request.session['uid'] = user.id
           request.session['nickname'] = user.nickname
           return redirect('/user/info/')
       else:
           return render(request, 'login.html', {'error': '密码错误'})
   else:
        return render(request, 'login.html')
def logout(request):
    request.session.flush()  # 其实退出登陆就是清空session的值 有个封装好的函数叫logout
    return redirect('/')

def user_info(request):
    uid = request.session['uid']  #或者用session.get方法request.session.get('uid')
    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        return redirect('/user/login/')
    else:
        return render(request, 'user_info.html', {'user': user})


