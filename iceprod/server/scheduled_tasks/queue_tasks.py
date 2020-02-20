"""
Queue tasks.

Move task statuses from waiting to queued, for a certain number of
tasks.  Also uses priority for ordering.

Initial delay: rand(1 minute)
Periodic delay: 5 minutes
"""

import logging
import random
import time
from collections import defaultdict

from tornado.ioloop import IOLoop

from iceprod.server import GlobalID

logger = logging.getLogger('queue_tasks')

NTASKS = 250000

def queue_tasks(module):
    """
    Initial entrypoint.

    Args:
        module (:py:class:`iceprod.server.modules.schedule`): schedule module
    """
    # initial delay
    IOLoop.current().call_later(random.randint(5,60), run, module.rest_client)

async def run(rest_client, debug=False):
    """
    Actual runtime / loop.

    Args:
        rest_client (:py:class:`iceprod.core.rest_client.Client`): rest client
        debug (bool): debug flag to propagate exceptions
    """
    start_time = time.time()
    try:
        num_tasks_waiting = 0
        num_tasks_queued = 0
        tasks = await rest_client.request('GET', '/task_counts/status')
        if 'waiting' in tasks:
            num_tasks_waiting = tasks['waiting']
        if 'queued' in tasks:
            num_tasks_queued = tasks['queued']
        tasks_to_queue = min(num_tasks_waiting, NTASKS - num_tasks_queued)

        while tasks_to_queue > 0:
            num = min(tasks_to_queue, 100)
            tasks_to_queue -= num

            ret = await rest_client.request('POST', '/task_actions/queue', {'num_tasks': num})
            if ret < num:
                break

    except Exception:
        logger.error('error queueing tasks', exc_info=True)
        if debug:
            raise

    # run again after 5 minute delay
    stop_time = time.time()
    delay = max(60*5 - (stop_time-start_time), 60)
    IOLoop.current().call_later(delay, run, rest_client)
