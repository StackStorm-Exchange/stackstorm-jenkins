from lib import action


class GetJobInfoRegex(action.JenkinsBaseAction):
    def run(self, pattern):
        result = ''
        for v in self.jenkins.get_job_info_regex(pattern, depth=0, folder_depth=0):
            result = result + v['displayName'] + '\n'
        return True, result
