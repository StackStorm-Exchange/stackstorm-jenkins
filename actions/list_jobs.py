from lib import action


class ListJobs(action.JenkinsBaseAction):
    def run(self, folder_depth=None, config_override=None):
        if config_override is not None:
            self.config_override(config_override)
        return self.jenkins.get_jobs(folder_depth=folder_depth)
