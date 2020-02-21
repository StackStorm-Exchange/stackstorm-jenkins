import re
from six.moves.urllib.parse import unquote

from jenkins import JenkinsException

from lib import action


class GetRunningBuilds(action.JenkinsBaseAction):
    def run(self, name_pattern, config_override=None):
        if config_override is not None:
            self.config_override(config_override)
        try:
            running_builds = self.jenkins.get_running_builds()
        except JenkinsException as e:
            return False, {'error': str(e)}

        for build in running_builds:
            # Jenkins returns url-encoded names
            build['name_decoded'] = unquote(build['name'])

        if name_pattern is not None:
            filtered_running_builds = []
            for build in running_builds:
                if re.match(name_pattern, build['name_decoded']):
                    filtered_running_builds.append(build)

            return True, filtered_running_builds
        else:
            return True, running_builds
