# ElevateAI Python SDK

ElevateAI - the most afforable, accurate Speech-to-text (ASR) API. Free to use for hundreds of hours of audio per month!

Steps  - Pre Req: signup for a free account @ https://app.elevateai.com and retrieve your API token 
1. Declare an interaction (give a URI if you want ElevateAI to download the interaction via a Public URI)  
2. Store Interaction ID
3. Upload a file if no URI specified during declare using the Interaction ID
4. Check status every 30 seconds using Interaction ID until status is 'processed' or an error status https://docs.elevateai.com/tutorials/check-the-processing-status
5. Retrieve results (transcripts, ai results) https://docs.elevateai.com/tutorials/get-phrase-by-phrase-transcript 

#Usage:

```
import ElevateAI
import time

#Prereq - make sure you create a free account @ https://app.elevateai.com - this will let you generate a token
token = "my-token"
langaugeTag = "en-us"
vert = "default"
transcriptionMode = "highAccuracy"
localFilePath = "A:\\05212005-255.wav"
#needed for codec parsing
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

```
