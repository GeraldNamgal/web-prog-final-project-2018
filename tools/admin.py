from django.contrib import admin
from .models import Memo, MemoCategory

admin.site.register(Memo)
admin.site.register(MemoCategory)
