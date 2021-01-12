# for Admin
from django.shortcuts import render, HttpResponseRedirect
from .forms import StudentRegistration
from .models import User

# For API GET information 
from rest_framework.response import Response
from django.shortcuts import render

from .serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view

@api_view(['GET'])
def user_api(request, pk=None):
    if request.method == 'GET':
        id = pk
        # id = request.data.get('id')
        if id is not None:
            student_api = User.objects.get(id=id)
            serializer = UserSerializer(student_api)
            return Response(serializer.data)

        student_api = User.objects.all()
        serializer = UserSerializer(student_api, many = True)
        return Response(serializer.data)


# For Admin Post the user information into the database
def add_show(request):
    if request.method == 'POST':
        fm = StudentRegistration(request.POST)
        if fm.is_valid():
            nm = fm.cleaned_data['name']
            em = fm.cleaned_data['email']
            pw = fm.cleaned_data['password']
            reg = User(name=nm, email=em, password=pw)
            reg.save()
            # fm.save()
            fm = StudentRegistration()
    else:
        fm = StudentRegistration()
    stud = User.objects.all()
    return render(request, 'enroll/addandshow.html', {'form':fm,'stu':stud})

# Update And Edit
def update_data(request, id):
    if request.method =='POST':
        pi = User.objects.get(pk=id)
        fm = StudentRegistration(request.POST, instance = pi)
        if fm.is_valid():
            fm.save()
    else:
        pi = User.objects.get(pk=id)
        fm = StudentRegistration(instance = pi)        
    return render(request, 'enroll/updatestudent.html', {'form': fm})


# For Delete Data
    
def delete_data(request, id):
    if request.method == 'POST':
        dlt = User.objects.get(pk=id)
        dlt.delete()
        return HttpResponseRedirect('/')