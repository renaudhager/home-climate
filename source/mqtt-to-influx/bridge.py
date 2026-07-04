import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import json

INFLUX_URL    = "http://localhost:8086"
INFLUX_TOKEN  = "<REDACTED>"
INFLUX_ORG    = "renorainz"
INFLUX_BUCKET = "temperature"

ROOMS = {
    "living room":  "indoor",
    "office":       "indoor",
    "our bedroom":  "indoor",
    "Owen bedroom": "indoor",
    "riverside balcony": "outdoor",
    "courtyard balcony": "outdoor",
}

write_client = InfluxDBClient(
    url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG
).write_api(write_options=SYNCHRONOUS)

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker (rc={rc})")
    for room in ROOMS:
        client.subscribe(f"zigbee2mqtt/{room}")
        print(f"Subscribed to zigbee2mqtt/{room}")

def on_message(client, userdata, msg):
    room = msg.topic.removeprefix("zigbee2mqtt/")
    if room not in ROOMS:
        return
    try:
        payload = json.loads(msg.payload)
    except json.JSONDecodeError:
        return

    location = ROOMS[room]  # "indoor" or "outdoor"

    point = (
        Point("sensor_reading")
        .tag("room", room)
        .tag("location", location)  # new tag
    )

    if "temperature" in payload:
        point = point.field("temperature", float(payload["temperature"]))
    if "humidity" in payload:
        point = point.field("humidity", float(payload["humidity"]))
    if "battery" in payload:
        point = point.field("battery", float(payload["battery"]))

    write_client.write(bucket=INFLUX_BUCKET, record=point)
    print(f"[{location}] {room}: {payload.get('temperature')}°C  {payload.get('humidity')}%")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883)
client.loop_forever()

