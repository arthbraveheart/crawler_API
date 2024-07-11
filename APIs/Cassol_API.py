# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 15:34:26 2024

@author: ArthurRodrigues

The following code uses the GraphQL API from Balaroti to get info from products


"""

from io import StringIO
import pandas as pd
import requests 
import urllib.parse
import base64
import json

# The URL you provided
url = 'https://www.cassol.com.br/_v/segment/graphql/v1?workspace=master&maxAge=short&appsEtag=remove&domain=store&locale=pt-BR&__bindingId=068ae44d-617a-4cb9-831b-2de9c4a4ab0e&operationName=productSearchV3&variables=%7B%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22fd92698fe375e8e4fa55d26fa62951d979b790fcf1032a6f02926081d199f550%22%2C%22sender%22%3A%22vtex.store-resources%400.x%22%2C%22provider%22%3A%22vtex.search-graphql%400.x%22%7D%2C%22variables%22%3A%22eyJoaWRlVW5hdmFpbGFibGVJdGVtcyI6ZmFsc2UsInNrdXNGaWx0ZXIiOiJBTEwiLCJzaW11bGF0aW9uQmVoYXZpb3IiOiJza2lwIiwiaW5zdGFsbG1lbnRDcml0ZXJpYSI6Ik1BWF9XSVRIT1VUX0lOVEVSRVNUIiwicHJvZHVjdE9yaWdpblZ0ZXgiOnRydWUsIm1hcCI6ImMsYyIsInF1ZXJ5IjoicGlzb3MtZS1yZXZlc3RpbWVudG9zL3Bpc29zLWNlcmFtaWNvcyIsIm9yZGVyQnkiOiJPcmRlckJ5VG9wU2FsZURFU0MiLCJmcm9tIjowLCJ0byI6MzUsInNlbGVjdGVkRmFjZXRzIjpbeyJrZXkiOiJjIiwidmFsdWUiOiJwaXNvcy1lLXJldmVzdGltZW50b3MifSx7ImtleSI6ImMiLCJ2YWx1ZSI6InBpc29zLWNlcmFtaWNvcyJ9XSwiZmFjZXRzQmVoYXZpb3IiOiJTdGF0aWMiLCJjYXRlZ29yeVRyZWVCZWhhdmlvciI6ImRlZmF1bHQiLCJ3aXRoRmFjZXRzIjpmYWxzZSwic2hvd1Nwb25zb3JlZCI6dHJ1ZX0%3D%22%7D'
# Extract the query parameters from the URL
parsed_url = urllib.parse.urlparse(url)
query_params = urllib.parse.parse_qs(parsed_url.query)

# Extract the 'extensions' parameter
extensions_encoded = query_params['extensions'][0]

# URL decode the 'extensions' parameter
extensions_decoded = urllib.parse.unquote(extensions_encoded)

# Parse the decoded JSON string
extensions_obj = json.loads(extensions_decoded) #extension string fixed

# Extract the 'variables' parameter
variables_encoded = extensions_obj['variables']

# Base64 decode the 'variables' parameter
variables_decoded = base64.b64decode(variables_encoded).decode('utf-8')

# Parse the JSON string to get the original JSON object
variables_obj = json.loads(variables_decoded)

# Modify the variables object
variables_obj['from'] = 0
variables_obj['to'] = 50

# Convert the modified object to a JSON string
modified_variables_json = json.dumps(variables_obj)
# Base64 encode the JSON string
modified_variables_encoded = base64.b64encode(modified_variables_json.encode('utf-8')).decode('utf-8')
# Update the extensions object with the new encoded variables
extensions_obj['variables'] = modified_variables_encoded
# Convert the updated extensions object to a JSON string
updated_extensions_json = json.dumps(extensions_obj)
# URL encode the JSON string
updated_extensions_encoded = urllib.parse.quote(updated_extensions_json)

# Construct the new URL with the updated 'extensions' parameter
new_query_params = query_params
new_query_params['extensions'] = updated_extensions_encoded
# Construct the new URL
new_url = urllib.parse.urlunparse(parsed_url._replace(query=urllib.parse.urlencode(new_query_params, doseq=True)))

#new_urll = """https://www.balaroti.com.br/_v/segment/graphql/v1?workspace=master&maxAge=short&appsEtag=remove&domain=store&locale=pt-BR&__bindingId=3d10c899-3307-422f-9440-1b8075245ef3&operationName=productSearchV3&variables=%7B%7D&extensions=%7B%22persistedQuery%22%3A%20%7B%22version%22%3A%201%2C%20%22sha256Hash%22%3A%20%22fd92698fe375e8e4fa55d26fa62951d979b790fcf1032a6f02926081d199f550%22%2C%20%22sender%22%3A%20%22vtex.store-resources%400.x%22%2C%20%22provider%22%3A%20%22vtex.search-graphql%400.x%22%7D%2C%20%22variables%22%3A%20%22eyJoaWRlVW5hdmFpbGFibGVJdGVtcyI6IGZhbHNlLCAic2t1c0ZpbHRlciI6ICJGSVJTVF9BVkFJTEFCTEUiLCAic2ltdWxhdGlvbkJlaGF2aW9yIjogImRlZmF1bHQiLCAiaW5zdGFsbG1lbnRDcml0ZXJpYSI6ICJNQVhfV0lUSE9VVF9JTlRFUkVTVCIsICJwcm9kdWN0T3JpZ2luVnRleCI6IGZhbHNlLCAibWFwIjogImMiLCAicXVlcnkiOiAicGlzb3MtZS1yZXZlc3RpbWVudG9zIiwgIm9yZGVyQnkiOiAiT3JkZXJCeVNjb3JlREVTQyIsICJmcm9tIjogMCwgInRvIjogNTAsICJzZWxlY3RlZEZhY2V0cyI6IFt7ImtleSI6ICJjIiwgInZhbHVlIjogInBpc29zLWUtcmV2ZXN0aW1lbnRvcyJ9XSwgImZhY2V0c0JlaGF2aW9yIjogIlN0YXRpYyIsICJjYXRlZ29yeVRyZWVCZWhhdmlvciI6ICJkZWZhdWx0IiwgIndpdGhGYWNldHMiOiBmYWxzZSwgInNob3dTcG9uc29yZWQiOiB0cnVlfQ%3D%3D%22%7D"""

url_base = 'https://www.cassol.com.br/_v/segment/graphql/v1?workspace=master&maxAge=short&appsEtag=remove&domain=store&locale=pt-BR&__bindingId=068ae44d-617a-4cb9-831b-2de9c4a4ab0e&operationName=productSearchV3&variables=%7B%7D&extensions='
new_urlll = url_base + updated_extensions_encoded

#Get new response of the modified url
response = requests.get(new_urlll)

jsons = response.json()







