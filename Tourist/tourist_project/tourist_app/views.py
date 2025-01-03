from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from tourist_app.models import places,contact,booking
import razorpay

# Create your views here.
def home_view(request):
    return render(request, 'index.html')


def package_view(request):
    p = places.objects.filter()
    context = {}
    context['places'] = p
    return render(request, 'package.html',context)


def contact_view(request):
    if request.method == 'POST':
        nme = request.POST['cname']
        mail = request.POST['cmail']
        sub = request.POST['csub']
        msge = request.POST['cmsg']

        data = contact.objects.create(name=nme, email=mail, subject=sub, msg=msge)
        data.save()
        return render(request, 'contact.html')
    
    else:
        return render(request, 'contact.html')


def allpackage_view(request):
    p = places.objects.filter()
    context = {}
    context['places'] = p
    return render(request, 'loginpackage.html',context)

def journey_view(request):
    data = booking.objects.filter(uid = request.user.id)
    context = {}
    context['info']=data

    return render(request, 'myjourney.html',context)

def remove_view(request, jid):
    data = booking.objects.filter(id=jid)
    data.delete()
    return redirect('/myjourney')

def payment_view(request, bid):
    if request.user.is_authenticated:
        userid = request.user.id
        u = User.objects.filter(id = userid)
        p = places.objects.filter(id = bid)
        uid = u[0]
        pid = p[0]
        print(uid,pid)
        if request.method == "POST":
            name = request.POST['bname']
            mail = request.POST['bemail']
            number = request.POST['bnum']
            dat = request.POST['bdate']
            msge = request.POST['bmsg']
            add = request.POST['bAdd']
            file = request.FILES.get('bfiles', None)

            data = booking.objects.create(name=name, email=mail, contact=number, date=dat, msg=msge, uid=u[0], pid=p[0], address=add, file=file)
            data.save()
            return redirect('/makepayment')

        else:
            p = places.objects.filter(id = bid)
            context = {}
            context['booking'] = p
            return render(request, 'payment.html', context)

def makepayment_view(request):
    uname = request.user.username
    book = booking.objects.filter(uid = request.user.id)
    for x in book:
        s = x.pid.price
    # books = list[book]
    # x = book.pid.price
    print(s)
    
    tfare = s
    client = razorpay.Client(auth=("rzp_test_RCOnqF2q5cJIsa", "AQeW0Weqw5daVhiwV6yQXSrR"))
    data = { "amount": s*100, "currency": "INR" }
    payment = client.order.create(data=data)
    print(payment)
    context = {}
    context['data']=payment
    context['uname']=uname
    context['totalfare'] = tfare

    return render(request, 'pay.html',context)

# Register Code --------------------------------------------------------------------------------------
def register_view(request):
    if request.method == 'POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        context={}

        if uname=="" or upass=="" or ucpass=="":
            context['errmsg']="Fields Cannot be Empty"
            return render(request, 'register.html',context)
        elif upass != ucpass:
            context['passerr']="password didn't match"
            return render(request,'register.html',context)
        else:
            try:
                u=User.objects.create(username=uname, password=upass, email=uname)
                u.set_password(upass)
                u.save()
                context['success']="User Created Successfully"
                return render(request,'register.html',context)
                # return HttpResponse("User Created Successfully")
            except:
                context['errmsg']="Username already exists"
                return render(request, 'register.html',context)
    
    else:
        return render(request,'register.html')
    

# Login Code --------------------------------------------------------------------------------------
def login_view(request):
    if request.method == 'POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        context={}
        if uname=="" or upass=="":
            context['errmsg']="Fields Cannot be Empty"
            return render(request, 'login.html',context)
        else:    
            u=authenticate(username=uname,password=upass)
            print(u)     
            if u is not None:
                login(request,u)
                # return HttpResponse("Data Fetched")
                return redirect('/allpackages')
            else:
                context['errmsg']="Invalid User"
                return render(request, 'login.html',context)
    else:
        return render(request,'login.html')

def logout_view(request):
    logout(request)
    return redirect('/home')

