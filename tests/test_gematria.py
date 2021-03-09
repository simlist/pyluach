from pyluach.gematria import _num_to_str

def test_one_letter():
    assert _num_to_str(5) == 'ה׳'
    assert _num_to_str(10) == 'י׳'
    assert _num_to_str(200) == 'ר׳'

def test_two_letters():
    assert _num_to_str(18) == 'י״ח'
    assert _num_to_str(15) == 'ט״ו'
    assert _num_to_str(16) == 'ט״ז'
    assert _num_to_str(101) == 'ק״א'

def test_three_letters():
    assert _num_to_str(127) == 'קכ״ז'
    assert _num_to_str(489) == 'תפ״ט'
    assert _num_to_str(890) == 'תת״צ'

def test_four_letters():
    assert _num_to_str(532) == 'תקל״ב'

def test_five_letters():
    assert _num_to_str(916) == 'תתקט״ז'

def test_thousands():
    assert _num_to_str(5781, True) == 'ה׳תשפ״א'
    assert _num_to_str(10000, True) == 'י׳'
    assert _num_to_str(12045, True) == 'יב׳מ״ה'