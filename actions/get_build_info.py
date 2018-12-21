from lib import action
from jenkins import JenkinsException


class GetBuildInfo(action.JenkinsBaseAction):
    def run(self, project, number, depth):
        try:
            build_info = self.jenkins.get_build_info(project, number, depth=depth)
            return build_info
        except JenkinsException as e:
            return False, {'error': str(e)}
