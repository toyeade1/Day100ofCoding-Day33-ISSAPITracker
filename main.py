import requests
from datetime import datetime
import smtplib
import time

keep_refreshing = True
MY_LAT = 33.748997
MY_LONG = -84.387985


def is_close():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True
    else:
        return False


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}


def is_night():
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    current_hour = time_now.hour

    if current_hour > sunset or current_hour < sunrise:
        return True
    else:
        return False


def look_up():
    if is_close() and is_night():
        my_email = 'randonEmail@gmail.com'
        my_password = 'randomPassword'

        with smtplib.SMTP('stmp.gmail.com') as connection:
            connection.starttls()
            connection.login(my_email, my_password)
            connection.sendmail(from_addr=my_email,
                                to_addrs=my_email,
                                msg=f'Subject:Dont Waste Time\n\nLook Up! See Something?')


while keep_refreshing:
    time.sleep(60)
    print('Checking Again')
    look_up()

