def add_display_time(schedule, predictions):
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
        display_time = prediction.attributes['arrival_time'] or prediction.attributes['departure_time']
    else:
        display_time = (schedule.attributes['arrival_time'] or schedule.attributes['departure_time'])
    schedule.attributes['display_time'] = display_time
    return schedule

def add_display_times(schedule_data, predictions):
    """Given schedule data and, if they exist, their associated predictions,
    add a display_time property to each schedule object, selecting the time that
    should be used for sorting/displaying to customers.

    Predicted time should be checked first. arrival_time should be used over
    departure_time.

    No departure_time indicates that the stop should not be displayed, and the
    schedule will be given a display_time of None and ignored."""
    display_times_schedules = map(lambda x: (add_display_time(x, predictions)), schedule_data)
    filtered_schedules = filter(lambda x: x.attributes['display_time'], display_times_schedules)
    return sorted(list(filtered_schedules), key = lambda x: x.attributes['display_time'])
