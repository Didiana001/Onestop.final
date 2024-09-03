from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Conversation
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from decouple import config

# Configure the API client
genai.configure(api_key=config('GOOGLE_API_KEY'))

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-pro')

# Upload and process the document
file_path = r"C:\Users\QUICK TECH\Desktop\policiestobeuploaded.txt"

try:
    uploaded_file = genai.upload_file(path=file_path, display_name="policiestobeuploaded")
    processed_document = genai.process_document(uri=uploaded_file.uri)
    document_content = processed_document.text
except Exception as e:
    document_content = "Sorry, there was an issue processing the document."

@csrf_exempt
@login_required
def chat_view(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')

        # Combine document content with user prompt
        full_prompt = f"{document_content}\n\nUser Query: {prompt}"
        response = model.generate_content(full_prompt)
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
            # Debugging: print form errors
            print(form.errors)
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
    return redirect('login')  # Redirect to the login page or home page
