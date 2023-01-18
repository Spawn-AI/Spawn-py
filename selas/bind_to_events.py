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
        try:
            self.websocket = await websockets.connect(self.url, ssl=True, loop=loop, ping_interval=5, ping_timeout=5, close_timeout=5)
        except Exception as e:
            print("Exception: def connect(self) Err: %s" % (e))

        return self.websocket

    async def disconnect(self):
        try:
            await self.websocket.close()
        except Exception as e:
            print("Exception: def disconnect(self) Err:%s" % (e))

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
            print("Exception: def subscribe(self, channel_name=%s, auth=%s) Err:%s" % (
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

async def bind_to_events(job_id, callbacks):
    pusherclient = PusherAsyncClient("ed00ed3037c02a5fd912", cluster="eu")
    pushersocket = await pusherclient.connect()
    channel = 'job-' + job_id
    print(channel)

    status = await pusherclient.subscribe(channel_name=channel)

    while True:
        if not pushersocket.open:
            print("Connection reconnecting")
            pushersocket = await pusherclient.connect()
            status = await pusherclient.subscribe(channel_name=channel)
            print("Subscription Status: %s" % (status))
        try:
            msg = await asyncio.wait_for(pushersocket.recv(), 5)
            msg = json.loads(msg)
            if msg: 
                if msg['event'] in callbacks:
                    callback_event = callbacks[msg['event']]
                    callback_event(msg)
        except asyncio.TimeoutError:
            pass
        except Exception as e:
            print(e) 
