"""Example code for interacting with ElevateAI API."""

import ElevateAI
import time

# Prereq - make sure you create a free account at
# https://app.elevateai.com and create a token.
token = "d7011e44-2266-4a64-bf12-5f2af2aeb84b"
langaugeTag = "en-us"
vert = "default"
transcriptionMode = "highAccuracy"
localFilePath = "/Users/nali/WIP/ElevateAIPythonSDK/sample.wav"
fileName = "sample1.wav"
originalFileName = "sample1-originalfilename.wav"
externalIdentifier = "My own id"

# Step 1,2
declareResp = ElevateAI.DeclareAudioInteraction(
    langaugeTag,
    vert,
    None,
    token,
    transcriptionMode,
    False,
    originalFileName,
    externalIdentifier,
)

declareJson = declareResp.json()

interactionId = declareJson["interactionIdentifier"]

# Step  3
uploadInteractionResponse = ElevateAI.UploadInteraction(
    interactionId, token, localFilePath, fileName
)
# Step 4
# Loop over status until processed
while True:
    getInteractionStatusResponse = ElevateAI.GetInteractionStatus(
        interactionId, token)
    getInteractionStatusResponseJson = getInteractionStatusResponse.json()
    if (
        getInteractionStatusResponseJson["status"] == "processed"
        or getInteractionStatusResponseJson["status"] == "fileUploadFailed"
        or getInteractionStatusResponseJson["status"] == "fileDownloadFailed"
        or getInteractionStatusResponseJson["status"] == "processingFailed"
    ):
        break
    time.sleep(30)


# Step 6
# get results after file is processed
getWordByWordTranscriptResponse = ElevateAI.GetWordByWordTranscript(
    interactionId, token
)
getPuncutatedTranscriptResponse = ElevateAI.GetPuncutatedTranscript(
    interactionId, token
)
getAIResultsResponse = ElevateAI.GetAIResults(interactionId, token)

input()
