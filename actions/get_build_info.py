from lib import action
from jenkins import JenkinsException


class GetBuildInfo(action.JenkinsBaseAction):
    def run(self, project, number, depth, config_override=None):
        if config_override is not None:
            self.config_override(config_override)
        try:
            build_info = self.jenkins.get_build_info(project, number, depth=depth)
            return build_info
        except JenkinsException as e:
            return False, {'error': str(e)}
