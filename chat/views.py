from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import typing_extensions as typing
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Conversation
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm




# class Response(typing.TypedDict):
#   response_item: str
genai.configure(api_key='AIzaSyASINCqIKiWdWEcmz3_Ij-u3ELqSSnBPDQ')
# Initialize the model
model = genai.GenerativeModel('gemini-1.5-pro',
                            #   generation_config={"response_mime_type": "application/json",
                            #                      "response_schema": list[Response]}
                            )

@csrf_exempt
@login_required
def chat_view(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        response = model.generate_content(prompt)
        bot_response = response.text

        # Save the conversation to the database
        conversation = Conversation(user=request.user, user_input=prompt, bot_response=bot_response)
        conversation.save()

        return JsonResponse({'response': bot_response})

    # Retrieve user-specific conversations
    conversations = Conversation.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'chat/index.html', {'conversations': conversations})




def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'chat/signup.html', {'form': form})


def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('chat')  # Redirect to the index page after login
    else:
        form = AuthenticationForm()
    return render(request, 'chat/login.html', {'form': form})

def custom_logout_view(request):
    logout(request)
    return render(request, 'chat/logout.html') # Redirect to the index page after logout