from .assetForm import AssetObjectModel
import requests, json, os, time


assetsFile = "assets.txt"
cwd = os.path.dirname(os.path.abspath(__file__))
myAssetsFile = f"{cwd}/{assetsFile}"
print(f"Current working directory is: {cwd}")
print(f"Assets output will be written to: {myAssetsFile}")

def handleAssets(subscription, batch_size, headers):
    assetCollection = list()
    
    ### Test with Subscription in Asset
    subscription = subscription
    
    ### Export Assets
    print("[Handle Assets] - Export Assets...")
    exportAssetsUrl = "https://cloud.tenable.com/assets/export"
    body = {
        "chunk_size": batch_size,
        "filters":{
            "sources": [
                "AZURE"
            ]
        }
    }
    payload = json.dumps(body)

    exportAssetsResponse = requests.request("POST", exportAssetsUrl, headers=headers, data=payload)

    export_assets_uuid = exportAssetsResponse.json()["export_uuid"]
    print(f"[Handle Assets] - The following 'export_assets_uuid' was found: {export_assets_uuid}")

    if export_assets_uuid:
        ### Get Assets export status
        print("[Handle Assets] - Get Assets Export Status...")
        for i in range(100):
            exportAssetsStatusUrl = f"https://cloud.tenable.com/assets/export/{export_assets_uuid}/status"
            exportAssetsStatusResponse = requests.get(exportAssetsStatusUrl, headers=headers)
            exportAssetsStatusJson = exportAssetsStatusResponse.json()
            if exportAssetsStatusJson["status"] == "PROCESSING":
                print("[Handle Assets] - Assets export processing...")
            else:
                break
        if exportAssetsStatusJson["status"] == "FINISHED":
            print(f"[Handle Assets] - Current chunk status: {exportAssetsStatusJson['status']}")
            print(f"[Handle Assets] - Current chunks available: {exportAssetsStatusJson['chunks_available']}")
            aChunks = exportAssetsStatusJson["chunks_available"]
            for aChunk in aChunks:
                ### Download the asset chunks
                print(f"[Handle Assets] - Current chunk ID: {aChunk}")
                print(f"[Handle Assets] - Start downloading...")
                downloadAssetsUrl = f"https://cloud.tenable.com/assets/export/{export_assets_uuid}/chunks/{aChunk}"
                downloadAssetsResponse = requests.get(downloadAssetsUrl, headers=headers)
                assets = downloadAssetsResponse.json()
                assetsCounter = 0
                with open(f"{myAssetsFile}", "w+") as f:
                    for asset in assets:
                        assetSubscription = (asset["azure_resource_id"]).split('/')[2]
                        assetsCounter += 1
                        if assetSubscription in subscription:
                            assetLogEntry = AssetObjectModel()
                            assetLogEntry._asset["AgentName"] = asset["agent_names"]
                            assetLogEntry._asset["AzureResourceID"] = asset["azure_resource_id"]
                            assetLogEntry._asset["AzureVMID"] = asset["azure_vm_id"]
                            assetLogEntry._asset["BigFixAssetID"] = asset["bigfix_asset_id"]
                            assetLogEntry._asset["BiosUUID"] = asset["bios_uuid"]
                            assetLogEntry._asset["CreatedAt"] = asset["created_at"]
                            assetLogEntry._asset["DeletedAt"] = asset["deleted_at"]
                            assetLogEntry._asset["DeletedBy"] = asset["deleted_by"]
                            assetLogEntry._asset["FirstScanTime"] = asset["first_scan_time"]
                            assetLogEntry._asset["FirstSeen"] = asset["first_seen"]
                            assetLogEntry._asset["FQDN"] = asset["fqdns"]
                            assetLogEntry._asset["HasAgent"] = asset["has_agent"]
                            assetLogEntry._asset["HasPluginResult"] = asset["has_plugin_results"]
                            assetLogEntry._asset["Hostname"] = asset["hostnames"]
                            assetLogEntry._asset["id"] = asset["id"]
                            assetLogEntry._asset["InstalledSoftware"] = asset["installed_software"]
                            assetLogEntry._asset["Interfaces"] = asset["network_interfaces"]
                            assetLogEntry._asset["IPv4"] = asset["ipv4s"]
                            assetLogEntry._asset["IPv6"] = asset["ipv6s"]
                            assetLogEntry._asset["LastAuthenticatedScanDate"] = asset["last_authenticated_scan_date"]
                            assetLogEntry._asset["LastLicensedScanDate"] = asset["last_licensed_scan_date"]
                            assetLogEntry._asset["LastScanTarget"] = asset["last_scan_id"]
                            assetLogEntry._asset["LastScanTime"] = asset["last_scan_time"]
                            assetLogEntry._asset["LastSeen"] = asset["last_seen"]
                            assetLogEntry._asset["MACAddress"] = asset["mac_addresses"]
                            assetLogEntry._asset["ManufacturerTPMID"] = asset["manufacturer_tpm_ids"]
                            assetLogEntry._asset["NetBIOSName"] = asset["netbios_names"]
                            assetLogEntry._asset["NetworkId"] = asset["network_id"]
                            assetLogEntry._asset["OperatingSystem"] = asset["operating_systems"]
                            assetLogEntry._asset["Sources"] = asset["sources"]
                            assetLogEntry._asset["SSHFingerprint"] = asset["ssh_fingerprints"]
                            assetLogEntry._asset["SystemType"] = asset["system_types"]
                            assetLogEntry._asset["Tags"] = asset["tags"]
                            assetLogEntry._asset["TenableUUID"] = asset["agent_uuid"]
                            assetLogEntry._asset["TerminatedAt"] = asset["terminated_at"]
                            assetLogEntry._asset["TerminatedBy"] = asset["terminated_by"]
                            assetLogEntry._asset["UpdatedAt"] = asset["updated_at"]
                            assetCollection.append(assetLogEntry._asset)
                    print(json.dumps(assetCollection), file=f)
                f.close()
                print(f"[Handle Assets] - Assets downloaded to {myAssetsFile}")
                print(f"[Handle Assets] - Assets Counter: {assetsCounter}")
                time.sleep(5)

