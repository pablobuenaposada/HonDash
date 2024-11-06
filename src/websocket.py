import asyncio
import contextlib
import json
import threading

import websockets

from constants import WEBSOCKET_HOST, WEBSOCKET_PORT
from devices.logger.logger import Logger
from devices.setup_validator.setup_validator import SetupValidator


class Websocket:
    def __init__(self, backend):
        self.backend = backend
        self.websocket = websockets.serve(
            self.connection_handler, WEBSOCKET_HOST, WEBSOCKET_PORT
        )
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.websocket)
        threading.Thread(target=self.loop.run_forever).start()

    async def connection_handler(self, websocket):
        await asyncio.gather(
            self.broadcast_data(websocket), self._consumer_handler(websocket)
        )

    async def broadcast_data(self, websocket):
        """Keeps sending updated ecu data forever"""
        while websocket.open:
            await websocket.send(json.dumps({"data": self.backend.update()}))
            await asyncio.sleep(0.01)

    async def _consumer_handler(self, websocket):
        """Here is where messages from clients are processed"""
        async for message in websocket:
            data = json.loads(message)
            if data["action"] == "setup":
                await websocket.send(json.dumps({"setup": self.backend.setup()}))
            elif data["action"] == "toggle_style":
                self.backend.style.toggle()
            elif data["action"] == "toggle_datalog":
                self.backend.logger.toggle()
            elif data["action"] == "datalogs":
                await websocket.send(json.dumps({"datalogs": Logger.get_logs()}))
            elif data["action"].startswith("datalog_"):
                file_name = data["action"].split("datalog_")[1]
                log = Logger.get_log(file_name)
                if log:
                    await websocket.send(json.dumps({f"datalog_{file_name}": log}))
            elif data["action"].startswith("remove_datalog_"):
                with contextlib.suppress(FileNotFoundError):
                    Logger.remove_log(data["action"].split("remove_datalog_")[1])
                await websocket.send(json.dumps({"datalogs": Logger.get_logs()}))
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
            elif data["action"] == "raw":
                await websocket.send(
                    json.dumps(
                        {
                            "data0": list(getattr(self.backend.ecu.ecu, "data0", [])),
                            "data1": list(getattr(self.backend.ecu.ecu, "data1", [])),
                            "data2": list(getattr(self.backend.ecu.ecu, "data2", [])),
                            "data3": list(getattr(self.backend.ecu.ecu, "data3", [])),
                            "data4": list(getattr(self.backend.ecu.ecu, "data4", [])),
                            "data5": list(getattr(self.backend.ecu.ecu, "data5", [])),
                            "data6": list(getattr(self.backend.ecu.ecu, "data6", [])),
                        }
                    )
                )

    def stop(self):
        self.websocket.ws_server.close()
        self.loop.call_soon_threadsafe(self.loop.stop)
