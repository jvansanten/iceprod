"""
Server
======

Run the iceprod server.
"""

from __future__ import absolute_import, division, print_function

import os
import logging
from functools import partial
import importlib
import subprocess

from tornado.ioloop import IOLoop

from concurrent.futures import ThreadPoolExecutor

from iceprod.core.logger import set_log_level
from iceprod.server.config import IceProdConfig


logger = logging.getLogger('Server')

class Server(object):
    """
    The actual server.

    """
    def __init__(self):
        self.io_loop = IOLoop.current()
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.cfg = IceProdConfig()
        self.modules = {}
        self.services = {'daemon': {'restart': self.restart,
                                    'reload': self.reload,
                                    'stop': self.stop,
                                    'kill': self.kill,
                                    'get_running_modules': lambda: self.modules.keys(),
                                   },
                        }

        set_log_level(self.cfg['logging']['level'])

        for mod_name in self.cfg['modules']:
            if self.cfg['modules'][mod_name]:
                m = importlib.import_module('iceprod.server.modules.'+mod_name)
                mod = getattr(m, mod_name)(cfg=self.cfg,
                                           io_loop=self.io_loop,
                                           executor=self.executor,
                                           modules=self.services)
                self.modules[mod_name] = mod
                self.services[mod_name] = mod.service
                mod.start()

    def run(self):
        self.io_loop.start()

    def restart(self):
        env = os.environ.copy()
        extra_path = os.path.join(os.environ['I3PROD'],'bin')
        env['PATH'] = extra_path+(':'+env['PATH'] if 'PATH' in env else '')
        subprocess.Popen(['iceprod_server.py','restart'],
                         cwd=os.environ['I3PROD'], env=env)

    def reload(self):
        for m in self.modules.values():
            m.stop()
            m.start()

    def stop(self):
        for m in self.modules.values():
            m.stop()
        self.io_loop.stop()

    def kill(self):
        for m in self.modules.values():
            m.kill()
        self.io_loop.stop()