"""
Cron database methods
"""

import logging
from datetime import datetime, timedelta
from functools import partial
from collections import OrderedDict

import tornado.gen

from iceprod.core.jsonUtil import json_encode,json_decode
from iceprod.server.dbmethods import _Methods_Base,datetime2str,str2datetime, nowstr

logger = logging.getLogger('dbmethods.cron')

class cron(_Methods_Base):
    """
    The scheduled (cron) DB methods.

    Takes a handle to a subclass of iceprod.server.modules.db.DBAPI
    as an argument.
    """

    @tornado.gen.coroutine
    def cron_dataset_completion(self):
        """Check for newly completed datasets and mark them as such"""
        with (yield self.parent.db.acquire_lock('dataset')):
            sql = 'select dataset_id,jobs_submitted,tasks_submitted '
            sql += ' from dataset where status = ? '
            bindings = ('processing',)
            ret = yield self.parent.db.query(sql, bindings)
            datasets = OrderedDict()
            for dataset_id,njobs,ntasks in ret:
                datasets[dataset_id] = {'jobs_submitted':njobs,
                                        'tasks_submitted':ntasks,
                                        'task_status':set(),
                                        'ntasks':0}
            if not datasets:
                return
            sql = 'select dataset_id,task_status from search '
            sql += ' where dataset_id in ('
            sql += ','.join(['?' for _ in datasets])
            sql += ')'
            bindings = tuple(datasets.keys())
            ret = yield self.parent.db.query(sql, bindings)
            for dataset_id,task_status in ret:
                datasets[dataset_id]['ntasks'] += 1
                datasets[dataset_id]['task_status'].add(task_status)

            dataset_status = {}
            for dataset_id in datasets:
                total_tasks = datasets[dataset_id]['tasks_submitted']
                #tasks_per_job = int(total_tasks/total_jobs)
                ntasks = datasets[dataset_id]['ntasks']
                if ntasks < total_tasks:
                    continue # not all tasks accounted for
                task_statuses = datasets[dataset_id]['task_status']
                if not task_statuses&{'waiting','queued','processing','resume','reset'}:
                    logger.info('dataset %s task statues %r',dataset_id,task_statuses)
                    if not task_statuses-{'complete'}:
                        dataset_status[dataset_id] = 'complete'
                    elif not task_statuses-{'complete','failed'}:
                        dataset_status[dataset_id] = 'errors'
                    elif not task_statuses-{'complete','failed','suspended'}:
                        dataset_status[dataset_id] = 'suspended'
            if dataset_status:
                # update dataset statuses
                now = nowstr()
                statuses = {}
                for dataset_id in dataset_status:
                    status = dataset_status[dataset_id]
                    logger.info('dataset %s marked as %s',dataset_id,status)
                    if status not in statuses:
                        statuses[status] = set()
                    statuses[status].add(dataset_id)
                multi_sql = []
                multi_bindings = []
                master_sql = []
                master_bindings = []
                for s in statuses:
                    bindings = (s,)
                    sql = 'update dataset set status = ?'
                    if s == 'complete':
                        sql += ', end_date = ? '
                        bindings += (now,)
                    sql += ' where dataset_id in ('
                    sql += ','.join(['?' for _ in statuses[s]])
                    sql += ')'
                    bindings += tuple([d for d in statuses[s]])
                    multi_sql.append(sql)
                    multi_bindings.append(bindings)
                    # now prepare individual master sqls
                    bindings = (s,)
                    sql = 'update dataset set status = ?'
                    if s == 'complete':
                        sql += ', end_date = ? '
                        bindings += (now,)
                    sql += ' where dataset_id = ? '
                    for d in statuses[s]:
                        master_sql.append(sql)
                        master_bindings.append(bindings+(d,))
                yield self.parent.db.query(multi_sql, multi_bindings)

                if self._is_master():
                    sql3 = 'replace into master_update_history (table_name,update_index,timestamp) values (?,?,?)'
                    for sql,bindings in zip(master_sql,master_bindings):
                        bindings3 = ('dataset',bindings[-1],now)
                        try:
                            yield self.parent.db.query(sql, bindings3)
                        except Exception:
                            logger.info('error updating master_update_history',
                                        exc_info=True)
                else:
                    for sql,bindings in zip(master_sql,master_bindings):
                        yield self._send_to_master(('dataset',bindings[-1],now,sql,bindings))

                # TODO: consolidate dataset statistics

    @tornado.gen.coroutine
    def cron_job_completion(self):
        """Check for newly completed jobs and mark them as such"""
        sql = 'select dataset_id,jobs_submitted,tasks_submitted '
        sql += ' from dataset where status = ? '
        bindings = ('processing',)
        ret = yield self.parent.db.query(sql, bindings)
        datasets = {}
        for dataset_id,njobs,ntasks in ret:
            datasets[dataset_id] = ntasks//njobs
        if not datasets:
            return

        sql = 'select dataset_id, job_id, count(*) from search '
        sql += ' where task_status = "complete" and dataset_id in ('
        sql += ','.join(['?' for _ in datasets])
        sql += ') group by job_id'
        bindings = tuple(datasets)
        ret = yield self.parent.db.query(sql, bindings)

        jobs = set()
        for dataset_id,job_id,num in ret:
            if datasets[dataset_id] <= num:
                jobs.add(job_id)

        now = nowstr()
        sql = 'update job set status = "complete", status_changed = ? '
        sql += ' where job_id = ?'
        for job_id in jobs:
            # update job status
            logger.info('job %s marked as complete',job_id)
            bindings = (now,job_id)
            yield self.parent.db.query(sql, bindings)
            if self._is_master():
                sql3 = 'replace into master_update_history (table_name,update_index,timestamp) values (?,?,?)'
                bindings3 = ('job',job_id,now)
                try:
                    yield self.parent.db.query(sql3, bindings3)
                except Exception as e:
                    logger.info('error updating master_update_history',
                                exc_info=True)
            else:
                yield self._send_to_master(('job',job_id,now,sql,bindings))

            # TODO: collate task stats

            # clean dagtemp
            if 'site_temp' in self.parent.cfg['queue']:
                temp_dir = self.parent.cfg['queue']['site_temp']
                dataset = GlobalID.localID_ret(dataset_id, type='int')
                sql = 'select job_index from job where job_id = ?'
                bindings = (job_id,)
                try:
                    ret = yield self.parent.db.query(sql, bindings)
                    job = ret[0][0]
                    dagtemp = os.path.join(temp_dir, dataset, job)
                    logger.info('cleaning site_temp %r', dagtemp)
                    functions.delete(dagtemp)
                except Exception as e:
                    logger.warn('failed to clean site_temp', exc_info=True)

    def cron_remove_old_passkeys(self):
        now = nowstr()
        sql = 'delete from passkey where expire < ?'
        bindings = (now,)
        return self.parent.db.query(sql, bindings)

    @tornado.gen.coroutine
    def cron_generate_web_graphs(self):
        sql = 'select task_status, count(*) from search '
        sql += 'where task_status not in (?,?,?) group by task_status'
        bindings = ('idle','waiting','complete')
        ret = yield self.parent.db.query(sql, bindings)

        now = nowstr()
        results = {}
        for status, count in ret:
            results[status] = count
        graph_id = yield self.parent.db.increment_id('graph')
        sql = 'insert into graph (graph_id, name, value, timestamp) '
        sql += 'values (?,?,?,?)'
        bindings = (graph_id, 'active_tasks', json_encode(results), now)
        yield self.parent.db.query(sql, bindings)
        
        time_interval = datetime2str(datetime.utcnow()-timedelta(minutes=1))
        sql = 'select count(*) from task where status = ? and '
        sql += 'status_changed > ?'
        bindings = ('complete', time_interval)
        ret = yield self.parent.db.query(sql, bindings)

        now = nowstr()
        results = {'completions':ret[0][0] if ret and ret[0] else 0}
        graph_id = yield self.parent.db.increment_id('graph')
        sql = 'insert into graph (graph_id, name, value, timestamp) '
        sql += 'values (?,?,?,?)'
        bindings = (graph_id, 'completed_tasks', json_encode(results), now)
        yield self.parent.db.query(sql, bindings)
