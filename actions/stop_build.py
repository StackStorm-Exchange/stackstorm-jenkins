from lib import action
from jenkins import NotFoundException


class StopBuild(action.JenkinsBaseAction):
    def run(self, project, number):
        try:
            return self.jenkins.stop_build(project, number)
        except NotFoundException as e:
            return False, {'error': str(e)}
