import ElevateAI
import time

#Prereq - make sure you create a free account @ https://app.elevateai.com - this will let you generate a token
token = "my-token"
langaugeTag = "en-us"
vert = "default"
transcriptionMode = "highAccuracy"
localFilePath = "A:\\05212005-255.wav"
fileName = "05212005-255.wav"

#Step 1,2
declareResp = ElevateAI.DeclareAudioInteraction(langaugeTag, vert, None, token, transcriptionMode, False)

declareJson = declareResp.json()

interactionId = declareJson["interactionIdentifier"]

#Step  3
uploadInteractionResponse =  ElevateAI.UploadInteraction(interactionId, token, localFilePath, fileName)
#Step 4
#Loop over status until processed
while True:
    getInteractionStatusResponse = ElevateAI.GetInteractionStatus(interactionId,token)
    getInteractionStatusResponseJson = getInteractionStatusResponse.json()
    if getInteractionStatusResponseJson["status"] == "processed" or getInteractionStatusResponseJson["status"] == "fileUploadFailed" or getInteractionStatusResponseJson["status"] == "fileDownloadFailed" or getInteractionStatusResponseJson["status"] == "processingFailed" :
        break
    time.sleep(30)


#Step 6
#get results after file is processed 
getWordByWordTranscriptResponse = ElevateAI.GetWordByWordTranscript(interactionId, token)
getPuncutatedTranscriptResponse = ElevateAI.GetPuncutatedTranscript(interactionId, token)
getAIResultsResponse = ElevateAI.GetAIResults(interactionId, token)

input()