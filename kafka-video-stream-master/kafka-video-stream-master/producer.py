from sys import argv, exit
from time import sleep
import cv2
from kafka import KafkaProducer

class KafkaVideoStreaming():
    def __init__(self, bootstrap_servers, topic, videoFile, client_id, batch_size=65536, frq=0.001):
        self.videoFile = videoFile.replace("\\", "\\\\")  # Properly escape backslashes
        self.topicKey = str(videoFile)
        self.topic = topic
        self.batch_size = batch_size
        self.client_id = client_id
        self.bootstrap_servers = bootstrap_servers
        self.frq = frq

    def setProducer(self):
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            api_version=(0, 10, 1),
            client_id=self.client_id,
            acks=1,
            value_serializer=None,
            key_serializer=str.encode,
            batch_size=self.batch_size,
            compression_type='gzip',
            linger_ms=0,
            buffer_memory=67108864,
            max_request_size=1048576,
            max_in_flight_requests_per_connection=1,
            retries=1,
        )

    def reportCallback(self, record_metadata):
        print("Topic Record Metadata: ", record_metadata.topic)
        print("Partition Record Metadata: ", record_metadata.partition)
        print("Offset Record Metadata: ", record_metadata.offset)

    def errCallback(self, excp):
        print('Errback', excp)

    def publishFrames(self, payload):
        self.producer.send(
            topic=self.topic, key=self.topicKey, value=payload
        ).add_callback(
            self.reportCallback
        ).add_errback(
            self.errCallback
        )

    def run(self):
        try:
            print("Opening file %s" % self.videoFile)
            __VIDEO_FILE = cv2.VideoCapture(self.videoFile)
        except Exception as e:
            print(f"Error opening video file: {e}")
            exit(1)

        if not __VIDEO_FILE.isOpened():
            print(f"Error: Could not open video file {self.videoFile}")
            exit(1)

        self.setProducer()

        print(
            "Publishing: %{v}\n\
            \tBatch Size: {b},\n\
            \tSleep ({t}) \n\
            \tTarget Topic: {t} \n\
            \tHost: {h}".format(
                v=self.topicKey,
                b=self.batch_size,
                t=self.topic,
                h=self.bootstrap_servers
            )
        )

        self.keep_processing = True
        try:
            while __VIDEO_FILE.isOpened() and self.keep_processing:
                readStat, frame = __VIDEO_FILE.read()

                print("Read Status:", readStat)

                if not readStat:
                    self.keep_processing = False
                    print("Failed to read frame. Video file may be at the end or there is an issue.")
                    break

                print("Successfully read a frame.")
                ret, buffer = cv2.imencode('.jpg', frame)

                if not ret:
                    print("Failed to encode frame.")
                    continue

                self.publishFrames(buffer.tostring())
                sleep(self.frq)

            print('Finished processing video %s' % self.topicKey)  # Move this line outside the while loop

            __VIDEO_FILE.release()
        except KeyboardInterrupt:
            __VIDEO_FILE.release()
            print("Keyboard interrupt was detected. Exiting...")


if __name__ == "__main__":
    videoStream = KafkaVideoStreaming(
        bootstrap_servers='localhost:9092',
        topic='KafkaVideoStreamNew',
        videoFile=argv[1],
        client_id='KafkaVideoStreamClient',
    )
    videoStream.run()

