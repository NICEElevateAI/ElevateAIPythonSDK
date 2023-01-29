import requests
import json

class Client:
    def __init__(self, url, token):
        self.url = url
        self.api_token = token
        self.declareUri = url + '/interactions'
        self.uploadUri = url + '/interactions/%s/upload'
        self.statusUri = url + '/interactions/%s/status'
        self.transcriptsUri = url + '/interactions/%s/transcripts'
        self.transcriptsUri2 = url + '/interactions/%s/transcripts/punctuated'
        self.aiUri = url + '/interactions/%s/ai'
        self.uploadHeader = {
            'X-API-TOKEN': token
        }
        self.jsonHeader = {
            'Content-Type': 'application/json; charset=utf-8',
            'X-API-TOKEN': token
        }
        self.session = requests.session()
        self.session.headers.update(self.jsonHeader)

    def declare(self, languageTag='en-us', vertical='default', transcriptionMode='highAccuracy',
                mediafile = None, url = None):
        data = {
            'type': 'audio',
            'downloadUrl': url,
            'languageTag': languageTag,
            'vertical': vertical,
            'audioTranscriptionMode': transcriptionMode,
            'includeAiResults': True
        }
        rsp = self.session.post(self.declareUri, data = json.dumps(data))
        i = rsp.json()
        if mediafile:
            self.upload(i, mediafile)
        i['status'] = self.status(i)
        return i

    def upload(self, i, f):
        if type(i) == dict:
            i = i['interactionIdentifier']
        files = [
            ('', (f, open(f, 'rb'), 'application/octet-stream'))
        ]
        rsp = requests.post(self.uploadUri % i, headers= self.uploadHeader, files = files)
        return rsp

    def status(self, interaction):
        if type(interaction) == dict:
            interaction = interaction['interactionIdentifier']
        rsp = self.session.get(self.statusUri % interaction)
        return rsp.json()['status']

    def transcripts(self, interaction, punctuated=True):
        if type(interaction) == dict:
            interaction = interaction['interactionIdentifier']
        url = self.transcriptsUri2 if punctuated else self.transcriptsUri
        rsp = self.session.get(url % interaction)
        return rsp.json()

    def ai(self, interaction):
        if type(interaction) == dict:
            interaction = interaction['interactionIdentifier']
        rsp = self.session.get(self.aiUri % interaction)
        return rsp.json()

if __name__ == '__main__':
    import time
    from pathlib import Path
    #files = list(Path('d:/dev/elevateai-cli/sample-media').glob('*.wav'))
    files = list(Path('c:/tmp').glob('*.wav'))

    #cli = Client('https://vaaissc01.nxondemand.com/PublicApi/v1', '75e63dc1-a121-43fd-8af6-626edc92d6a9')
    cli = Client('http://localhost:5280/v1', '75e63dc1-a121-43fd-8af6-626edc92d6a9')
    tab = []
    for f in files * 4:
        fn = str(f)
        print("declaring interaction on %s ..." % fn)
        entry = cli.declare(languageTag='en-us', transcriptionMode='highAccuracy',mediafile=fn)
        tab.append(entry)

    while True:
        for e in tab:
            s = cli.status(e)
            if s != e['status']:
                e['status'] = s
            if s == 'processed':
                tx = cli.transcripts(e)
                aiResult = cli.ai(e)
                print("Results[%s]:" % e['interactionIdentifier'], tx, aiResult)

        processed = len([i for i in tab if i['status']=='processed'])
        if processed== len(tab):
            print("DONE!")
            break
        else:
            print("......")
            time.sleep(10)