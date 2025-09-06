import os


def get_env_file_path():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
