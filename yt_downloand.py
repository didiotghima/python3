from pytube import YouTube

url = input("URL: ")
type_obj = input('mp3, mp4: ')
yt = YouTube(url)
if type_obj == "mp4":
    yt.streams.filter(progressive=True, file_extension='mp4').first().download()
elif type_obj == "mp3":
    yt.streams.filter(only_audio=True).first().download('audio', f'{yt.title}.mp3')
print("Скачано")

