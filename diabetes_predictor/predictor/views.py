from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
import  pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def home(request):
    if request.method == 'POST':
        if 'signup' in request.POST:
            # Sign Up Form Submission
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Username already exists.")
                elif User.objects.filter(email=email).exists():
                    messages.error(request, "Email already exists.")
                else:
                    user = User.objects.create_user(username=username, email=email, password=password1)
                    user.save()
                    messages.success(request, "Your account has been created. You can now log in!")
            else:
                messages.error(request, "Passwords do not match.")
            return redirect('home')

        elif 'login' in request.POST:
            # Login Form Submission
            username = request.POST['login_username']
            password = request.POST['login_password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('predict')
            else:
                messages.error(request, "Invalid username or password.")
            return redirect('home')

    return render(request, 'home.html')
def predict(request):
    return render(request,'predict.html')
def result(request):
    data = pd.read_csv('/Users/faizan/Documents/diabetes.csv')
    X = data.drop("Outcome", axis=1)
    Y = data['Outcome']
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
    model = LogisticRegression()
    model.fit(X_train, Y_train)

    # Use POST instead of GET if the form method is POST
    value1 = float(request.POST.get('n1', 0))
    value2 = float(request.POST.get('n2', 0))
    value3 = float(request.POST.get('n3', 0))
    value4 = float(request.POST.get('n4', 0))
    value5 = float(request.POST.get('n5', 0))
    value6 = float(request.POST.get('n6', 0))
    value7 = float(request.POST.get('n7', 0))
    value8 = float(request.POST.get('n8', 0))

    pred = model.predict([[value1, value2, value3, value4, value5, value6, value7, value8]])

    result1 = "POSITIVE" if pred == [1] else "NEGATIVE"
    
    return render(request, 'predict.html', {"result1": result1})
