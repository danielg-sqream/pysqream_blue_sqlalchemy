

def pytest_addoption(parser):
    parser.addoption("--domain", action="store", help="SQream Server domain")
    parser.addoption("--access_token", action="store", help="SQream server token")


def pytest_generate_tests(metafunc):
    metafunc.config.getoption("domain")
    metafunc.config.getoption("access_token")