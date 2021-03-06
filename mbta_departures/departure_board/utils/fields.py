from dateutil.parser import isoparse
from .filters import is_commuter_rail

def add_prediction_fields(schedule, predictions):
    """Given a schedule and included predictions, add a display_time property to
    the schedule, selecting the time that should be used for sorting/displaying
    to customers.

    Predicted time should be checked first. arrival_time should be used over
    departure_time. No departure_time indicates that the stop should not be displayed, and the
    schedule will be given a display_time of None.

    If a matching prediction is found, also add its status to the schedule."""
    prediction = None
    if schedule.relationships['prediction']:
        id_to_match = schedule.relationships['prediction'].data.id
        for x in predictions:
            if id_to_match == x.id:
                prediction = x
                break

    # if there is no departure_time in either the schedule or the prediction,
    # assign a display_time of None (last stop)
    if not schedule.attributes['departure_time']:
        if (not prediction) or (not prediction.attributes['departure_time']):
            schedule.attributes['display_time'] = None
            return schedule
    # otherwise, assign the appropriate display_time
    if prediction:
        iso_time = prediction.attributes['arrival_time'] or prediction.attributes['departure_time']
        status = prediction.attributes['status']
        predicted_track = prediction.relationships['stop'].data.id
        # if predicted_track.startswith('North Station-'):
        track_num = prediction.relationships['stop'].data.id[14:] or 'TBD'
    else:
        iso_time = (schedule.attributes['arrival_time'] or schedule.attributes['departure_time'])
        status = 'On time'
        track_num = 'TBD'
    display_time = isoparse(iso_time)
    schedule.attributes['display_time'] = display_time
    schedule.attributes['status'] = status
    schedule.attributes['track_num'] = track_num
    return schedule

def add_trip_fields(schedule, trips):
    """Given a schedule and included trips, add the train number and headsign
    to the scheudle from its associated trip."""
    for trip in trips:
        if trip.id == schedule.relationships['trip'].data.id:
            schedule.attributes['train_num'] = trip.attributes['name']
            schedule.attributes['headsign'] = trip.attributes['headsign']
    return schedule

def check_add_schedule(schedule, included_dict, commuter_schedules):
    """Given a schedule, a dict with included data for trips and predictions,
    and a list of commuter rail schedules, add relevant fields to that
    schedule and add it to the list if it is a relevant schedule to display
    (i.e. north station is not its last stop)"""
    add_prediction_fields(schedule, included_dict['predictions'])
    if schedule.attributes['display_time']:
        add_trip_fields(schedule, included_dict['trips'])
        commuter_schedules.append(schedule)

def get_display_schedules(schedule_data, included_dict):
    """Given schedule data and a dict with included data for trips and
    predictions, filter out irrelevant schedules (non-commuter rail, no further
    stops beyond N station) and return schedules with necessary information to
    display on the departure board."""
    commuter_schedules = []
    for schedule in schedule_data:
        if is_commuter_rail(schedule):
            check_add_schedule(schedule, included_dict, commuter_schedules)
    return sorted(commuter_schedules, key = lambda x: x.attributes['display_time'])
