from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views import View

from .models import MusicFile
from .forms import MusicFileForm

@login_required
def home(request):
    user = request.user
    user_music_files = user.music_files.all()
    public_music_files = MusicFile.objects.filter(access='public').exclude(user=user)
    protected_music_files = MusicFile.objects.filter(access='protected', allowed_users=user)

    context = {
        'user_music_files': user_music_files,
        'public_music_files': public_music_files,
        'protected_music_files': protected_music_files,
    }
    return render(request, 'music_sharing_portal/home.html', context)

@login_required
def upload_music_file(request):
    if request.method == 'POST':
        form = MusicFileForm(request.POST, request.FILES)
        if form.is_valid():
            music_file = form.save(commit=False)
            music_file.user = request.user
            music_file.save()
            messages.success(request, 'Music file uploaded successfully!')
            return redirect('home')
    else:
        form = MusicFileForm()

    context = {
        'form': form,
    }
    return render(request, 'music_sharing_portal/upload_music_file.html', context)

@login_required
def view_music_file(request, pk):
    music_file = get_object_or_404(MusicFile, pk=pk)

    if music_file.access == 'public':
        # Allow access to all users
        pass
    elif music_file.access == 'private':
        # Allow access only to the user who uploaded the file
        if music_file.user != request.user:
            raise PermissionDenied
    else:
        # Allow access to the users who have been granted access
        if request.user not in music_file.allowed_users.all():
            raise PermissionDenied

    file_data = open(music_file.file.path, 'rb').read()
    response = HttpResponse(file_data, content_type='audio/mpeg')
    response['Content-Disposition'] = 'inline; filename=' + music_file.title + '.mp3'

    return response

class AccessMusicFileView(View):
    def post(self, request):
        music_file_pk = request.POST.get('music_file_pk')
        music_file = get_object_or_404(MusicFile, pk=music_file_pk)

        if music_file.access != 'protected':
            # Only protected music files can be accessed using email
            raise PermissionDenied

        email = request.POST.get('email')
        if not email:
            messages.error(request, 'Please provide a valid email address')
            return redirect('home')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'No user found with the provided email address')
            return redirect('home')

        if user != request.user and user not in music_file.allowed_users.all():
            music_file.allowed_users.add(user)

        return redirect('home')
