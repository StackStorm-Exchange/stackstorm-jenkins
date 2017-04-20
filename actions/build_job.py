from lib import action


class BuildProject(action.JenkinsBaseAction):
    def run(self, project, parameters=None):
        return self.jenkins.build_job(project, parameters)
