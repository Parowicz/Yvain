from yvain.membership_functions import *

import pytest

_Triangle_VERTEXES = [
    (0, 5, 10), (-10, 0, 10),
    (-1.5, 0, 1.5), (-3.14, 3.14, 6.28),
    (-100, 0, 100), (20, 25, 30),
    (0, 5, 80), (-10, -9, 100),
]


def test_triangle_b_lesser_than_a_raises_value_error():
    with pytest.raises(ValueError):
        Triangle(a=0, b=-2, c=5)


def test_triangle_c_lesser_than_b_raises_value_error():
    with pytest.raises(ValueError):
        Triangle(a=0, b=2, c=1)


@pytest.mark.parametrize("a, b, c", _Triangle_VERTEXES)
def test_triangle_fx_at_b_is_always_equal_to_one(a, b, c):
    mf = Triangle(a, b, c)
    assert mf(b) == pytest.approx(1)


@pytest.mark.parametrize("a, b, c", _Triangle_VERTEXES)
def test_triangle_fx_lesser_or_equal_to_a_returns_zero(a, b, c):
    mf = Triangle(a, b, c)

    assert mf(a) == pytest.approx(0)
    assert mf(a - 10) == pytest.approx(0)


@pytest.mark.parametrize("a, b, c", _Triangle_VERTEXES)
def test_triangle_fx_greater_or_equal_to_c_returns_zero(a, b, c):
    mf = Triangle(a, b, c)
    assert mf(c) == pytest.approx(0)
    assert mf(c + 10) == pytest.approx(0)


@pytest.mark.parametrize("a, b, c, proportion", [(0, 10, 15, 0.1)])
def test_triangle_fx_between_a_c_is_proportional_to_distance_to_b(a, b, c, proportion):
    mf = Triangle(a, b, c)

    assert mf(a + ((b - a) * proportion)) == pytest.approx(proportion)
    assert mf(b + ((c - b) * (1 - proportion))) == pytest.approx(proportion)


_TRAPEZE_VERTEXES = [
    (0, 2, 4, 6), (-10, -5, 5, 10),
    (0, 1, 100, 200), (-100, 100, 200, 300),
    (-1.5, -1., -0.5, 0), (-1.1, -1., -0.9, -0.8)
]

_TRAPEZE_VERTEXES_WITH_PROPORTION = [
    (0, 2, 4, 6, 0.2), (-10, -5, 5, 10, 0.05),
    (0, 1, 100, 200, 1.), (-100, 100, 200, 300, 0.6),
    (-1.5, -1., -0.5, 0, 0.3), (-1.1, -1., -0.9, -0.8, 0.8)
]


def test_trapezoid_when_b_is_lesser_or_equal_to_a_raise_value_error():
    with pytest.raises(ValueError):
        Trapezoid(a=0, b=-1, c=2, d=3)

    with pytest.raises(ValueError):
        Trapezoid(a=0, b=1, c=1, d=2)


def test_trapezoid_when_c_is_lesser_or_equal_to_b_raise_value_error():
    with pytest.raises(ValueError):
        Trapezoid(a=0, b=2, c=1, d=3)

    with pytest.raises(ValueError):
        Trapezoid(a=0, b=2, c=2, d=3)


def test_trapezoid_when_d_is_lesser_or_equal_to_c_raise_value_error():
    with pytest.raises(ValueError):
        Trapezoid(a=0, b=1, c=3, d=2)

    with pytest.raises(ValueError):
        Trapezoid(a=0, b=2, c=3, d=3)


@pytest.mark.parametrize("a, b, c, d, proportion", _TRAPEZE_VERTEXES_WITH_PROPORTION)
def test_trapezoid_fx_between_b_and_c_is_equal_to_one(a, b, c, d, proportion):
    mf = Trapezoid(a, b, c, d)

    assert mf(b) == pytest.approx(1)
    assert mf(c) == pytest.approx(1)
    assert mf(b + ((c - b) * proportion)) == pytest.approx(1)


@pytest.mark.parametrize("a, b, c, d", _TRAPEZE_VERTEXES)
def test_trapezoid_fx_lesser_or_equal_to_a_returns_zero(a, b, c, d):
    mf = Trapezoid(a, b, c, d)

    assert mf(a) == pytest.approx(0)
    assert mf(a - 10) == pytest.approx(0)


@pytest.mark.parametrize("a, b, c, d", _TRAPEZE_VERTEXES)
def test_trapezoid_fx_greater_or_equal_to_d_returns_zero(a, b, c, d):
    mf = Trapezoid(a, b, c, d)
    assert mf(d) == pytest.approx(0)
    assert mf(d + 10) == pytest.approx(0)


@pytest.mark.parametrize("a, b, c, d, proportion", _TRAPEZE_VERTEXES_WITH_PROPORTION)
def test_trapezoid_fx_between_a_b_is_proportional_to_distance(a, b, c, d, proportion):
    mf = Trapezoid(a, b, c, d)

    assert mf(a + ((b - a) * proportion)) == pytest.approx(proportion)


@pytest.mark.parametrize("a, b, c, d, proportion", _TRAPEZE_VERTEXES_WITH_PROPORTION)
def test_trapezoid_fx_between_d_c_is_proportional_to_distance(a, b, c, d, proportion):
    mf = Trapezoid(c - 200, c - 100, c, d)

    assert mf(c + ((d - c) * (1 - proportion))) == pytest.approx(proportion)


_GAUSSIAN_PARAMETERS = [
    (0, 1), (10, 4), (-10, 0.5), (-100, 0.6), (-0.1, 2), (0.1, 2)
]


@pytest.mark.parametrize("mu, sigma", _GAUSSIAN_PARAMETERS)
def test_gaussian_fx_in_mu_shall_be_equal_to_one(mu, sigma):
    mf = Gaussian(mu, sigma)
    assert mf(mu) == pytest.approx(1)


@pytest.mark.parametrize("mu, sigma", _GAUSSIAN_PARAMETERS)
def test_gaussian_shall_be_symmetric(mu, sigma):
    mf = Gaussian(mu, sigma)

    assert mf(mu - sigma) == pytest.approx(mf(mu + sigma))
    assert mf(mu - (2 * sigma)) == pytest.approx(mf(mu + (2 * sigma)))
    assert mf(mu - (3 * sigma)) == pytest.approx(mf(mu + (3 * sigma)))


_BELL_PARAMETERS = [
    (0, 1, 2), (10, 4, 1), (-10, 0.5, 0.2), (-100, 0.6, 4),
    (-0.1, 2, 6), (0.1, 2, 0.2)
]


@pytest.mark.parametrize("mu, sigma, gamma", _BELL_PARAMETERS)
def test_bell_fx_in_mu_shall_be_equal_to_one(mu, sigma, gamma):
    mf = Bell(mu, sigma, gamma)
    assert mf(mu) == pytest.approx(1)


@pytest.mark.parametrize("mu, sigma, gamma", _BELL_PARAMETERS)
def test_bell_shall_be_symmetric(mu, sigma, gamma):
    mf = Bell(mu, sigma, gamma)

    assert mf(mu - sigma) == pytest.approx(mf(mu + sigma))
    assert mf(mu - (2 * sigma)) == pytest.approx(mf(mu + (2 * sigma)))
    assert mf(mu - (3 * sigma)) == pytest.approx(mf(mu + (3 * sigma)))


_SIGMOID_PARAMETERS = [
    (5, -0.1), (0, 10), (-10, 13),
    (10, 0.1), (15, 0.8), (-2.5, 10.2),
    (0, -3)
]


@pytest.mark.parametrize("a, b", _SIGMOID_PARAMETERS)
def test_sigmoid_a_is_always_equal_to_half(a, b):
    mf = Sigmoid(a, b)
    assert mf(a) == pytest.approx(0.5)


@pytest.mark.parametrize("a, b", _SIGMOID_PARAMETERS)
def test_sigmoid_changing_b_symbol_reverses_function(a, b):
    mf = Sigmoid(a, b)
    mf2 = Sigmoid(a, -b)

    assert mf(a - 10) == pytest.approx(mf2(a + 10))
    assert mf(a - 10) == pytest.approx(1 - mf2(a - 10))
