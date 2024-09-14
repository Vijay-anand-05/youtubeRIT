from django.db import models
from django.contrib.auth.models import User
import os

# Predefined category choices
CATEGORY_CHOICES = [
    ('NeotericAI', 'NeotericAI'),
    ('ASI Inauguration', 'ASI Inauguration'),
    ('RIT Promo', 'RIT Promo'),
    ('FDP', 'FDP'),
    ('Program', 'Program'),
    ('Webinar', 'Webinar'),
    ('Testimonials', 'Testimonials'),
    ('Subject Lecture', 'Subject Lecture'),
    ('Data Structures', 'Data Structures'),
    ('RIT-AD & Histos Conf.', 'RIT-AD & Histos Conf.'),
]

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    youtube_url = models.URLField()
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_youtube_thumbnail_url(self):
        video_id = self.youtube_url.split('v=')[-1]
        return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

