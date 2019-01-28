from lib import action


class GetJobInfo(action.JenkinsBaseAction):
    def run(self, project, config_override=None):
        if config_override is not None:
            self.config_override(config_override)
        return self.jenkins.get_job_info(project, depth=0, fetch_all_builds='False')
