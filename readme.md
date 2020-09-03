!============================================!
======= Tenable to Azure Log Analytics =======
!============================================!

1. Installing the CLI App
- Navigate to "integration-azla"
- run "pip3 install ."

2. Go through the Help option: Tenable2AzLA --help
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

2. Call the CLI App after it's been installed run a test of the CLI App
- Tenable2AzLA --workspace-id --workspace-key --tio-access-key --tio-secret-key -s
-- optionally, you can call "-b" for the Batch size (it defaults to 1000 if no value is specified) and "-v" for verbosity;

3. In your Azure Log Analytics workspace, you can find all the logs under 2 Custom category logs:
- AVAS_Assets_CL
- AVAS_Vulns_CL