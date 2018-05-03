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

# Import models
from .models import Memo, MemoCategory

def index(request):
    # If user is not signed in
    if not request.user.is_authenticated:
        return render(request, 'tools/login.html')

    # If user is signed in, get their info
    context = {
        'user': request.user
    }

    # Return index page
    return render(request, 'tools/index.html', context)

def loginView(request):
    if request.method == 'GET':
        return render(request, 'tools/login.html')

    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'tools/login.html', {'message': 'Invalid credentials.'})

def register(request):
    if request.method == 'GET':
        return render(request, 'tools/register.html')

    if request.method == 'POST':
        # Error check user input
        username = request.POST['username'].strip()
        if User.objects.filter(username=username).exists():
            return render(request, 'tools/register.html', {'message': 'Username already exists.'})

        # Process user input
        else:
            firstName = request.POST['firstName'].strip()
            lastName = request.POST['lastName'].strip()
            email = request.POST['emailAddress'].strip()
            password = request.POST['password']

            # Save user in database
            user = User.objects.create_user(username, email, password)
            user.first_name = firstName
            user.last_name = lastName
            user.save()

            # Create default memo categories for the new user
            category = MemoCategory(userID=user.pk, name='Important')
            category.save()
            category = MemoCategory(userID=user.pk, name='Work')
            category.save()
            category = MemoCategory(userID=user.pk, name='School')
            category.save()

            return HttpResponseRedirect(reverse('index'))

def logoutView(request):
    logout(request)
    return render(request, 'tools/login.html', {'message': 'Logged out.'})

# Default calendar is the current month's, hence the 'date' argument
def cal(request, date=str(datetime.date.today())):
    # Create calendar
    htmlCalendar = calendar.HTMLCalendar()
    day = datetime.datetime.strptime(date, '%Y-%m-%d')
    cal = htmlCalendar.formatmonth(day.year, day.month, withyear=True)
    cal = cal.replace('class="mon"', 'class="day"')
    cal = cal.replace('class="tue"', 'class="day"')
    cal = cal.replace('class="wed"', 'class="day"')
    cal = cal.replace('class="thu"', 'class="day"')
    cal = cal.replace('class="fri"', 'class="day"')
    cal = cal.replace('class="sat"', 'class="day"')
    cal = cal.replace('class="sun"', 'class="day"')
    cal = cal.replace('class="noday"', 'class="day"')

    # Get first day of last month (format is 'yyyy-mm-dd...')
    previousMonthDate = (day.replace(day=1) - datetime.timedelta(1)).replace(day=1)
    # Convert previous month's date to string
    previousDate = previousMonthDate.strftime('%Y-%m-%d')
    # Get first day of next month (format is 'yyyy-mm-dd...')
    nextMonthDate = (day.replace(day=calendar.monthrange(day.year, day.month)[1]) + \
        datetime.timedelta(1)).replace(day=1)
    # Convert next month's date to string
    nextDate = nextMonthDate.strftime('%Y-%m-%d')

    # Create context to pass to template
    context = {
        'cal': mark_safe(cal),
        'previousDate': previousDate,
        'nextDate': nextDate
    }

    # Return Calendar page
    return render(request, 'tools/calendar.html', context)

def addMemo(request):
    if request.method == 'POST':
        # Get name from form
        name = request.POST.get('name').strip()

        # Get category from form
        category = request.POST.get('category').strip()
        if MemoCategory.objects.filter(userID=request.user.id, name=category).exists():
            # User selected a category
            category = MemoCategory.objects.get(userID=request.user.id, name=category)
        else:
            # User did not select a category
            category = None

        # Get date from form; do validity checks and necessary conversions
        date = request.POST.get('date')
        validDate = None
        try:
            date = datetime.datetime.strptime(date, '%m/%d/%Y')
        except ValueError:
            validDate = False
        if validDate is False:
            return render(request, 'tools/memoDetails.html', { \
                'message': "ERROR: Please enter a date in 'mm/dd/yyyy' format."
            })

        # Get times from form (if any) and do necessary conversions and checks
        startTime = request.POST.get('startTime')
        validTime = None
        try:
            startTime = datetime.datetime.strptime(startTime, '%H:%M')
        except ValueError:
            validTime = False
        if validTime is False:
            startTime = None

        endTime = request.POST.get('endTime')
        validTime = None
        try:
            endTime = datetime.datetime.strptime(endTime, '%H:%M')
        except ValueError:
            validTime = False
        if validTime is False:
            endTime = None

        if (startTime != None) and (endTime != None):
            if endTime < startTime:
                return render(request, 'tools/memoDetails.html', { \
                    'message': 'ERROR: End Time cannot be less than Start Time.'
                })

        # Get description from form (if any)
        description = request.POST.get('description').strip()

        # Add data to database
        memo = Memo(name=name , day=date , startTime=startTime, endTime=endTime, \
            description=description, userID=request.user.id, category=category)
        memo.save()

        # Return user to the Calendar page
        return HttpResponseRedirect(reverse('calendar'))

    if request.method == 'GET':
        # Get Memo categories
        memoCategories = MemoCategory.objects.filter(userID=request.user.id)
        context = {
            'categories': memoCategories
        }

        # Direct user to Memo form
        return render(request, 'tools/memoDetails.html', context)

def memoCategoryManager(request, operation):
    if request.method == 'POST':
        if operation == 'add':
            # Get name from form
            name = request.POST.get('name').strip()

            # Validate category name (names are case-sensitive)
            if MemoCategory.objects.filter(userID=request.user.id, name=name).exists():
                # Return error if category already exists
                return render(request, 'tools/memoCategory.html', { \
                    'message': 'Category already exists.'
                })

            # Add category to database if passsed validation checks
            category = MemoCategory(userID=request.user.id, name=name)
            category.save()

            # Return user to the Calendar page
            return HttpResponseRedirect(reverse('calendar'))

        # Allow users to delete categories
        if operation == 'delete':
            # Get name from form
            name = request.POST.get('name').strip()

            # Delete category
            if MemoCategory.objects.filter(userID=request.user.id, name=name).exists():
                MemoCategory.objects.get(userID=request.user.id, name=name).delete()

            # Return user to the Calendar page
            return HttpResponseRedirect(reverse('calendar'))

    if request.method == 'GET':
        # Get Memo categories
        memoCategories = MemoCategory.objects.filter(userID=request.user.id)
        context = {
            'categories': memoCategories
        }

        # Direct user to category manager
        return render(request, 'tools/memoCategory.html', context)

    # TODO: Allow users to add 'communal' categories, e.g., for a communal / social calendar?

# TODO: Allows users to alter their memo's, e.g., change the category, etc.
