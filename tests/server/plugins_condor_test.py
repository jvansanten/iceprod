"""
Test script for condor plugin
"""

from __future__ import absolute_import, division, print_function

from tests.util import unittest_reporter, glob_tests

import logging
logger = logging.getLogger('plugins_condor_test')

import os
import sys
import time
import random
from datetime import datetime,timedelta
from contextlib import contextmanager
import shutil
import subprocess
from multiprocessing import Queue,Pipe

try:
    import cPickle as pickle
except:
    import pickle

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from flexmock import flexmock

import iceprod.server
from iceprod.server.plugins.condor import condor
from iceprod.core import dataclasses

from tests.server import grid_test

class plugins_condor_test(grid_test.grid_test):
    @unittest_reporter
    def test_100_generate_submit_file(self):
        """Test generate_submit_file"""
        site = 'thesite'
        self.check_run_stop = False
        name = 'grid1'
        gridspec = site+'.'+name
        submit_dir = os.path.join(self.test_dir,'submit_dir')
        os.mkdir(submit_dir)
        cfg = {'site_id':site,
               'queue':{'max_resets':5,
                        'submit_dir':submit_dir,
                        name:{'platform':None,
                              'batchopts':{},
                              'monitor_address':None,
                              }},
               'download':{'http_username':None,'http_password':None},
               'db':{'address':None,'ssl':False}}

        # init
        args = (gridspec,cfg['queue'][name],cfg,self._check_run,
                getattr(self.messaging,'db'))
        g = condor(args)
        if not g:
            raise Exception('init did not return grid object')

        # call normally
        g.tasks_queued = 0

        task = {'task_id':'thetaskid', 'submit_dir':submit_dir}
        g.generate_submit_file(task)
        if not os.path.isfile(os.path.join(submit_dir,'condor.submit')):
            raise Exception('submit file not written')
        for l in open(os.path.join(submit_dir,'condor.submit')):
            if l.startswith('arguments'):
                logger.info('args: %s',l)
                if '--passkey' in l:
                    raise Exception('passkey present when not supposed to be')
                if '--url' not in l:
                    raise Exception('download address not in args')
        os.unlink(os.path.join(submit_dir,'condor.submit'))

        # add passkey
        task = {'task_id':'thetaskid','submit_dir':submit_dir}
        passkey = 'aklsdfj'
        g.generate_submit_file(task,passkey=passkey)
        if not os.path.isfile(os.path.join(submit_dir,'condor.submit')):
            raise Exception('submit file not written')
        for l in open(os.path.join(submit_dir,'condor.submit')):
            if l.startswith('arguments'):
                if '--passkey' not in l:
                    raise Exception('passkey missing')
        os.unlink(os.path.join(submit_dir,'condor.submit'))

        # add batch opt
        cfg = dataclasses.Job()
        cfg['steering'] = dataclasses.Steering()
        cfg['steering']['batchsys'] = dataclasses.Batchsys()
        cfg['steering']['batchsys']['condor'] = {'+GPU_JOB':'true',
                'Requirements':'Target.Has_GPU == True'}
        g.generate_submit_file(task,cfg=cfg)
        if not os.path.isfile(os.path.join(submit_dir,'condor.submit')):
            raise Exception('submit file not written')
        gpu_job = False
        has_gpu = False
        for l in open(os.path.join(submit_dir,'condor.submit')):
            if (l.startswith('+GPU_JOB') and
                l.split('=')[-1].strip() == 'true'):
                gpu_job = True
            if (l.startswith('requirements') and
                'Target.Has_GPU == True' in l):
                has_gpu = True
        if not gpu_job:
            raise Exception('steering +GPU_JOB batchopt failed')
        if not has_gpu:
            raise Exception('steering requirements failed')
        os.unlink(os.path.join(submit_dir,'condor.submit'))

        # add batch opt
        cfg = dataclasses.Job()
        cfg['tasks'].append(dataclasses.Task())
        cfg['tasks'][0]['batchsys'] = dataclasses.Batchsys()
        cfg['tasks'][0]['batchsys']['condor'] = {'+GPU_JOB':'true',
                'Requirements':'Target.Has_GPU == True'}
        g.generate_submit_file(task,cfg=cfg)
        if not os.path.isfile(os.path.join(submit_dir,'condor.submit')):
            raise Exception('submit file not written')
        gpu_job = False
        has_gpu = False
        for l in open(os.path.join(submit_dir,'condor.submit')):
            if (l.startswith('+GPU_JOB') and
                l.split('=')[-1].strip() == 'true'):
                gpu_job = True
            if (l.startswith('requirements') and
                'Target.Has_GPU == True' in l):
                has_gpu = True
        if not gpu_job:
            raise Exception('task +GPU_JOB batchopt failed')
        if not has_gpu:
            raise Exception('task requirements failed')
        os.unlink(os.path.join(submit_dir,'condor.submit'))

    @unittest_reporter
    def test_101_submit(self):
        """Test submit"""
        def caller(*args,**kwargs):
            caller.called = True
            caller.args = args
            caller.kwargs = kwargs
            if isinstance(caller.ret,Exception):
                raise caller.ret
            return caller.ret
        flexmock(subprocess).should_receive('check_output').replace_with(caller)

        site = 'thesite'
        self.check_run_stop = False
        name = 'grid1'
        gridspec = site+'.'+name
        submit_dir = os.path.join(self.test_dir,'submit_dir')
        os.mkdir(submit_dir)
        cfg = {'site_id':site,
               'queue':{'max_resets':5,
                        'submit_dir':submit_dir,
                        name:{'platform':None,
                              'batchopts':{},
                              'monitor_address':None,
                              }},
               'download':{'http_username':None,'http_password':None},
               'db':{'address':None,'ssl':False}}

        # init
        args = (gridspec,cfg['queue'][name],cfg,self._check_run,
                getattr(self.messaging,'db'))
        g = condor(args)
        if not g:
            raise Exception('init did not return grid object')

        # call normally
        caller.called = False
        caller.ret = ''
        g.tasks_queued = 0

        task = {'task_id':'thetaskid','submit_dir':submit_dir}
        g.submit(task)
        if not caller.called:
            raise Exception('subprocess.call not called')
        if caller.args[0][0] != 'condor_submit':
            logger.info('args: %r',caller.args)
            raise Exception('does not start with condor_submit')
        if 'cwd' not in caller.kwargs or caller.kwargs['cwd'] != submit_dir:
            raise Exception('did not change to submit dir')

        # call failed
        caller.called = False
        caller.ret = Exception('bad call')
        g.tasks_queued = 0

        task = {'task_id':'thetaskid','submit_dir':submit_dir}
        try:
            g.submit(task)
        except:
            pass
        else:
            raise Exception('did not return Exception')


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    alltests = glob_tests(loader.getTestCaseNames(plugins_condor_test))
    suite.addTests(loader.loadTestsFromNames(alltests,plugins_condor_test))
    return suite
