# Jenkins Integration Pack

This pack creates a basic integration with Jenkins

To trigger events from Jenkins, use Jenkins to send a webhook to StackStorm.
Examples of rules can be found in the `rules` directory.

Jenkins jobs are required to have the "parameterized" setting enabled in order
for this pack to be able to start jobs.

![param-step-1](https://cloud.githubusercontent.com/assets/125088/14975817/41cddcc8-10cb-11e6-8758-2c25e01d5227.png)

## Configuration

# Modern way
Once the pack is installed, issue `st2 pack config jenkins` command to enter url, username and password (if auth is enabled) of your primary Jenkins instance.

# Legacy way
Copy the example configuration in [jenkins.yaml.example](./jenkins.yaml.example)
to `/opt/stackstorm/configs/jenkins.yaml` and edit as required.

* `url` - FQDN to Jenkins API endpoint (e.x.: http://jenkins.mycompany.org:8080)
* `username` - Jenkins Username (if auth is enabled)
* `password` - Jenkins Password (if auth is enabled)

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

**Note** : Configuration can be overridden per each action execution. See below. 

**Note** : When modifying the configuration in `/opt/stackstorm/configs/` please
           remember to tell StackStorm to load these new values by running
           `st2ctl reload --register-configs`
          
**Note** : If your Jenkins server has a self-signed certificate and you get
           `certificate verify failed` Error, set `PYTHONHTTPSVERIFY=0`
           in `/etc/sysconfig/st2api` and `/etc/sysconfig/st2actionrunner`.
           Then reload st2api and st2actionrunner services with commands
           `st2ctl restart-component st2api` and `st2ctl restart-component st2actionrunner`
           to apply the changes.

## Actions

**Note** : As of v0.7.2 each action supports optional `config_override` parameter to override `url`, `username` and `password` configuration values. Pass it as an object, e.g. `{"url": "http://someotherjenkinshost.example.com:8080", "username": "user1", "password": "somepassword"}` or `{"url": "http://someotherjenkinshost.example.com:8080"}` if auth is not required. 

* `build_job` - Kick off CI build based on project name
* `build_job_enh` - Kick off CI build based on project name and wait for it to be executed (and optionally to complete), return build info
* `list_jobs` - List all jobs
* `enable_job` - Enable Jenkins job
* `disable_job` - Disable Jenkins job
* `get_job_info` - Retrieve Jenkins job information
* `get_job_params` - Retrieve Jenkins job params with default values and merge with the provided dict of params, if any 
* `get_build_info` - Retrieve Jenkins build information
* `get_running_builds` - Retrieve all running Jenkins builds (possible to filter with regex by name)
* `get_queue_info` - Retrieve queue information from the Jenkins instance
* `install_plugin` - Install plugin
* `rebuild_last_job` - Rebuild last Jenkins job
* `list_jobs_regex` - List Jenkins job name by regex pattern
* `stop_build` - Stop a running Jenkins build
* `cancel_queued_build` - Cancel a queued build
* `set_build_logkeep` - Set build's LogKeep flag to true or false


