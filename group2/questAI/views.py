from django.shortcuts import render
from django.http import HttpResponse
from questAI.forms import UserForm,UserProfileForm
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'questAI/index.html')

def home(request):
    return render(request, 'questAI/base.html')

# def login(request):
#     return HttpResponse("Test for Login Page")


def register(request):
    registered = False#标识用户是否注册成功
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)#对密码进行hash处理，将明文转换成安全的形式
            user.save()
            profile = profile_form.save(commit=False)#保存不提交数据库，用于设置用户与附加信息的关联
            profile.user = user#建立user以及profile的关联
            # if 'picture' in request.FILES:
            #     profile.picture = request.FILES['picture']
            profile.save()
            registered = True
            return redirect(reverse('questAI:login'))
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,
              'questAI/register.html',
              context = {'user_form':user_form,
                         'profile_form':profile_form,
                         'registered':registered})


def user_login(request):
    if request.method == 'POST':#POST请求用于提交表单数据
        username = request.POST.get('username')#从请求中提取用户名和密码
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)#该函数使用提供的用户名和密码进行用户认证，成功则返回user对象，失败返回None
        if user:
            if user.is_active:#检查用户账号是否活跃（用于管理员暂时停用账号的作用）
                login(request,user)#将用户标记为已登录状态
                if user.is_staff == True:
                    return redirect(reverse('questAI:manage'))
                else:
                    return redirect(reverse('questAI:home'))#重定向到网站首页
            else:
                return HttpResponse("Your questAI account is disabled.")#提示账户被禁用消息
        else:
            print(f"Invalid login details:{username},{password}")
            context={'error_message':"Invalid login details supplied."}
            return render(request,'questAI/login.html',context)#登录信息无效
    else:
        return render(request,'questAI/login.html')
@login_required#限制访问权限，只有当用户已经登录时才能访问这个视图函数，未登录的用户尝试访问这个视图将会自动将用户重定向到登录页面
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('questAI:login'))

# def signup(request):
#     return HttpResponse("Test for Sign-Up Page")
def manage(request):
    return render(request, 'questAI/managebase.html')
def add(request):
    return render(request, 'questAI/add.html')
def basket(request):
    return HttpResponse("Test for Basket Page")

def topup(request):
    return HttpResponse("Test for Top Up Page")

def checkout(request):
    return HttpResponse("Test for Checkout Page")

