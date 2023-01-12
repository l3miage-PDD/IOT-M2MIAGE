# -*- coding: utf-8 -*-
import logging
import asyncio
import platform
import struct
import requests
from bleak import BleakClient

########################################
# BLE datas

# UUID de la led
_LED_UUID = "20000000-0001-11E1-AC36-0002A5D5C51B"
# UUID des capteurs
SENSOR_UUID = "001c0000-0001-11e1-ac36-0002a5d5c51b"

ADDRESS = (
    "02:09:13:5D:26:86"                         # <--- Change to your device's address here if you are using Windows or Linux
    if platform.system() != "Darwin"
    else "B9EA5233-37EF-4DD6-87A8-2A875E821C46" # <--- Change to your device's address here if you are using macOS
)

########################################
# MQTT datas

accesstoken='YzRw451I5GyzLZcS198j'
host = f"https://im2ag-thingboard.univ-grenoble-alpes.fr/api/v1/YzRw451I5GyzLZcS198j/telemetry"

# Coroutine handling BLE
async def run(address, debug=False):
	print("Bleak connects..")

	async with BleakClient(address) as bleak_client:
		print(f"Bleak connected: {bleak_client}")

		def notification_handler(sender, data):
			timestamp, tension = struct.unpack('<Hi', data)
			msg = {'timestamp': timestamp, 'Puissance(W)':tension}
			print(msg)
			r = requests.post(host, json=msg, verify='./chain.pem')

		await bleak_client.start_notify(SENSOR_UUID, notification_handler)
		print("Start notify ok")
		try:
			while True:
				await asyncio.sleep(1)
		except asyncio.CancelledError:
			print("Shutdown Request Received")
		print("Stop")
		await bleak_client.stop_notify(SENSOR_UUID)
			
			
# Starts BLE handling
loop = asyncio.get_event_loop()
loop.run_until_complete(run(ADDRESS))
		
