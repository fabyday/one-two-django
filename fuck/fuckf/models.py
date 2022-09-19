from pickle import FALSE
from unicodedata import category
from django.db import models

from django.contrib.auth.models import User, Group


class Post(models.Model):
    title = models.CharField(max_length=256, verbose_name="title")  
    contents = models.TextField(verbose_name="content")
    category = models.ForeignKey("PostCategory", related_name="post", on_delete=models.DO_NOTHING, verbose_name="category")
    author = models.ForeignKey(User, related_name='post', on_delete=models.DO_NOTHING, verbose_name="author")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created_at')
    recently_modified_at = models.DateTimeField(auto_now=True, verbose_name="recently_modified_at")
    visited_at = models.PositiveIntegerField(default=0, verbose_name='visited')
    
    def __str__(self):
        return self.title


    class Meta:
        db_table = "Post"
        verbose_name = "Post"
        


class PostCategory(models.Model):
    parent_category = models.CharField(max_length=256, verbose_name="super_category",default='null', null=True)
    name = models.CharField(max_length=256, verbose_name="category_name")
    created_at = models.DateTimeField(auto_now=True, verbose_name='created_at')
    recently_modified_at = models.DateTimeField(auto_now_add=True, verbose_name='created_at')
    # is_private = models.ForeignKey(Group, related_name="post_category", on_delete=models.DO_NOTHING, verbose_name="category")
    is_private = models.BooleanField(False)

    class Meta:
        db_table="PostCategory"
        verbose_name="PostCategory"
        unique_together = (("parent_category", "name"),) # primary key is (parent_category, name)


    