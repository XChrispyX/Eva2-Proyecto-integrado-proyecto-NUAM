import json
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from kafka import KafkaProducer
from .models import CalificacionTributaria

def get_kafka_producer():
    try:
        producer = KafkaProducer(
            bootstrap_servers=['kafka:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        return producer
    except Exception:
        logging.exception("No se pudo conectar a Kafka")
        return None

@receiver(post_save, sender=CalificacionTributaria)
def publicar_calificacion_en_kafka(sender, instance, created, **kwargs):
    if not created:
        return  # solo publicar cuando se crea

    producer = get_kafka_producer()
    if producer is None:
        return

    mensaje = {
        "id": instance.id,
        "rut_empresa": instance.rut_empresa,
        "anio": instance.anio,
        "instrumento": instance.instrumento,
        "monto": float(instance.monto),
        "moneda": instance.moneda,
        "usuario_id": instance.usuario.id,
    }

    try:
        producer.send('nuam_calificaciones', mensaje)
        producer.flush()
        logging.info("Mensaje enviado a Kafka: %s", mensaje)
    except Exception:
        logging.exception("Error enviando mensaje a Kafka")