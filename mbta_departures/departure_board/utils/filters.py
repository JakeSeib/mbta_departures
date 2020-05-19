def is_commuter_rail(element):
    return element.relationships['route'].data.id.startswith('CR-')
