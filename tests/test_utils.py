import pytest
from api.utils import calcDistSchiphol

def test_distance_to_schiphol(app):
    with app.app_context():
        # test if schiphol is 0
        schiphol_lat = 52.30907
        schiphol_lon = 4.763385
        dist_schiphol_schiphol = calcDistSchiphol(schiphol_lat, schiphol_lon)
        amm_lat = 31.722534
        amm_lon = 35.98932
        dist_schiphol_amm = calcDistSchiphol(amm_lat, amm_lon)

        assert 0 == dist_schiphol_schiphol
        assert 3401 == dist_schiphol_amm
