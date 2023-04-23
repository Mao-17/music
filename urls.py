from django.urls import path
from .views import home, upload_music_file, view_music_file, AccessMusicFileView

urlpatterns = [
    path('', home, name='home'),
    path('upload/', upload_music_file, name='upload_music_file'),
    path('music-file/<int:pk>/', view_music_file, name='view_music_file'),
    path('music-file/<int:pk>/access/', AccessMusicFileView.as_view(), name='access_music_file'),
]
