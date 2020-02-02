import re
from six.moves.urllib.parse import unquote

from jenkins import JenkinsException

from lib import action


class GetQueueInfo(action.JenkinsBaseAction):
    def run(self, name_pattern, config_override=None):
        if config_override is not None:
            self.config_override(config_override)
        try:
            queued_jobs = self.jenkins.get_queue_info()
        except JenkinsException as e:
            return False, {'error': str(e)}

        for job in queued_jobs:
            # Jenkins returns url-encoded names
            try:
                job['task']['name_decoded'] = unquote(job['task']['name'])
            except KeyError:
                continue

        if name_pattern is not None:
            filtered_queued_jobs = []
            for job in queued_jobs:
                try:
                    if re.match(name_pattern, job['task']['name_decoded']):
                        filtered_queued_jobs.append(job)
                except KeyError:
                    continue

            return True, filtered_queued_jobs
        else:
            return True, queued_jobs
