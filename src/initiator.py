import paho.mqtt.client as mqtt


# The callback when the client receives a CONNACK response from the broker
def on_connect(client, userdata, flags, rc):
    print("[LOG] Connected with result code "+str(rc))
    client.subscribe("read/file")
    if rc != 0:
        client.reconnect()


# The callback when a PUBLISH message is received from the broker
def on_message(client, userdata, msg):
    if msg.payload.decode() == "done":
        print("[LOG] The file processing is " + msg.payload.decode())
        client.disconnect()


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--brokerip", help="ip address of the broker",
                        type=str, default="localhost")
    parser.add_argument("--port", help="broker port", type=int, default=1883)
    args = parser.parse_args()

    initiator = mqtt.Client(parser.prog)
    initiator.connect(args.brokerip, args.port)
    initiator.on_connect = on_connect
    initiator.on_message = on_message
    initiator.publish("read/file", "start")
    initiator.loop_forever()


if __name__ == "__main__":
    main()
