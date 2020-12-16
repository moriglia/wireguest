# Configuration Headers

This folder contains all the headers with the configuration variables.

## Subfolders

* `production/`: for configuration parameters used in production
* `test/`: for parameters that have no meaning in production:
    it doesn't matter if they are committed and pushed.
    They can be used for testing

In order to tune the correct settings use the `SETTINGS_HEADERS`
parameter in make like:
```bash
make CONFIGURATION_HEADERS=production configure
```
for `production` configuration, default is `test`
