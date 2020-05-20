from .filters import is_commuter_rail

def sort_included(included_coll):
    """Given all included items, filter out non-commuter rail items and sort
    the remainer into stops, trips, and predictions."""
    included_dict = {'trips': [], 'predictions': []}
    for el in included_coll:
        if is_commuter_rail(el):
            included_dict[el.type + 's'].append(el)
    return included_dict
