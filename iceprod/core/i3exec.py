"""
The task runner.

Run it with `python -m iceprod.core.i3exec`.

optional arguments:
  -h, --help            show this help message and exit
  -f CFGFILE, --cfgfile CFGFILE
                        Specify config file
  -v VALIDATE, --validate VALIDATE
                        Specify if the config file should be validated
  -u URL, --url URL     URL of the iceprod server
  -p PASSKEY, --passkey PASSKEY
                        passkey for communcation with iceprod server
  -d, --debug           Enable debug actions and logging
  --offline             Enable offline mode (don't talk with server)
"""

import os
import sys
import logging
import logging.config
import time
import signal
from functools import partial

from iceprod.core import to_file, constants
import iceprod.core.dataclasses
import iceprod.core.serialization
import iceprod.core.exe

import iceprod.core.logger
logging.basicConfig()
logger = None

def handler(signum, frame):
    """Signal handler. Exit on SIGQUIT or SIGINT."""
    logger.warn('Signal handler called with signal %s' % signum)
    logger.warn('Exiting...')
    os._exit(0)

def load_config(cfgfile):
    """Load a config from file, serialized string, dictionary, etc"""
    config = None
    if isinstance(cfgfile,str):
        try:
            if os.path.exists(cfgfile):
                config = iceprod.core.serialization.serialize_json.load(cfgfile)
            else:
                config = iceprod.core.serialization.serialize_json.loads(cfgfile)
            if not config:
                raise Exception('Config not found')
        except Exception as e:
            logger.critical('Error loading configuration: %s' % str(e))
            raise
    elif isinstance(cfgfile,iceprod.core.dataclasses.Job):
        config = cfgfile
    elif isinstance(cfgfile,dict):
        config = iceprod.core.serialization.dict_to_dataclasses(cfgfile)
    else:
        logger.warn('cfgfile: %r',cfgfile)
        raise Exception('cfgfile is not a str or a Job')
    return config

def main(cfgfile=None, logfile=None, url=None, debug=False,
         passkey='', offline=False):
    """Main task runner for iceprod"""
    global logger
    # set up stdout and stderr
    stdout = partial(to_file,sys.stdout,constants['stdout'])
    stderr = partial(to_file,sys.stderr,constants['stderr'])
    with stdout(), stderr():
        # set up logger
        if debug:
            logl = 'INFO'
        else:
            logl = 'WARNING'
        if logfile:
            logf = logfile
        else:
            logf = os.path.abspath(os.path.expandvars(constants['stdlog']))
        iceprod.core.logger.setlogger('i3exec',
                                      None,
                                      loglevel=logl,
                                      logfile=logf,
                                      logsize=67108864,
                                      lognum=1)
        iceprod.core.logger.removestdout()
        logger = logging.getLogger('i3exec')
        logger.warn('starting...%s ' % logger.name)

        signal.signal(signal.SIGQUIT, handler)
        signal.signal(signal.SIGINT, handler)

        if cfgfile is None:
            logger.critical('There is no cfgfile')
            raise Exception('missing cfgfile')
        config = load_config(cfgfile)
        logger.info('config: %r',config)

        if offline is True:
            # run in offline mode
            runner(config,url,debug,offline)
            return

        # setup jsonRPC
        kwargs = {}
        if 'username' in config['options']:
            kwargs['username'] = config['options']['username']
        if 'password' in config['options']:
            kwargs['password'] = config['options']['password']
        if 'ssl' in config['options'] and config['options']['ssl']:
            kwargs.update(config['options']['ssl'])
        iceprod.core.exe.setupjsonRPC(url+'/jsonrpc',passkey,**kwargs)

        if 'tasks' in config and config['tasks']:
            logger.info('default configuration - a single task')
            runner(config,url,debug)
        else:
            logger.info('pilot mode - get many tasks from server')
            if 'gridspec' not in config['options']:
                logger.critical('gridspec missing')
                raise Exception('gridspec missing')
            errors = 0
            while errors < 5:
                try:
                    task_config = iceprod.core.exe.downloadtask(config['options']['gridspec'])
                except Exception:
                    errors += 1
                    logger.error('cannot download task. current error count is %d',
                                 errors, exc_info=True)
                    continue
                logger.info('task config: %r', task_config)

                if task_config is None:
                    break # assuming server wants client to exit
                else:
                    try:
                        runner(task_config,url,debug)
                    except Exception:
                        errors += 1
                        logger.error('task encountered an error. current error count is %d',
                                     errors, exc_info=True)
            if errors >= 5:
                logger.failure('too many errors when running tasks')
        logger.warn('finished running normally; exiting...')

def runner(config,url,debug=False,offline=False):
    """Run a config"""
    # set logging verbosity
    if ('debug' in config['options'] and config['options']['debug'] and
        'loglevel' not in config['options']):
        config['options']['loglevel'] = 'INFO'
    if ('loglevel' in config['options'] and
        config['options']['loglevel'].upper() in iceprod.core.logger.setlevel):
        try:
            logging.getLogger().setLevel(iceprod.core.logger.setlevel[config['options']['loglevel'].upper()])
        except Exception:
            logger.warn('failed to set a new log level', exc_info=True)

    # check that resource_url and debug are in options
    if 'resource_url' not in config['options']:
        config['options']['resource_url'] = str(url)+'/download'
    if 'debug' not in config['options']:
        config['options']['debug'] = bool(offline)

    # make sure some basic options are set
    if 'offline' not in config['options']:
        config['options']['offline'] = offline
    if 'data_url' not in config['options']:
        config['options']['data_url'] = 'gsiftp://gridftp.icecube.wisc.edu/'
    if 'svn_repository' not in config['options']:
        config['options']['svn_repository'] = 'http://code.icecube.wisc.edu/svn/'
    if 'job_temp' not in config['options']:
        config['options']['job_temp'] = os.path.join(os.getcwd(),'job_temp')
    if 'local_temp' not in config['options']:
        config['options']['local_temp'] = os.path.join(os.getcwd(),'local_temp')
    if 'job' not in config['options']:
        config['options']['job'] = '0'
    if 'stillrunninginterval' not in config['options']:
        config['options']['stillrunninginterval'] = 60

    if not config['steering']:
        # make sure steering exists in the config
        config['steering'] = iceprod.core.dataclasses.Steering()

    # make exe Config
    cfg = iceprod.core.exe.Config(config=config)

    # set up global env, based on config['options'] and config.steering
    env = iceprod.core.exe.setupenv(cfg, config['steering'],{'options':config['options']})

    logger.warn("config options: %r",config['options'])

    if not offline:
        # tell the server that we are processing this task
        try:
            iceprod.core.exe.processing(cfg)
        except Exception as e:
            logging.error(e)

    # keep track of the start time
    start_time = time.time()

    # find tasks to run
    try:
        if 'task' in config['options']:
            logger.warn('task specified: %r',config['options']['task'])
            # run only this task name or number
            if isinstance(config['options']['task'],iceprod.core.dataclasses.String):
                # find task by name
                for task in config['tasks']:
                    if task['name'] == config['options']['task']:
                        iceprod.core.exe.runtask(cfg, env, task)
                        break
                else:
                    logger.critical('cannot find task named \'%s\'',
                                    config['options']['task'])
                    raise Exception('cannot find specified task')
            elif isinstance(config['options']['task'],int):
                # find task by index
                if (config['options']['task'] >= 0 and
                    config['options']['task'] < len(config['tasks'])):
                    iceprod.core.exe.runtask(cfg, env, config['tasks'][config['options']['task']])
                else:
                    logger.critical('cannot find task index %d',
                                    config['options']['task'])
                    raise Exception('cannot find specified task')

            else:
                logger.critical('task specified in options is \'%r\', but no task found',config['options']['task'])
                raise Exception('cannot find specified task')
        else:
            # run all tasks in order
            for task in config['tasks']:
                iceprod.core.exe.runtask(cfg, env, task)
    except Exception as e:
        logger.error('task failed, exiting without running completion steps.',
                     exc_info=True)
        # set task status on server
        if not offline:
            try:
                iceprod.core.exe.taskerror(cfg, start_time=start_time)
            except Exception as e:
                logger.error(e)
        raise
    else:
        # destroy env
        iceprod.core.exe.destroyenv(env)
        del env
    finally:
        # upload log files to server
        try:
            if 'upload' in config['options']:
                if isinstance(config['options']['upload'],
                              iceprod.core.dataclasses.String):
                    upload = config['options']['upload'].lower().split('|')
                elif isinstance(config['options']['upload'],(tuple,list)):
                    upload = [x.lower() for x in config['options']['upload']]
                else:
                    raise Exception('upload config is not a valid type')
                for up in upload:
                    if up.startswith('logging'):
                        # upload err,log,out files
                        iceprod.core.exe.uploadLogging(cfg)
                        break
                    elif up.startswith('log'):
                        # upload log files
                        iceprod.core.exe.uploadLog(cfg)
                    elif up.startswith('err'):
                        # upload err files
                        iceprod.core.exe.uploadErr(cfg)
                    elif up.startswith('out'):
                        # upload out files
                        iceprod.core.exe.uploadOut(cfg)
        except Exception as e:
            logger.error('failed when uploading logging info',exc_info=True)


if __name__ == '__main__':
    # get arguments
    import argparse
    parser = argparse.ArgumentParser(description='IceProd Core')
    parser.add_argument('-f','--cfgfile', type=str,
                        help='Specify config file')
    parser.add_argument('-u','--url', type=str,
                        help='URL of the iceprod server')
    parser.add_argument('-p','--passkey', type=str,
                        help='passkey for communcation with iceprod server')
    parser.add_argument('-d','--debug', action='store_true', default=False,
                        help='Enable debug actions and logging')
    parser.add_argument('--offline', action='store_true', default=False,
                        help='Enable offline mode (don\'t talk with server)')
    parser.add_argument('--logfile', type=str, default=None,
                        help='Specify the logfile to use')

    args = vars(parser.parse_args())
    print args

    # check cfgfile
    if args['cfgfile'] is not None and not os.path.isfile(args['cfgfile']):
        if os.path.isfile(os.path.join(os.getcwd(),args['cfgfile'])):
            args['cfgfile'] = os.path.join(os.getcwd(),args['cfgfile'])
        else:
            args['cfgfile'] = None

    # start iceprod
    main(**args)
