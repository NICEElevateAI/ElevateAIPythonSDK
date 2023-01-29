import aiohttp
import asyncio
 
class AsycClient:
    BOUNDARY = '_____123456789_____'
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
            'Content-Type': 'multipart/form-data;boundary=%s' % self.BOUNDARY,
            'X-API-TOKEN': token
        }
        self.jsonHeader = {
            'Content-Type': 'application/json; charset=utf-8',
            'X-API-TOKEN': token
        }

    async def declare(self, languageTag='auto', vertical='default', transcriptionMode='highAccuracy',
                mediafile = None, url = None):
        data = {
            'type': 'audio',
            'downloadUrl': url,
            'languageTag': languageTag,
            'vertical': vertical,
            'audioTranscriptionMode': transcriptionMode,
            'includeAiResults': True
        }
        async with aiohttp.ClientSession() as asess:
            async with asess.post(self.declareUri, headers = self.jsonHeader, json = data) as rsp:
                i = await rsp.json()
        if mediafile:
            await self.upload(i, mediafile)
        i['status'] = await self.status(i)
        return i

    async def upload(self, i, f):
        if type(i) == dict:
            i = i['interactionIdentifier']
        async with aiohttp.ClientSession() as asess:
            with aiohttp.MultipartWriter('form-data', boundary= self.BOUNDARY) as dw:
                fp = dw.append(open(f, 'rb'), headers = {'Content-Type': 'application/octet-stream'})
                fp.set_content_disposition('form-data', filename=f)
                rsp = await asess.post(self.uploadUri % i, headers= self.uploadHeader, data = dw)
                return rsp.ok

    async def status(self, interaction):
        if type(interaction) == dict:
            interaction = interaction['interactionIdentifier']
        async with aiohttp.ClientSession() as asess:
            async with asess.get(self.statusUri % interaction, headers = self.jsonHeader) as rsp:
                j = await rsp.json()
                return j['status']

    async def transcripts(self, interaction, punctuated=True):
        if type(interaction) == dict:
            interaction = interaction['interactionIdentifier']
        url = self.transcriptsUri2 if punctuated else self.transcriptsUri
        async with aiohttp.ClientSession() as asess:
            rsp = await asess.get(url % interaction, headers = self.jsonHeader)
            return await rsp.json()

    async def ai(self, interaction):
        if type(interaction) == dict:
            interaction = interaction['interactionIdentifier']
        async with aiohttp.ClientSession() as asess:
            rsp = await asess.get(self.aiUri % interaction, headers = self.jsonHeader)
            return await rsp.json()

async def test():
    import time
    from pathlib import Path
    files = list(Path('d:/dev/elevateai-cli/sample-media').glob('*.wav'))
    #files = list(Path('c:/tmp').glob('*.wav'))

    #cli = AsycClient('https://vaaissc01.nxondemand.com/PublicApi/v1', '75e63dc1-a121-43fd-8af6-626edc92d6a9')
    cli = AsycClient('http://localhost:5280/v1', '75e63dc1-a121-43fd-8af6-626edc92d6a9')

    tab = []
    for f in files:
        fn = str(f)
        print("declaring interaction on %s ..." % fn)
        entry = await cli.declare(languageTag='auto', mediafile=fn)
        tab.append(entry)

    while True:
        for e in tab:
            s = await cli.status(e)
            if s == 'processed':
                tx = await cli.transcripts(e)
                ai = await cli.ai(e)
                print("Results[%s]:" % e['interactionIdentifier'], tx, ai)
            if e['status'] != s:
                e['status'] = s
                print('Status changed to %s' % s)

        processed = len([i for i in tab if i['status']=='processed'])
        if processed== len(tab):
            print("DONE!")
            break
        else:
            print("......")
            time.sleep(10)

if __name__ == '__main__':
    asyncio.run(test())
