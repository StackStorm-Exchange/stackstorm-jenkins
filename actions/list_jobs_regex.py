from lib import action


class GetJobInfoRegex(action.JenkinsBaseAction):
    def run(self, pattern, folder_depth=None, config_override=None):
        if config_override is not None:
            self.config_override(config_override)
        result = ''
        for v in self.jenkins.get_job_info_regex(pattern, depth=0, folder_depth=folder_depth):
            result = result + v['displayName'] + '\n'
        return True, result
