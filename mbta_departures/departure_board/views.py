from django.shortcuts import render

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

    api = jsonapi_requests.Api.config({
        'API_ROOT': 'https://api-v3.mbta.com',
        'VALIDATE_SSL': False,
        'TIMEOUT': 1,
        # 'api_key': 'TODO: insert an api_key here',
    })

    schedule_endpoint = api.endpoint('/schedules')
    schedule_response = schedule_endpoint.get(params={
        'filter[stop]': 'place-north',
        'include': 'trip,prediction',
        'sort': 'departure_time',
        'filter[min_time]': f'{curr_time.hour}:{curr_time.minute}',
        })
    included_dict = sort_included(schedule_response.content.included)
    schedule_data = get_display_schedules(schedule_response.data, included_dict)

    context = {
    'schedule_data': schedule_data[0:10],
    'included_trips': included_dict['trips'],
    'included_predictions': included_dict['predictions'],
    }

    return render(request, 'departure_board/index.html', context)
