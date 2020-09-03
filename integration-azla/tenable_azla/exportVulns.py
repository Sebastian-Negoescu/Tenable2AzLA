from .vulnForm import VulnObjectModel
from .exportAssets import myAssetsFile
import requests, json, os, time


vulnsFile = "vulns.txt"
cwd = os.path.dirname(os.path.abspath(__file__))
myVulnsFile = f"{cwd}/{vulnsFile}"
print(f"Current working directory is: {cwd}")
print(f"Vulnerabilities output will be written to: {myVulnsFile}")

def handleVulns(batch_size, headers):
    vulnsCollection = list()

    ### Export Vulnerabilities
    print("[Handle Vulns] - Export Vulns")
    exportVulnsUrl = "https://cloud.tenable.com/vulns/export"
    body = {
        "num_assets": batch_size
    }
    payload = json.dumps(body)

    exportVulnsResponse = requests.request("POST", exportVulnsUrl, headers=headers, data=payload)
    export_vulns_uuid = exportVulnsResponse.json()["export_uuid"]
    print(f"[Handle Vulns] - The following 'export_vulns_uuid' was found: {export_vulns_uuid}")

    if export_vulns_uuid:
        ### Get Vulns export status
        print("[Handle Vulns] - Get Vulnerabilities Export Status")
        for i in range(100):
            exportVulnsStatusUrl = f"https://cloud.tenable.com/vulns/export/{export_vulns_uuid}/status"
            exportVulnsStatusResponse = requests.get(exportVulnsStatusUrl, headers=headers)
            exportVulnsStatusJson = exportVulnsStatusResponse.json()
            if exportVulnsStatusJson["status"] == "PROCESSING":
                print("[Handle Vulns] - Vulnerabitlities export processing...")
            else:
                break    
        if exportVulnsStatusJson["status"] == "FINISHED":
            print(f"[Handle Vulns] - Current chunk status: {exportVulnsStatusJson['status']}")
            print(f"[Handle Vulns] - Current chunks available: {exportVulnsStatusJson['chunks_available']}")
            vChunks = exportVulnsStatusJson["chunks_available"]
            assetsIds = list()
            for vChunk in vChunks:
                ### Download the vulnerabilities chunks
                print(f"[Handle Vulns] - Current chunk ID: {vChunk}")
                print(f"[Handle Vulns] - Start downloading...")
                downloadVulnsUrl = f"https://cloud.tenable.com/vulns/export/{export_vulns_uuid}/chunks/{vChunk}"
                downloadVulnsResponse = requests.get(downloadVulnsUrl, headers=headers)
                vulns = downloadVulnsResponse.json()
                vulnsCounter = 0
                with open(myAssetsFile, "r") as f:
                    assetsObjs = json.load(f)
                    for assetObj in assetsObjs:
                        assetId = assetObj["id"]
                        assetsIds.append(assetId)
                f.close()
                with open(f"{myVulnsFile}", "w+") as f:
                    for assetId in assetsIds:
                        for vuln in vulns:
                            if assetId == vuln["asset"]["uuid"]:
                                vulnsCounter += 1
                                vulnLogEntry = VulnObjectModel()
                                vulnLogEntry._vuln["AssetUUID"] = vuln["asset"]["uuid"]
                                vulnLogEntry._vuln["CVE"] = vuln["plugin"].get("cve")
                                vulnLogEntry._vuln["CVSS3TemporalScore"] = vuln["plugin"].get("cvss3_temporal_score")
                                vulnLogEntry._vuln["CVSS3TemporalVector"] = vuln["plugin"].get("cvss3_temporal_vector")
                                vulnLogEntry._vuln["CVSS3BaseScore"] = vuln["plugin"].get("cvss3_base_score")
                                vulnLogEntry._vuln["CVSS3Vector"] = vuln["plugin"].get("cvss3_vector")
                                vulnLogEntry._vuln["CVSSBaseScore"] = vuln["plugin"].get("cvss_base_score")
                                vulnLogEntry._vuln["CVSSTemporalScore"] = vuln["plugin"].get("cvss_temporal_score")
                                vulnLogEntry._vuln["CVSSTemporalVector"] = vuln["plugin"].get("cvss_temporal_vector")
                                vulnLogEntry._vuln["CVSSVector"] = vuln["plugin"].get("cvss_vector")
                                vulnLogEntry._vuln["Description"] = vuln["plugin"].get("description")
                                vulnLogEntry._vuln["FQDN"] = vuln["asset"].get("fqdn")
                                vulnLogEntry._vuln["Host"] = vuln["asset"].get("hostname")
                                vulnLogEntry._vuln["HostEnd"] = "##########"
                                vulnLogEntry._vuln["HostStart"] = "##########"
                                vulnLogEntry._vuln["IPAddress"] = vuln["asset"].get("ipv4")
                                vulnLogEntry._vuln["MACAddress"] = "##########"
                                vulnLogEntry._vuln["NetBios"] = vuln["asset"].get("netbios_name")
                                vulnLogEntry._vuln["OS"] = vuln["asset"].get("operating_system")
                                vulnLogEntry._vuln["PluginName"] = vuln["plugin"].get("name")
                                vulnLogEntry._vuln["PluginFamily"] = vuln["plugin"].get("family")
                                vulnLogEntry._vuln["PluginID"] = vuln["plugin"].get("id")
                                vulnLogEntry._vuln["PluginOutput"] = vuln.get("output")
                                vulnLogEntry._vuln["Port"] = vuln["port"].get("port")
                                vulnLogEntry._vuln["Protocol"] = vuln["port"]["protocol"]
                                vulnLogEntry._vuln["Risk"] = vuln["plugin"]["risk_factor"]
                                vulnLogEntry._vuln["SeeAlso"] = vuln["plugin"].get("see_also")
                                vulnLogEntry._vuln["Solution"] = vuln["plugin"].get("solution")
                                vulnLogEntry._vuln["Synopsis"] = vuln["plugin"].get("synopsis")
                                vulnLogEntry._vuln["SystemType"] = vuln["plugin"].get("type")
                                vulnLogEntry._vuln["VulnerabilityPriorityRating"] = vuln["plugin"].get("vpr")
                                vulnLogEntry._vuln["VulnerabilityState"] = vuln["state"]
                                vulnsCollection.append(vulnLogEntry._vuln)
                    print(json.dumps(vulnsCollection), file=f)
                f.close()
                print(f"[Handle Vulns] - Vulns downloaded to {myVulnsFile}")
                print(f"[Handle Vulns] - Vulns Counter: {vulnsCounter}")                        
