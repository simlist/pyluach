from pyluach.gematria import num_to_string

def test_one_letter():
    assert num_to_string(5) == 'ה׳'
    assert num_to_string(10) == 'י׳'
    assert num_to_string(200) == 'ר׳'

def test_two_letters():
    assert num_to_string(18) == 'י״ח'
    assert num_to_string(15) == 'ט״ו'
    assert num_to_string(16) == 'ט״ז'
    assert num_to_string(101) == 'ק״א'

def test_three_letters():
    assert num_to_string(127) == 'קכ״ז'
    assert num_to_string(489) == 'תפ״ט'
    assert num_to_string(890) == 'תת״צ'

def test_four_letters():
    assert num_to_string(532) == 'תקל״ב'

def test_five_letters():
    assert num_to_string(916) == 'תתקט״ז'