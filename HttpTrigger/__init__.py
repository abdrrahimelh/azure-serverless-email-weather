import logging

import azure.functions as func
from azure.communication.email import EmailClient, EmailContent, EmailAddress, EmailMessage, EmailRecipients
import dload

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        connection_string = "$SECRET"
        client = EmailClient.from_connection_string(connection_string)
        sender = "$SENDER"
        data = dload.json("https://api.openweathermap.org/data/2.5/weather?q=" +
                          "Bordeaux"+"&units=metric&appid=10233baa27900bde1363821e57d39603")
        temperature = data["main"]["feels_like"]
        description = data["weather"][0]["description"]
        icon = data["weather"][0]["icon"]
        content = EmailContent(
            subject="Today's weather in Bordeaux",
            plain_text=("The temperature is "+str(temperature)+"\r\n"
                        "Today is "+description
                        ),
            html="""<html>
            <head></head>
            <body>
                <h1>Today is """ + description+"""</h1>
                <p>The temperature is """+str(temperature)+""" °C</p>
                <p style="text-align:center;">
                <img src="http://openweathermap.org/img/wn/"""+icon+"""@2x.png" alt="weather" width="100" height="100"</img>
                </p>
            </body>
            </html>
                        """,
        )

        recipient = EmailAddress(
            email="$SEDER", display_name="NAME")

        message = EmailMessage(
            sender=sender,
            content=content,
            recipients=EmailRecipients(to=[recipient])
        )

        response = client.send(message)
       
    except Exception as ex:
        print(ex)

