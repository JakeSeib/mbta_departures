![N Station Board](https://upload.wikimedia.org/wikipedia/commons/8/8b/North_Station_departure_board%2C_December_2011.jpg)

## About
This is a simple Django app to display Commuter Rail departures from North Station in Boston. The app consists of a single web page, hosted [here](http://ec2-18-224-137-245.us-east-2.compute.amazonaws.com/) on an Amazon EC2 instance running an Apache web server.

The MBTA's [V3 API](https://www.mbta.com/developers/v3-api) is used to get and display information for the next 10 upcoming departures from North Station. Typically these will conform to their scheduled times, but if they are predicted to depart late, their new departure times and statuses will be displayed.

Only departures are displayed, as they would be on a departures board in the station itself. Unlike in the station itself though, Amtrak departures are not displayed, since they are not available from the MBTA's API.

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

In the base app directory, add a file named `.config.ini` and add the following lines, using your own content for the keys:

```
[DEFAULT]
MY_APP_SECRET_KEY = Your-Key-Goes-Here
MY_APP_API_KEY = Your-Key-Goes-Here
```

Django can generate a secret key for you, with `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`.

Obtaining a valid key for the MBTA's API is free, and can be done by visiting [their API's portal](https://api-v3.mbta.com/).

To enable the static javascript and css files attached to the app to work locally, navigate to `mbta_departures/mbta_departures/settings.py` and change

`DEBUG = False`

to

`DEBUG = True`

After installing the app, navigate to the outermost mbta_departures directory containing manage.py in the terminal and run:

`python manage.py runserver`

Depending on your python installation, you may need to run `python3 manage.py runserver` instead. Then, navigate to http://127.0.0.1:8000/ in a browser to see the board of departures.

## Issues/Improvements
- **Reloading page information**: Currently, the app uses JavaScript to periodically make an AJAX requests to a Django view and manipulate the DOM via jQuery. This would not be the best implementation for a production environment.
  - While the V3 API does have 'streaming' functionality, this is only available for predictions, not schedules- chosen as the primary resource to take advantage of time filtering on the API. The app would have to be refactored to make predictions the primary resource to utilize streaming. For a larger-scale production app, this would be the desired method of updating and avoiding rate limiting issues.
    - Django Channels could be used in conjunction with this method to update the web page whenever a change occurs.
- **Additional station departures**: Although the app is currently hard-coded to look for departures from North Station, it would be relatively simple to add buttons/dropdowns to allow the user to affect the station filter being used in the call to the MBTA's API.
- **Styling**: The app currently has minimal styling and could look much better.
  - Arguably, only the times of departures should be shown, not the full date. This should be looked at as part of any larger style pass.
- **Additional information**: 10 was chosen somewhat arbitrarily as the cutoff for departures to show, to mimic a physical departure board. More information is available than this, though, and it could be displayed as well.
