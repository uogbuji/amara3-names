from copy import deepcopy

from amara3.names.model import human_name
from amara3.names.config import SETTINGS
from amara3.names.utils import deep_update_dict
from amara3.names.utils import normalize, namelist_possibilities


def ratio(fullname1, fullname2, strictness='default', options=None):
    """
    Takes two single names and returns ratio expressing likelihood they describe the same person.
    Uses difflib's sequence matching on a per-field basis for names

    :param string fullname1: first human name
    :param string fullname2: second human name
    :param string strictness: strictness settings to use
    :param dict options: custom strictness settings updates
    :return float: sequence ratio match (0-1.0)
    
    >>> from amara3.names import compare as namecompare
    >>> namecompare.ratio('Uche Ogbuji', 'Uchenna Ogbuji')
    0.8781818181818182
    >>> namecompare.ratio('Uche Ogbuji', 'Uche Ogbuji')
    1.0
    >>> namecompare.ratio('Tom, Dick and Harry', 'Harry, Tom Dick')
    0.43000000000000005
    >>> namecompare.ratio('Tom, Dick, and Harry', 'Harry, Tom Dick') #One looks like a list
    0.0
    >>> namecompare.ratio('Uche Ogbuji', '') #One is empty
    0.0
    """

    if options is not None:
        settings = deepcopy(SETTINGS[strictness])
        deep_update_dict(settings, options)
    else:
        settings = SETTINGS[strictness]

    namelists1 = namelist_possibilities(normalize(fullname1))
    namelists2 = namelist_possibilities(normalize(fullname2))
    
    #If either is empty, or looks like a list of multiple names, return ratio of 0
    if len(namelists1) == 0 or len(namelists2) == 0 or len(namelists1) > 2 or len(namelists2) > 2:
        return 0.0

    ratios = []
    for ns1 in namelists1:
        if len(ns1) != 1: continue
        for ns2 in [n for n in namelists2 if len(n) == 1]:
            if len(ns2) != 1: continue
            n1 = human_name.parse(ns1[0])
            n2 = human_name.parse(ns2[0])
            ratios.append(n1.ratio_deep_compare(n2, settings))

    #print(namelists1, namelists2, ratios, settings)
    return max(ratios, default=0.0)

