"""Class to use when interacting with ElevateAI."""

import requests
import json


class Client:
    """Base class."""

    def __init__(self, url="https://api.elevateai.com/v1", token=None):
        """Initialize."""
        self.url = url
        self.api_token = token
        self.declareUri = url + "/interactions"
        self.uploadUri = url + "/interactions/%s/upload"
        self.statusUri = url + "/interactions/%s/status"
        self.transcriptsUri = url + "/interactions/%s/transcripts"
        self.transcriptsUri2 = url + "/interactions/%s/transcripts/punctuated"
        self.aiUri = url + "/interactions/%s/ai"
        self.uploadHeader = {"X-API-TOKEN": token}
        self.jsonHeader = {
            "Content-Type": "application/json; charset=utf-8",
            "X-API-TOKEN": token,
        }
        self.session = requests.session()
        self.session.headers.update(self.jsonHeader)

    def declare(
        self,
        languageTag="en-us",
        vertical="default",
        transcriptionMode="highAccuracy",
        mediafile=None,
        url=None,
    ):
        """First step is to declare the interaction."""
        data = {
            "type": "audio",
            "downloadUrl": url,
            "languageTag": languageTag,
            "vertical": vertical,
            "audioTranscriptionMode": transcriptionMode,
            "includeAiResults": True,
        }
        rsp = self.session.post(self.declareUri, data=json.dumps(data))
        i = rsp.json()
        if mediafile:
            self.upload(i, mediafile)
        i["status"] = self.status(i)
        return i

    def upload(self, i, f):
        """Second step is to upload the file."""
        if type(i) == dict:
            i = i["interactionIdentifier"]
        files = [("", (f, open(f, "rb"), "application/octet-stream"))]
        rsp = requests.post(self.uploadUri % i,
                            headers=self.uploadHeader, files=files)
        return rsp

    def status(self, interaction):
        """Check the status of the interaction."""
        if type(interaction) == dict:
            interaction = interaction["interactionIdentifier"]
        rsp = self.session.get(self.statusUri % interaction)
        return rsp.json()["status"]

    def transcripts(self, interaction, punctuated=True):
        """Get the transcriptions."""
        if type(interaction) == dict:
            interaction = interaction["interactionIdentifier"]
        url = self.transcriptsUri2 if punctuated else self.transcriptsUri
        rsp = self.session.get(url % interaction)
        return rsp.json()

    def ai(self, interaction):
        """Get the JSON AI results."""
        if type(interaction) == dict:
            interaction = interaction["interactionIdentifier"]
        rsp = self.session.get(self.aiUri % interaction)
        return rsp.json()


# if __name__ == "__main__":
#     import time
#     from pathlib import Path

#     # files = list(Path('d:/dev/elevateai-cli/sample-media').glob('*.wav'))
#     files = list(Path("c:/tmp").glob("*.wav"))

#     cli = Client("http://api.elevateAI.com/v1",
#                  "<API-TOKEN>")
#     tab = []
#     for f in files * 4:
#         fn = str(f)
#         print("declaring interaction on %s ..." % fn)
#         entry = cli.declare(
#             languageTag="en-us", transcriptionMode="highAccuracy", mediafile=fn
#         )
#         tab.append(entry)

#     while True:
#         for e in tab:
#             s = cli.status(e)
#             if s != e["status"]:
#                 e["status"] = s
#             if s == "processed":
#                 tx = cli.transcripts(e)
#                 aiResult = cli.ai(e)
#                 print("Results[%s]:" % e["interactionIdentifier"], tx, aiResult)

#         processed = len([i for i in tab if i["status"] == "processed"])
#         if processed == len(tab):
#             print("DONE!")
#             break
#         else:
#             print("......")
#             time.sleep(10)
