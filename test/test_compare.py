# -*- coding: utf-8 -*-
import pytest #Consider also installing pytest_capturelog
import math

from amara3.names.model import human_name
from amara3.names import compare, config

def test_compare():
    name = 'Robert Evan Liebowitz'

    #n = human_name.parse(name)
    #assert n.title_list == ['']
    #assert n.first_list == ['robert']
    #assert n.middle_list == ['evan']
    #assert n.last_list == ['liebowitz']
    #assert n.suffix_list == ['']
    #assert n.nickname_list == ['']

    #assert compare.ratio(name, 'attaché Robert Evan Liebowitz') == 1.0
    assert compare.ratio(name, 'Rōbért Èvān Lîęböwitz') == 1.0
    assert compare.ratio(name, 'Rōbért Èvān Lęîböwitz') < 1.0

    assert math.isclose(compare.ratio(name, 'R. Evan Liebowitz'), 0.95, abs_tol=0.05)
    assert math.isclose(compare.ratio(name, 'Robert E. Liebowitz'), 0.95, abs_tol=0.05)
    assert math.isclose(compare.ratio(name, 'R. E. Liebowitz'), 0.9, abs_tol=0.05)

    assert math.isclose(compare.ratio(name, 'Robert Liebowitz'), 0.95, abs_tol=0.05)
    assert math.isclose(compare.ratio(name, 'R. Liebowitz'), 0.8, abs_tol=0.05)
    #Coming out at 0.419; Expect higher
    #assert math.isclose(compare.ratio(name, 'Robert E. E. Liebowitz'), 0.75, abs_tol=0.05)
    #assert math.isclose(compare.ratio(name, 'R. E. E. Liebowitz'), 0.78, abs_tol=0.05)
    #assert math.isclose(compare.ratio('R.E.E. Liebowitz', 'R. E. E. Liebowitz'), 0.9, abs_tol=0.05)

    #assert math.isclose(compare.ratio(name, 'E. R. Liebowitz'), 0.75, abs_tol=0.05)
    assert math.isclose(compare.ratio(name, 'E. Liebowitz'), 0.8, abs_tol=0.05)
    assert math.isclose(compare.ratio(name, 'R. V. Liebowitz'), 0.75, abs_tol=0.05)
    assert math.isclose(compare.ratio(name, 'O. E. Liebowitz'), 0.75, abs_tol=0.05)

    #At present seeing AssertionError: assert 0.75 < 0.33 ; seems weird
    #assert compare.ratio(name, 'E. R. Liebowitz') < compare.ratio(name, 'E. E. Liebowitz')
    assert compare.ratio(name, 'E. R. Liebowitz') >= compare.ratio(name, 'R. R. Liebowitz')
    #???
    #assert compare.ratio(name, 'E. R. Liebowitz') >= compare.ratio(name, 'E. Liebowitz')

    assert math.isclose(compare.ratio(name, 'Rob Liebowitz'), 0.85, abs_tol=0.05)
    #??? assert math.isclose(compare.ratio(name, 'Bert Liebowitz'), 0.7, abs_tol=0.05)
    assert math.isclose(compare.ratio(name, 'Robbie Liebowitz'), 0.85, abs_tol=0.05)

    #??? assert compare.ratio(name, 'xxxxx Liebowitz') < compare.ratio(name, 'Bobby Liebowitz')

    name = 'Robert Liebowitz Jr'
    assert math.isclose(compare.ratio(name, 'Robert Liebowitz'), 0.92, abs_tol=0.05)
    #assert compare.ratio(name, 'Robert Liebowitz Jr') == 1
    assert math.isclose(compare.ratio(name, 'Robert Liebowitz, PhD'), 0.92, abs_tol=0.05)
    #assert math.isclose(compare.ratio(name, 'Robert Liebowitz, Sr'), 0.92, abs_tol=0.05)
    #Check we're avoiding the list trap
    #assert math.isclose(compare.ratio(name, 'Robert Liebowitz, Sr, PhD'), 0.85, abs_tol=0.05)
    #assert math.isclose(compare.ratio(name, 'Robert Liebowitz, Jr, PhD'), 0.85, abs_tol=0.05)

    assert math.isclose(compare.ratio(name, 'Robert Liebowitz Jnr'), 0.92, abs_tol=0.05)
    #assert math.isclose(compare.ratio(name, 'Robert Liebowitz Snr'), 0.92, abs_tol=0.05)

    name = 'Zachary Liebowitz'
    # Suffixes
    assert math.isclose(compare.ratio(name, 'Dr. Zachary Liebowitz'), 0.92, abs_tol=0.05)

    name = 'Mr. Robert Liebowitz'
    assert math.isclose(compare.ratio(name, 'Robert Liebowitz'), 0.92, abs_tol=0.05)

    # Titles
    assert math.isclose(compare.ratio(name, 'Sir Robert Liebowitz'), 0.92, abs_tol=0.05)
    assert math.isclose(compare.ratio(name, 'Dr. Robert Liebowitz'), 0.92, abs_tol=0.05)
    #assert math.isclose(compare.ratio(name, 'Mrs. Robert Liebowitz'), 0.92, abs_tol=0.05)

    name = 'Robert "Evan" Liebowitz'
    assert math.isclose(compare.ratio(name, 'Evan Liebowitz'), 0.8, abs_tol=0.05)
    assert compare.ratio(name, 'Evan Liebowitz') == compare.ratio('Evan Liebowitz', name)
    assert math.isclose(compare.ratio(name, 'Wrongbert Lieobwitz'), 0.8, abs_tol=0.05)
    assert math.isclose(compare.ratio(name, 'Robert Evan'), 0.6, abs_tol=0.1)
    assert math.isclose(compare.ratio(name, 'Evan Liebowitz', options={'check_nickname': False}), 0.75, abs_tol=0.05)

    name = 'Jackson, Hazel I.'
    assert math.isclose(compare.ratio(name, 'Jackson, Hazel Brill'), 0.75, abs_tol=0.1), compare.ratio(name, 'Jackson, Hazel Brill')

    #assert compare.ratio(name, 'xxxx Liebowitz') < compare.ratio(name, 'xvax Liebowitz')
    #assert compare.ratio(name, 'xxxx Liebowitz') == compare.ratio(name, 'xvax Liebowitz', 'strict')


if __name__ == '__main__':
    raise SystemExit("Use py.test")
