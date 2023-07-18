
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy

from .forms import NewPostForm
from .models import *
import datetime
from operator import attrgetter
import json



def index(request):
    posts = Post.objects.all().order_by('-id')
    
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {"posts":page_obj})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

@login_required(login_url=reverse_lazy("login"))
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required(login_url=reverse_lazy("login"))
def new_post(request):
    if request.method == "POST":
        username = request.user
        description = request.POST.get('content')
        images = request.FILES.getlist('images')
        post=Post.objects.create(content=description, user=username)
        post.save
        for image in images:
            post_image = PostImage.objects.create(post=post, image=image)
            post_image.save 
        return HttpResponseRedirect(reverse("index"))
    return render(request, "network/newpost.html")

def profile(request, username):        
    if request.method == "POST":
        account = User.objects.get(username=username)
        current_user = request.user
        data = request.POST
        action = data.get("follow")
        if action == "Follow":
            current_user.follows.add(account)
        elif action == "Unfollow":
            current_user.follows.remove(account)
        current_user.save()
    if username in str(User.objects.all()):
        user = User.objects.get(username=username)
        posts = user.posts.all().order_by('-id')

        paginator = Paginator(posts, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'network/profile.html', {'profile': user, 'posts':page_obj})
    else:
        return HttpResponse('User Does not Exist')

@login_required(login_url=reverse_lazy("login"))
def following(request):
    user = request.user
    accounts = user.follows.all()
    posts = []
    for account in accounts:
        posts.extend(account.posts.all())
    res = sorted(posts, key=attrgetter('id'), reverse=True)
    paginator = Paginator(res, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {"posts":page_obj})

@csrf_exempt
@login_required(login_url=reverse_lazy("login"))
def likes(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse(post.serialize())
    
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("likes") != post.likes:
            post.likes = data.get("likes")
        post.save()
        return HttpResponse(status=204)

@login_required(login_url=reverse_lazy("login"))
def edit(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user.is_authenticated and request.user == post.user:
        if request.method == "POST":
            new_content = request.POST.get("content")
            post.content = new_content
            post.save()
            return HttpResponseRedirect(reverse("index"))
        return render(request, "network/edit.html", {"post": post})
    return HttpResponseRedirect(reverse('index'))