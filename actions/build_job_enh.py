from lib import action
from time import sleep
from jenkins import NotFoundException, JenkinsException


class BuildProject(action.JenkinsBaseAction):
    def run(self, project, max_wait=30, parameters=None, config_override=None):
        if config_override is not None:
            self.config_override(config_override)
        (status, queue_id) = self.kick_off_job(project, parameters)
        if status == 1:
            # try again without parameters
            (status, queue_id) = self.kick_off_job(project, {})
            if status > 0:
                # give up
                return False, queue_id
        elif status == 2:
            # queue_id will contain error
            return False, queue_id

        attempt = 0
        sleep_interval = 3
        max_attempts = int(max_wait / sleep_interval)
        run_build_result = False
        queue_item = None
        while attempt <= max_attempts and not run_build_result:
            queue_item = self.jenkins.get_queue_item(queue_id)
            if 'executable' in queue_item:
                run_build_result = True
                break
            else:
                attempt += 1
                sleep(sleep_interval)

        if not run_build_result and 'why' in queue_item:
            return run_build_result, queue_item['why']
        elif not run_build_result and 'why' not in queue_item:
            return run_build_result, {'error': 'General failure for queue_id {0}.'.format(queue_id)}
        else:
            return run_build_result, queue_item['executable']

    def kick_off_job(self, prj, prm):
        try:
            queue_id = self.jenkins.build_job(prj, prm)
        except NotFoundException:
            # terminal error
            return 2, {'error': 'Project {0} not found.'.format(prj)}
        except JenkinsException as e:
            msg = e.message
            msg = msg.encode('ascii', 'ignore')
            if 'doBuildWithParameters' in msg:
                # most likely build is not parameterized but we sent parameters, return non-terminal status
                return 1, {}
            else:
                # most likely something else and very bad happened, return terminal status
                return 2, {'error': 'General error: {0}'.format(msg)}
        else:
            return 0, queue_id

