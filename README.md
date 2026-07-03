# Home Climate

A full-stack home climate monitoring system built on a Raspberry Pi, using Zigbee wireless sensors, Zigbee2MQTT, InfluxDB, and Grafana.

![Dashboard](./images/home-climate.png)

## Software stack

| Component | Purpose | Port |
|---|---|---|
| Mosquitto | MQTT broker | 1883 |
| Zigbee2MQTT | Zigbee coordinator + MQTT bridge | 8080 |
| InfluxDB 2.x | Time-series database | 8086 |
| Python bridge | MQTT → InfluxDB writer | — |
| Grafana | Dashboard + visualisation | 3000 |

## Architecture

```mermaid
flowchart LR
    subgraph sensors[Zigbee sensors]
        S1[Living room]
        S2[Office]
        S3[Our bedroom]
        S4[Bob bedroom]
    end

    subgraph pi[Raspberry Pi]
        DON[Sonoff dongle]
        Z2M[Zigbee2MQTT :8080]
        MOS[Mosquitto :1883]
        PY[Python bridge]
        IDB[(InfluxDB :8086)]
        GRA[Grafana :3000]
    end

    BRW[Browser / LAN device]

    S1 & S2 & S3 & S4 -->|Zigbee radio| DON
    DON -->|USB serial| Z2M
    Z2M -->|MQTT publish| MOS
    MOS -->|subscribe| PY
    PY -->|write| IDB
    IDB -->|Flux query| GRA
    GRA -->|HTTP :3000| BRW
```

## Hardware

- Raspberry Pi (4B or 3B+, 64-bit OS required)
- Sonoff Zigbee 3.0 USB Dongle Plus (coordinator)
- SONOFF SNZB-02P sensors (one per room, temperature + humidity, battery powered)

