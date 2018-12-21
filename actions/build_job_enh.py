from lib import action
from time import sleep
from jenkins import NotFoundException


class BuildProject(action.JenkinsBaseAction):
    def run(self, project, parameters=None):
        try:
            queue_id = self.jenkins.build_job(project, parameters)
        except NotFoundException:
            return False, {'error': 'Project {0} not found.'.format(project)}
        attempt = 0
        sleep_interval = 3
        run_build_result = False
        queue_item = None
        while attempt < 10 and not run_build_result:
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
