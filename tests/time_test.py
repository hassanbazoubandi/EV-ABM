from hypothesis import given
from hypothesis import strategies as st

from model.Time import Time


@given(year=st.integers(), month=st.integers(1, 12), step=st.integers(0, 10000))
def test_time(year, month, step):
    t = Time(year, month)

    actual = t.get_current_date(step // 12, step % 12)

    assert actual[1] == (month + step % 12 - 1) % 12 + 1
    assert actual[0] == (year + step // 12) + (month + step % 12 - 1) // 12
