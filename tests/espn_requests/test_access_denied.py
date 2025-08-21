import pytest
from espn_api.requests.espn_requests import EspnFantasyRequests, ESPNAccessDenied

class DummyLogger:
    def log_request(self, **kwargs):
        pass

def test_access_denied_no_cookies():
    req = EspnFantasyRequests(sport='nfl', year=2024, league_id=123456, cookies=None, logger=DummyLogger())
    # Simulate 401 response and alternate endpoint failure
    with pytest.raises(ESPNAccessDenied) as excinfo:
        req.checkRequestStatus(401)
    assert 'espn_s2 and swid are required' in str(excinfo.value)

def test_access_denied_missing_espn_s2():
    cookies = {'SWID': 'some_swid'}
    req = EspnFantasyRequests(sport='nfl', year=2024, league_id=123456, cookies=cookies, logger=DummyLogger())
    with pytest.raises(ESPNAccessDenied) as excinfo:
        req.checkRequestStatus(401)
    assert 'espn_s2 and swid are required' in str(excinfo.value)

def test_access_denied_missing_swid():
    cookies = {'espn_s2': 'some_s2'}
    req = EspnFantasyRequests(sport='nfl', year=2024, league_id=123456, cookies=cookies, logger=DummyLogger())
    with pytest.raises(ESPNAccessDenied) as excinfo:
        req.checkRequestStatus(401)
    assert 'espn_s2 and swid are required' in str(excinfo.value)

def test_access_denied_with_cookies(monkeypatch):
    cookies = {'espn_s2': 'some_s2', 'SWID': 'some_swid'}
    req = EspnFantasyRequests(sport='nfl', year=2024, league_id=123456, cookies=cookies, logger=DummyLogger())
    # Patch requests.get to always return a response with status_code != 200
    class DummyResponse:
        status_code = 401
        def json(self):
            return {}
    monkeypatch.setattr('requests.get', lambda *args, **kwargs: DummyResponse())
    with pytest.raises(ESPNAccessDenied) as excinfo:
        req.checkRequestStatus(401)
    assert f"League {req.league_id} cannot be accessed" in str(excinfo.value)
