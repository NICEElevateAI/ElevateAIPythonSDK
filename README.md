<p align="center">
<img src="https://raw.githubusercontent.com/NICEElevateAI/NICEElevateAI/main/images/ElevateAI-blue-red-logo.png" />
</p>

<div align="center"><a name="menu"></a>
  <h4>
    <a href="https://www.elevateai.com">
      Website
    </a>
    <span> | </span>
    <a href="https://docs.elevateai.com">
      Documentation
    </a>
    <span> | </span>
    <a href="https://www.elevateai.com/blogs">
      Blog
    </a>
  </h4>
</div>

# ElevateAI Python SDK

[ElevateAI](https://www.elevateai.com) provides an API for Speech-to-text (ASR), behavioral analysis and sentiment analysis of voice interactions.

There are three implementations available:

- AsyncClient.py :: defines class to be instantiated when needing concurrency.
- Client.py :: defines class is to be instantiated
- ElevateAI.py :: defines functions that can be called.


## Example
This examples use ElevateAI.py.

1. [Signup](https://app.elevateai.com) and retrieve API token from ElevateAI.
1. Declare an interaction. Provide a URI if you want ElevateAI to download the interaction via a Public URI.
2. Retrieve Interaction ID from JSON response and store.
3. Upload a file.
4. Check status every 30 seconds using Interaction ID until status returns 'processed' or an [error status](https://docs.elevateai.com/tutorials/check-the-processing-status).
5. Retrieve results - [phrase-by-phrase transcript](https://docs.elevateai.com/tutorials/get-phrase-by-phrase-transcript), [punctuated transcript](https://docs.elevateai.com/tutorials/get-punctuated-transcript), and [AI results](https://docs.elevateai.com/tutorials/get-cx-ai).


```python
import ElevateAI
import time

#Step 1
token = "API-TOKEN"
langaugeTag = "en-us"
vert = "default"
transcriptionMode = "highAccuracy"
localFilePath = "A:\\05212005-255.wav"
#extension needed for codec parsing
fileName = "05212005-255.wav"

#Step 2
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

#Step 5
#get results after file is processed 
getWordByWordTranscriptResponse = ElevateAI.GetWordByWordTranscript(interactionId, token)
getPuncutatedTranscriptResponse = ElevateAI.GetPuncutatedTranscript(interactionId, token)
getAIResultsResponse = ElevateAI.GetAIResults(interactionId, token)

```
