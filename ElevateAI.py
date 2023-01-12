import requests
import json

def DeclareAudioInteraction(language, verticle, downloadUri, token, audioTranscriptionMode, includeAiResults : bool):
    url = "https://api.elevateai.com/v1/interactions/"

    payload = json.dumps({
    "type": "audio",
    "languageTag": language,
    "vertical": verticle,
    "audioTranscriptionMode": audioTranscriptionMode,
    "downloadUri":downloadUri,
    "includeAiResults": includeAiResults
    })   

    if downloadUri is None :
        payload = json.dumps({
        "type": "audio",
        "languageTag": language,
        "vertical": verticle,
        "audioTranscriptionMode": audioTranscriptionMode,
        "includeAiResults": includeAiResults
        })   


    headers = {
    'X-API-TOKEN': token,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload) 
    return response

def GetInteractionStatus(interactionId, token):
    url = "https://api.elevateai.com/v1/interactions/%s/status" % interactionId

    headers = {
    'X-API-TOKEN': token,
    'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers) 
    
    return response

def UploadInteraction(interactionId, token, localFilePath, fileName):
    url = "https://api.elevateai.com/v1/interactions/%s/upload" % interactionId

    payload={}
    files=[
    (fileName,(fileName,open(localFilePath,'rb'),'application/octet-stream'))
    ]
    headers = {
    'X-API-Token': token
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    return response

def GetWordByWordTranscript(interactionId, token):
    url = "https://api.elevateai.com/v1/interactions/%s/transcript" % interactionId

    headers = {
    'X-API-TOKEN': token,
    'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers) 
    
    return response

def GetPuncutatedTranscript(interactionId, token):
    url = "https://api.elevateai.com/v1/interactions/%s/transcripts/punctuated" % interactionId

    headers = {
    'X-API-TOKEN': token,
    'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers) 
    
    return response

def GetAIResults(interactionId, token):
    url = "https://api.elevateai.com/v1/interactions/%s/ai" % interactionId

    headers = {
    'X-API-TOKEN': token,
    'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers) 
    
    return response

