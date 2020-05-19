from django.shortcuts import render

# Create your views here.
import jsonapi_requests
from .utils.filters import is_commuter_rail
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def index(request):
    api = jsonapi_requests.Api.config({
        'API_ROOT': 'https://api-v3.mbta.com',
        'VALIDATE_SSL': False,
        'TIMEOUT': 1,
        # 'api_key': 'todo: insert an api_key here',
    })

    schedule_endpoint = api.endpoint('/schedules')
    schedule_response = schedule_endpoint.get(params={'filter[stop]': 'place-north', 'include': 'prediction', 'sort': 'departure_time'})
    prediction_endpoint = api.endpoint('/predictions')
    prediction_response = prediction_endpoint.get(params={'filter[stop]': 'place-north', 'filter[route_type]': '2'})

    context = {
    'schedule_data': filter(is_commuter_rail, schedule_response.data),
    'included_predictions': filter(is_commuter_rail, schedule_response.content.included),
    }

    return render(request, 'departure_board/index.html', context)
