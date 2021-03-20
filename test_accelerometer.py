from accelerometer import floating_point_to_fixed_point_bin_array


def test_floating_point_to_fixed_point_bin_array_over_max():
    expected = [True, True, True, True, True, True, True, True]
    actual = floating_point_to_fixed_point_bin_array(2.5)
    assert actual == expected


def test_floating_point_to_fixed_point_bin_array_too_small():
    expected = [False, False, False, False, False, False, False, False]
    actual = floating_point_to_fixed_point_bin_array(0.0000000000000000000001)
    assert actual == expected


def test_floating_point_to_fixed_point_bin_array_1():
    expected = [False, False, True, False, False, False, False, False]
    actual = floating_point_to_fixed_point_bin_array(0.25)
    assert actual == expected


def test_floating_point_to_fixed_point_bin_array_2():
    expected = [False, False, True, False, True, False, False, False]
    actual = floating_point_to_fixed_point_bin_array(0.3125)
    assert actual == expected


def test_floating_point_to_fixed_point_bin_array_3():
    expected = [False, False, False, False, False, False, False, True]
    actual = floating_point_to_fixed_point_bin_array(0.0078126)
    assert actual == expected