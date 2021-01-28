from lib import action
from jenkins import NotFoundException


class StopBuild(action.JenkinsBaseAction):
    def run(self, project, number, config_override=None):
        if config_override is not None:
            self.config_override(config_override)
        try:
            return self.jenkins.stop_build(project, number)
        except NotFoundException as e:
            return False, {'error': str(e)}
