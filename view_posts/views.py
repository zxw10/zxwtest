# coding: utf-8

from math import ceil

from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect

from view_posts.models import Posts
# Create your views here.


def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Posts.objects.create(title=title, content=content)  # 在表中添加字段的值
        return redirect('/post/read/?post_id=%s' % post.id)
    else:
        return render(request, 'create.html')
    # return HttpResponse('create')

def edit(request):
    if request.method == 'POST':  # edit页面的post方式
        post_id = request.POST.get('post_id')
        post = Posts.objects.get(id=post_id)

        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('/post/read/?post_id=%s' % post.id)
        # return redirect('/post/read/?post_id=%s' % 3)
    else:
        post_id = request.GET.get('post_id')  # 其他页面GET
        post = Posts.objects.get(id=post_id)
        return render(request, 'edit.html',{'post': post})


def read(request):
    post_id = request.GET.get('post_id')  # get拼接
    post = Posts.objects.get(id=post_id)
    return render(request, 'read.html', {'post': post})

def post_list(request):  # 进行帖子列表查看
    page = int(request.GET.get('page',1))  # 从GET的参数里拿到页码,拿不到就默认为1
    posts = Posts.objects.all()  # 类/表的管理器的方法
    posts_num = posts.count()
    per_num = 3  #每页显示数量
    page_num = ceil(posts_num / per_num)
    page_start = (page-1)*per_num
    page_posts = posts[page_start : page_start+per_num]
    return render(request, 'posts_list.html',{'posts':page_posts, 'pages':range(page_num)})  # 将拿到的帖子数据再传给后台
    # return HttpResponse('posts_view')


def search(request):
    keyword = request.POST.get('keyword')  # 从前端搜索框拿到搜索数据
    posts = Posts.objects.filter(content__contains=keyword)
    return render(request, 'search.html',{'posts':posts})
    # return render(request, 'search.html')