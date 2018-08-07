from lib import action


class RebuildLastJob(action.JenkinsBaseAction):
    def run(self, project):
        last_build_number = self.jenkins.get_job_info(project)['lastCompletedBuild']['number']
        build_info_all = self.jenkins.get_job_info(project, last_build_number)['lastStableBuild']['actions']
        for p in build_info_all:
            if 'parameters' in p:
                build_info = p['parameters']
        build_parameters = {}
        for v in build_info:
            build_parameters.update({ v['name'] : v['value'] })
        return self.jenkins.build_job(project, build_parameters)
