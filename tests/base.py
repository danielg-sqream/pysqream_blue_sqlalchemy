import pytest
import socket
import sys
import os
from pytest_logger import Logger
from sqlalchemy import orm, create_engine, MetaData
import sqlalchemy as sa

_access_token="Zk5QN1RxUXNzVTZPTmJiN3I2a2duekNFTXAwYVhKUVlISTltYVVuTllUdnhkb3lZRUxJeDJOT3pXZU5sM0Jzb09uVkNsSl9USEJPc1RFQlVISXowRDdTZ1dkaEM1UDBt"

def connect(domain, clustered=False, use_ssl=False, access_token=_access_token):
    print_echo = False
    conn_str = f"sqream_blue://{domain}:443/master"
    connect_args = {'access_token': access_token}
    engine = create_engine(conn_str, connect_args=connect_args, echo=print_echo)
    sa.Tinyint = engine.dialect.Tinyint
    session = orm.sessionmaker(bind=engine)()
    metadata = MetaData()
    metadata.bind = engine
    return engine, metadata, session, conn_str


def setTinyint(engine):
    sa.Tinyint = engine.dialect.Tinyint


class TestBase():

    @pytest.fixture()
    def domain(self, pytestconfig):
        return pytestconfig.getoption("domain")

    @pytest.fixture()
    def access_token(self, pytestconfig):
        return pytestconfig.getoption("access_token")


    @pytest.fixture(autouse=True)
    def Test_setup_teardown(self, domain, access_token):
        Logger().info("Before Scenario")
        Logger().info(f"Connect to server {domain}")
        self.domain = domain
        self.engine ,self.metadata ,self.session, self.conn_str = connect(domain, access_token=access_token)
        setTinyint(self.engine)
        yield
        Logger().info("After Scenario")
        self.engine.dispose()
