from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Conversation
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from decouple import config
import google.generativeai as genai
import logging

# Configure logging for debugging purposes
logger = logging.getLogger(__name__)

# Configure the API client
genai.configure(api_key=config('GOOGLE_API_KEY'))

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-pro')

# File path
file_path = r"C:\Users\QUICK TECH\Downloads\Onestop.final-master\Onestop.final-master\chat\Data\Financial_Regulations_2015.pdf"

# Process file content function
def process_file_content():
    try:
        sample_file = genai.documents.upload_file(
            file_path=file_path, 
            display_name="Financial Regulations"
        )
        file = genai.documents.get_file(file_id=sample_file['id'])
        document_content = genai.documents.process_file(file_uri=file['uri'])
        return document_content

    except Exception as e:
        logger.error(f"Error processing file: {e}")
        return "Error processing file"

# Preload document content
document_content = process_file_content()

@csrf_exempt
@login_required
def chat_view(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')

        if not document_content or "Error" in document_content:
            return JsonResponse({'response': "Error: Unable to process document content"})

        full_prompt = f"{document_content}\n\nUser Query: {prompt}"
        try:
            response = model.generate_content(full_prompt)
            bot_response = response['text']

            # Save the conversation to the database
            conversation = Conversation(user=request.user, user_input=prompt, bot_response=bot_response)
            conversation.save()

            return JsonResponse({'response': bot_response})
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return JsonResponse({'response': 'Error generating response'})

    conversations = Conversation.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'chat/index.html', {'conversations': conversations})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'chat/signup.html', {'form': form, 'errors': form.errors})
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
                return redirect('chat')  # Redirect to the chat after login
        return render(request, 'chat/login.html', {'form': form, 'errors': form.errors})
    else:
        form = AuthenticationForm()
    return render(request, 'chat/login.html', {'form': form})

def custom_logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout

# New views for Home, Courses, and Format Guide pages
def index_view(request):
    return render(request, 'chat/index.html')  # Render the index.html as home page

def courses_view(request):
    return render(request, 'chat/courses.html')

def format_guide_view(request):
    return render(request, 'chat/format_guide.html')

# Redirect for AskOneStop button to home page
def askonestop_view(request):
    return redirect('home')


