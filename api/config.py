import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# Function that checks if code is running in docker container for tests
def is_running_in_docker():
    try:
        with open('/proc/self/cgroup', 'r') as cgroup_file:
            for line in cgroup_file:
                if 'docker' in line:
                    return True
    except FileNotFoundError:
        pass
    return False


class BaseConfig():
    if is_running_in_docker():
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
        SECRET_KEY = os.environ.get('SECRET_KEY')
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
        SECRET_KEY = "da64f456dfeb4eae915bf4acc9283c9f"
class TestConfig():
    if is_running_in_docker():
        print(os.environ.get('DATABASE_URL'))
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
        SECRET_KEY = os.environ.get('SECRET_KEY')
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
        SECRET_KEY = "da64f456dfeb4eae915bf4acc9283c9f"
