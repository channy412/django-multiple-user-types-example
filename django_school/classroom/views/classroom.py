from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# import os
# import flask
import requests
from django.conf import settings
# import google.oauth2.credentials
# import google_auth_oauthlib.flow
# import googleapiclient.discovery

# from datetime import datetime
# # from urllib import urlencode
# from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login

# from app.models import User
from classroom.models import User
redirect_url = "http://127.0.0.1:8000/google/login/callback/"

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teachers:quiz_change_list')
        else:
            return redirect('students:quiz_list')
    return render(request, 'classroom/home.html')

#"project_id":"project-343322",
# "auth_uri":"https://accounts.google.com/o/oauth2/auth",
# "token_uri":"https://oauth2.googleapis.com/token",
# "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs"

# @login_required
def google_login_request(request):
    print(request)
    # redirect_uri = "%s://%s%s" % (
    #     request.scheme, request.get_host(), reverse('pain:google_login')
    # )
    if('code' in request.GET):
        params = {
            'grant_type': 'authorization_code',
            'code': request.GET.get('code'),
            'redirect_uri': redirect_url,
            'client_id': settings.GP_CLIENT_ID,
            'client_secret': settings.GP_CLIENT_SECRET
        }
        url = 'https://accounts.google.com/o/oauth2/token'
        response = requests.post(url, data=params)
        url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        access_token = response.json().get('access_token')
        print("token")
        print(access_token)
        
        response = requests.get(url, params={'access_token': access_token})
        print("response")
        print(response)
        print(response.headers)
        
        user_data = response.json()
        print(user_data)
        id = user_data.get('id')
        first_name = user_data.get('name', '').split()[0]
        last_name = user_data.get('family_name')
        google_avatar = user_data.get('picture')
        gender = user_data.get('gender', '').lower()
        if id:
            print("google login going well, proceed")
        else:
            print("Warning: Google login failed with code")
            messages.error(
                request,
                'Unable to login with Google Please try again'
            )
            return redirect(url)
    else:
        print("Warning: Google login failed")
        url = "https://accounts.google.com/o/oauth2/auth?client_id=%s&response_type=code&scope=%s&redirect_uri=%s&state=google"
        scope = [
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email"
        ]
        scope = " ".join(scope)
        url = url % (settings.GP_CLIENT_ID, scope, redirect_url)
        return redirect(url)

    if request.user.is_authenticated:
        print("connect google account")
        user_to_connect = request.user
        user_to_connect.google_first_name = first_name
        user_to_connect.google_last_name = last_name
        user_to_connect.google_avatar = google_avatar
        user_to_connect.google_gender = gender
        user_to_connect.google_connected = True
        user_to_connect.google_id = id
        user_to_connect.save()
        messages.success(
            request,
            'Google Account Connected! Yay!'
        )
        return redirect('/')
    else:
        # user = request.user
        print("login with google crediential")
        print(id)
        # print(User.objects.raw())
        print(User.objects.count())
        print(User.objects.all())
        users = User.objects.all()
        
        for u in users:
            print(u)
            print(u.google_id)
            if u.google_id == id:
                print("found user\n")
                username = u.username
                break
        # user, _ = User.objects.get(google_id = id)
        # print("user type")
        # print(type(user))

        user = User.objects.get(username=username)
        print("user")
        print(user.google_id)
        print(user.username)
        
        print(user.google_avatar)
        user.backend = settings.AUTHENTICATION_BACKENDS[0]
        login(request, user)
        messages.success(
            request,
            'Google Account Connected! Yay!'
        )

        # return redirect('/home')

        if user.is_teacher:
            return redirect('/teachers')
        
        else:
            return redirect('/')


