########################################################################################
################## CONNECT TO AZURE LOG ANALYTICS - TESTING PROCEDURE ##################
########################################################################################

import requests
import json
import datetime
import hashlib
import hmac
import base64
import os
# import exportAssets
# import cli


def ConstructAzLA(workspace_id, primary_key, body, log_type):
#######################
###### Functions ######
#######################

# Build the API signature
    def build_signature(workspace_id, primary_key, date, content_length, method, content_type, resource):
        print("Create the connection's signature for Azure LogAnalytics...")
        x_headers = 'x-ms-date:' + date
        string_to_hash = method + "\n" + str(content_length) + "\n" + content_type + "\n" + x_headers + "\n" + resource
        bytes_to_hash = bytes(string_to_hash, encoding="utf-8")
        decoded_key = base64.b64decode(primary_key)
        encoded_hash = base64.b64encode(hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest()).decode()
        authorization = "SharedKey {}:{}".format(workspace_id,encoded_hash) # or authorization = f"SharedKey{workspace_id}:{encoded_hash}"
        print("Signature built... \nContinue the request...")
        return authorization


    # Build and send a request to the POST API
    def stream_logs(workspace_id, primary_key, body, log_type):
        print(f"Create the POST API request to stream the data - {log_type}")
        method = "POST"
        content_type = "application/json"
        resource = "/api/logs"
        rfc1123date = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        content_length = len(body)
        signature = build_signature(workspace_id, primary_key, rfc1123date, content_length, method, content_type, resource)
        uri = f"https://{workspace_id}.ods.opinsights.azure.com{resource}?api-version=2016-04-01"

        headers = {
            "Content-Type": content_type,
            "Authorization": signature,
            "Log-Type": log_type,
            "x-ms-date": rfc1123date
        }

        response = requests.post(uri, data=body, headers=headers)
        if (response.status_code >= 200 and response.status_code <= 299):
            print("Accepted")
        else:
            print(f"Response Code & Reason: {response.status_code}:{response.reason}")
            print(f"Detailed message: {response.text}")

            
    stream_logs(workspace_id, primary_key, body, log_type)