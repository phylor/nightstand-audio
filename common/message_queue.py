import pika
import json
import sys

class MessageQueue:

    def connect(self):
        connection_params = pika.ConnectionParameters('localhost')
        self.connection = pika.BlockingConnection(connection_params)
        channel = self.connection.channel()
        channel.queue_declare(queue='nightstand-audio')

    def disconnect(self):
        self.connection.channel().close()

    def send(self, content):
        self.connect()

        self.channel.basic_publish(exchange='',
                      routing_key='nightstand-audio',
                      body=json.dumps(content))

        self.disconnect()
