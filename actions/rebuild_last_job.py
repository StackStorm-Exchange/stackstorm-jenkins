from lib import action


class RebuildLastJob(action.JenkinsBaseAction):
    def run(self, project, config_override=None):
        if config_override is not None:
            self.config_override(config_override)
        last_number = self.jenkins.get_job_info(project)['lastCompletedBuild']['number']
        binfo_all = self.jenkins.get_job_info(project, last_number)['lastStableBuild']['actions']
        for p in binfo_all:
            if 'parameters' in p:
                build_info = p['parameters']
        build_parameters = {}
        for v in build_info:
            build_parameters.update({v['name']: v['value']})
        return self.jenkins.build_job(project, build_parameters)
