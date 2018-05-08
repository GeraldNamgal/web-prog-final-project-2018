from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.loginView, name='login'),
    path('logout', views.logoutView, name='logout'),
    path('register', views.register, name='register'),
    path('<str:monthDay>/<str:selectedCategory>/addMemo', views.addMemo, name='addMemo'),
    # For 'operation' I used 'add', 'delete', or None
    path('<str:monthDay>/<str:selectedCategory>/<str:operation>/memoCategoryManager', views.memoCategoryManager, name='memoCategoryManager'),
    path('calendar', views.cal, name='calendarToday'),
    path('<str:date>/calendar', views.cal, name='calendarDate'),
    path('<str:date>/<str:selectedCategory>/calendar', views.cal, name='calendarState'),
    path('<str:monthDay>/<int:memoID>/<str:selectedCategory>/memo', views.memo, name='memo'),
    path('<str:monthDay>/<str:selectedCategory>/viewMemos', views.viewMemos, name='viewMemos'),
    path('deleteMemo', views.deleteMemo, name='deleteMemo')
]
