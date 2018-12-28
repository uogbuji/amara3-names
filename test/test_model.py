# -*- coding: utf-8 -*-
import pytest #Consider also installing pytest_capturelog

from amara3.names.model import Name


def test_warmup():
    name = 'Rôbert E. Liebowitz'

    n = Name(name)
    assert n.title_list == ['']
    assert n.first_list == ['robert']
    assert n.middle_list == ['e']
    assert n.last_list == ['liebowitz']
    assert n.suffix_list == ['']
    assert n.nickname_list == ['']

