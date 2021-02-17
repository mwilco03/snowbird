import os
from pyhtcc import PyHTCC
import json
import smtplib

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
except:
    print ('Something went wrong...')

def send_Email(recipients,alert):
    sent_from ='NoReply@SnowBird.Watcher'
    subject = 'SnowBirdWatcher'
    body = alert
    email_text ="""\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(recipients), subject, body)
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, recipients, email_text)
        server.close()
        print ('Email sent!')
    except:
        print ('Something went wrong...')

def get_Info(usr,pswd):
    thermostat = PyHTCC(usr,pswd)
    tInfo = thermostat.get_zones_info()
    form = {}
    mymsg = []
    for info in tInfo:
        form["temp"] = info["latestData"]["uiData"]["DispTemperature"]
        if info["latestData"]["uiData"]["SystemSwitchPosition"] == 1:
            form["mode"] = "heat"
            form["set"] = info["latestData"]["uiData"]["HeatSetpoint"]
        elif info["latestData"]["uiData"]["SystemSwitchPosition"] == 3:
            form["mode"] = "cool"
            form["set"] = info["latestData"]["uiData"]["CoolSetpoint"]
        if len(info["Alerts"])  >= 0:
            for msg in info["Alerts"]:
                form["message"] = str(msg).split(".")[0] + "\r\nWhen connection was lost settings were as follows. \r\n"
        if (info["GatewayIsLost"] == False) and (info["deviceLive"] == True) and (info["communicationLost"] == False):
            form["message"] = "Online"
        elif info["GatewayUpgrading"] == True:
            form["message"] = "Being Upgradd'd"
        mode = "Mode is set to: "+form["mode"]
        current = "Current temp reading: "+str(form["temp"])
        setpoint = "Thermostat set point: "+str(form["set"])
        mymsg = (form["message"].lstrip(),current,setpoint,mode)
        tdata = "\r\n".join(mymsg)
        return str(tdata)
        
