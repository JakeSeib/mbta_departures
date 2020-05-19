from django.http import Http404
from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse
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

    prediction_endpoint = api.endpoint('/predictions')
    prediction_response = prediction_endpoint.get(params={'filter[stop]': 'place-north'})

    context = {
    'prediction_data': prediction_response.data,
    }

    return render(request, 'departure_board/index.html', context)
