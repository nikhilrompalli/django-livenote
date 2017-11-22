from django.conf.urls import url
from LNote import views

urlpatterns=[

    url(r'^notebooks/$',views.notebooks.as_view(),name='Notebooks_List'),          #list of all notebooks
    url(r'^notebookDetails/(?P<pk>[0-9]+)/$',views.notebookDetails.as_view(),name='Notebook'),
    url(r'^notebook/(?P<pk>[0-9]+)/$',views.notebook.as_view(),name='Notebook'),
    url(r'^note/(?P<pk>[0-9]+)/$',views.noteContent.as_view(),name='note'),
    url(r'^allUserDetails/',views.allUsers.as_view(),name='note'),
    url(r'^allSharedNotes/',views.AllsharedNotes.as_view(),name='note'),
    url(r'^sharedNoteById/(?P<pk>[0-9]+)/$',views.sharedNoteById.as_view(),name='note'),
    url(r'^sharedNotesOfUser/',views.sharedNotesOfUser.as_view(),name='note'),
    url(r'^Home/$',views.home,name='home'),
    url(r'^Home/note$',views.noteHome,name='homeNotes'),

]


