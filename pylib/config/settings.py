'''

Per name component:

* absence_penalty: Degree to which match ratio is decreased if this component is missing
* initials_weight': Degree to which match ratio is increased if this component matches only as an initial
* prefix_weight': Degree to which match ratio is increased if this component matches only as a prefix
* weight': Contribution of this component's match ratio to the overall

Global to setting:

* threshold: Minimum ratio before name is considered a match

'''

DEFAULT_SETTINGS = {
    'given': {
        'initials_weight': 0.5,
        'prefix_weight': 0.7,
        'weight': 3,
    },
    'particle': {
        'initials_weight': 0.5,
        'prefix_weight': 0.7,
        'weight': 1,
    },
    'familial': {
        'initials_weight': 0.5,
        'prefix_weight': 0.7,
        'weight': 5,
    },
    'check_nickname': True,
    'threshold': 0.7,
}

# FIXME NEED TO UPDATE OTHER SETTINGS

STRICT_SETTINGS = {
    'first': {
        'absence_penalty': True,
        'initials_weight': False,
        'prefix_weight': False,
        'weight': 3,
    },
    'middle': {
        'absence_penalty': False,
        'initials_weight': False,
        'prefix_weight': False,
        'weight': 2,
    },
    'last': {
        'absence_penalty': True,
        'initials_weight': False,
        'prefix_weight': False,
        'weight': 5,
    },
    'check_nickname': False,
    'threshold': 0.7,
}

LENIENT_SETTINGS = {
    'first': {
        'absence_penalty': False,
        'initials_weight': True,
        'prefix_weight': True,
        'weight': 3,
    },
    'middle': {
        'absence_penalty': False,
        'initials_weight': True,
        'prefix_weight': True,
        'weight': 2,
    },
    'last': {
        'absence_penalty': True,
        'initials_weight': True,
        'prefix_weight': False,
        'weight': 5,
    },
    'check_nickname': True,
    'threshold': 0.7,
}
