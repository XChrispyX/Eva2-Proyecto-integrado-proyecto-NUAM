from django.core.management.base import BaseCommand
from kafka import KafkaConsumer
import json
import logging

class Command(BaseCommand):
    help = 'Consume mensajes de Kafka del topic nuam_calificaciones'

    def handle(self, *args, **options):
        consumer = KafkaConsumer(
            'nuam_calificaciones',
            bootstrap_servers=['kafka:9092'],
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='nuam_group'
        )

        self.stdout.write(self.style.SUCCESS("Escuchando mensajes de Kafka..."))

        for msg in consumer:
            data = msg.value
            logging.info("Mensaje recibido: %s", data)
            self.stdout.write(self.style.WARNING(f"Mensaje recibido: {data}"))
