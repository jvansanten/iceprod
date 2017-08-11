"""
The master_updater module queues and sends updates to the master.
It uses a disk-based store to make sure updates survive restarting
the local instance.
"""

import os
import logging
import tempfile
try:
    import cPickle as pickle
except ImportError:
    import pickle
from collections import deque

import tornado.gen
from tornado.concurrent import run_on_executor
from tornado.locks import Lock

import requests

import iceprod.server
from iceprod.server import module
from iceprod.server.master_communication import send_master

logger = logging.getLogger('modules_master_updater')

class master_updater(module.module):
    """
    Run the master_updater module, which handles updating the master.
    """

    def __init__(self,*args,**kwargs):
        # run default init
        super(master_updater,self).__init__(*args,**kwargs)
        self.service['add'] = self.add

        self.filename = '.master_updater_queue'
        self.buffer = []
        self.send_in_progress = False
        self.session = requests.Session()
        self.save_timeout = None

    def start(self):
        """Start master updater"""
        super(master_updater,self).start()
        if ('master_updater' in self.cfg and
            'filename' in self.cfg['master_updater']):
            self.filename = os.path.expandvars(os.path.expanduser(
                            self.cfg['master_updater']['filename']))
        if os.path.exists(self.filename):
            self._load()
        self.io_loop.add_callback(self._send)

    def stop(self):
        """Stop master updater"""
        self.save_timeout = None
        super(master_updater,self).stop()

    def kill(self):
        """Kill master updater"""
        self.save_timeout = None
        super(master_updater,self).kill()

    def _load(self):
        """Load from cache file"""
        with open(self.filename,'rb') as f:
            self.buffer = pickle.load(f)

    def _save_to_file(self):
        """Save to cache file"""
        p = os.path.basename(self.filename)
        d = os.path.dirname(os.path.abspath(self.filename))
        fd,fname = tempfile.mkstemp(prefix=p, dir=d)
        try:
            with os.fdopen(fd, 'wb') as f:
                pickle.dump(self.buffer, f, -1)
            os.rename(fname, self.filename)
        except Exception:
            logger.warn('did not save cache file', exc_info=True)
            os.remove(fname)
        self.save_timeout = None

    def _save(self):
        """
        Initiate save event.

        Because saves are expensive, only do one per second.
        """
        if self.save_timeout is None:
            self.save_timeout = self.io_loop.call_later(1, self._save_to_file)

    @tornado.gen.coroutine
    def add(self, obj):
        """Add obj to queue"""
        try:
            self.buffer.append(obj)
            self._save()
            if not self.send_in_progress:
                self.send_in_progress = True
                self.io_loop.add_callback(self._send)
        except Exception:
            logger.error('failed to add %r to buffer', obj, exc_info=True)
            raise

    @tornado.gen.coroutine
    def _send(self):
        """Send an update to the master"""
        if self.buffer:
            self.send_in_progress = True
            data = self.buffer[:1000]
            params = {'updates':data}
            try:
                yield send_master(self.cfg, 'master_update',
                                  session=self.session, **params)
            except Exception:
                logger.warn('error sending to master', exc_info=True)
                # If the problem is server side, give it a minute.
                # This should stop a DDOS from happening.
                self.io_loop.call_later(60, self._send)
            else:
                # remove data we just successfully sent
                self.buffer = self.buffer[1000:]
                self._save()
                self.io_loop.add_callback(self._send)
        else:
            self.send_in_progress = False

