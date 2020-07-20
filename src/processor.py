import paho.mqtt.client as mqtt


readfile = ""
writefile = ""


# File I/O processing
def file_processor():
    with open(writefile, 'w') as out:
        with open(readfile, 'r') as f:
            for chunk in read_chunks_from_file(f):
                # Appending chunks with newline/linefeed(Hex: 0x0A)
                chunk.append(0x0A)
                out.write(chunk.decode())
    print("[LOG] The processed file is " + writefile)


# Read chunks of 1KB from the file
def read_chunks_from_file(fileobj, chunksize=1024):
    while True:
        chunk = fileobj.read(chunksize)
        if not chunk:
            break
        yield bytearray(chunk.encode())


# The callback when the client receives a CONNACK response from the broker
def on_connect(client, userdata, flags, rc):
    print("[LOG] Connected with result code "+str(rc))
    client.subscribe("read/file")
    if rc != 0:
        client.reconnect()


# The callback when a PUBLISH message is received from the broker
def on_message(client, userdata, msg):
    if msg.payload.decode() == "start":
        print("[LOG] Processing file " + readfile)
        file_processor()
        client.publish("read/file", "done")
        client.disconnect()


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--brokerip", "-b", help="ip address of the broker",
                        type=str, default="localhost")
    parser.add_argument("--port", "-p", help="broker port",
                        type=int, default=1883)
    parser.add_argument("--file", "-f", help="input file path",
                        type=str, required=True)
    args = parser.parse_args()

    global readfile
    readfile = args.file
    global writefile
    writefile = args.file + ".processed"

    processor = mqtt.Client(parser.prog)
    processor.connect(args.brokerip, args.port)
    processor.on_connect = on_connect
    processor.on_message = on_message
    processor.loop_forever()


if __name__ == "__main__":
    main()
