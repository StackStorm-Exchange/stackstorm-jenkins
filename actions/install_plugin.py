from lib import action


class InstallPlugin(action.JenkinsBaseAction):
    def run(self, plugin, config_override=None):
        if config_override is not None:
            self.config_override(config_override)
        return self.jenkins.install_plugin(plugin, include_dependencies='True')
