"""
The schedule module is a basic cron for IceProd, executing tasks
at various intervals or fixed times.
"""

from __future__ import absolute_import, division, print_function

import time
from threading import Thread,Event,Condition
import logging
from functools import partial
from contextlib import contextmanager
from itertools import izip

import tornado.gen
from tornado.concurrent import run_on_executor

import iceprod.server
from iceprod.server import module
from iceprod.server.schedule import Scheduler

logger = logging.getLogger('modules_schedule')

class schedule(module.module):
    """
    Run the schedule module, which handles periodic tasks.
    """

    def __init__(self,*args,**kwargs):
        # run default init
        super(schedule,self).__init__(*args,**kwargs)
        self.scheduler = None

    def start(self):
        """Start schedule"""
        super(schedule,self).start()
        if not self.scheduler:
            # make Scheduler
            self.scheduler = Scheduler()
            try:
                self._make_schedule()
            except Exception:
                logger.info('error making schedule', exc_info=True)
                self.messaging.daemon.stop()
                raise

        # start things
        self.scheduler.start()

    def stop(self):
        """Stop schedule"""
        if self.scheduler:
            self.scheduler.finish()
            self.scheduler.join(10) # wait up to 10 seconds for scheduler to finish
            if self.scheduler.is_alive():
                logger.warn('scheduler still running after 10 seconds')
            self.scheduler = None
        super(schedule,self).stop()

    def kill(self):
        """Kill thread"""
        if self.scheduler:
            self.scheduler.finish()
            self.scheduler.join(0.01) # wait only a very short amount of time
            self.scheduler = None
        super(schedule,self).kill()

    def _make_schedule(self):
        """Make the default schedule"""

        # mark dataset complete
        self.scheduler.schedule('every 1 hours',
                partial(self._db_call,'cron_dataset_completion'))

        # collate node resources
        self.scheduler.schedule('every 1 hours',
                partial(self._db_call,'node_collate_resources',
                        site_id=self.cfg['site_id']))

        self.scheduler.schedule('every 6 hours',
                partial(self._db_call, 'cron_remove_old_passkeys'))

        self.scheduler.schedule('every 10 minutes',
                partial(self._db_call, 'cron_generate_web_graphs'))

        if ('master' in self.cfg and 'status' in self.cfg['master'] and
            self.cfg['master']['status']):
            self._master_schedule()

    def _master_schedule(self):
        # fake a grid, so we can do grid-like things
        from iceprod.server.grid import grid
        @contextmanager
        def checkrun():
            yield
        args = [None, self.cfg['queue']['*'], self.cfg, checkrun,
                self.messaging.db]
        master_grid = grid(args)

        self.scheduler.schedule('every 1 minutes', master_grid.check_iceprod)

    def _db_call(self,func,**kwargs):
        """Call DB func, handling any errors"""
        logger.info('running %s',func)
        def cb(ret):
            if isinstance(ret,Exception):
                logger.warn('error running %s: %r',func,ret)
            else:
                logger.info('completed %s',func)
        try:
            ret = getattr(self.messaging.db,func)(callback=cb,**kwargs)
        except Exception as e:
            logger.warn('error running %s',func,exc_info=True)
