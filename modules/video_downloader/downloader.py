import yt_dlp

class VideoDownloader:
    def get_video_info(self, url):
        with yt_dlp.YoutubeDL() as ydl:
            return ydl.extract_info(url)

    def download_video(self, url):
        with yt_dlp.YoutubeDL() as ydl:
            ydl.download([url])

    def download_audio_only(self, url):
        options = {'format': 'bestaudio'}
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])

    def get_downloaded_files(self):
        # Logic to return a list of downloaded files
        pass