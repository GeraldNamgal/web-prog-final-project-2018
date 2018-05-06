from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.loginView, name='login'),
    path('logout', views.logoutView, name='logout'),
    path('register', views.register, name='register'),
    path('addMemo', views.addMemo, name='addMemo'),
    # For 'operation' I used 'add', 'delete', or None
    path('<str:operation>/memoCategoryManager', views.memoCategoryManager, name='memoCategoryManager'),
    path('calendar', views.cal, name='calendar'),
    path('<str:date>/calendar', views.cal, name='calendarOtherMonth'),
    # Also used 'All' for 'memoCategory' to get all Memo categories
    path('calendar/memoCategory', views.cal, name='changeCalendarView'),
    path('<int:memoID>/memo', views.memo, name='memo')
]
