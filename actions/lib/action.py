from st2common.runners.base_action import Action
import jenkins


class JenkinsBaseAction(Action):

    def run(self, **kwargs):
        pass

    def __init__(self, config):
        super(JenkinsBaseAction, self).__init__(config)
        self.jenkins = self._get_client()

    def config_override(self, new_config):
        self.config = new_config
        self.jenkins = self._get_client()

    def _get_client(self):
        url = self.config['url']
        try:
            username = self.config['username']
        except KeyError:
            username = None
        try:
            password = self.config['password']
        except KeyError:
            password = None

        client = jenkins.Jenkins(url, username, password)
        return client
