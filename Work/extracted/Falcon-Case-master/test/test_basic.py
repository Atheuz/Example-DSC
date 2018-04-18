import unittest
import requests
import asyncio
import websockets
import signal

async def test_ws():
    async with websockets.connect('ws://127.0.0.1:5555/api/task/events/task-succeeded/') as ws:
	    msg = await ws.recv()
	    return "{}".format(msg)

class TestAPI(unittest.TestCase):
    
    def test_add(self):
        """Test adding objects."""
        url = "http://127.0.0.1/endpoint/"
        req = requests.post(url, json={"1":1})
        self.assertEqual(req.status_code, 200) # Should go through fine.
    
        req = requests.post(url, json={"a": 1234, "b": 5678, "c": 90})
        self.assertEqual(req.status_code, 200) # Should go through fine.
    
        req = requests.post(url, data='???????????')
        self.assertEqual(req.status_code, 400) # Invalid param should fail.

    def test_retrieve_all(self):
        """Test retrieval of all objects."""
        url = "http://127.0.0.1/endpoint/"
        req = requests.get(url)
        out = req.json()
    
        d = { "message": [], "status": "Success" }
        d["message"].append([1,{"1":1}])
        d["message"].append([2, {"a": 1234,"b": 5678,"c": 90}])
    
        self.assertDictEqual(out, d)
    
    def test_retrieve(self):
        """Test retrieval of a specific object."""
        url = "http://127.0.0.1/endpoint/{}"
        req = requests.get(url.format(1))
        out = req.json()
    
        d = { "message": [], "status": "Success" }
        d["message"].extend([1,{"1":1}])
        
        self.assertDictEqual(out, d)
    
        url = "http://127.0.0.1/endpoint/{}" # Redeclaration for clarity's sake.
        req = requests.get(url.format(2))
        out = req.json()
    
        d = { "message": [], "status": "Success" }
        d["message"].extend([2, {"a": 1234,"b": 5678,"c": 90}])
    
        self.assertDictEqual(out, d)

    def test_websocket(self):
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        loop = asyncio.get_event_loop()
        a = asyncio.async(test_ws())
    
        url = "http://127.0.0.1/endpoint/"
        req = requests.post(url, json={"1":1})

        res = loop.run_until_complete(a)
    
        self.assertIsNotNone(res)