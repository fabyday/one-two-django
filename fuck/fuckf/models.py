from django.db import models

from django.contrib.auth.models import User, Group



class Post(models.Model):
    title = models.CharField(max_length=256, verbose_name="title")
    contents = models.TextField(verbose_name="content")
    author = models.ForeignKey(User, related_name='post', on_delete=models.DO_NOTHING, verbose_name="author")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created_at')
    recently_modified_at = models.DateTimeField(auto_now_add=True, verbose_name="recently_modified_at")
    visited_at = models.PositiveIntegerField(default=0, verbose_name='visited')
    
    def __str__(self):
        return self.title


    class Meta:
        db_table = "Post"
        verbose_name = "Post"
        
