import requests
from datetime import datetime, timedelta

from twilio.rest import Client
account_sid = "ACf226c4466d7d222efafc7ada099ee0dd"
auth_token = '91b48b9e3f23e399483b47f9384d78cc'
client = Client(account_sid, auth_token)

import time
import json

age = 25
pincodes = ["800001"]

num_days = 2

print_flag = 'Y'

print("starting search for Covid vaccine slot")

actual = datetime.today()
list_format = [actual + timedelta(days=i) for i in range(num_days)]
actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]

while True:
    counter = 0

    for pincode in pincodes:
        for given_date in actual_dates:
            url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pincode, given_date)
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

            result = requests.get(url, headers=header)
            # print('-------------------------------------------------------------')
            # print(result.text)
            # print('-------------------------------------------------------------')

            if result.ok:
                response_json = result.json()

                flag = False
                if response_json["centers"]:
                    if (print_flag.lower() == 'y'):

                        for center in response_json["centers"]:
                            # print('-------------------------------------------------------------')
                            # print(center)
                            # print('-------------------------------------------------------------')

                            for session in center["sessions"]:
                                if (session["min_age_limit"] <= age and session["available_capacity"] > 0):
                                    print('Pincode: ' + pincode)
                                    print("Available on: {}".format(given_date))
                                    print("\t", center["name"])
                                    print("\t", center["block_name"])
                                    print("\t Price: ", center["fee_type"])
                                    print("\t Availablity : ", session["available_capacity"])

                                    if (session["vaccine"] != ''):
                                        print("\t Vaccine type: ", session["vaccine"])
                                    print("\n")

                                    counter = counter + 1
                                else:
                                    pass
                else:
                    pass

            else:
                print("No Response!")
                message = client.messages.create(body="No Response!",
                                                 from_="+19549510503",
                                                 to="+91 7677911485")
                print(message.sid)

        if (counter == 0):
            print("No Vaccination slot avaliable!")
            message = client.messages.create(body="No Vaccination slot avaliable!",
                                             from_="+19549510503",
                                             to="+91 7677911485")
            print(message.sid)
        else:
            print("Search Completed!")
            message = client.messages.create(body="Search Completed",
                                             from_="+19549510503",
                                             to="+91 7677911485")
            print(message.sid)

        dt = datetime.now() + timedelta(minutes=3)

        while datetime.now() < dt:
            time.sleep(1)

