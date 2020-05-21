## About
This is a simple Django app to display Commuter Rail departures from North Station in Boston.

The MBTA's [V3 API](https://www.mbta.com/developers/v3-api) is used to get and display information for the next 10 upcoming departures from North Station. Typically these will conform to their scheduled times, but if they are predicted to depart late, their new departure times and statuses will be displayed.

Only departures are displayed, as they would be on a departures board in the station itself. Unlike in the station itself though, Amtrak departures are not displayed, since they are not available from the MBTA's API.

The page only pings the API once, on page load. To get up-to-date information, refresh the page.

## Dependencies
- Python 3.8.2
  - See https://www.python.org/downloads/release/python-382/
  - Recommended to use a virtual environment with a tool like [pyenv](https://github.com/pyenv/pyenv)
- Django 3.0.6
  - See https://docs.djangoproject.com/en/3.0/topics/install/
- jsonapi_requests 0.6.1
  - `pip install jsonapi-requests[flask]`
- dateutil 2.8.1
  - `pip install python-dateutil`

## Setup
After installing dependencies and downloading the app, navigate to the mbta_departures directory containing manage.py in the terminal and run:

`python manage.py runserver`

Depending on your python installation, you may need to run `python3 manage.py runserver` instead. Then, navigate to http://127.0.0.1:8000/departure_board/ in a browser to see the board of departures.

## Issues/Improvements
- (In progress) App could be hosted and accessed directly via the web
- (In progress) Django's secret_key should be private, not public
- Though available information on commuter rail departures does not change often, the app could refresh automatically. As changes are infrequent, the simplest version of this could just re-ping the API every 60 seconds or so.
  - While the V3 API does have 'streaming' functionality, this is only available for predictions, not schedules. The app would have to be refactored to make predictions the primary resource to make use of this- and in any case, predictions are not often available for departures from North Station, since it is the first stop and thus experiences the fewest delays.
- The app currently has no styling and could look much better
- To support more concurrent users or quicker page reloads, an API key could be added as an environment variable
