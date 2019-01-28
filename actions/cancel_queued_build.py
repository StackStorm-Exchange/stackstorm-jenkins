from lib import action
from jenkins import NotFoundException


class CancelQueuedBuild(action.JenkinsBaseAction):
    def run(self, job_id, config_override=None):
        if config_override is not None:
            self.config_override(config_override)
        try:
            return self.jenkins.cancel_queue(job_id)
        except NotFoundException as e:
            return False, {'error': str(e)}
