def is_commuter_rail(schedule):
    return schedule.relationships['route'].data.id.startswith('CR-')
