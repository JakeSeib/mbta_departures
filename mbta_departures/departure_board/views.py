from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.template import loader

# Create your views here.
import jsonapi_requests
from datetime import datetime

from .utils.filters import is_commuter_rail
from .utils.fields import get_display_schedules
from .utils.sorting import sort_included
# import the logging library
# import logging

# Get an instance of a logger
# logger = logging.getLogger(__name__)

def index(request):
    curr_time = datetime.now().time()
    curr_hour, curr_minute = curr_time.hour, curr_time.minute
    if curr_hour < 10:
        # mbta's v3 api states that between midnight and 3am is considered
        # part of the previous calendar day, and a time of >24 hours should
        # be used
        if curr_hour < 3:
            curr_hour += 24
        else:
            curr_hour = f'0{curr_hour}'
    if curr_minute < 10:
        curr_minute = f'0{curr_minute}'

    api = jsonapi_requests.Api.config({
        'API_ROOT': 'https://api-v3.mbta.com',
        'VALIDATE_SSL': False,
        'TIMEOUT': 1,
        'api_key': settings.API_KEY,
    })

    schedule_endpoint = api.endpoint('/schedules')
    schedule_response = schedule_endpoint.get(params={
        'filter[stop]': 'place-north',
        'include': 'trip,prediction',
        'sort': 'departure_time',
        'filter[min_time]': f'{curr_hour}:{curr_minute}',
        })
    included_dict = sort_included(schedule_response.content.included)
    schedule_data = get_display_schedules(schedule_response.data, included_dict)

    context = {
    # Could show more schedules than this if mimicking a real departure board
    # isn't desired
    'schedule_data': schedule_data[0:10],
    'included_trips': included_dict['trips'],
    'included_predictions': included_dict['predictions'],
    'django_debug': str(settings.DEBUG),
    }

    # ajax requests, i.e. from static js files in the app, return a JSON object
    # with the html for the table
    if request.is_ajax():
        table_template = loader.get_template('departure_board/table.html')
        return JsonResponse({'table_html': table_template.render(context, request)})
    else:
        return render(request, 'departure_board/board.html', context)
