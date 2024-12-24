from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def signup(request): 
    if request.method == 'POST': 
        firstname = request.POST['firstname'] 
        lastname = request.POST['lastname'] 
        email = request.POST['email'] 
        password = request.POST['password'] 
        confirmpassword = request.POST['confirmpassword'] 
        errors = {} 
        
        if password != confirmpassword: 
            errors['confirmpassword'] = 'Passwords do not match' 

        if User.objects.filter(username=email).exists(): 
            errors['email'] = 'Email is already registered' 

        if errors: 
            return render(request, 'signup.html', {'errors': errors, 'firstname': firstname, 'lastname': lastname, 'email': email}) 
            
        user = User.objects.create_user(username=email, first_name=firstname, last_name=lastname, password=password) 
        user.save() 
        messages.success(request, 'Account created successfully') 
        return redirect('signin') 
    return render(request, 'signup.html')

def signin(request): 
    error_msg = None 
    if request.method == 'POST': 
        username = request.POST['email'] 
        password = request.POST['password'] 
        user = authenticate(request, username=username, password=password)
        
        if user is not None: 
            login(request, user) 
            messages.success(request, 'You have successfully signed in') 
            return redirect('home')
        else: 
            error_msg = 'Invalid email or password' 
    
    return render(request, 'signin.html', {'error_msg': error_msg})

def signout(request):
    logout(request)
    return redirect('signin')