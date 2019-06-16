# -*- coding: utf-8 -*-

#from .config import (UNIQUE_SUFFIXES, MALE_TITLES, FEMALE_TITLES,
#                                    EQUIVALENT_SUFFIXES)
from .utils import normalize, simple_compare, compound_compare, initial_compare
from .kb import DK_AFFIXES


class particle(str):
    weight = 2
    def __repr__(self):
        return f'particle("{self}")'


class given(str):
    weight = 5
    initials_weights_factor = 0.9
    prefix_weights_factor = 0.7
    def __repr__(self):
        return f'given("{self}")'


class familial(str):
    weight = 5
    def __repr__(self):
        return f'familial("{self}")'


class human_name:
    '''
    '''
    def __init__(self, segments):
        self.segments = segments

    @classmethod
    def parse(cls, fullname):
        '''
        Parse a human name string and return a Name instance or None
        '''
        name_segments = cls._parse(fullname)
        if name_segments is None:
            return None
        name_obj = cls(name_segments)
        return name_obj

    #Some logic borrowed from https://github.com/derek73/python-nameparser
    @classmethod
    def _parse(cls, fullname):
        '''
        Low level parse function
        
        Return name segments list
        '''
        segments = []
        comma_sep_parts = [x.strip() for x in fullname.split(",")]
        if len(comma_sep_parts) == 1:
            # No comma, so parse name segments accordingly, e.g. "{prefixes} {givens} {family} {suffixes}"
            candidate_familial = None
            raw_segments = comma_sep_parts[0].split()
            if len(raw_segments) == 1:
                # Single segment treated as given: "Pelé", "Madonna"
                return [given(subparts[0])]
            for rseg in raw_segments:
                if rseg in DK_AFFIXES:
                    segments.append(particle(rseg))
                else:
                    # The familial will be the last encountered non-particle part
                    if candidate_familial is not None:
                        placeholder_ix = segments.index(None)
                        segments[placeholder_ix] = given(candidate_familial)
                    candidate_familial = rseg
                    # Insert Placeholder
                    segments.append(None)

            if candidate_familial is not None:
                placeholder_ix = segments.index(None)
                segments[placeholder_ix] = familial(candidate_familial)
        else:
            # Always assume this is familal, particles + givens
            # See utility routines for e.g. parsing name lists
            raw_segments = comma_sep_parts[1].split()
            for rseg in raw_segments:
                if rseg in DK_AFFIXES:
                    segments.append(particle(rseg))
                else:
                    segments.append(given(rseg))

            segments.append(familial(comma_sep_parts[0]))
        return segments


    def stripes(self):
        '''
        return a striping of name segments, which always starts with a single string giving the familial (or empty)
        followed by an optional particles cluster followed by a givens cluster,
        and possibly more particles, more givens, etc
        e.g. Don Juan de Marco -> ['marco', ['don'], ['juan'], ['de']]
        Don Quixote de la Mancha -> ['mancha', ['don'], ['quixote'], ['de la']] (note 'mancha' is interpreted as the familial rather than 'quixote')
        Martin Luther King Jr -> ['king', ['martin luther'], ['jr']]
        
        In case of no familial, e.g.
        Pelé -> ['', ['pelé']]

        Stripes are a valuable form for name comparisons
        '''
        # TODO: We'll have to distinguish ordinals, such as "de la" from severals such as "alhaja chief dr mrs". These should be represented accordingly within the stripes, e.g. ['de la Mancha'] vs ['alhaja', 'chief', 'dr', 'mrs'] where the separate strings in the latter list indicate that they can be reordered
        stripes = [familial('')]
        prev_seg = None
        for seg in self.segments:
            stripe_type = seg.__class__
            # Note: we don't expect to have more than one familial segment
            if type(prev_seg) == type(seg):
                stripes[-1].append(seg)
                #stripes[-1] = stripe_type(f'{stripes[-1]} {seg}')
            else:
                # New stripe, but always inserted at 1st position if familial
                if stripe_type == familial:
                    stripes[0] = seg
                else:
                    stripes.append([seg])
            prev_seg = seg
        return stripes


    def ratio_deep_compare(self, other, settings):
        """
        Compares each field of the name one at a time to see if they match.
        Each name field has context-specific comparison logic.

        :param Name other: other Name for comparison
        :return int: sequence ratio match (out of 100)
        """
        # FIXME: Bring this back,which e.g. shortcuts a Mr from a Mrs comparison
        #if not self._is_compatible_with(other):
        #    return 0

        #threshold = settings['threshold']
        
        #List of weighted segment comparisons
        w_stripe_comps = 0
        total_weight = 0
        explanation = ''
        
        # Strategy is to run a series of striped comparisons, where a list of particles is compared self to other, then any given or familial, and so on
        left_stripes = self.stripes()
        right_stripes = other.stripes()

        #e.g. Don Juan de Marco -> ['marco', ['don'], ['juan'], ['de']]
        #Don Quixote de la Mancha -> ['mancha', ['don'], ['quixote'], ['de la']] (note 'mancha' is interpreted as the familial rather than 'quixote')
        #Pelé -> ['', ['pelé']]

        ix = 0
        offset = 0
        while ix < len(left_stripes) and ix + offset < len(right_stripes):
            left_stripe, right_stripe = left_stripes[ix], right_stripes[ix + offset]
            lstripe_type = familial if isinstance(left_stripe, familial) else type(left_stripe[0])
            rstripe_type = familial if isinstance(right_stripe, familial) else type(right_stripe[0])
            if lstripe_type == rstripe_type:
                weight = lstripe_type.weight
                compare_func = simple_compare if lstripe_type == familial else compound_compare
                ratio = compare_func(left_stripe, right_stripe)
                #print(left_stripe, lstripe_type)
                if lstripe_type == given:
                    ratio = max((ratio, initial_compare(left_stripe, right_stripe, given.initials_weights_factor)))
                    # Boost for cases where the first given matches but a later one is missing
                    if ratio < 0.85 and left_stripe[0] == right_stripe[0] and len(left_stripe) != len(right_stripe):
                        ratio += 0.1
                w_stripe_comps += ratio * weight
                
                #print(left_stripes[ix], right_stripes[ix + offset], compare_func(left_stripes[ix], right_stripes[ix + offset]), weight)
                ix += 1
            else:
                # One stripe missing from the other; contributing 0 to comparison value but weight will still be added below
                # Then advance the offset for the right index & try again, looping
                offset += 1
            total_weight += weight
            
        # TODO: Check Nicknames, e.g. https://github.com/rliebz/whoswho/blob/master/whoswho/model.py#L115

        return w_stripe_comps / total_weight

    def _is_compatible_with(self, other):
        """
        Return True if names are not incompatible.

        This checks that the gender of titles and compatibility of suffixes
        """

        title = self._compare_title(other)
        suffix = self._compare_suffix(other)

        return title and suffix

    def _compare_title(self, other):
        """Return False if titles have different gender associations"""

        # If title is omitted, assume a match
        if not self.title or not other.title:
            return True

        titles = set(self.title_list + other.title_list)

        return not (titles & MALE_TITLES and titles & FEMALE_TITLES)

    def _compare_suffix(self, other):
        """Return false if suffixes are mutually exclusive"""

        # If suffix is omitted, assume a match
        if not self.suffix or not other.suffix:
            return True

        # Check if more than one unique suffix
        suffix_set = set(self.suffix_list + other.suffix_list)
        unique_suffixes = suffix_set & UNIQUE_SUFFIXES
        for key in EQUIVALENT_SUFFIXES.keys():
            if key in unique_suffixes:
                unique_suffixes.remove(key)
                unique_suffixes.add(EQUIVALENT_SUFFIXES[key])

        return len(unique_suffixes) < 2

    def _compare_components(self, other, settings):
        """
        Return comparison of first, middle, and last components
        """
        threshold = settings['threshold']
        first = compare_name_component(
            self.first_list,
            other.first_list,
            settings['first'],
        )

        if settings['check_nickname']:
            first = max(
                compare_name_component(
                    self.nickname_list,
                    other.first_list,
                    settings['first'],
                ),
                compare_name_component(
                    self.first_list,
                    other.nickname_list,
                    settings['first'],
                ),
                first,
            )

        middle = compare_name_component(
            self.middle_list,
            other.middle_list,
            settings['middle'],
        )

        last = compare_name_component(
            self.last_list,
            other.last_list,
            settings['last'],
        )

        return first, middle, last

    def _determine_weights(self, other, settings):
        """
        Return weights of name components based on whether or not they were
        omitted
        """

        # TODO: Reduce weight for matches by prefix or initials

        first_is_used = settings['first']['required'] or \
            self.first and other.first
        first_weight = settings['first']['weight'] if first_is_used else 0

        middle_is_used = settings['middle']['required'] or \
            self.middle and other.middle
        middle_weight = settings['middle']['weight'] if middle_is_used else 0

        last_is_used = settings['last']['required'] or \
            self.last and other.last
        last_weight = settings['last']['weight'] if last_is_used else 0

        return first_weight, middle_weight, last_weight

