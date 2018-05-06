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

# Import your own miscellaneous things
from .cal import Cal

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
            return render(request, 'tools/login.html', {'message': 'ERROR: Invalid credentials.'})

def register(request):
    if request.method == 'GET':
        return render(request, 'tools/register.html')

    if request.method == 'POST':
        # Error check user input
        username = request.POST['username'].strip()
        if User.objects.filter(username=username).exists():
            return render(request, 'tools/register.html', {'message': 'ERROR: Username already exists.'})

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

def cal(request, date=str(datetime.date.today())):
    # Retrieve calendar (right now we're using HTMLCalendar)
    monthDay = datetime.datetime.strptime(date, '%Y-%m-%d')
    if request.method =='POST':
        selectedCategory = request.POST.get('category')
    else:
        selectedCategory = 'All'
    htmlCalendar = Cal(monthDay, selectedCategory)
    cal = htmlCalendar.formatmonth(monthDay.year, monthDay.month, withyear=True)

    # Modify classes in calendar for formatting, etc.
    cal = cal.replace('class="mon"', 'class="mon dayOfWeek"')
    cal = cal.replace('class="tue"', 'class="tue dayOfWeek"')
    cal = cal.replace('class="wed"', 'class="wed dayOfWeek"')
    cal = cal.replace('class="thu"', 'class="thu dayOfWeek"')
    cal = cal.replace('class="fri"', 'class="fri dayOfWeek"')
    cal = cal.replace('class="sat"', 'class="sat dayOfWeek"')
    cal = cal.replace('class="sun"', 'class="sun dayOfWeek"')
    cal = cal.replace('class="noday"', 'class="noday dayOfWeek"')

    # Get first day of last month (a datetime object with format 'yyyy-mm-dd...')
    previousMonthDate = htmlCalendar.getPrevMonthDate()
    # Convert previous month's date to string
    previousMonthDate = previousMonthDate.strftime('%Y-%m-%d')
    # Get first day of next month (a datetime object with format 'yyyy-mm-dd...')
    nextMonthDate = htmlCalendar.getNextMonthDate()
    # Convert next month's date to string
    nextMonthDate = nextMonthDate.strftime('%Y-%m-%d')

    # Get Memo categories
    memoCategories = MemoCategory.objects.filter(userID=request.user.id)

    # Create context to pass to template
    context = {
        'cal': mark_safe(cal),
        'selectedCategory': selectedCategory,
        'previousMonthDate': previousMonthDate,
        'nextMonthDate': nextMonthDate,
        'memoCategories': memoCategories
    }

    # Return Calendar page
    return render(request, 'tools/calendar.html', context)

def addMemo(request):
    # Get Memo categories
    memoCategories = MemoCategory.objects.filter(userID=request.user.id)

    # Create context to send to template
    context = {
        'categories': memoCategories
    }

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
            context['message'] = "ERROR: Please enter a date in 'mm/dd/yyyy' format."
            return render(request, 'tools/memoDetails.html', context)

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
                context['message'] = 'ERROR: End Time cannot be less than Start Time.'
                return render(request, 'tools/memoDetails.html', context)

        # Get description from form (if any)
        description = request.POST.get('description').strip()

        # Add data to database
        memo = Memo(name=name , day=date , startTime=startTime, endTime=endTime, \
            description=description, userID=request.user.id, category=category)
        memo.save()

        # Return user to the Calendar page
        return HttpResponseRedirect(reverse('calendar'))

    if request.method == 'GET':
        # Direct user to Memo form
        return render(request, 'tools/memoDetails.html', context)

def memoCategoryManager(request, operation):
    # Get Memo categories
    memoCategories = MemoCategory.objects.filter(userID=request.user.id)

    # Create context to send to template
    context = {
        'categories': memoCategories
    }

    if request.method == 'POST':
        if operation == 'add':
            # Get name from form
            name = request.POST.get('name').strip()

            # Validate category name (names are case-sensitive)
            if MemoCategory.objects.filter(userID=request.user.id, name=name).exists():
                # Return error if category already exists
                context['message'] = 'ERROR: Category already exists.'
                return render(request, 'tools/memoCategory.html', context)

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
        # Direct user to category manager
        return render(request, 'tools/memoCategory.html', context)

def memo(request, memoID):
    # Get context to send to template
    if Memo.objects.filter(pk=memoID).exists():
        context = {
            'memo': Memo.objects.get(pk=memoID)
        }

        # Return user to the Memo information page
        return render(request, 'tools/memo.html', context)

    else:
        context = {
            'message': 'ERROR: Memo does not exist.',
            'returnURL': reverse(viewname='calendar')
        }

        return render(request, 'tools/error.html', context)

    # TODO: Allow users to add 'communal' categories, e.g., for a communal / social calendar?

# TODO: Allows users to alter their memo's, e.g., change the category, etc.
