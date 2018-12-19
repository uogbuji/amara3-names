# -*- coding: utf-8 -*-

import sys
import re
import unicodedata
from difflib import SequenceMatcher
import itertools

from amara3.names.config import STRIPPED_CHARACTERS

STICKY_NAME_PARTS = ['jr', 'sr', 'i', 'ii', 'iii', 'iv', 'iiii', 'v', 'vi', 'vii', 'viii', 'ix', 'x']

NORMALIZE_SPACE_PAT = re.compile(r'\s+', flags=re.MULTILINE)
STRIP_TO_NORMALIZE_PAT = re.compile(r'[^\w, ]')

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def normalize(namestr):
    '''
    >>> from amara3.names.utils import normalize
    >>> normalize('DiCamillo, Kate, Van Dusen, Chris')
    'dicamillo, kate, van dusen, chris'
    >>> normalize('King, Martin Luther, Jr.')
    'king, martin luther, jr'
    '''
    normalized = unicodedata.normalize('NFKD', namestr)
    normalized = NORMALIZE_SPACE_PAT.sub(' ', normalized)
    normalized = STRIP_TO_NORMALIZE_PAT.sub('', normalized)
    return normalized.lower()


def namelist_possibilities(namestr):
    '''
    Warning: it is a good idea to call normalize on any string sent to this function
    
    >>> from amara3.names.utils import normalize, namelist_possibilities
    >>> namelist_possibilities(normalize('DiCamillo, Kate, Van Dusen, Chris'))
    [['dicamillo', 'kate', 'van dusen', 'chris'], ['dicamillo', 'kate', 'van dusen, chris'], ['dicamillo', 'kate, van dusen', 'chris'], ['dicamillo, kate', 'van dusen', 'chris']]
    >>> namelist_possibilities(normalize('Krentz, Jayne Anne'))
    [['krentz', 'jayne anne'], ['krentz, jayne anne']]
    >>> namelist_possibilities(normalize('Uche Ogbuji'))
    [['uche ogbuji']]
    >>> namelist_possibilities(normalize('Ogbuji, Uche'))
    [['ogbuji', 'uche'], ['ogbuji, uche']]
    >>> namelist_possibilities(normalize('King, Martin Luther, Jr.'))
    [['king', 'martin luther, jr'], ['king, martin luther, jr']]
    >>> namelist_possibilities(normalize('Churchill, Winston, 1871-1947'))
    [['churchill', 'winston'], ['churchill, winston']]
    '''
    possibilities = []
    #Divvy up into comma-separated segments, then omit empties & ones e.g. from "1900-1990"
    raw_segments = [ seg.strip() for seg in namestr.split(',') if seg.strip() ]
    raw_segments = [ seg for seg in raw_segments if seg and not seg.isdigit() ]
    segments = []
    skip_next = False
    
    #Any sticky segments, e.g. "jr" or "III"? Stick them back
    for pre, seg in pairwise(raw_segments):
        if skip_next:
            skip_next = False
            continue
        if seg in STICKY_NAME_PARTS:
            segments.append(f'{pre}, {seg}')
            skip_next = True
        else:
            segments.append(pre)
    if raw_segments[-1] not in STICKY_NAME_PARTS: segments.append(raw_segments[-1])

    #Special cases pairwise wouldn't cover
    if len(segments) == 1: return [segments]
    if len(segments) == 2: return [segments, [f'{segments[0]}, {segments[1]}']]

    #Arrange permutations of name with each comma interpreted as inversion as well as separator
    stems = []
    for ix, (segthis, segnext) in enumerate(pairwise(segments)):
        if not stems:
            stems = [[segthis, None], [f'{segthis}, {segnext}']]
            continue
        if ix < len(segments) - 2:
            new_stems = []
            for stem in stems:
                if stem[-1] == None:
                    new_stems.append(stem[:-1] + [segthis, None])
                    new_stems.append(stem[:-1] + [f'{segthis}, {segnext}'])
                else:
                    new_stems.append(stem + [segnext])
            stems = new_stems
        else:
            for stem in stems:
                if stem[-1] == None:
                    possibilities.append(stem[:-1] + [segthis, segnext])
                    possibilities.append(stem[:-1] + [f'{segthis}, {segnext}'])
                else:
                    possibilities.append(stem + [segnext])
            
    return possibilities

def compare_name_component(list1, list2, settings):
    """
    Compare a list of names from a name component based on settings
    """
    #First contribution to the aggregate is checking whether this component is entirely missing from one side
    #List of different length are treated as equialane to absense of one component
    absence_penalty = settings['absence_penalty']
    if not list1[0] or not list2[0] or (len(list1) != len(list2)):
        aggregate = 1 - absence_penalty
        return aggregate

    aggregate = 1
    initials_weight = settings['initials_weight']
    prefix_weight = settings['prefix_weight']
    for i, n1 in enumerate(list1):
        n2 = list2[i]

        #Match initials and apply weight to aggregate according to the result
        if (len(n1) == 1 or len(n2) == 1):
            aggregate *= initials_weight if equate_initial(n1, n2) else (1 - initials_weight)
            continue

        #Try a prefix match, factored by ratio and a full match. Take the higher of the two.
        prefix_match = prefix_weight if equate_prefix(n1, n2) else (1 - prefix_weight)
        full_match = seq_ratio(n1, n2)
        aggregate *= max((prefix_match, full_match))

    return aggregate


def equate_initial(name1, name2):
    """
    Evaluates whether names match, or one name is the initial of the other
    """
    if len(name1) == 0 or len(name2) == 0:
        return False

    if len(name1) == 1 or len(name2) == 1:
        return name1[0] == name2[0]

    return name1 == name2


def equate_prefix(name1, name2):
    """
    Evaluates whether names match, or one name prefixes another
    """

    if len(name1) == 0 or len(name2) == 0:
        return False

    return name1.startswith(name2) or name2.startswith(name1)


def equate_nickname(name1, name2):
    """
    Evaluates whether names match based on common nickname patterns

    This is not currently used in any name comparison
    """
    # Convert '-ie' and '-y' to the root name
    nickname_regex = r'(.)\1(y|ie)$'
    root_regex = r'\1'

    name1 = re.sub(nickname_regex, root_regex, name1)
    name2 = re.sub(nickname_regex, root_regex, name2)

    if equate_prefix(name1, name2):
        return True

    return False


def strip_punctuation(word):
    """
    Strips punctuation from name and lower cases it
    """
    return word.translate(STRIPPED_CHARACTERS).lower()


def seq_ratio(word1, word2):
    """
    Returns sequence match ratio for two words
    """
    return SequenceMatcher(None, word1, word2).ratio()


def deep_update_dict(default, options):
    """
    Updates the values in a nested dict, while unspecified values will remain
    unchanged
    """
    for key in options.keys():
        default_setting = default.get(key)
        new_setting = options.get(key)
        if isinstance(default_setting, dict):
            deep_update_dict(default_setting, new_setting)
        else:
            default[key] = new_setting