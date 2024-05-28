from django.shortcuts import render, redirect
from ETS_app.models import Gender,Occupation,Customer,Technician,Service,serviceCategory,M_Occupation,Main,Order,Review
from django.contrib.auth import  authenticate,login,logout
from django.contrib.auth.models import User,Group
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required,permission_required
from django.db.models import Q
from django.contrib import messages
from datetime import datetime
from django.core.paginator import Paginator

from django.conf import settings
from django.core.mail import send_mail

from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.

def check_user_login(username_or_email,password):
    # Check if the input is an email or a username
    if '@' in username_or_email:  # If it contains '@', treat it as an email
        user = User.objects.filter(email=username_or_email).first()
    else:
        user = User.objects.filter(username=username_or_email).first()
    if user and user.check_password(password):
        return user
    else:
        return None


# local default
def custom_404_view(request):
    return render(request, "404.html")

def local(request):
    return render(request, "main.html")

def t_main(request):
    return render(request, "T_main.html")

def m_main(request):
    return render(request, "M_main.html")

# C,T,M Home/Dashboard
@login_required(login_url='c_login')
def C_home(request):
    return render(request, 'C_home.html')

@login_required(login_url='m_login')
def M_dashboard(request):
    order = Order.objects.all()
    customer = Customer.objects.all()
    technician = Technician.objects.filter(status=True)
    t_reg = Technician.objects.filter(status=False)
    main = Main.objects.filter(status=True)
    m_reg = Main.objects.filter(status=False)
    service = Service.objects.all()
    review = Review.objects.all()
    return render(request, "M_dashboard.html",{'order':order,'customer':customer,'technician':technician,'t_reg':t_reg,'main':main,'m_reg':m_reg,'service':service,'review':review})

@login_required(login_url='t_login')
def T_home(request):
    return render(request, 'T_home.html')

# C,T,M login/logout/register

#--->customer

def C_login(request):
    if request.method == "GET":
        return render(request,'C_login.html')
    if request.method == "POST":
        n_or_e = request.POST.get('n_or_e')
        password = request.POST.get('password')

        n_or_e_check = User.objects.filter(Q(username=n_or_e)|Q(email=n_or_e)).exists()

        if not n_or_e_check:
            messages.error(request,"Username or Email doestn't exist")
            return redirect('/c_login/')
        else:
            n_or_e_check1 = Customer.objects.filter(Q(name=n_or_e)|Q(email=n_or_e)).exists()

            if not n_or_e_check1:
                messages.error(request,"Username or Email doestn't exist")
                return redirect('/c_login/')

            else:
                user1 = User.objects.get(Q(username=n_or_e)|Q(email=n_or_e))
                customer = Customer.objects.get(Q(name=n_or_e)|Q(email=n_or_e))

                if customer.password == password:
                    login(request,user1)
                    messages.success(request, f"Welcome back {user1.username}" )
                    return redirect('/ets/c_home/')
                else:
                    messages.error(request,"Username or Email or Password is worng")
                    return redirect('/c_login/')
    else:
        messages.errr(request,"Invalid method in login!")
        return redirect('/c_login/')

def C_register(request):
    if request.method == "GET":
        return render(request, 'C_register.html')
    elif request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')

        if User.objects.filter(username = name).exists():
            messages.error(request, "Username has been already used!")
            return redirect('/c_register/')
        elif User.objects.filter(email = email).exists():
            messages.error(request, "Email has been already existed!")
            return redirect('/c_register/')
        else:
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if password == confirm_password:
                create_at = datetime.now()

                user1 = User.objects.create_user(
                    username=name,
                    password=password,
                    email=email,
                )
                user1.save()

                customer_group = Group.objects.get(name='customers')
                user1.groups.add(customer_group)

                customer = Customer.objects.create(
                    name=name,
                    email=email,
                    password=password,
                    create_at=create_at,
                )
                customer.save()
                login(request,user1)

                # subject = 'welcome to Django'
                # message = f'Hi {user1.username}, thank you'
                # email_from = settings.EMAIL_HOST_USER
                # recipient_list = [user1.email,]
                # send_mail(subject,message,email_from,recipient_list)

                # subject = 'welcome to django'
                # html_message = render_to_string('C_login.html')
                # message = strip_tags(html_message)
                # email_from = settings.EMAIL_HOST_USER
                # recipient_list = [user1.email,]
                # send_mail(subject,message,email_from,recipient_list,html_message=html_message)
                

                return redirect('/ets/c_home/')
            else:
                messages.error(request, "Confirm password doesn't match!")
                return redirect('c_register')
    else:
        messages.error(request, "Invalid method in register!")

def C_logout(request):
    logout(request)
    return redirect('/c_login/')

#-->technician

def T_login(request):
    if request.method == "GET":
        return render(request, 'T_login.html')
    elif request.method == "POST":
        n_or_e = request.POST.get('name')
        password = request.POST.get('password')
        if Technician.objects.filter(Q(full_name=n_or_e)|Q(email=n_or_e)).exists():
            technician = Technician.objects.get(Q(full_name=n_or_e)|Q(email=n_or_e))
            if technician.status==True:

                n_or_e_check = User.objects.filter(Q(username=n_or_e)|Q(email=n_or_e)).exists()

                if not n_or_e_check:
                    messages.error(request, "Username or Email doesn't exist!")
                    return redirect('/t_login/')
                else:

                    n_or_e_check1 = Technician.objects.filter(Q(full_name=n_or_e)|Q(email=n_or_e)).exists()

                    if not n_or_e_check1:
                        messages.error(request, "Username  or Email doesn't exist!")
                        return redirect('/t_login/')
                    else:

                        user1 = User.objects.get(Q(username=n_or_e)|Q(email=n_or_e))
                        technician = Technician.objects.get(Q(full_name=n_or_e)|Q(email=n_or_e))

                        if technician.password == password:
                            login(request,user1)
                            return redirect('/ets/t_home/')
                        else:
                            messages.error(request, "Username or Email or Password is worng!")
                            return redirect('/t_login/')
            else:
                messages.error(request, "You are not technician")
                return redirect('/t_login/')
        else:
            messages.error(request, "Username or Email doesn't exist!")
            return redirect('/t_login/')
    else:
        messages.error(request, "Invalid method in login!")
        return redirect('/t_login/')

def T_register(request):
    if request.method == "GET":
        gender = Gender.objects.all()
        occupation = Occupation.objects.all()
        return render(request, 'T_register.html',{'gender':gender,'occupation':occupation})
    elif request.method == "POST":
        full_name = request.POST.get('name')
        email = request.POST.get('email')

        if User.objects.filter(username = full_name).exists():
            messages.error(request, "Name has been already existed!")
            return redirect('/t_register/')
        elif User.objects.filter(email = email).exists():
            messages.error(request, "Email has been already existed!")
            return redirect('/t_register/')
        else:
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if password == confirm_password:
                phone = request.POST.get('phone')
                birth = request.POST.get('birth')
                gender_id = request.POST.get('gender')
                nrc = request.POST.get('nrc')
                occupation_id = request.POST.get('occupation')
                qualification = request.POST.get('qualification')
                image = request.FILES.get('image')
                create_at = datetime.now()

                user1 = User.objects.create_user(
                    username=full_name,
                    email=email,
                    password=password,
                )
                user1.save()

                technician_group = Group.objects.get(name='technicians')
                user1.groups.add(technician_group)

                technician = Technician.objects.create(
                    full_name=full_name,
                    email=email,
                    phone=phone,
                    birth=birth,
                    nrc=nrc,
                    gender_id=gender_id,
                    occupation_id=occupation_id,
                    qualification=qualification,
                    image=image,
                    password=password,
                    create_at=create_at,
                )
                technician.save()
                return redirect('/t_login/')
            else:
                messages.error(request, "Confirm password doesn't match!")
                return redirect('/t_register/')
    else:
        messages.error(request, "Invalid method in register!")
        return redirect('/t_register/')
            

def T_logout(request):
    logout(request)
    return redirect('/t_login/')

#-->main office

def M_login(request):
    if request.method =="GET":
        return render(request, 'M_login.html')
    elif request.method =="POST":
        n_or_e = request.POST.get('name')
        password = request.POST.get('password')
        if User.objects.filter(Q(username=n_or_e)|Q(email=n_or_e)).exists():
            user = User.objects.get(Q(username=n_or_e)|Q(email=n_or_e))
            if user.is_superuser:
                if Customer.objects.filter(Q(name=n_or_e)|Q(email=n_or_e)).exists():
                    messages.error(request, "Username or Email doesn't exist!")
                    return redirect('/m_login')
                elif Technician.objects.filter(Q(full_name=n_or_e)|Q(email=n_or_e)).exists():
                    messages.error(request, "Username or Email doesn't exist!")
                    return redirect('/m_login')
                # elif Main.objects.filter(Q(name=n_or_e)|Q(email=n_or_e)).exists():
                #     messages.error(request, "Username or Email doesn't exist!")
                #     return redirect('/m_login')
                else:
                    user1 = check_user_login(username_or_email=n_or_e,password=password)
                    if user1 is not None:
                        login(request,user1)
                        return redirect('/ets/m_dashboard/')
                    else:
                        messages.error(request, "Username or Email or Password is wrong")
                        return redirect('/m_login/')

            elif Main.objects.filter(Q(name=n_or_e)|Q(email=n_or_e)).exists():
                main = Main.objects.get(Q(name=n_or_e)|Q(email=n_or_e))
                if main.status == True:
                    n_or_e_check = User.objects.filter(Q(username=n_or_e)|Q(email=n_or_e)).exists()
                    if not n_or_e_check:
                        messages.error(request, "Username or Email doesn't exist!")
                        return redirect('/m_login/')
                    else:
                        user1 = User.objects.get(Q(username=n_or_e)|Q(email=n_or_e))
                        main = Main.objects.get(Q(name=n_or_e)|Q(email=n_or_e))
                        if main.password == password:
                            login(request,user1)
                            return redirect('/ets/m_dashboard/')
                        else:
                            messages.error(request, "Username or Email or Password is worng!")
                            return redirect('/m_login/')
                else:
                    messages.error(request, "You are not employee!")
                    return redirect('/m_login/')
            else:
                messages.error(request, "Username or Email doesn't exist!")
                return redirect('/m_login/')
        else:
            messages.error(request, "Username or Email doesn't exist!")
            return redirect('/m_login/')
    else:
        messages.error(request, "Invalid method in login!")
        return redirect('/m_login/')

def M_register(request):
    if request.method == "GET":
        occ = M_Occupation.objects.all()
        return render(request, "M_register.html",{'occ':occ})
    elif request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')

        if User.objects.filter(username=name):
            messages.error(request, "Username has been already exist!")
            return redirect('/m_register/')
        elif User.objects.filter(email=email):
            messages.error(request, "Email has been already exist!")
            return redirect('/m_register/')
        else:
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password == confirm_password:
                occupation_id = request.POST.get('occupation')
                image = request.FILES.get('image')
                create_at = datetime.now()

                user1 = User.objects.create_user(
                    username=name,
                    email=email,
                    password=password,
                )
                user1.save()

                controller_group = Group.objects.get(name='controllers')
                user1.groups.add(controller_group)

                main = Main.objects.create(
                    name=name,
                    email=email,
                    occupation_id=occupation_id,
                    image=image,
                    password=password,
                    create_at=create_at,
                )
                main.save()
                return redirect('/m_login/')
            else:
                messages.error(request, "Confirm Password doesn't match!")
                return redirect('/m_register/')
    else:
        messages.error(request, "Invalid method in register!")
        return redirect('/m_register/')

def M_logout(request):
    logout(request)
    return redirect('/m_login/')

# technician

@permission_required('ETS_app.view_order', login_url='t_login')
def T_order_list(request,post_e):
    order = Order.objects.filter(Q(t_status=True) & Q(t_email=post_e)).order_by('-create_at')
    paginator = Paginator(order, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'T_order_list.html', {'order': page_obj})

@permission_required('ETS_app.view_order', login_url='t_login')
def T_order_detail(request,post_id):
    order = Order.objects.get(id=post_id)
    return render(request, "T_order_detail.html",{'order':order})

@login_required(login_url='t_login')
def T_order_approve(request,id):
    order = Order.objects.get(id = id)
    order.status = 'approve'
    order.f_status = 'on-going'
    order.save()
    messages.success(request,"Order has been approved")
    return redirect(f'/ets/t_order/list/{order.t_email}')

@login_required(login_url='t_login')
def T_order_reject(request,id):
    order = Order.objects.get(id = id)
    order.status = 'reject'
    order.save()
    messages.success(request,"Order has been rejected")
    return redirect(f'/ets/t_order/list/{order.t_email}')

@login_required(login_url='t_login')
def T_order_finish(request,id):
    order = Order.objects.get(id = id)
    order.f_status = 'finish'
    order.save()
    messages.success(request,"Order has been finished")
    return redirect(f'/ets/t_order/list/{order.t_email}')

@login_required(login_url='t_login')
def T_order_delete(request,id):
    order = Order.objects.get(id = id)
    order.t_status = False
    order.save()
    messages.success(request,"Order has been deleted")
    return redirect(f'/ets/t_order/list/{order.t_email}')

@permission_required('ETS_app.view_technician', login_url='t_login')
def T_technician(request):
    technician = Technician.objects.filter(status=True).order_by('-create_at')
    paginator = Paginator(technician, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'T_technician.html', {"technician":page_obj})

@permission_required('ETS_app.view_technician', login_url='t_login')
def search_by8(request):
    search = request.GET.get('search')
    if search:
        technician = Technician.objects.filter(
            Q(full_name__icontains=search) |
            Q(occupation__name__icontains=search),
            status=True
        )
        paginator = Paginator(technician, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'T_technician.html', {'technician': page_obj})
    else:
        technician = Technician.objects.filter(status=True).order_by('-create_at')
        paginator = Paginator(technician, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'T_technician.html', {'technician': page_obj})

@permission_required('ETS_app.add_review', login_url='t_login')
def T_review_create(request):
    if request.method == "GET":
        return render(request,"T_review.html")
    if request.method == "POST":
        review = Review.objects.create(
            name = request.POST.get('name'),
            email = request.POST.get('email'),
            phone = request.POST.get('phone'),
            message = request.POST.get('message'),
            create_at = datetime.now()
        )
        review.save()
        messages.success(request,"Review has been sent")
        return redirect('/ets/t_review/create')

@permission_required('ETS_app.change_technician', login_url='t_login')
def T_profile_edit(request,id):
    if request.method == "GET":
        technician = Technician.objects.get(id=id)
        return render(request,"T_base.html",{'technician':technician})
    if request.method == "POST":
        technician = Technician.objects.get(id=id)
        if request.FILES.get('image'):
            technician.image.delete()
            technician.image = request.FILES.get('image')
        technician.save()
        messages.success(request, "Profile photo has been uploaded")
        return redirect('/ets/t_home')

# --> customer
# services
# service category(customer)

@permission_required('ETS_app.view_servicecategory', login_url='c_login')
def C_service_category_view(request):
    category = serviceCategory.objects.all()
    return render(request, 'C_service_category.html', {'category':category})

@permission_required('ETS_app.view_service', login_url='c_login')
def C_service_category(request, ser):
    category = serviceCategory.objects.get(name=ser)
    service = Service.objects.filter(category=category)
    return render(request, "C_service.html", {'service':service,'category':category})

@permission_required('ETS_app.view_technician', login_url='c_login')
def C_technician(request):
    technician = Technician.objects.filter(status=True).order_by('-create_at')
    paginator = Paginator(technician, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'C_technician.html', {"technician":page_obj})

@permission_required('ETS_app.view_technician', login_url='c_login')
def search_by6(request):
    search = request.GET.get('search')
    if search:
        technician = Technician.objects.filter(
            Q(full_name__icontains=search) |
            Q(occupation__name__icontains=search),
            status=True
        )
        paginator = Paginator(technician, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'C_technician.html', {'technician': page_obj})
    else:
        technician = Technician.objects.filter(status=True).order_by('-create_at')
        paginator = Paginator(technician, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'C_technician.html', {'technician': page_obj})

@permission_required('ETS_app.change_customer', login_url='c_login')
def C_profile_edit(request,id):
    if request.method == "GET":
        customer = Customer.objects.get(id=id)
        return render(request,"C_base.html",{'customer':customer})
    if request.method == "POST":
        customer = Customer.objects.get(id=id)
        if request.FILES.get('image'):
            customer.image.delete()
            customer.image = request.FILES.get('image')
        customer.save()
        messages.success(request, "Profile photo has been uploaded")
        return redirect('/ets/c_home')

@permission_required('ETS_app.delete_customer', login_url='c_login')
def C_account_delete(request,post_e):
    order = Order.objects.get(c_email = post_e)
    if order:
        order.c_status = False
        order.save()
        customer = Customer.objects.get(email=post_e)
        if customer:
            customer.image.delete()
            customer.delete()
            user1 = User.objects.get(email=post_e)
            if user1:
                user1.delete()
                messages.success(request,"Your account has been deleted successfully")
                return redirect('/c_login')

@permission_required('ETS_app.view_technician', login_url='c_login')      
def C_technician_select(request,post_id):
    service = Service.objects.get(id=post_id)
    technician = Technician.objects.all()
    return render(request,"C_technician_select.html",{'technician':technician,'service':service})

@permission_required('ETS_app.add_order', login_url='c_login')
def C_order_create(request,post_id,t_id):
    if request.method == "GET":
        service = Service.objects.get(id=post_id)
        technician = Technician.objects.get(id=t_id)
        return render(request,"C_order.html",{'service':service,'technician':technician})
    if request.method == "POST":
        service = Service.objects.get(id=post_id)
        technician = Technician.objects.get(id=t_id)
        order = Order.objects.create(
            service = request.POST.get('service'),
            price = request.POST.get('price'),
            c_name = request.POST.get('c_name'),
            t_name = request.POST.get('t_name'),
            c_email = request.POST.get('c_email'),
            t_email = request.POST.get('t_email'),
            t_phone = request.POST.get('t_phone'),
            c_phone = request.POST.get('c_phone'),
            c_address = request.POST.get('c_address'),
            order_date = request.POST.get('order_date'),
            create_at = datetime.now(),
        )
        order.save()
        messages.success(request,"Service has been ordered!Please wait reply from technician")
        return redirect('/ets/c_home')

@permission_required('ETS_app.view_order', login_url='c_login')
def C_order_list(request,post_e):
    order = Order.objects.filter(Q(c_status=True) & Q(c_email=post_e)).order_by('-create_at')
    paginator = Paginator(order, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'C_order_list.html', {'order': page_obj})

@permission_required('ETS_app.view_order', login_url='c_login')
def C_order_detail(request,post_id):
    order = Order.objects.get(id=post_id)
    return render(request, "C_order_detail.html",{'order':order})

@login_required(login_url='c_login')
def C_order_delete(request,id):
    order = Order.objects.get(id = id)
    order.c_status = False
    order.save()
    messages.success(request,"Order has been deleted")
    return redirect(f'/ets/c_order/list/{order.c_email}')

@permission_required('ETS_app.add_review', login_url='c_login')
def C_review_create(request):
    if request.method == "GET":
        return render(request,"C_review.html")
    if request.method == "POST":
        review = Review.objects.create(
            name = request.POST.get('name'),
            email = request.POST.get('email'),
            phone = request.POST.get('phone'),
            message = request.POST.get('message'),
            status = False,
            create_at = datetime.now(),
        )
        review.save()
        messages.success(request,"Review has been sent")
        return redirect('/ets/c_review/create')

# --> main
# service

@permission_required('ETS_app.add_service', login_url='m_login')
def M_service_add(request):
    if request.method == "GET":
        category = serviceCategory.objects.all()
        return render(request, "M_service_add.html", {'category':category})
    if request.method == "POST":
        service = Service.objects.create(
            category_id = request.POST.get('category'),
            name = request.POST.get('name'),
            price = request.POST.get('price'),
            description = request.POST.get('description'),
            image = request.FILES.get('image'),
            create_at = datetime.now(),
        )
        service.save()
        messages.success(request,"Service creates successfully!")
        return redirect('/ets/m_service/list/')

@permission_required('ETS_app.view_service', login_url='m_login')
def M_service_list(request):
    category = serviceCategory.objects.all()
    service = Service.objects.all().order_by('-create_at')
    paginator = Paginator(service, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'M_service_lists.html', {"service":page_obj,'category':category})

@permission_required('ETS_app.view_service', login_url='m_login')
def search_by(request):
    search = request.GET.get('search')
    if search:
        service = Service.objects.filter(
            Q(category__name__icontains=search) |
            Q(name__icontains=search) |
            Q(id__icontains=search) |
            Q(price__icontains=search)
        )
        paginator = Paginator(service, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'M_service_lists.html', {'service': page_obj})
    else:
        service = Service.objects.all().order_by('-create_at')
        paginator = Paginator(service, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'M_service_lists.html', {'service': page_obj})
    
@permission_required('ETS_app.view_service', login_url='m_login')
def M_service_detail(request,post_id):
    service = Service.objects.get(id=post_id)
    return render(request,'M_service_detail.html',{'service':service})

@permission_required('ETS_app.change_service', login_url='m_login')
def M_service_edit(request, post_id):
    if request.method == "GET":
        category = serviceCategory.objects.all()
        service = Service.objects.get(id=post_id)
        return render(request, "M_service_edit.html",{'service':service,'category':category})
    if request.method == "POST":
        service = Service.objects.get(id=post_id)
        service.name = request.POST.get('name')
        service.price = request.POST.get('price')
        service.category_id = request.POST.get('category')
        service.description = request.POST.get('description')
        if request.FILES.get('image'):
            service.image.delete()
            service.image = request.FILES.get('image')
        service.save()
        messages.success(request,"Service has been edited successfully.")
        return redirect('/ets/m_service/list/')
    
@permission_required('ETS_app.delete_service', login_url='m_login')
def M_service_delete(request,post_id):
    service = Service.objects.get(id=post_id)
    service.image.delete()
    service.delete()
    messages.info(request, "Service has been deleted successfully.")
    return redirect('/ets/m_service/list/')

# M_customer_list

@permission_required('ETS_app.view_customer', login_url='m_login')
def M_customer_list(request):
    customer = Customer.objects.all().order_by('-create_at')
    paginator = Paginator(customer, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'M_customer_lists.html', {"customer":page_obj})

@permission_required('ETS_app.view_customer', login_url='m_login')
def search_by1(request):
    search = request.GET.get('search')
    if search:
        customer = Customer.objects.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search)
        )
        paginator = Paginator(customer, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'M_customer_lists.html', {'customer': page_obj})
    else:
        customer = Customer.objects.all().order_by('-create_at')
        paginator = Paginator(customer, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'M_customer_lists.html', {'customer': page_obj})

# technician list & register

@permission_required('ETS_app.view_technician', login_url='m_login')
def M_technician_list(request):
    technician = Technician.objects.filter(status=True).order_by('-create_at')
    paginator = Paginator(technician, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'M_technician_lists.html', {"technician":page_obj})

@permission_required('ETS_app.view_technician', login_url='m_login')
def search_by2(request):
    search = request.GET.get('search')
    if search:
        technician = Technician.objects.filter(
            Q(full_name__icontains=search) |
            Q(occupation__name__icontains=search),
            status=True
        )
        paginator = Paginator(technician, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'M_technician_lists.html', {'technician': page_obj})
    else:
        technician = Technician.objects.filter(status=True).order_by('-create_at')
        paginator = Paginator(technician, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'M_technician_lists.html', {'technician': page_obj})
    
@permission_required('ETS_app.view_technician', login_url='m_login')
def M_technician_register_list(request):
    technician = Technician.objects.filter(status=False).order_by('-create_at')
    paginator = Paginator(technician, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'M_technician_register_lists.html', {"technician":page_obj})

@permission_required('ETS_app.view_technician', login_url='m_login')
def search_by3(request):
    search = request.GET.get('search')
    if search:
        technician = Technician.objects.filter(
            Q(full_name__icontains=search) |
            Q(occupation__name__icontains=search),
            status=False
        )
        paginator = Paginator(technician, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'M_technician_register_lists.html', {'technician': page_obj})
    else:
        technician = Technician.objects.filter(status=False).order_by('-create_at')
        paginator = Paginator(technician, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'M_technician_register_lists.html', {'technician': page_obj})

@permission_required('ETS_app.view_technician', login_url='m_login')  
def M_technician_detail(request,post_id):
    technician = Technician.objects.get(id=post_id)
    return render(request,'M_technician_detail.html',{'technician':technician})

@permission_required('ETS_app.delete_technician', login_url='m_login')
def M_technician_delete(request,post_e):
    order = Order.objects.get(c_email=post_e)
    if order:
        order.t_status = False
        order.status = "reject"
        order.save()
        technician = Technician.objects.get(email=post_e)
        if technician:
            technician.image.delete()
            technician.delete()
            user1 = User.objects.get(email=post_e)
            if user1:
                user1.delete()
                messages.info(request, "Technician has been deleted successfully.")
                return redirect('/ets/m_technician/list/')

@permission_required('ETS_app.delete_technician', login_url='m_login')
def M_technician_register_delete(request,post_e):
    technician = Technician.objects.get(email=post_e)
    if technician:
        technician.image.delete()
        technician.delete()
        user1 = User.objects.get(email=post_e)
        if user1:
            user1.delete()
            messages.info(request, "Technician Register has been deleted successfully.")
            return redirect('/ets/m_technician/register/list/')

@login_required(login_url='m_login')  
def M_technician_employee(request,id):
    technician = Technician.objects.get(id = id)
    technician.status = True
    technician.save()
    messages.success(request,f"{technician.full_name} has been employeed")
    return redirect('/ets/m_technician/list/')

# employee list & register

@permission_required('ETS_app.view_main', login_url='m_login')
def M_employee_list(request):
    main = Main.objects.filter(status=True).order_by('-create_at')
    paginator = Paginator(main, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'M_employee_lists.html', {"main":page_obj})

@permission_required('ETS_app.view_main', login_url='m_login')
def search_by4(request):
    search = request.GET.get('search')
    if search:
        main = Main.objects.filter(
            Q(name__icontains=search) |
            Q(occupation__name__icontains=search),
            status=True
        )
        paginator = Paginator(main, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'M_employee_lists.html', {'main': page_obj})
    else:
        main = Main.objects.filter(status=True).order_by('-create_at')
        paginator = Paginator(main, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'M_employee_lists.html', {'main': page_obj})
    
@permission_required('ETS_app.view_main', login_url='m_login')
def M_employee_register_list(request):
    main = Main.objects.filter(status=False).order_by('-create_at')
    paginator = Paginator(main, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'M_employee_register_lists.html', {"main":page_obj})

@permission_required('ETS_app.view_main', login_url='m_login')
def search_by5(request):
    search = request.GET.get('search')
    if search:
        main = Main.objects.filter(
            Q(name__icontains=search) |
            Q(occupation__name__icontains=search),
            status=False
        )
        paginator = Paginator(main, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'M_employee_register_lists.html', {'main': page_obj})
    else:
        main = Main.objects.filter(status=False).order_by('-create_at')
        paginator = Paginator(main, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'M_employee_register_lists.html', {'main': page_obj})

@permission_required('ETS_app.delete_main', login_url='m_login')
def M_employee_delete(request,post_e):
    main = Main.objects.get(email=post_e)
    if main:
        main.image.delete()
        main.delete()
        user1 = User.objects.get(email=post_e)
        if user1:
            user1.delete()
            messages.info(request, "Employee has been deleted successfully.")
            return redirect('/ets/m_employee/list/')

@permission_required('ETS_app.delete_main', login_url='m_login')
def M_employee_register_delete(request,post_e):
    main = Main.objects.get(email=post_e)
    if main:
        main.image.delete()
        main.delete()
        user1 = User.objects.get(email=post_e)
        if user1:
            user1.delete()
            messages.info(request, "Employee Register has been deleted successfully.")
            return redirect('/ets/m_employee/register/list/')
        
@login_required(login_url='m_login')
def M_employee_employee(request,id):
    main = Main.objects.get(id = id)
    main.status = True
    main.save()
    messages.success(request,f"{main.name} has been employeed")
    return redirect('/ets/m_employee/list/')

# category add

@permission_required('ETS_app.add_servicecategory', login_url='m_login')
def M_service_category(request):
    if request.method == "GET":
        category = serviceCategory.objects.filter().order_by('name')
        paginator = Paginator(category, 7)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "M_service_category.html",{'category':page_obj})
    if request.method == "POST":
        category = serviceCategory.objects.create(
            name = request.POST.get('name'),
            image = request.FILES.get('image'),
        )
        category.save()
        messages.success(request,"Service Category has been created")
        return redirect('/ets/m_service/category')

@permission_required('ETS_app.delete_servicecategory', login_url='m_login')
def M_service_category_delete(request,post_id):
    category = serviceCategory.objects.get(id=post_id)
    category.image.delete()
    category.delete()
    messages.info(request, "Service Category has been deleted successfully.")
    return redirect('/ets/m_service/category')

@permission_required('ETS_app.add_m_occupation', login_url='m_login')
def M_technician_occupation(request):
    if request.method == "GET":
        occupation = M_Occupation.objects.filter().order_by('name')
        paginator = Paginator(occupation, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "M_technician_occupation.html",{'occupation':page_obj})
    if request.method == "POST":
        occupation = M_Occupation.objects.create(
            name = request.POST.get('name'),
        )
        occupation.save()
        messages.success(request,"Technician-Occupation-Category has been created")
        return redirect('/ets/m_technician/occupation')

@permission_required('ETS_app.delete_m_occupation', login_url='m_login')
def M_technician_occupation_delete(request,post_id):
    occupation = M_Occupation.objects.get(id=post_id)
    occupation.delete()
    messages.info(request,"Technician-Occupation-Category has been deleted successfully.")
    return redirect('/ets/m_technician/occupation')

# order
@permission_required('ETS_app.view_order', login_url='m_login')
def M_order_list(request):
    order = Order.objects.all()
    return render(request,"M_order_list.html",{'order':order})

@permission_required('ETS_app.view_order', login_url='m_login')
def M_order_detail(request,post_id):
    order = Order.objects.get(id=post_id)
    return render(request,"M_order_detail.html",{'order':order})

@permission_required('ETS_app.delete_order', login_url='m_login')
def M_order_delete(request,post_id):
    order = Order.objects.get(id=post_id)
    order.delete()
    messages.success(request,"Order have been deleted")
    return redirect('/ets/m_order/list')

@permission_required('ETS_app.view_order', login_url='m_login')
def search_by7(request):
    search = request.GET.get('search')
    if search:
        order = Order.objects.filter(
            Q(status__icontains=search) |
            Q(f_status__icontains=search)
        )
        paginator = Paginator(order, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'M_order_list.html', {'order': page_obj})
    else:
        order = Order.objects.all().order_by('-create_at')
        paginator = Paginator(order, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'M_orderlist.html', {'order': page_obj})

@permission_required('ETS_app.view_review', login_url='m_login')  
def M_technician_review(request):
    review = Review.objects.filter(status=True).order_by('-create_at')
    paginator = Paginator(review, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'M_technician_review.html', {'review': page_obj})

@permission_required('ETS_app.view_review', login_url='m_login')
def M_customer_review(request):
    email = Customer.objects.filter()
    review = Review.objects.filter(status=False).order_by('-create_at')
    paginator = Paginator(review, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'M_customer_review.html', {'review': page_obj})

@permission_required('ETS_app.delete_review',login_url='m_login')
def M_review_delete(request,id):
    review = Review.objects.get(id=id)
    review.delete()
    if review.status == False:
        messages.success(request,"Customer Review have been deleted")
        return redirect('/ets/m_customer/review')
    else:
        messages.success(request,"Technician Review have been deleted")
        return redirect('/ets/m_technician/review')
    
@permission_required('ETS_app.delete_review',login_url='m_login')
def M_review_detail(request,id):
    review = Review.objects.get(id=id)
    return render(request,"M_review_detail.html",{'review':review})