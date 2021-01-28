from lib import action
from time import sleep
from jenkins import NotFoundException, JenkinsException


class BuildProject(action.JenkinsBaseAction):
    def run(self, project, max_wait=30, wait_for_results=False, parameters=None,
            config_override=None):
        if config_override is not None:
            self.config_override(config_override)
        (status, queue_id) = self.kick_off_job(project, parameters)
        if status == 1:
            # try again without parameters
            (status, queue_id) = self.kick_off_job(project, {})
            if status > 0:
                # give up
                return False, queue_id
        elif status == 2:
            # queue_id will contain error
            return False, queue_id

        attempt = 0
        sleep_interval = 3
        max_attempts = int(max_wait / sleep_interval)
        run_build_result = False
        queue_item = None
        while attempt <= max_attempts and not run_build_result:
            queue_item = self.jenkins.get_queue_item(queue_id)
            if 'executable' in queue_item:
                run_build_result = True
                break
            else:
                attempt += 1
                self.logger.debug("Waiting for the job to get executed...")
                sleep(sleep_interval)

        job_completed = False
        if run_build_result and wait_for_results:
            while not job_completed:
                try:
                    number = queue_item['executable']['number']
                    build_info = self.jenkins.get_build_info(project, number, depth=0)
                    if 'building' in build_info.keys():
                        if not build_info['building']:
                            self.logger.debug("Build job {} number {} completed.".format(
                                project, number
                            ))
                            job_completed = True
                            queue_item['executable'].update(build_info)
                    else:
                        # for safety let's exit here
                        self.logger.debug("Build info doesn't have 'building' field. "
                                          "Can't wait for results.")
                        break

                except KeyError:
                    # could not find out build number
                    self.logger.debug("Could not find build number for this job, will not "
                                      "wait for results")
                    break
                self.logger.debug("Waiting for the job to complete...")
                sleep(sleep_interval)

        if not run_build_result and 'why' in queue_item:
            return run_build_result, {'error': queue_item['why'], 'queue_id': queue_id}
        elif not run_build_result and 'why' not in queue_item:
            return run_build_result, {'error': 'General failure for queue_id {0}.'.format(queue_id),
                                      'queue_id': queue_id}
        else:
            return run_build_result, queue_item['executable']

    def kick_off_job(self, prj, prm):
        try:
            queue_id = self.jenkins.build_job(prj, prm)
        except NotFoundException:
            # terminal error
            return 2, {'error': 'Project {0} not found.'.format(prj)}
        except JenkinsException as e:
            msg = e.message  # pylint: disable=no-member
            msg = msg.encode('ascii', 'ignore')
            if 'doBuildWithParameters' in msg:
                # most likely build is not parameterized but we sent parameters,
                # return non-terminal status
                return 1, {}
            else:
                # most likely something else and very bad happened, return terminal status
                return 2, {'error': 'General error: {0}'.format(msg)}
        else:
            return 0, queue_id


# local testing
if __name__ == '__main__':
    import os
    import pprint

    j_url = os.environ.get("JENKINS_URL")
    j_username = os.environ.get("JENKINS_USERNAME")
    j_password = os.environ.get("JENKINS_PASSWORD")

    conf_override = {'url': j_url, 'username': j_username, 'password': j_password}
    act = BuildProject(config=conf_override)
    res_flag, res_dict = act.run(project='demo',
                                 wait_for_results=True,
                                 parameters={'PARAM1': 'VALUE1'})

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(res_flag)
    pp.pprint(res_dict)
