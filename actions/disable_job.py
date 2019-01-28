from lib import action


class DisableProject(action.JenkinsBaseAction):
    def run(self, name, config_override=None):
        if config_override is not None:
            self.config_override(config_override)
        return self.jenkins.disable_job(name)
