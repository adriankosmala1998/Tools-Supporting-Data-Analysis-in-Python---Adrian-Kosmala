import pytest
from nbp_change import get_courses
import nbp_change

def test_calc_statistics_one_value(monkeypatch):
    def mockreturn(currency_code, days):
        return [1], 'EUR'

    monkeypatch.setattr('nbp_change.get_courses', mockreturn)
    assert nbp_change.calc_statistics(['EUR'], 1)


def test_calc_statistics_division_by_zero(monkeypatch):
    def mockreturn_2(currency_code, days):
        return [0,0.5], 'EUR'

    monkeypatch.setattr('nbp_change.get_courses', mockreturn_2)
    assert nbp_change.calc_statistics(['EUR'], 2)
