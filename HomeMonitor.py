# -*- coding: utf-8 -*-
import xively
import smtplib
import datetime
import sys
import time
import xml.etree.ElementTree as etree


class Gmail():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.SMTP_SERVER = 'smtp.gmail.com'
        self.SMTP_PORT = 587
        self.session = None

    def login(self):
        self.session = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
        self.session.ehlo()
        self.session.starttls()
        self.session.ehlo
        login = self.session.login(self.username, self.password)
        if login:
            return True
        else:
            return False

    def createHeader(self, subject, recipient):
        header = ["from: " + self.username,
        "subject: " + subject,
        "to: " + recipient,
        "mime-version: 1.0",
        "content-type: text/html"]
        header = "\r\n".join(header)
        return header

    def sendMail(self, subject, recipients, body):
        login = self.login()
        if login:
            for recipient in recipients:
                header = self.createHeader(subject, recipient)
                message = header + "\r\n\r\n" + body
                sent = self.session.sendmail(self.username, recipient, message)
                if not sent:
                    print "Email could not be sent to " + recipient + "!"
            self.session.quit()
            self.session = None
        else:
            print "You could not be logged in!"


class HomeMonitor():
    def __init__(self):
        self.XIVELY_API_KEY = ""
        self.XIVELY_FEED_ID = 
        self.feed = None
        self.DEBUG = False

    def getTemp(self):
        try:
            self.getFeed()
            datastream = self.feed.datastreams.get("humidity1")  # 'humidity1 is correct here for now I mislabeled it on the arduino'
            if self.DEBUG:
                print "Found Temperature Stream."
            return datastream
        except:
            if self.DEBUG:
                print "Could not get temp datastream from Xively"

    def getHumidity(self):
        try:
            self.getFeed()
            datastream = self.feed.datastreams.get("temp1")  # 'temp1 is correct here for now I mislabeled it on the arduino'
            if self.DEBUG:
                print "Found Humidity Stream."
            return datastream
        except:
            if self.DEBUG:
                print "Could not get humidity datastream from Xively"

    def getFeed(self):
        api = xively.XivelyAPIClient(self.XIVELY_API_KEY)
        self.feed = api.feeds.get(self.XIVELY_FEED_ID)

    def currentTemp(self):
        temp = self.getTemp()
        return temp.current_value

    def checkTemp(self, previous, current, gmail, recipients):
        if previous != current:
            gmail.sendMail("Change in Temperature", recipients, "There was a change in temperature. The previous temperature reading was " + str(previous) + " and the current reading is " + str(current) + ".")
