import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

def add_display_time(schedule, prediction=None):
    schedule.attributes['display_time'] = (schedule.attributes['arrival_time'] or schedule.attributes['departure_time'])
    return schedule

def add_display_times(schedule_data, predictions=None):
    """Given schedule data and, if they exist, their associated predictions,
    add a display_time property to each schedule object, selecting the time that
    should be used for sorting/displaying to customers. Predicted time should be
    checked first. arrival_time should be used over departure_time."""
    # todo: check if there is an associated prediction for each schedule item,
    # and if so pass it to add_display_time along with the schedule item
    return list(map(lambda x: (add_display_time(x)), schedule_data))
