from lib import action
from jenkins import JenkinsException
import requests

TOGGLE_LOGKEEP_BUILD = '%(folder_url)sjob/%(short_name)s/%(number)s/toggleLogKeep'


class SetBuildLogKeep(action.JenkinsBaseAction):
    def run(self, project, number, logkeep, config_override=None):
        if config_override is not None:
            self.config_override(config_override)
        try:
            build_info = self.jenkins.get_build_info(project, number, depth=0)
            if 'keepLog' in build_info.keys():
                current_flag = build_info['keepLog']
                if current_flag == logkeep:
                    return True, 'Already set to the desired value. No actions necessary.'
                else:
                    return True, self.toggle_logkeep(project, number)
            else:
                # no keepLog found in the build info, fallback to regular keeplog toggle
                self.logger.warning("Job name {} build {} has no keepoLog parameter, "
                                    "falling back to traditional toggle "
                                    "logkeep way.".format(project, number))
                return True, self.toggle_logkeep(project, number)
        except JenkinsException as e:
            return False, {'error': str(e)}

    def toggle_logkeep(self, project, number):
        folder_url, short_name = self.jenkins._get_job_folder(project)
        response = self.jenkins.jenkins_request(requests.Request(
            'POST', self.jenkins._build_url(TOGGLE_LOGKEEP_BUILD, locals())
        ))

        if 200 <= response.status_code < 300:
            return "Successfully set LogKeep flag."
        else:
            return "Failed to toggle logkeep. " \
                   "Respose headers: {}, Response Body: {}".format(response.headers,
                                                                   response.content)
