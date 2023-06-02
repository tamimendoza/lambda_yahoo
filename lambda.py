import boto3
from urllib.request import urlopen
import json

cliente = boto3.client("ses", region_name="us-east-1")

class Accion:
    def __init__(self, empresa, ticker, precio_compra, cantidad):
        self.empresa = empresa
        self.ticker = ticker
        self.precio_compra = precio_compra
        self.cantidad = cantidad
        self.precio_actual = self.get_precio_actual()

    def get_precio_actual(self):
        url = "https://query1.finance.yahoo.com/v8/finance/chart/" + self.ticker
        response = urlopen(url)
        data = json.loads(response.read())
        precio = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
        return precio
    
def lambda_handler(event, context):
    accion1 = Accion("Apple", "AAPL", 172.99, 10)
    accion2 = Accion("Meta Platforms", "META", 252.69, 15)
    accion3 = Accion("Alphabet", "GOOGL", 123.48, 5)
    accion4 = Accion("Microsoft", "MSFT", 325.92, 20)

    acciones = [accion1, accion2, accion3, accion4]

    mensaje_html = "Acciones compradas: <br><lu>"
    for accion in acciones:
        mensaje_html += "<li>{} ({:.2f}/{:.2f}) = {:.2f}</li><br>".format(accion.empresa, accion.precio_compra, accion.precio_actual, accion.precio_actual - accion.precio_compra)

    mensaje_html += "</lu>"

    response = cliente.send_email(
        Destination={
            'ToAddresses': ['TUCORREO@gmail.com'],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': 'UTF-8',
                    'Data': mensaje_html,
                }
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': 'Reporte de acciones',
            }

        },
        Source='TUCORREO@gmail.com'
    )

    return {
        'statusCode': 200,
        'body': response['MessageId']
    }
