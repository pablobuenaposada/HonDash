import asyncio
import json
import threading

import websockets

from backend.constants import WEBSOCKET_HOST, WEBSOCKET_PORT
from backend.devices.setup_validator.setup_validator import SetupValidator


class Websocket:
    clients_connected = set()
    backend = None

    def __init__(self, backend):
        self.backend = backend
        self.websocket = websockets.serve(
            self._websocket_handler, WEBSOCKET_HOST, WEBSOCKET_PORT
        )
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.websocket)
        threading.Thread(target=self.loop.run_forever).start()

    async def _websocket_handler(self, websocket, path):
        await self._register(websocket)  # register this client to keep tracking of it
        consumer_task = asyncio.ensure_future(self._consumer_handler(websocket))
        producer_task = asyncio.ensure_future(self._producer_handler(websocket))
        done, pending = await asyncio.wait(
            [consumer_task, producer_task], return_when=asyncio.FIRST_COMPLETED
        )
        for task in pending:
            task.cancel()

    async def _consumer_handler(self, websocket):
        """Here is where messages from clients are processed"""
        async for message in websocket:
            data = json.loads(message)
            if data["action"] == "setup":
                await websocket.send(json.dumps({"setup": self.backend.setup()}))
            elif data["action"] == "save":
                try:
                    self.backend.save(data["data"])
                except SetupValidator.ValidationError as e:
                    await self._send_all_clients(
                        json.dumps(
                            {"action": "alert", "message": f"ERROR: {e.message}"}
                        )
                    )
                else:
                    # send refresh action to all the frontends so the new changes are applied
                    await self._send_all_clients(json.dumps({"action": "refresh"}))
                    await self._send_all_clients(
                        json.dumps(
                            {"action": "alert", "message": "SUCCESS: setup saved!"}
                        )
                    )
            elif data["action"] == "reset":
                self.backend.reset()
                # send refresh action to all the frontends so the new changes are applied
                await self._send_all_clients(json.dumps({"action": "refresh"}))
                await self._send_all_clients(
                    json.dumps({"action": "alert", "message": "SUCCESS: setup reset!"})
                )

    async def _producer_handler(self, websocket):
        """Keeps sending updated ecu data forever"""
        while True:
            await websocket.send(json.dumps({"data": self.backend.update()}))
            await asyncio.sleep(0.1)

    async def _send_all_clients(self, message):
        """Broadcast to all the clients"""
        if self.clients_connected:  # asyncio.wait doesn't accept an empty list
            await asyncio.wait([user.send(message) for user in self.clients_connected])

    async def _register(self, websocket):
        """Appends a new client to the connected clients list"""
        self.clients_connected.add(websocket)

    def stop(self):
        self.websocket.ws_server.close()
        self.loop.call_soon_threadsafe(self.loop.stop)
