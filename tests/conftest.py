

def pytest_addoption(parser):
    parser.addoption("--domain", action="store", help="SQream Server domain")


def pytest_generate_tests(metafunc):
    metafunc.config.getoption("domain")
