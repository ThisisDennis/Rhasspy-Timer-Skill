import threading
import time
from rhasspyhermes.nlu import NluIntent
from rhasspyhermes_app import EndSession, HermesApp
import paho.mqtt.client as mqtt

app = HermesApp("TimerApp")
t = None
soundfile = bytes()

class TimerJob(object):
    answer  = u"Biep biep, dein Teimer ist abgelaufen, Biep biep"
    intent = None
    timer = None
    start_time = None
    time_range = 0

    def __init__(self, intent): 
        self.intent = intent

    def buildSentence(self):
        seconds = self.getSeconds()[1]
        minutes = self.getMinutes()[1]
        hours = self.getHours()[1]

        s = len(seconds)>1
        m = len(minutes)>1
        h = len(hours)>1

        if(seconds == "eins"):
            seconds = "eine Sekunde"
        else:
            seconds = seconds + " Sekunden"
        if(minutes == "eins"):
            minutes = "eine Minute"
        else:
            minutes = minutes + " Minuten"
        if(hours == "eins"):
            hours = "eine Stunde"
        else:
            hours = hours + " Stunden"
        
        sentence = ""

        if s and (not m) and (not h):
            sentence =  "Habe Teimer auf " + seconds +  " gestellt"

        elif s and m and (not h):
            sentence =  "Habe Teimer auf " + minutes + " und " + seconds + " gestellt"

        elif (not s) and m and (not h):
            sentence =  "Habe Teimer auf " + minutes + " gestellt"
            
        elif not m and (not s):
            sentence =  "Habe Teimer auf " + hours + " gestellt"

        elif (not m) and s and h:
            sentence =  "Habe Teimer auf " + hours + " und " + seconds + " gestellt"
            
        elif (not s) and m and h:
            sentence =  "Habe Teimer auf " + hours + " und " + minutes + " gestellt"

        elif s and m and h:
            sentence =  "Habe Teimer auf " + hours + " und " + minutes + " und " + seconds + "gestellt"
        
        #print(sentence)
        app.notify(sentence, self.intent.site_id)
        global t
        t = None
        self.timer = None
        self.start_time = 0


    def notify(self):
        #print(self.answer)
        app.notify(self.answer, self.intent.site_id)
        self.playSound()
    
    def playSound(self):
        client.publish("hermes/audioServer/" + self.intent.site_id + "/playBytes/activate", soundfile)
 
    def getSeconds(self):
        for slot in self.intent.slots:
            if slot.slot_name == 'seconds':
                return [slot.value['value'], slot.raw_value]
        return [0, ""]

    def getMinutes(self):
        for slot in self.intent.slots:
            if slot.slot_name == 'minutes':
                return [slot.value['value'], slot.raw_value]
        return [0, ""]

    def getHours(self):
        for slot in self.intent.slots:
            if slot.slot_name == 'hours':
                return [slot.value['value'], slot.raw_value]
        return [0, ""]

    def start(self):
        seconds = int(self.getSeconds()[0])
        minutes = int(self.getMinutes()[0])
        hours   = int(self.getHours()[0])
        self.time_range = seconds + minutes * 60 + hours * 3600
        print("start Timer: " + str(self.time_range))
        timer = threading.Timer(self.time_range, self.notify)
        self.buildSentence()
        self.start_time = time.time()
        self.timer = timer
        timer.start()
    
    def stop(self):
        global t
        self.timer.cancel()
        self.timer = None
        self.start_time = 0
        self.time_range = 0
        t = None
        return "Teimer wurde gestoppt"

    def timeRemaining(self):
        if self.timer == None:
            return "kein Teimer gestellt"
        timePassed = time.time() - self.start_time
        timeDiff = self.time_range - int(timePassed)
        m, s = divmod(timeDiff, 60)
        h, m = divmod(m, 60)
        if(h > 0):
            sentence = "Der Teimer läuft noch " + str(int(h)) + " Stunden, " + str(int(m)) + " Minuten und " + str(int(s)) + " Sekunden "
        elif(m > 0):
            sentence = "Der Teimer läuft noch " + str(int(m)) + " Minuten und " + str(int(s)) + " Sekunden "
        elif(s > 0):
            sentence = "Der Teimer läuft noch " + str(int(s)) + " Sekunden "
        return sentence

@app.on_intent("Timerjob:start")
async def timer(intent: NluIntent):
    global t
    if t!= None:
        app.notify("Bereits laufender Teimer wird gestoppt", intent.site_id)
        t.stop()
    t = TimerJob(intent)
    t.start()

    """Timer"""
    return EndSession()

@app.on_intent("Timerjob:remaining")
async def timer(intent: NluIntent):
    """Verbleibende Zeit"""
    global t
    if t == None:
        return EndSession("Kein Teimer vorhanden")
    else:
        return EndSession(t.timeRemaining())

@app.on_intent("Timerjob:stop")
async def timer(intent: NluIntent):
    """stop Timer"""
    global t
    if t == None:
        return EndSession("Kein Teimer vorhanden")
    else:
        return EndSession(t.stop())

if __name__ == "__main__":
    mqtt_broker_host = "192.168.28.43" # base station -- needed to play sound on satellite
    mqtt_broker_port = 1883

    # MQTT-Client erstellen und verbinden
    client = mqtt.Client()
    client.connect(mqtt_broker_host, mqtt_broker_port)

    ## Load soundfile
    with open("timersound.wav", "rb") as f:
        soundfile = f.read()

    t = None
    app.run()

