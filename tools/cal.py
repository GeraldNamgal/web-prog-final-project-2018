from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.apps import apps
import datetime
from django.db.models import Q
import calendar
from django.utils.safestring import mark_safe

# Import your models
from .models import Memo, MemoCategory

# Code referenced from: https://alexpnt.github.io/2017/07/15/django-calendar/

# Create a calendar class that overrides the HTMLCalendar
class Cal(calendar.HTMLCalendar):
    def __init__(self, monthDay, userID, selectedCategory):
        super(Cal, self).__init__()
        self.monthDay = monthDay
        self.userID = userID
        self.selectedCategory = selectedCategory

    def formatday(self, day, weekday):
        # Add memo links to the day (if any)
        if MemoCategory.objects.filter(userID=self.userID, name=self.selectedCategory).exists():
            memosForDay = Memo.objects.filter(userID=self.userID, day__day=day, day__month=self.monthDay.month, \
                day__year=self.monthDay.year, category__name__contains=self.selectedCategory)
        # Return all memos by default (if category is not specified / is 'All')
        else:
            memosForDay = Memo.objects.filter(userID=self.userID, day__day=day, day__month=self.monthDay.month, \
                day__year=self.monthDay.year)
        memosHTML = '<ul class="dayMemos">'
        for memo in memosForDay:
            # Add memo link to day on calendar
            url = reverse(viewname='memo', kwargs={'monthDay':(self.monthDay).strftime('%Y-%m-%d'), \
                'memoID': memo.pk, 'selectedCategory': self.selectedCategory})
            if memo.category is not None:
                memosHTML += f'<li class="dayMemo {memo.category.name}"><a href={url}>{memo.name}</a></li>'
            else:
                memosHTML += f'<li class="dayMemo"><a href={url}>{memo.name}</a></li>'
        memosHTML += '</ul>'

        if day == 0:
            # For days that aren't in the current month
            return '<td class="noday"></td>'
        else:
            return '<td class="%s">%d%s</td>' % (self.cssclasses[weekday], day, memosHTML)

    def formatweek(self, theweek):
        htmlString = ''.join(self.formatday(day, weekday) for (day, weekday) in theweek)
        return '<tr>%s</tr>' % htmlString

    def formatmonth(self, theyear, themonth, withyear=True):
        htmlList = []
        htmlList.append('<table border="0" cellpadding="0" cellspacing="0" class="month">')
        htmlList.append(self.formatmonthname(theyear, themonth, withyear=withyear))
        htmlList.append(self.formatweekheader())
        # Add each week's table data including memos (if any)
        for week in self.monthdays2calendar(theyear, themonth):
            htmlList.append(self.formatweek(week))
        htmlList.append('</table>')
        return ''.join(htmlList)

    # Returns first day of last month (a datetime object with format 'yyyy-mm-dd...')
    def getPrevMonthDate(self):
        return (self.monthDay.replace(day=1) - datetime.timedelta(1)).replace(day=1)

    # Returns first day of next month (a datetime object with format 'yyyy-mm-dd...')
    def getNextMonthDate(self):
        return (self.monthDay.replace(day=calendar.monthrange(self.monthDay.year, self.monthDay.month)[1]) \
            + datetime.timedelta(1)).replace(day=1)
