# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from board.models import Board, Topic, Post

admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(Post)