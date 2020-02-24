from django.shortcuts import render , redirect
from django.http import HttpResponse 
from .models import CurrentChat , Chat
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
from django.contrib.auth import login as auth_login , logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q


#to fix

# user cant send himself messages

def homepage(request):
    
    #searching 
    if request.method == 'POST':
        search_ = request.POST.get('search')
        result = User.objects.filter(Q(username=search_)) 
        if result and (result[0] != '' and result[0] != request.user) and (str(result[0]) not in [i.user for i in CurrentChat.objects.filter(for_user = request.user)]):
            result = User.objects.filter(Q(username=search_))[0]
            to_save = CurrentChat(user = result , for_user = request.user)
            to_save.save()
        else:
            return HttpResponse('User not found or the user is already connected !')

    #main
    try:
        all_conn = list(CurrentChat.objects.filter(for_user = request.user))
        context = {'connect' : all_conn}
    except:
        context = {}
    return render(request , 'ChatApp/homepage.html', context)

@login_required(login_url = 'http://127.0.0.1:8000/login')
def chat(request , user1):

    #saving messages

    if request.method == 'POST':
        msg = request.POST.get('text')
        to_send = Chat(sender =request.user, message = msg , reciever = user1)
        to_send.save()
        return redirect(f'http://127.0.0.1:8000/chat/{user1}')
    
    #displaying message

    message1 = (Chat.objects.filter(sender = request.user , reciever = user1) | Chat.objects.filter(sender = user1 , reciever = request.user)).order_by('date_time')
    all_msg = [i.message for i in message1]
    datetime = [i.date_time for i in message1]
    senders = [i.sender for i in message1]
    chats = zip(all_msg,datetime,senders)
    context = {'chat' : chats , 'message' : all_msg}
    return render(request , 'ChatApp/chat.html' , context)


def login(request):
    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        auth_login(request , user)
        messages.success(request , f'Successfully logged in as {form.cleaned_data["username"]}')
        return redirect('homepage')
    context = {'form' : form}
    return render(request , 'ChatApp/login.html' , context)


def logout(request): 
    auth_logout(request)
    return render(request , 'ChatApp/logout.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request , f'Successfully created an account for {form.cleaned_data["username"]}')
            return redirect('homepage')
    else:
        form = UserCreationForm()
    context = {'form':form}
    return render(request , 'ChatApp/register.html' , context)

def contact(request):
    return render(request , 'ChatApp/contact.html')