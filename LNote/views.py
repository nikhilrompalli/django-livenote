# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


from django.views.decorators.csrf import csrf_exempt
from LNote.serializers import *
from rest_framework import authentication, permissions


def get_object(self):
    obj = get_object_or_404(self.get_queryset())
    self.check_object_permissions(self.request, obj)
    return obj



class CSRFExemptMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CSRFExemptMixin, self).dispatch(request, *args, **kwargs)

# Create your views here.

def home(request):
    return render(request,'LNote/index.html')

def noteHome(request):
    return render(request,'LNote/note.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})



class notebooks(CSRFExemptMixin, APIView):
    """
       List all snippets, or create a new snippet.
   """

    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):  # retrive all notebook of a user using user id
        id = request.user.id
        list = noteBook.objects.all().filter(user_id=id)
        serializer = NoteBookSerializer(list, many=True)
        # request.method='GET'
        return Response(serializer.data)

    def post(self, request, format=None):  # create a new notebook
        item = request.data
        list = {}
        list["title"] = request.data["title"]
        list["tag"] = request.data["tag"]
        list["user"] = request.user.id
        serializer = NoteBookSerializer(data=list)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class notebookDetails(CSRFExemptMixin, APIView):   #nb by id
        """
            List all snippets, or create a new snippet.
            """

        authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication]
        permission_classes = (permissions.IsAuthenticated,)

        def get(self, request, pk, format=None):  # accessing the nb based on nb id
            nb = noteBook.objects.all().filter(id=pk)
            serializer = NoteBookSerializer(nb, many=True)
            return Response(serializer.data)


        def put(self, request, pk, format=None):  # updating noteBoook by nb id
            nb = noteBook.objects.get(pk=pk)
            data = request.data
            newData = {}
            newData['user'] = request.user.id
            newData["title"] = data["title"]
            newData["tag"] = data["tag"]
            serializer = NoteBookSerializer(nb, data=newData)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        def delete(self, request, pk, format=None):  # deleting notebook by nb id
            nb = noteBook.objects.get(pk=pk)
            nb.delete()
            return Response(status=status.HTTP_201_CREATED)


class notebook(CSRFExemptMixin, APIView):  # nb by id
    """
        List all snippets, or create a new snippet.
        """

    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):  # accessing the nb based on nb id
        notes = note.objects.all().filter(notebook__id=pk)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    def post(self, request,pk, format=None):  # create a new notebook
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class noteContent(CSRFExemptMixin,APIView):
    """
            List all snippets, or create a new snippet.
            """

    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request,pk, format=None):             #retrive note details using note id
        Note = note.objects.all().filter(pk=pk)
        serializer = NoteSerializer(Note, many=True)
        return Response(serializer.data)

    def put(self, request,pk, format=None):             #update note details using note id

        Note=note.objects.get(pk= pk)
        data=request.data
        newData = {}
        newData['text'] = data['text']
        newData['tag']=data['tag']
        newData['title']=data['title']
        newData['notebook']=data['notebook']
        serializer = NoteSerializer(Note,data=newData)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):  # deleting note using note id
        Note = note.objects.get(pk= pk)
        Note.delete()
        return Response(status=status.HTTP_201_CREATED)


class allUsers(CSRFExemptMixin, APIView):  # nb by id
    """
        List all snippets, or create a new snippet.
        """

    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):  # accessing the nb based on nb id
        users = User.objects.exclude(id=request.user.id)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class AllsharedNotes(CSRFExemptMixin, APIView):  # nb by id
    """
        List all snippets, or create a new snippet.
        """

    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):  # accessing the nb based on nb id
        Note = sharedNote.objects.all()
        serializer = SharedNoteSerializer(Note, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):  # create a new notebook
        note = {}
        res=(User.objects.filter(id=request.user.id)).values("username")
        userName=res[0]["username"]
        note["title"] = request.data["title"]
        note["text"] = request.data["text"]
        sharedByName=User.objects.filter(id=request.user.id)
        note["sharedById"] = request.user.id
        note["sharedByName"] = userName
        note["sharedWithId"] = request.data["sharedWithId"]
        note["note"] = request.data["note"]
        serializer = SharedNoteSerializer(data=note)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class sharedNotesOfUser(CSRFExemptMixin, APIView):
    """
        List all snippets, or create a new snippet.
        """

    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):  # accessing the nb based on nb id
        Note = sharedNote.objects.filter(sharedWithId=request.user.id)
        serializer = SharedNoteSerializer(Note, many=True)
        return Response(serializer.data)

class sharedNoteById(CSRFExemptMixin, APIView):
    """
        List all snippets, or create a new snippet.
        """

    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request,pk, format=None):  # accessing the nb based on nb id
        Note = sharedNote.objects.filter(id=pk)
        serializer = SharedNoteSerializer(Note, many=True)
        return Response(serializer.data)
