"""
Test script for database server module
"""

from __future__ import absolute_import, division, print_function

from tests.util import unittest_reporter, glob_tests, messaging_mock

import logging
logger = logging.getLogger('modules_db_test')

import os
import sys
import time
import shutil
import tempfile
import signal
import unittest

from flexmock import flexmock

import iceprod.core.logger
from iceprod.core import functions
from iceprod.server import module
from iceprod.server import basic_config
from iceprod.server.modules import db


""" List of things that must be mocked:
    def _start_db(self):
    def _start_rpc(self):
    def _stop_db(self,force=False):
    def _stop_rpc(self):
    def _setup_tables(self):
    def _backup_worker(self):
    def _dbsetup(self):
    def _db_read(self,sql,bindings,archive_sql,archive_bindings):
    def _db_write(self,sql,bindings,archive_sql,archive_bindings):
    def _increment_id_helper(self,table):
"""

class _Methods:
    def __init__(self):
        self.db_func_called = None
    def db_func(self,*args,**kwargs):
        self.db_func_called = [args,kwargs]
class _DB(object):
    def __init__(self,*args,**kwargs):
        self.args = args
        self.kwargs = kwargs
        self.started = False
        self.stopped = False
        self.killed = False
        self.cfg = None
        self.backuped = False
        self.dbmethods = _Methods()
    def start(self):
        self.started = True
    def stop(self,force=False):
        if force:
            self.killed = True
        else:
            self.stopped = True
    def update_cfg(self,cfg):
        self.cfg = cfg
    def backup(self):
        self.backuped = True

class modules_db_test(unittest.TestCase):
    def setUp(self):
        super(modules_db_test,self).setUp()
        self.test_dir = tempfile.mkdtemp(dir=os.getcwd())

        self.ca_cert = os.path.join(self.test_dir,'ca.crt')
        self.ca_key = os.path.join(self.test_dir,'ca.key')
        self.ssl_key = os.path.join(self.test_dir,'test.key')
        self.ssl_cert = os.path.join(self.test_dir,'test.crt')

        # set hostname
        self.hostname = 'localhost'

        def sig(*args):
            sig.args = args
        flexmock(signal).should_receive('signal').replace_with(sig)
        def basicConfig(*args,**kwargs):
            pass
        flexmock(logging).should_receive('basicConfig').replace_with(basicConfig)
        def setLogger(*args,**kwargs):
            pass
        flexmock(iceprod.core.logger).should_receive('setlogger').replace_with(setLogger)
        def removestdout(*args,**kwargs):
            pass
        flexmock(iceprod.core.logger).should_receive('removestdout').replace_with(removestdout)

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        super(modules_db_test,self).tearDown()

    @unittest_reporter
    def test_01_init(self):
        """Test init"""
        # mock some functions so we don't go too far
        def start(*args,**kwargs):
            start.called = True
        flexmock(db.db).should_receive('start').replace_with(start)
        start.called = False

        cfg = basic_config.BasicConfig()
        cfg.messaging_url = 'localhost'
        q = db.db(cfg)
        q.messaging = messaging_mock()
        if not q:
            raise Exception('did not return db object')
        if start.called is not True:
            raise Exception('init did not call start')

        new_cfg = {'new':1}
        q.messaging.BROADCAST.reload(cfg=new_cfg)
        if not q.messaging.called:
            raise Exception('init did not call messaging')
        if q.messaging.called != [['BROADCAST','reload',(),{'cfg':new_cfg}]]:
            raise Exception('init did not call correct message')

    @unittest_reporter
    def test_02_start_stop(self):
        """Test start_stop"""
        # mock some functions so we don't go too far
        def start(*args,**kwargs):
            start.called = True
        flexmock(db.db).should_receive('start').replace_with(start)
        start.called = False

        cfg = basic_config.BasicConfig()
        cfg.messaging_url = 'localhost'
        q = db.db(cfg)
        q.messaging = messaging_mock()

        q.start()
        if start.called is not True:
            raise Exception('did not start')

        local_db = _DB()
        q.db = local_db
        q.stop()
        if local_db.stopped is not True:
            raise Exception('did not stop DB')

        q.kill()
        if local_db.killed is not True:
            raise Exception('did not kill DB')

        cfg = {'test':1,'a':3}
        q.update_cfg(cfg)
        if q.cfg != cfg:
            raise Exception('did not update cfg')
        if local_db.cfg != cfg:
            raise Exception('did not update cfg on DB')

        q.db = None
        try:
            q.stop()
            q.kill()
            q.update_cfg(cfg)
        except Exception:
            logger.info('exception raised',exc_info=True)
            raise Exception('db = None and exception raised')

    @unittest_reporter
    def test_10_DBService(self):
        """Test DBService"""
        # mock some functions so we don't go too far
        def start(*args,**kwargs):
            start.called = True
        flexmock(db.db).should_receive('start').replace_with(start)
        start.called = False

        def cb(*args,**kwargs):
            cb.called = [args,kwargs]
        cb.called = None

        cfg = basic_config.BasicConfig()
        cfg.messaging_url = 'localhost'
        q = db.db(cfg)
        q.messaging = messaging_mock()
        local_db = _DB()
        q.db = local_db

        cb.called = None
        q.service_class.start(callback=cb)
        if start.called is not True:
            raise Exception('did not start')
        if not cb.called:
            raise Exception('did not call callback')

        cb.called = None
        q.service_class.stop(callback=cb)
        if local_db.stopped is not True:
            raise Exception('did not stop DB')
        if not cb.called:
            raise Exception('did not call callback')

        cb.called = None
        q.service_class.kill(callback=cb)
        if local_db.killed is not True:
            raise Exception('did not kill DB')
        if not cb.called:
            raise Exception('did not call callback')

        cb.called = None
        cfg = {'test':1,'a':3}
        q.service_class.reload(cfg,callback=cb)
        if local_db.cfg != cfg:
            raise Exception('did not update cfg')
        if not cb.called:
            raise Exception('did not call callback')

        cb.called = None
        q.service_class.backup(callback=cb)
        if local_db.backuped is not True:
            raise Exception('did not backup DB')
        if not cb.called:
            raise Exception('did not call callback')

        q.service_class.db_func(1,a=2)
        if local_db.dbmethods.db_func_called != [(1,),{'a':2}]:
            logger.info('db_func_called: %r',local_db.dbmethods.db_func_called)
            raise Exception('did not call rpc db func with correct args')

        q.db = None
        try:
            q.service_class.start()
            q.service_class.stop()
            q.service_class.kill()
            q.service_class.reload(cfg)
            q.service_class.backup()
        except Exception:
            logger.info('exception raised',exc_info=True)
            raise Exception('db = None and exception raised')

        try:
            q.service_class.db_func(1,a=2)
        except Exception:
            logger.info('e',exc_info=True)
        else:
            raise Exception('rpc db func did not raise error when db is None')

class conf_test(unittest.TestCase):
    @unittest_reporter
    def test_01_read_db_conf(self):
        d = db.read_db_conf()
        if not d:
            raise Exception('cannot load conf')
        if 'tables' not in d:
            raise Exception('tables not in conf')

        t = db.read_db_conf('tables')
        if not t:
            raise Exception('cannot get only tables')
        if d['tables'] != t:
            raise Exception('only tables != all["tables"]')
        if 'site' not in t:
            raise Exception('missing site table')
        if 'queues' not in t['site']:
            raise Exception('cannot find site queues')

class dbapi_test(unittest.TestCase):
    def setUp(self):
        super(dbapi_test,self).setUp()
        self.test_dir = tempfile.mkdtemp(dir=os.getcwd())

        # get hostname
        hostname = functions.gethostname()
        if hostname is None:
            hostname = 'localhost'
        elif isinstance(hostname,set):
            hostname = hostname.pop()
        self.hostname = hostname

        # set db class
        self._dbclass = db.DBAPI

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        super(dbapi_test,self).tearDown()

    @unittest_reporter
    def test_01_init(self):
        """Test init"""
        # mock db
        def start():
            start.called = True
        flexmock(self._dbclass).should_receive('start').replace_with(start)
        def tables():
            tables.called = True
        flexmock(self._dbclass).should_receive('_setup_tables').replace_with(tables)
        def init():
            init.called = True
        flexmock(self._dbclass).should_receive('init').replace_with(init)

        start.called = False
        tables.called = False
        init.called = False

        cfg = {'test':1}
        newdb = self._dbclass(cfg,None)
        if not newdb:
            raise Exception('init did not return db object')
        elif tables.called != True:
            raise Exception('init did not call _setup_tables')
        elif init.called != True:
            raise Exception('init did not call init')
        elif start.called != False:
            raise Exception('init called start when not supposed to')
        elif not newdb.cfg or 'test' not in newdb.cfg or newdb.cfg['test'] != 1:
            raise Exception('init did not copy cfg properly')

    @unittest_reporter
    def test_02_start_stop(self):
        """Test start_stop"""
        # mock db
        def _start_db():
            _start_db.called = True
        flexmock(self._dbclass).should_receive('_start_db').replace_with(_start_db)
        def _stop_db(force=False):
            _stop_db.called = True
        flexmock(self._dbclass).should_receive('_stop_db').replace_with(_stop_db)
        def tables():
            tables.called = True
        flexmock(self._dbclass).should_receive('_setup_tables').replace_with(tables)
        def init():
            init.called = True
        flexmock(self._dbclass).should_receive('init').replace_with(init)

        _start_db.called = False
        _stop_db.called = False
        tables.called = False
        init.called = False

        # test start
        cfg = {'db':{'name':'name','numthreads':1,'sqlite_cachesize':1000}}
        newdb = self._dbclass(cfg,None)
        if not newdb:
            raise Exception('start_stop did not return db object')

        newdb.start()
        if _start_db.called != True:
            raise Exception('start_stop did not call _start_db')
        elif tables.called != True:
            raise Exception('start_stop did not call _setup_tables')
        elif init.called != True:
            raise Exception('start_stop did not call init')

        # test stop
        newdb.stop()
        if _stop_db.called != True:
            raise Exception('start_stop did not call _stop_db')


try:
    import apsw
except:
    logger.error('Cannot import apsw. sqlite db not tested')
    print('Cannot import apsw. sqlite db not tested')
    sqlite_test = None
else:
    class sqlite_test(dbapi_test):
        def setUp(self):
            super(sqlite_test,self).setUp()

            # set db class
            self._dbclass = db.SQLite

        def tearDown(self):
            super(sqlite_test,self).tearDown()


try:
    import MySQLdb
except:
    logger.error('Cannot import MySQLdb. MySQL db not tested')
    print('Cannot import MySQLdb. MySQL db not tested')
    mysql_test = None
else:
    class mysql_test(dbapi_test):
        def setUp(self):
            super(mysql_test,self).setUp()

            # set db class
            self._dbclass = db.MySQL

        def tearDown(self):
            super(mysql_test,self).tearDown()


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    alltests = glob_tests(loader.getTestCaseNames(modules_db_test))
    suite.addTests(loader.loadTestsFromNames(alltests,modules_db_test))
    alltests = glob_tests(loader.getTestCaseNames(conf_test))
    suite.addTests(loader.loadTestsFromNames(alltests,conf_test))
    alltests = glob_tests(loader.getTestCaseNames(dbapi_test))
    suite.addTests(loader.loadTestsFromNames(alltests,dbapi_test))
    if sqlite_test:
        alltests = glob_tests(loader.getTestCaseNames(sqlite_test))
        suite.addTests(loader.loadTestsFromNames(alltests,sqlite_test))
    if mysql_test:
        alltests = glob_tests(loader.getTestCaseNames(mysql_test))
        suite.addTests(loader.loadTestsFromNames(alltests,mysql_test))
    return suite