from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.urls import reverse
from django.contrib import messages
from .models import Messages, FriendList, Handle
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='login')
def home(request):
    friend_requests = Handle.objects.filter(receiver=request.user, is_active=True)
    friends = FriendList.objects.all()
    amount = friend_requests.count()
    context = {"friend_requests": friend_requests, "amount": amount, "friends": friends}

    if request.method == "POST":
        #users = User.objects.get(username=request.POST.get('search'))
        User = get_user_model()
        searched_user = request.POST.get('search')
        users = User.objects.filter(username__icontains=searched_user)
        
        try:
            if users:
                return redirect(reverse('results', kwargs={'pk': users[0].username}))
        except User.DoesNotExist:
                return redirect(reverse('results', kwargs={'pk': 'none'}))

        
    return render(request, 'base/index.html', context)


@login_required(login_url='login')
def results(request, pk):
    User = get_user_model()
    users = User.objects.get(username=pk)
    last_login = users.last_login if users.last_login else "Inactive"
    context = {"user": users, "last_login": last_login}



    if request.method == "POST":
            try:
                # Get the logged-in user
                logged_in_user = request.user

                # Get the receiver user
                receiver = users

                # Create a friend request
                friend_request = Handle(sender=logged_in_user, receiver=receiver)
                friend_request.save()
                
                # Optionally, you can provide a success message to the user
                context['success_message'] = "Friend request sent successfully!"

                # Redirect the user back to the home page
                return redirect('home')
            except Exception as e:
                # Handle any exceptions that occur and provide an appropriate error message
                context['error_message'] = f"Failed to send friend request: {str(e)}"

    return render(request, 'base/result.html', context)


def login(request):
    if request.method == "POST":
        print(request.user.username)
        assigned_username = request.POST.get('username')
        assigned_password = request.POST.get('password')
        print("username:", assigned_username)
        print("password:", assigned_password)

        user = authenticate(request, username=assigned_username, password=assigned_password)
        if user is not None:
            # Authentication successful, log in the user
            auth_login(request, user)
            return redirect('home')
        else:
            # Authentication failed
            print("authentication failed")
            messages.error(request, 'Invalid username or password')

    return render(request, 'base/login.html')



def sign(request):
    User = get_user_model()

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email =  request.POST.get('email')

        try:
            user = User.objects.get(username=username, password=password, email=email)
        except:
            messages.error(request, 'User already exist')
        
        user = authenticate(username=username, password=password)

        if user is None:
            new_user = User.objects.create(username=username, password=password,email=email)
            new_user.save()
            return redirect('/login')
        else:
            return redirect('/login')
    return render(request, 'base/signup.html')



def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return redirect('login')

    return render(request, 'base/logout.html')

def add_back(request, pk):
    User = get_user_model()
    sender = User.objects.get(username=pk)
    receiver = request.user

    if request.method == "POST":
        try:
            sender_friend_list = FriendList.objects.get(user=sender)
        except FriendList.DoesNotExist:
            sender_friend_list = FriendList.objects.create(user=sender)

        friend_request = Handle.objects.filter(sender=sender, receiver=receiver, is_active=True).first()
        if friend_request:
            friend_request.accept()

        return redirect('home')

    context = {"user": sender}
    return render(request, 'base/add.html', context)


def msg(request, pk):
    User = get_user_model()
    receiver = User.objects.get(username=pk)
    sender = request.user
    sent_messages = Messages.objects.filter(user=sender, receiver=receiver)
    received_messages = Messages.objects.filter(user=receiver, receiver=sender)
    messages = sent_messages | received_messages  # Combine sent and received messages
    new_messages = messages.order_by('created')

    if request.method == "POST":
        message = request.POST.get('msg')
        send = Messages.objects.create(user=sender, receiver=receiver, message=message)
        print("Message sent!")
        send.save()

    context = {"messages": new_messages}

    return render(request, 'base/msg.html', context)