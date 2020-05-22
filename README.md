## About
This is a simple Django app to display Commuter Rail departures from North Station in Boston. The app consists of a single web page, hosted [here](http://ec2-18-224-137-245.us-east-2.compute.amazonaws.com/) on an Amazon EC2 instance running an Apache web server.

The MBTA's [V3 API](https://www.mbta.com/developers/v3-api) is used to get and display information for the next 10 upcoming departures from North Station. Typically these will conform to their scheduled times, but if they are predicted to depart late, their new departure times and statuses will be displayed.

Only departures are displayed, as they would be on a departures board in the station itself. Unlike in the station itself though, Amtrak departures are not displayed, since they are not available from the MBTA's API.

The page only pings the API once, on page load. To get up-to-date information, users must refresh the page.

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
To run the app locally, start by installing dependencies as described above and downloading this repository.

After installing the app, navigate to the outermost mbta_departures directory containing manage.py in the terminal and run:

`python manage.py runserver`

Depending on your python installation, you may need to run `python3 manage.py runserver` instead. Then, navigate to http://127.0.0.1:8000/ in a browser to see the board of departures.

## Issues/Improvements
- (In progress) Though available information on commuter rail departures does not change often, the app could refresh automatically. As changes are infrequent, the simplest version of this could just re-ping the API every 60 seconds.
  - While the V3 API does have 'streaming' functionality, this is only available for predictions, not schedules- chosen as the primary resource to take advantage of time filtering on the API. The app would have to be refactored to make predictions the primary resource to utilize streaming. For a larger-scale production app, this would be the desired method of updating and avoiding rate limiting issues.
- The app currently has no styling and could look much better.
  - Arguably, only the times of departures should be shown, not the full date. This should be looked at as part of any larger style pass.
- 10 was chosen semi-arbitrarily as the cutoff for departures to show, to mimic a physical departure board. More information is available than this, though, and it could be displayed as well.
