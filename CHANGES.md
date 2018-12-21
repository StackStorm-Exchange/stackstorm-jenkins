# Change Log

# 0.6.0

- Add `build_job_enh` (which waits to get build info), `stop_build` and `get_build_info` actions.
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
