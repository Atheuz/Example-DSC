import asyncio
import websockets
import signal

async def hello():
    async with websockets.connect('ws://127.0.0.1:5555/api/task/events/task-succeeded/') as ws:
	    msg = await ws.recv()
	    print("{}".format(msg))

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    while True:
        asyncio.get_event_loop().run_until_complete(hello())

if __name__ == '__main__':
    main()