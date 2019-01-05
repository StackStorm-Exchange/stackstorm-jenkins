from lib import action


class ListJobs(action.JenkinsBaseAction):
    def run(self):
        return self.jenkins.get_jobs()
