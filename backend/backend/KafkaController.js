const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'KafkaVSClient',
  brokers: ['localhost:9092'],
});

const consumer = kafka.consumer({ groupId: 'KafkaVideoStreamConsumer' });

const run = async () => {
  await consumer.connect();
  await consumer.subscribe({ topic: 'KafkaVideoStreamNew' });

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      console.log({
        value: message.value.toString(),
      });
    },
  });
};

run().catch(console.error);
