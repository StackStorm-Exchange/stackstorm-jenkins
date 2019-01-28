from lib import action


class EnableProject(action.JenkinsBaseAction):
    def run(self, name, config_override=None):
        if config_override is not None:
            self.config_override(config_override)
        return self.jenkins.enable_job(name)
