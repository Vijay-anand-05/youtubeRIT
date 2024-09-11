from django.db import models

class YouTubeVideo(models.Model):
    title = models.CharField(max_length=255)
    video_url = models.URLField()  # Field to store YouTube URL
    description = models.TextField(blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_youtube_id(self):
        # Extract YouTube ID from URL
        if 'v=' in self.video_url:
            return self.video_url.split('v=')[1]
        elif 'youtu.be/' in self.video_url:
            return self.video_url.split('youtu.be/')[1]
        return None

    def get_thumbnail_url(self):
        # Generate thumbnail URL from YouTube ID
        youtube_id = self.get_youtube_id()
        if youtube_id:
            return f'https://img.youtube.com/vi/{youtube_id}/hqdefault.jpg'
        return ''
