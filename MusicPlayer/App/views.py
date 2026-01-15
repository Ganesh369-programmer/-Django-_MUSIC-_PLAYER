from django.shortcuts import render , redirect
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required


from django.core.paginator import Paginator
from .models import Song

from django.contrib.auth.models import User
import os
import yt_dlp
from django.conf import settings
# Create our views here.

def download_playlist(url, user):
    user_folder = os.path.join(settings.MEDIA_ROOT, 'music', str(user))
    os.makedirs(user_folder, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{user_folder}/%(title).200s.%(ext)s',
        'ignoreerrors': True,
        'writethumbnail': True,
        'postprocessors': [
            {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'},
            {'key': 'EmbedThumbnail'},
            {'key': 'FFmpegMetadata'},
        ],
        'noplaylist': False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=True)
    
    



def extract_entries(info):
    """
    Always return a list of entries
    """
    if 'entries' in info:
        return [e for e in info['entries'] if e]
    else:
        return [info]


def save_songs_to_db(info, user):
    entries = extract_entries(info)

    for entry in entries:
        try:
            file_path = entry['requested_downloads'][0]['filepath']
        except (KeyError, IndexError):
            continue

        if not os.path.exists(file_path):
            continue

        relative_path = os.path.relpath(file_path, settings.MEDIA_ROOT)

        # Avoid duplicates
        Song.objects.get_or_create(
            user=user,
            title=entry.get('title', 'Unknown'),
            defaults={
                'artist': entry.get('uploader', ''),
                'file': relative_path,
                'duration': entry.get('duration')
            }
        )


@login_required(login_url='/login')
def index(request ):
    
    return render(request , "base.html")


@login_required(login_url='/login')
def player(request):
    songs = Song.objects.filter(user=request.user)
    return render(request, 'player.html',{'songs' : songs} )


@login_required(login_url='/login')
def download(request):
    if request.method == 'POST':
        url = request.POST.get('url')

        info = download_playlist(url, request.user)
        
        save_songs_to_db(info, request.user)

        return redirect('player')
    
    return render(request , 'download.html')



def register(request):
    p_msg = ""
    if request.method =='POST':
        fnm = request.POST.get('username')
        emailid = request.POST.get('email')
        pwd = request.POST.get('password')
        pwd1 = request.POST.get('confirmPassword')

        if pwd == pwd1:
            my_user = User.objects.create_user(fnm , emailid , pwd)
            my_user.save()
            return redirect('/login')
        else:
            return render(request, 'register.html', {
                'p_msg': 'Passwords do not match'
            })
        

    return render(request , 'register.html')


def loginn(request):
    if request.method == 'POST':
        fnm = request.POST.get('username')
        pwd = request.POST.get('password')

        userr = authenticate(request , username=fnm , password=pwd)

        if userr is not None:
             login(request , userr)
             return redirect('/')
        else:
            msg = "Passward is wrong or Username is Wrong" 
            return render(request , 'loginn.html' , {'msg' : msg})

    return render(request , 'loginn.html')

def delete(request , id ):
    s = Song.objects.get(id=id)

    if s.file:
        if(os.path.isfile(s.file.path)):
            os.remove(s.file.path)


    s.delete()
    return redirect('/player')


def logoutt(request):
    logout(request)
    return redirect('/login')