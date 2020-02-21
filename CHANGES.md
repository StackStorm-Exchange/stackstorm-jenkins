# Change Log

# 0.8.1

- Explicitly specify Python versions
- Python 3 fixups and linting

# 0.8.0

- Changed action `build_job_enh`: added optional parameter `wait_for_results`, be careful with the action's default `timeout` when turning it on.

# 0.7.7

- Bumping requirements to python-jenkins>=1.4.0.
- Added `set_build_logkeep` action to set build's keep forever flag.

# 0.7.6

- If `build_job_enh` fails and `queue_id` is known, include it in the result to let users follow up later.

# 0.7.5

- Added `get_queue_info` action.
- Added `cancel_queued_build` action.

# 0.7.4

- `get_running_builds` now decodes/unquotes jobs' names and adds them as `name_decoded` into the resulting array.

# 0.7.3

Security release.
- `config_override` optional parameter is marked as secret so whatever is provided there is not exposed in the UI.

# 0.7.2

- All actions got `config_override` optional parameter to support multi-tenancy. The parameter takes an object with `url`, `username` and `password` keys with appropriate values to contact arbitrary Jenkins instance instead of the one configured in the global pack configuration.

# 0.7.1

- Added `get_job_params` action to get all params of a certain job and their default values, and optionally merge it with user provided params.

# 0.7.0

- Added `get_running_builds` action to get all currently running builds.
- Renamed `list_running_jobs` -> `list_jobs` to reflect its meaning properly, the old name was misleading.
- Updated `build_job_enh` to support `max_wait` parameter (wait for about this many seconds to get the job executed).

# 0.6.0

- Added `build_job_enh` (which waits to get build info), `stop_build` and `get_build_info` actions.
- Old `build_job` action has not been changed for the purpose of not introducing any breaking changes as the data returned from the two actions is quite different.

# 0.5.0

- Add rebuild last Jenkins job. Add list Jenkins jobs by regex.

# 0.4.0

- Updated action `runner_type` from `run-python` to `python-script`.

# 0.3.0

- Remove parameter 'branch'. Add optional parameter 'parameters'.

# 0.2.0

- Rename `config.yaml` to `config.schema.yaml` and update to use schema.

# 0.1.0

- First release.
