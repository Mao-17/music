from celery import shared_task
from .models import MusicFile

@shared_task
def process_music_file(music_file_id):
    music_file = MusicFile.objects.get(id=music_file_id)
    # code to process the music file goes here
    music_file.processed = True
    music_file.save()
