import os


def get_env_file_path() -> str:
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')


def get_hosts_file_path() -> str:
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'hosts.txt')


def get_hosts_from_file() -> list[str]:
    filepath = get_hosts_file_path()
    
    with open(filepath, 'r') as f:
        hosts = [h.strip() for h in f.readlines()]
    
    return hosts
