from dotenv import load_dotenv
import os
from selas import SelasClient
import asyncio
import websockets
import json

VERSION = '0.6.0'


class PusherAsyncClient(object):
    host = "ws.pusherapp.com"
    client_id = "PusherAsyncClients"
    protocol = 6

    def __init__(self, key, cluster="", secure=True,
                 port=443, custom_host=""):

        if cluster:
            self.host = "ws-{cluster}.pusher.com".format(cluster=cluster)
        else:
            self.host = "ws.pusherapp.com"
        self.key = key
        self.channels = {}
        self.url = self._build_url(secure, port, custom_host)
        self.websocket = None

    async def connect(self, loop=None):
        self.logger.debug("Connecting to: %s" % (self.url))
        try:
            self.websocket = await websockets.connect(self.url, ssl=True, loop=loop, ping_interval=5, ping_timeout=5, close_timeout=5)
        except Exception as e:
            self.logger.error("Exception: def connect(self) Err: %s" % (e))

        return self.websocket

    async def disconnect(self):
        try:
            await self.websocket.close()
        except Exception as e:
            self.logger.error("Exception: def disconnect(self) Err:%s" % (e))

    async def subscribe(self, channel_name, event_name='pusher:subscribe', auth=None):
        """Subscribe to a channel.
        :param str channel_name: The name of the channel to subscribe to.
        :param str auth: The token to use if authenticated externally.
        :rtype: pysher.Channel
        """
        data = {'channel': channel_name}

        event = {'event': event_name, 'data': data}
        if channel_name:
            event['channel'] = channel_name
        msg = json.dumps(event)

        resp = None
        try:
            await self.websocket.send(msg)
            resp = await self.websocket.recv()
            resp = json.loads(resp)
        except Exception as e:
            self.logger.error("Exception: def subscribe(self, channel_name=%s, auth=%s) Err:%s" % (
                channel_name, auth, e))
        return resp

    def _build_url(self, secure=True, port=None, custom_host=None):
        path = "/app/{}?client={}&version={}&protocol={}".format(
            self.key, self.client_id, VERSION, self.protocol
        )

        proto = "wss" if secure else "ws"

        host = custom_host or self.host
        if not port:
            port = 443 if secure else 80

        return "{}://{}:{}{}".format(proto, host, port, path)

async def bindToEvents(job_id, callbacks):
    # Create an instance of PusherAsyncClient and pass it the appkey
    pusherclient = PusherAsyncClient("ed00ed3037c02a5fd912", cluster="eu")
    # Connect to websocket
    pushersocket = await pusherclient.connect()

    # Subscribe to channel

    channel = 'job-' + job_id
    print(channel)

    status = await pusherclient.subscribe(channel_name=channel)
    # pushersocket = await pusherclient.connect()

    #print("Subscription Status: %s" % (status))
    while True:
        # This is because re-connection logic is not implemented yet
        if not pushersocket.open:
            # on disconnections, reconnect
            print("Connection reconnecting")
            # re-connect
            pushersocket = await pusherclient.connect()
            # re-subscribe
            status = await pusherclient.subscribe(channel_name='job-dfa7e563-13d2-4b2b-ba0a-6d651e38f441')
            print("Subscription Status: %s" % (status))
        try:
            # wait for msg
            msg = await asyncio.wait_for(pushersocket.recv(), 5)
            # parse to json
            msg = json.loads(msg)
            # print the msg
            if msg: 
                if msg['event'] in callbacks:
                    callback_event = callbacks[msg['event']]
                    callback_event(msg['data'])
        except asyncio.TimeoutError:
            pass
            #print("asyncio timeout while waiting for ws msg")
        except Exception as e:
            print(e) 

load_dotenv()
loop = asyncio.new_event_loop()


if __name__ == "__main__":

    TEST_APP_ID = os.environ.get("TEST_APP_ID")
    TEST_APP_KEY = os.environ.get("TEST_APP_KEY")
    TEST_APP_SECRET = os.environ.get("TEST_APP_SECRET")

    selas = SelasClient(TEST_APP_ID, TEST_APP_KEY, TEST_APP_SECRET)

    job = selas.runStableDiffusion("Selas", patches=[{
        "name": 'Skippy Jack/f-boopboop',
        "alpha_text_encoder": 0.5,
        "alpha_unet": 0.5,
        "steps": 1000,
    }])
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(selas.subscribeToJob(job.data['job_id'],{'result':(lambda x : print(x))}))
    loop.close()