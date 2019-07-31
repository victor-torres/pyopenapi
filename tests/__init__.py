import os.path

import yaml


BASE_DIR = os.path.dirname(__file__)
FIXTURES_DIR = os.path.join(BASE_DIR, 'fixtures')


def load_fixture(file_name):
    with open(os.path.join(FIXTURES_DIR, file_name), 'r') as f:
        return f.read()


def load_yaml_fixture(file_name):
    return yaml.safe_load(load_fixture(file_name))
