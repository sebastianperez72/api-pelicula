import boto3
import uuid
import os
import json


def log(tipo, log_datos):
    # Formato json de log estandar: {"tipo": "INFO"/"ERROR", "log_datos": {...}}
    print(json.dumps({
        "tipo": tipo,
        "log_datos": log_datos
    }, ensure_ascii=False, default=str))


def lambda_handler(event, context):
    try:
        # Entrada (json)
        tenant_id = event['body']['tenant_id']
        pelicula_datos = event['body']['pelicula_datos']
        nombre_tabla = os.environ["TABLE_NAME"]

        # Proceso
        uuidv4 = str(uuid.uuid4())
        pelicula = {
            'tenant_id': tenant_id,
            'uuid': uuidv4,
            'pelicula_datos': pelicula_datos
        }
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(nombre_tabla)
        response = table.put_item(Item=pelicula)

        # Salida (json) - Log de ejecucion correcta
        log("INFO", pelicula)
        return {
            'statusCode': 200,
            'pelicula': pelicula,
            'response': response
        }

    except Exception as e:
        # Log de error
        log("ERROR", {
            'tipo_error': type(e).__name__,
            'mensaje': str(e),
            'event': event
        })
        return {
            'statusCode': 500,
            'error': type(e).__name__,
            'mensaje': str(e)
        }
