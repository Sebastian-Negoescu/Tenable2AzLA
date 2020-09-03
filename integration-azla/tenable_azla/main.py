#!/usr/bin/env python
'''
MIT License

Copyright (c) 2020 Sebastian-Daniel NEGOESCU

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from .exportAssets import handleAssets, myAssetsFile
from .exportVulns import handleVulns, myVulnsFile
from .ConstructAzLA import ConstructAzLA
import click, logging, time

@click.command()
@click.option("--workspace-id", envvar="WORKSPACE_ID",
    help="Azure Log Analytics - Workspace ID")
@click.option("--workspace-key", envvar="WORKSPACE_KEY",
    help="Azure Log Analytics - Primary/Secondary Key")
@click.option('--tio-access-key', envvar='TIO_ACCESS_KEY',
    help='Tenable.io Access Key')
@click.option('--tio-secret-key', envvar='TIO_SECRET_KEY',
    help='Tenable.io Secret Key')    
@click.option("--subscription", "-s", envvar= "SUBSCRIPTION",
    help="Only verify resources in a particular Azure Subscription")
@click.option("--batch-size", "-b", envvar="BATCH_SIZE", default=1000,
    type=click.INT, help="Export/Import Batch Sizing")
@click.option("--verbose", "-v", envvar="VERBOSITY", default=0,
    count=True, help="Logging Verbosity: 0 = Warning; 1 = INFO; >1 = DEBUG")
def cli(workspace_id, workspace_key, tio_access_key, tio_secret_key, subscription, batch_size, verbose):
    '''
    Tenable Assets & Vulnerabilities -> Azure Log Analytics
    '''
    # Setup the logging verbosity.
    if verbose == 0:
        logging.basicConfig(level=logging.WARNING)
    if verbose == 1:
        logging.basicConfig(level=logging.INFO)
    if verbose > 1:
        logging.basicConfig(level=logging.DEBUG)

    _tio_access_key = tio_access_key
    _tio_secret_key = tio_secret_key
    _subscription = subscription
    _batch_size = batch_size

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-apikeys": f"accessKey={_tio_access_key};secretKey={_tio_secret_key}"
    }

    log_type_assets = "AVAS_Assets"
    log_type_vulns = "AVAS_Vulns"

    handleAssets(_subscription, _batch_size, headers)
    handleVulns(_batch_size, headers)
    ### Assets JSON data
    def streamAssets():
        with open(f"{myAssetsFile}", "r") as assetFile:
            print("Start iterating through assets...")
            assetData = assetFile.read()
        assetFile.close()
        return assetData

    ### Vulns JSON data
    def streamVulns():
        with open(f"{myVulnsFile}", "r") as vulnFile:
            print("Start iterating through vulnerabilities...")
            vulnData = vulnFile.read()
        vulnFile.close()
        return vulnData

    print("Initiate script...")
    print("[Debug]: Look over the format...")
    print("Invoke Azure Log Analytics...")

    ConstructAzLA(workspace_id, workspace_key, streamAssets(), log_type_assets)
    ConstructAzLA(workspace_id, workspace_key, streamVulns(), log_type_vulns)

