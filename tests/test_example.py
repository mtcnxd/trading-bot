import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import MagicMock
from Services.BitsoService import BitsoService

def test_example():
    assert True

'''
def test_endpoint_success():
    expected_response = {
        'success': True,
        'message': 'Operacion exitosa'
    }

    if expected_response['success'] == True:
        assert True
    else:
        assert False

def test_endpoint_failure():
    expected_response = {
        'success': False,
        'message': 'Operacion fallida'
    }

    if expected_response['success'] == True:
        assert False
    else:
        assert True

def test_bitso_service():
    session = MagicMock()
    bitso_service = BitsoService(session=session)
    bitso_service.get_account_status()

'''