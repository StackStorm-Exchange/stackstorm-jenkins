from lib import action


class BuildProject(action.JenkinsBaseAction):
    def run(self, project, parameters=None, config_override=None):
        if config_override is not None:
            self.config_override(config_override)
        return self.jenkins.build_job(project, parameters)
