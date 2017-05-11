#!/usr/bin/env python

"""
Create a Condor DAG that runs a given IceProd2 dataset in offline mode. This
can't use any of IceProd2's load-balancing, resource caching, or monitoring
facilities, but can at least run while the server is busy chewing through
long-running datasets.
"""

from __future__ import print_function

from iceprod.core.exe import Config, setupenv
from iceprod.core.i3exec import load_config
from functools import partial
import getpass, pwd
from os.path import expandvars, basename, isdir
from os import mkdir
import sys
from collections import OrderedDict
import logging

def condor_stringify(obj):
    if isinstance(obj, (str, float, int, unicode)):
        return str(obj)
    elif isinstance(obj, (list, tuple)):
        return " ".join([condor_stringify(subobj) for subobj in obj])
    else:
        raise TypeError, "Can't convert '%s' into something DAGMan understands" % obj

class Node(object):
    def __init__(self, label, subfile, pre=None, post=None, done=False, retry=1, category='GENERIC', priority=None, **vars):
        self.label = str(label)
        self.subfile = str(subfile)
        self.done = done
        self.pre = pre
        self.post = post
        self.retry = retry
        self.vars = vars
        if not 'DAGNodeName' in vars:
            self.vars['DAGNodeName'] = label
        self.category = category
        self.priority = priority
    def dump(self, fh=sys.stdout):
        fh.write("JOB %s %s\n" % (self.label, self.subfile))
        fh.write("CATEGORY %s %s\n" % (self.label, self.category))
        varargs = ['%s="%s"' % (k, condor_stringify(v)) for k,v in self.vars.iteritems() if v is not None]
        if len(varargs) > 0:
            fh.write("VARS %s %s\n" % (self.label, " ".join(varargs)))
        if self.pre:
            fh.write("SCRIPT PRE %s %s\n" % (self.label, condor_stringify(self.pre)))
        if self.post:
            fh.write("SCRIPT POST %s %s\n" % (self.label, condor_stringify(self.post)))
        if self.priority:
            fh.write("PRIORITY %s %s\n" % (self.label, condor_stringify(self.priority)))
        if self.retry != 1:
            fh.write("RETRY %s %s\n" % (self.label, condor_stringify(self.retry)))
        if self.done:
            fh.write("DONE %s \n" % (self.label))
            
class DAG(object):

    def __init__(self, maxjobs=30):
        self.maxjobs = maxjobs
        self.nodes = OrderedDict()
        
    def __len__(self):
        return len(self.nodes)

    def add(self, node, depends=[]):
        deps = []
        for d in depends:
            if isinstance(d, Node):
                label = d.label
            else:
                label = d
            if not label in self.nodes:
                raise ValueError, "Can't declare dependency on unknown node '%s'" % (label)
            deps.append(label)
        self.nodes[node.label] = (node, deps)

    def dump_node(self, key, dest, memo):
        if key in memo:
            return
        node, deps = self.nodes[key]

        # Recurse to dependencies if they exist
        for dep in deps:
            self.dump_node(dep, dest, memo)

        # Emit the job
        node.dump(dest)

        # Declare dependencies (_after_ both PARENT and CHILD have been declared)
        if len(deps) > 0:
            dest.write("PARENT %s CHILD %s\n" % (condor_stringify(deps), key))

        # Mark as done
        memo.add(key)
            

    def write(self, dest=sys.stdout):
        if isinstance(dest, file):
            out = dest
        elif isinstance(dest, str):
            out = open(dest, 'w')

        # Keep track of which nodes have already been emitted
        memo = set()
    
        for job in self.nodes:
            self.dump_node(job, out, memo)

        if dest is not sys.stdout:
            out.write("NODE_STATUS_FILE %s 30\n" % (dest + ".nodestatus"))
        #categories = set([node.category for node in self.nodes.itervalues()])
        #for cat in categories:
        #   out.write("MAXJOBS %s %d\n" % (category, self.maxjobs))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('-x', dest='x509', default='/tmp/x509up_u{}'.format(pwd.getpwnam(getpass.getuser()).pw_uid), help='x509 proxy path')
    parser.add_argument('-e', dest='loader', default=expandvars('$ICEPRODROOT/bin/loader.sh'), help='path to iceprod loader script')
    parser.add_argument('--jobs', type=int, help="Number of jobs to schedule", default=None)
    parser.add_argument('--run-only', nargs='+', type=int, help="Only run these job indices. If omitted, run all jobs.", default=None)
    parser.add_argument('--retry', type=int, help="Number of times to retry failed jobs", default=1)
    parser.add_argument('--blacklist', type=str, nargs='+', help="Glidein sites to exclude", default=None)
    parser.add_argument('cfgfile', help='path to iceprod dataset configuration file')
    opts = parser.parse_args()
    
    logging.basicConfig(level='INFO')
    
    config = load_config(opts.cfgfile)
    cfg = Config(config=config)

    def label_for_task(index, name):
        return '{}.{:06d}.{}'.format(cfg.config['dataset'], index, name)

    # write a generic submit file
    subfile = '{}.sub'.format(cfg.config['dataset'])
    with open(subfile, 'w') as f:
        p = partial(print,sep='',file=f)
        p('transfer_input_files={}'.format(','.join([opts.x509, opts.cfgfile])))
        p('skip_filechecks = True')
        p('should_transfer_files = always')
        p('when_to_transfer_output = ON_EXIT_OR_EVICT')
        p('+SpoolOnEvict = False')
        p('transfer_output_files = iceprod_log, iceprod_out, iceprod_err')
        p('log = {}.log'.format(cfg.config['dataset']))
        p('+FileSystemDomain=lalaland')
        requirements = ['(TARGET.ICECUBE_CVMFS_Exists)']
        if opts.blacklist is not None:
            blacklist = ",".join(['"{}"'.format(s) for s in opts.blacklist])
            p("+blacklist={"+blacklist+"}")
            requirements.append("(!member(TARGET.GLIDEIN_Site, MY.blacklist))")
        p("requirements = {}".format('&&'.join(requirements)))
        p('queue')
    logging.info("Wrote submit file: {}".format(subfile))
    if not isdir('logs'):
        mkdir('logs')

    dag = DAG()
    
    default_args = '-s {} -x {} --offline --cfgfile {}'.format('/cvmfs/icecube.opensciencegrid.org/iceprod/master', basename(opts.x509), basename(opts.cfgfile))
    
    for task in cfg.config['tasks']:
    
        requirements = dict(request_memory='{}G'.format(task['requirements'].get('memory', 1)),
                            request_disk='{}G'.format(task['requirements'].get('disk', 1)))
        if 'gpu' in task['requirements']:
            requirements['request_gpus'] = task['requirements']['gpu']
    
        maxjobs = cfg.config['options']['jobs_submitted']
        if opts.jobs is not None:
            maxjobs = min((maxjobs, opts.jobs))
        for job in range(maxjobs):
            if opts.run_only is not None and not job in opts.run_only:
                continue
            cfg.config['options']['job'] = job
        
            label = label_for_task(job, task['name'])
            dependencies = map(partial(label_for_task, job), task['depends'])
        
            options = {
                'executable' : opts.loader,
                'arguments'  : default_args+' --task {} --job {}'.format(task['name'], job),
                'output'     : 'logs/{}.out'.format(label),
                'error'      : 'logs/{}.err'.format(label),
                'transfer_output_remaps' : '\\"iceprod_log=logs/{}.iceprod.log;iceprod_out=logs/{}.iceprod.out;iceprod_err=logs/{}.iceprod.err\\"'.format(*((label,)*3)),
            }
            options.update(requirements)
        
            node = Node(label, subfile, **options)
            dag.add(node, dependencies)

    dagfile = '{}.dag'.format(cfg.config['dataset'])
    dag.write(dagfile)
    logging.info("Wrote {} nodes to {}".format(len(dag.nodes), dagfile))
    logging.info("Submit with `condor_submit_dag {}`".format(dagfile))
    
