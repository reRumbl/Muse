import os
from src.utils import get_env_file_path


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
