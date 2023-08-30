from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from django.forms import ModelForm
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from requests.auth import HTTPBasicAuth
import requests
# from .models import StoryEntry
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from .forms import *
from .models import *


# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(
            username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Username or password is incorrect!'})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(username=request.POST['username'])
                return render(request, 'register.html', {'error': 'Username is already taken!'})
            except User.DoesNotExist:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'], first_name=request.POST['first_name'], last_name=request.POST['last_name'])
                auth.login(request, user)
                return redirect('index')
        else:
            return render(request, 'register.html', {'error': 'Password does not match!'})
    else:
        return render(request, 'register.html')

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect(index)
    else:
        return redirect(index)

def profile_user(request):
    check_user_login(request)

    stories = storyHistory.objects.filter(user_id=request.user.id)

    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        
        if len(request.POST['password1']) > 0:
            if request.POST['password1'] == request.POST['password2']:
                user.password = make_password(request.POST['password1'])
            else:
                return render(request, 'profile.html', {'error': 'Password does not match!'})
            
        user.save()
        return logout_user(request)
    
    else:
        return render(request, 'profile.html', {'stories' : stories})


def check_user_login(request):
    if not request.user.is_authenticated:
        return redirect(index)

# def search_story(request):

#     if request.method == "POST":
#         form = SearchStoryForm(request.POST)

#         if form.is_valid():
#             your_name = form.cleaned_data["your_name"]
#             your_friend_name = form.cleaned_data["your_friend_name"]
#             story_you_want = form.cleaned_data["story_you_want"]
#             story = generate_story(your_name, your_friend_name, story_you_want)
#             return render(request, 'index.html', {"form": form, "story": story})
#     else:
#         form = SearchStoryForm()
#         return render(request, 'index.html', {"form": form})

def search_story(request):
    check_user_login(request)

    your_name = ""
    your_friend_name = ""
    story = ""

    if request.method == "POST":
        your_name = request.POST.get("your_name")
        your_friend_name = request.POST.get("your_friend_name")
        story_you_want = request.POST.get("story_you_want")

        if your_name and your_friend_name and story_you_want:
            story = generate_story(your_name, your_friend_name, story_you_want)
            userobj = User.objects.get(id=1)
            # saving the story
            history_entry = storyHistory(
                user_id=userobj,
                name=your_name,
                friend_name=your_friend_name,
                story_topic=story_you_want,
                generated_story=story
            )
            history_entry.save()

            return render(request, 'search.html', {"your_name": your_name, "your_friend_name": your_friend_name, "story_you_want": story_you_want, "story": story})

    return render(request, 'search.html')

def generate_story(name, friend, story):
    base_url = "https://vicuna-api.aieng.fim.uni-passau.de/v1"
    auth_token = "1"
    endpoint = "/chat/completions"
    url = base_url + endpoint

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system","content": f"Create a child friendly story using protagonist:{name}, friend's name:{friend}, and on the topic:{story}. Do not have violent words in the story and let it have a good moral message."},
        ]
    }

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        return response_data['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}, Response: {response.text}"

def get_story():
    name = "rat"
    friend = "lamp"
    story = "blueberry"
    
    story = generate_story(name, friend, story)
    print("Story:", story)

def custom_404(request, exception):
    return render(request, '404.html', status=404)