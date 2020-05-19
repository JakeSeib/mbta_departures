from django.shortcuts import render

# Create your views here.
import jsonapi_requests
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
    schedule_response = schedule_endpoint.get(params={'filter[stop]': 'place-north', 'include': 'prediction'})
    prediction_endpoint = api.endpoint('/predictions')
    prediction_response = prediction_endpoint.get(params={'filter[stop]': 'place-north'})

    context = {
    'schedule_full_response': schedule_response,
    'prediction_data': prediction_response.data,
    }

    return render(request, 'departure_board/index.html', context)
