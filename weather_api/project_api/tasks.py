import requests
import os
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from celery import shared_task

from project_api.models import CityWeatherCollection, MailingTask


@shared_task(name='email_report')
def email_report(emails, uuid):
    """Email weather report."""
    objects = CityWeatherCollection.objects.all()
    cities = []
    curr_weather = []
    feel_like = []
    for obj in objects:
        cities.append(obj.city)
        curr_weather.append(obj.current_temp)
        feel_like.append(obj.feels_like_temp)

    data_dict = {"cities": cities, "curr_weather": curr_weather, "feel_like": feel_like}
    df = pd.DataFrame(data_dict)
    df.to_csv("weather_report.csv", index=False)

    for email in emails:
        fromaddr = os.environ['email_id']
        toaddr = email
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Weather Report"

        # string to store the body of the mail
        body = "Attached file for weather report."
        msg.attach(MIMEText(body, 'plain'))

        # open the file to be sent
        filename = 'weather_report.csv'
        attachment = open('/', 'rb')

        # instance of MIMEBase and named as p
        p = MIMEBase('application', 'octet-stream')
        p.set_payload(tuple(attachment).read())
        encoders.encode_base64(p)

        p.add_header('Weather-Report', "attachment; filename= %s" % filename)
        msg.attach(p)

        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        # Authentication
        password = os.environ['password']
        s.login(fromaddr, password)
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
        s.quit()

    # Update Mailing task object status
    task_obj = MailingTask.objects.get(uuid=uuid)
    task_obj.status = 'Success'
    task_obj.save()


@shared_task(name='email_weather')
def weather_report():
    """Task for updating weather report every 30 minutes."""
    api_key = os.environ['api_key']

    # "http://api.openweathermap.org/data/2.5/weather?"
    main_url = os.environ['main_url']

    objects = CityWeatherCollection.objects.all()

    for obj in objects:
        url = main_url + "appid=" + api_key + "&q=" + obj.city  # It adds up city and api to form Complete Url
        raw = requests.get(url).json()
        obj.current_temp = raw['main']['temp']
        obj.feels_like_temp = raw['main']['feels_like']
        obj.save()
