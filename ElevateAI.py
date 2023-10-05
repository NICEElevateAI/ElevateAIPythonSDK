"""ElevateAI functions to get transcriptions."""

import requests
import json


def DeclareAudioInteraction(
    language,
    verticle,
    downloadUri,
    token,
    audioTranscriptionMode,
    includeAiResults: bool,
    originalFileName=None,
    externalIdentifier=None,
):
    """1st step in processing an interaction is to declare the interaction."""
    url = "https://api.elevateai.com/v1/interactions/"

    payload = json.dumps(
        {
            "type": "audio",
            "languageTag": language,
            "vertical": verticle,
            "audioTranscriptionMode": audioTranscriptionMode,
            "downloadUri": downloadUri,
            "includeAiResults": includeAiResults,
            "originalfilename": originalFileName,
            "externalidentifier": externalIdentifier,
        }
    )

    if downloadUri is None:
        payload = json.dumps(
            {
                "type": "audio",
                "languageTag": language,
                "vertical": verticle,
                "audioTranscriptionMode": audioTranscriptionMode,
                "includeAiResults": includeAiResults,
                "originalfilename": originalFileName,
                "externalidentifier": externalIdentifier,
            }
        )

    headers = {"X-API-TOKEN": token, "Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload)
    return response


def GetInteractionStatus(interactionId, token):
    """Check if interaction has been processed."""
    url = "https://api.elevateai.com/v1/interactions/%s/status" % interactionId

    headers = {"X-API-TOKEN": token, "Content-Type": "application/json"}

    response = requests.request("GET", url, headers=headers)

    return response


def UploadInteraction(
    interactionId, token, localFilePath, fileName, originalFileName=None
):
    """Upload file to ElevateAI."""
    url = "https://api.elevateai.com/v1/interactions/%s/upload" % interactionId

    payload = {}

    files = [
        (fileName, (fileName, open(localFilePath, "rb"), "application/octet-stream"))
    ]
    headers = {"X-API-Token": token}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    return response


def GetWordByWordTranscript(interactionId, token):
    """Get the word by word transcription of the interaction."""
    url = "https://api.elevateai.com/v1/interactions/%s/transcript" % interactionId

    headers = {"X-API-TOKEN": token, "Content-Type": "application/json"}

    response = requests.request("GET", url, headers=headers)

    return response


def GetPuncutatedTranscript(interactionId, token):
    """Get the punctuated version of the transcription."""
    url = (
        "https://api.elevateai.com/v1/interactions/%s/transcripts/punctuated"
        % interactionId
    )

    headers = {"X-API-TOKEN": token, "Content-Type": "application/json"}

    response = requests.request("GET", url, headers=headers)

    return response


def GetAIResults(interactionId, token):
    """Get JSON with AI results."""
    url = "https://api.elevateai.com/v1/interactions/%s/ai" % interactionId

    headers = {"X-API-TOKEN": token, "Content-Type": "application/json"}

    response = requests.request("GET", url, headers=headers)

    return response
