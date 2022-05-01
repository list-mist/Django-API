
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.decorators import api_view
from .models import User
from .forms import userForm,EditForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .serializers import UserSerializer, EditSerializer
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics , mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend


@api_view(['POST'])
def AddData(request):
    serializer = UserSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    else:
        msg = "Data not added"
        return Response({"msg":msg})
@api_view(['PUT']) 
def EditData(request):
    serializer = EditSerializer(data = request.data, instance=request.user)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def DRF_view(request):
    data = {}
    try:
        data = UserSerializer(request.user)
        return Response(data.data)
    except:
        data = UserSerializer()
        return Response(data.data)


def register(request):
    if request.method == 'GET':
        form = userForm()

        return render(request,'register.html',{'form':form})
    else:
        form = userForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'register.html',{'form':form,'msg':"You are registered"})
        return render(request,'register.html',{'form':form,'msg':"Try again"})

def loginUser(request):
    msg = ""
    if request.method == "GET":
       form = AuthenticationForm()

       return render(request,'login.html',{"form":form})
    else:
        form=AuthenticationForm(request.POST,data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            request.session['username'] = username
            user = authenticate(username=username,password=password)

            if user is not None:
                login(request,user)
                return redirect('/details/')
            else:
                msg = "Invalid details"
                return render(request,'login.html',{"form":form,"msg":msg})
        else:
            msg = "Require all the fields"
            return render(request,'login.html',{"form":form,"msg":msg})


def logoutUser(request):
    logout(request)
    return redirect('/login/')

def details(request):
    try:
        data = User.objects.get(username = request.session['username'])
        return render(request,'details.html',{"data":data})
    except:
        data = User.objects.get(username = request.user)
        return render(request,'details.html',{"data":data})

def editDetails(request):
    if request.method == "GET":
        form = EditForm(instance = request.user)
        
        return render(request,'edit.html',{"form":form})
    else:
        form = EditForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
        return redirect('/details/')


# class based views

class userList(APIView):
    def get(self,request):
        users = User.objects.all()
        user_serializer = EditSerializer(users, many = True)
        return Response(user_serializer.data)
    
    def post(self,request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        serializer = EditSerializer(data = request.data, instance=User.objects.get(pk = pk))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        user = User.object.get(pk = pk)
        user.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


# class based views using mixins

class userListMixin(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self,request):
        return self.list(request)
    
    def post(self,request):
        return self.create(request)

class userEditMixin(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = EditSerializer

    def put(self,request,pk):
        return self.update(request,pk)
    def delete(self,request,pk):
        return self.destroy(request,pk)

# claas based views using generics

class userListGen(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
class userEditGen(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# class based views using viewset
class userPagination(PageNumberPagination):
    page_size = 1
class userListViewSet(viewsets.ModelViewSet):
   queryset = User.objects.all()
   serializer_class = UserSerializer
   pagination_class = userPagination
   filter_backends = [DjangoFilterBackend]
   filterset_fields = ['username','email']
   