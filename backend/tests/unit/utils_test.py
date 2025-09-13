import os
from src.utils import get_env_file_path, get_hosts_file_path, get_hosts_from_file


def test_get_env_file_path():
    # Tests directory path
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Unit tests directory path
    unit_tests_dir = os.path.dirname(tests_dir)
    
    # Backend directory path
    backend_dir = os.path.dirname(unit_tests_dir)
    
    # Expected .env path
    expected_path = os.path.join(backend_dir, '.env')
    
    # Actual .env path
    actual_path = get_env_file_path()
    
    assert actual_path == expected_path, '.env should be in backend directory (not found)'


def test_get_hosts_file_path():
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Unit tests directory path
    unit_tests_dir = os.path.dirname(tests_dir)
    
    # Backend directory path
    backend_dir = os.path.dirname(unit_tests_dir)
    
    # Expected .env path
    expected_path = os.path.join(backend_dir, 'hosts.txt')
    
    # Actual .env path
    actual_path = get_hosts_file_path()
    
    assert actual_path == expected_path, 'hosts.txt should be in backend directory (not found)'
    
    
def test_get_hosts_from_file():
    hosts = get_hosts_from_file()

    assert len(hosts) > 0, 'hosts.txt is empty, fill it with some hosts'
