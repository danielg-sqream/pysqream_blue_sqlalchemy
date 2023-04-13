import pytest
import socket
import sys
import os
from pytest_logger import Logger
from sqlalchemy import orm, create_engine, MetaData
import sqlalchemy as sa

_access_token="bFo2djNpTFBvYXJ4QTNEN0tHMmlDNTlKRW9hSEdEUGdDZjNVUVYyS3lUaGNDNFl0MFYtSTNncFhCaFl2SlYxdC12Y08zbm80VFo2emxndzBrbl92NEhDYTNfc2pnUDZu"


def connect(domain, clustered=False, use_ssl=False):
    print_echo = False
    conn_str = f"pysqream+dialect://sqream:sqream@{domain}:443/master;access_token={_access_token}"
    engine = create_engine(conn_str, echo=print_echo)
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

    @pytest.fixture(autouse=True)
    def Test_setup_teardown(self, domain):
        Logger().info("Before Scenario")
        Logger().info(f"Connect to server {domain}")
        self.domain = domain
        self.engine ,self.metadata ,self.session, self.conn_str = connect(domain)
        setTinyint(self.engine)
        yield
        Logger().info("After Scenario")