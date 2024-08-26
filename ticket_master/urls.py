from django.urls import path
from ticket_notes.views import homepage_view, bookmark_event, edit_note, delete_bookmark, bookmarks_view

urlpatterns = [
    path('', homepage_view, name='index'),
    path('bookmark_event/',bookmark_event, name='bookmark_event'),
    path('edit_note/<int:bookmark_id>/', edit_note, name='edit_note'),
    path('delete_bookmark/<int:bookmark_id>/', delete_bookmark, name='delete_bookmark'),
    path('bookmarks/', bookmarks_view, name='bookmarks'),
]

