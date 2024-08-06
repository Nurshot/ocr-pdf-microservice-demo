import pika
import json
import os
import base64
import ocrmypdf


rabbitmq_host = os.getenv("RABBITMQ_URL", "rabbitmq")

def connect_to_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue='pdf_service')
    return connection, channel

connection, channel = connect_to_rabbitmq()


if not os.path.exists("tmp"):
    os.makedirs("tmp")

class OCRService:

    def ocr_pdf(self, pdf_path):
        output_file = "tmp/output_pdf.pdf"
        try:
            ocrmypdf.ocr(
                pdf_path,
                output_file,
                language="eng",
                rotate_pages=True,
                deskew=True,
                title="",
                jobs=4,
                output_type="pdfa",
                force_ocr=True
            )
            print(f"Processed {pdf_path} to {output_file}")
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")
            #return None

        try:
            with open(output_file, "rb") as buffer:
                file_data = buffer.read()
                file_base64 = base64.b64encode(file_data).decode()
        except Exception as e:
            print(f"Error reading {output_file}: {e}")
            #return None

        #os.remove(output_file)
        return file_base64

    def process_request(self, message):
        message_body = json.loads(message)
        file_base64 = message_body['file']
        print(f" [x] Processing request...")

        file_data = base64.b64decode(file_base64.encode())
        temp_file_path = 'tmp/decoded_pdf.pdf'
        with open(temp_file_path, 'wb') as f:
            f.write(file_data)

        ocr_pdf = self.ocr_pdf(temp_file_path)
        if ocr_pdf is None:
            return None

        print(" [^] OCR processing done!")

        response = {"file_output": ocr_pdf}
        #os.remove(temp_file_path)
        return response

def callbackfunc(ch, method, props, body):
    ocr_service = OCRService()
    response = ocr_service.process_request(body)

    if response is not None:
        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(correlation_id=props.correlation_id),
            body=json.dumps(response)
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

channel.basic_qos(prefetch_count=2)
channel.basic_consume(queue='pdf_service', on_message_callback=callbackfunc)

print(" [x] Awaiting RPC requests")
channel.start_consuming()
