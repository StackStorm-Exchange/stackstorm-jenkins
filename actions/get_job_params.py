from lib import action


class GetJobParams(action.JenkinsBaseAction):
    def run(self, project, params, config_override=None):
        if config_override is not None:
            self.config_override(config_override)
        job_info = self.jenkins.get_job_info(project, depth=0, fetch_all_builds='False')
        try:
            job_actions = job_info['actions']
        except KeyError:
            job_actions = []
        self.logger.debug("Read jobs config: %s", job_actions)
        job_params = {}
        for i in job_actions:
            try:
                cls = i['_class']
            except KeyError:
                continue
            self.logger.debug("Class detected as: %s", cls)
            if cls == 'hudson.model.ParametersDefinitionProperty':
                for p_def in i['parameterDefinitions']:
                    try:
                        job_params[p_def['name']] = p_def['defaultParameterValue']['value']
                        self.logger.debug("Adding param %s with value %s", p_def['name'],
                                          p_def['defaultParameterValue']['value'])
                    except KeyError as e:
                        self.logger.debug("Exception %s when reading param %s", e, p_def['name'])
                        continue

        params = self.merge_dicts(job_params, params)
        return True, params

    @staticmethod
    def merge_dicts(dict1, dict2):
        d = dict1.copy()
        d.update(dict2)
        return d
