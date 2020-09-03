!============================================!
======= Tenable to Azure Log Analytics =======
!============================================!

## Setup
```shell
cd integration-azla
pip3 install .
```

## Options
The following script details, both, command-line arguments and equivalent environment variables.

```
Usage: Tenable2AzLA [OPTIONS]

  Tenable Assets & Vulnerabilities -> Azure Log Analytics

Options:
  --workspace-id TEXT       Azure Log Analytics - Workspace ID
  --workspace-key TEXT      Azure Log Analytics - Primary/Secondary Key
  --tio-access-key TEXT     Tenable.io Access Key
  --tio-secret-key TEXT     Tenable.io Secret Key
  -s, --subscription TEXT   Only verify resources in a particular Azure
                            Subscription

  -b, --batch-size INTEGER  Export/Import Batch Sizing
  -v, --verbose             Logging Verbosity: 0 = Warning; 1 = INFO; >1 =
                            DEBUG

  --help                    Show this message and exit.
```

## Example Usage

Run the import once:

```
Tenable2AzLA 
    --workspace-id {WORKSPACE_ID} \
    --workspace-key {WORKSPACE_KEY} \
    --tio-access-key {TIO_ACCESS_KEY} \
    --tio-secret-key {TIO_SECRET_KEY} \
    -s / --subscription {SUBSCRIPTION}
```
Optionally, you can add 
```
    -b {BATCH_SIZE} / --batch-size
    -v {VERBOSITY} / --verbose
```

## Azure

In your Azure Log Analytics workspace, you can find all the logs under 2 Custom category logs:
- AVAS_Assets_CL
- AVAS_Vulns_CL

[tio_keys]: https://docs.tenable.com/cloud/Content/Settings/GenerateAPIKey.htm
[azla_wskeys]: https://docs.microsoft.com/en-us/rest/api/loganalytics/workspace%20shared%20keys/getsharedkeys
