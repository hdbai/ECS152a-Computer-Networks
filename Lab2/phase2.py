import random
import math


# Negatively distritibuted stuff...
def nedTime(rate):
    u = random.random()
    return round(((-1 / rate) * math.log(1 - u)), 2)


# generate the backoff time
def backOff(T, n):
    u = random.random()
    return round(T * u, 2)


# generate a negativley distributed random variable with average of 772 (1544/2)
def genFrameLen():
    while True:
        u = random.expovariate(1.0 / 772.0)
        if u < 1544:
            return round(u)


# Event Class
class Event():
    def __init__(self, event_time, event_type, frame_len, b_count):  # event_n_event, event_p_event):
        self.time = event_time
        self.type = event_type  # 0 indicates arrival, 1 departure
        self.subType = 0 #0 for genesis, 1 for data, 2 for ack or 0 for check, 1 for nocheck
        self.frame_len = frame_len  # service time of the event
        self.b_count = b_count  # amount of times it has backed off
        self.src = 0
        self.dest = 0

    def newEvent(self,type,src,time):
        self.type = type
        self.src = src
        self.dest = random.randint(0,9)
        while(self.src == self.dest):
            self.dest = random.randint(0,9)
        if self.type == 0:
             self.time = time + nedTime(1)
        elif self.type == 1:
             self.time = time + nedTime(1)
        elif self.type == 2:
            self.time = time + 0.01
        elif self.type == 3:
            self.time = time
        else:
            raise Exception('ERROR')
        return self


# Host Class
class Host():
    def __init__(self):
        self.gel = []
        self.b_time = 0
        self.dropped = 0
        self.N = 0 # FOR backoff
        self.backoff = 0 # backoff counter
        self.tTime = 0 # transimission time
        self.qTime = 0 # queueing time

        # b_count = 0 #amount of times we have backed off

        # def genTransEvent(cur_time, lambda):

        # proccess the hosts list events
        # def procHostEvent(hosts, cur_time, busy_time):
        #     #find host with most current event
        #     hosts.sort(key = lambda x: x.gel[0].event_time)
        #     #if (cur_time > busy_time)
        #     if cur_time > busy_time:
        #         #begin transmission
        #         #pop Event of GEL
        #         event = hosts[0].gel.pop(0)
        # set cur_time & busy_time

        # else
        # update backoff and attempt to transmit later


def do_everything(lam, n_hosts, T):
    # throughput analysis
    total_bytes = 0
    total_time = 0

    # network Delay
    total_frames = 0
    total_delays = 0

    totalDelay = 0
    averageDelay = 0

    t = T  # <-----------------------------------------------VARAIBLE

    hostCount = n_hosts  # <--------------------------------VARIABLE
    a_rate = lam  # <-----------------------------------------VARAIBLE
    totalTransmitted = 0

    hostBuffer = []  # will be use to store all 10 hosts
    cur_time = 0  # UNITS ms
    busy_time = 0  # UNITS ms

    length = 0  # queue length

    SIFS = 0.05  # 0.05 msec
    DIFS = 0.1  # 0.1 msec
    SENSE = 0.00001  # 0.01 msec
    FRAMESIZE = 64
    CHANNELCAP = 11  # 11MB channel transtmission
    MAXFRAMELENGTH = 1544  # data frame length

    # create each host using for loop
    for i in range(hostCount):  # we making 10 hosts first part
        new_host = Host()
        hostBuffer.append(new_host)  # and we stored it inside the hostBuffer, which contains all 10 hosts

    # create initial arrival event
    for host in hostBuffer:
        new_event = Event(nedTime(a_rate), 0, genFrameLen(), 0)
        host.gel.append(new_event)
        # print(new_event.time)

    # DO THE SHIT -----------------------------------------------------*****
    for i in range(10000):
        # print(len(hostBuffer))
        # print(len(hostBuffer[0].gel))
        hostBuffer.sort(key=lambda x: x.gel[0].time)
        # print hostBuffer[1].b_time
        idle = cur_time >= busy_time
        # get our first event
        cur_event = hostBuffer[0].gel.pop(0)
        f_len = cur_event.frame_len
        b_count = cur_event.b_count

        # set the current time
        cur_time = cur_event.time

        # Process the event!!! -----------------------------------------------
        # WAIT FOR DIFS
        if cur_event.type == 0:
            if idle:  # wait for
                new_event = Event(cur_time + DIFS, 1, f_len, b_count)
            else:  # backoff
                new_event = Event(cur_time + backOff(t, b_count), 0, f_len, b_count + 1)
            # insert back into hostBuffer
            hostBuffer[0].gel.append(new_event)

            # BEGIN TANSMISSION
        elif cur_event.type == 1:
            if idle:  # transmit  #transmission delay             #SSIFS
                total_bytes = f_len + total_bytes + 64  # update total_bytes
                total_frames = total_frames + 1
                # print(cur_time)
                # print(b_count)
                trans_time = round((f_len * 8) / (11 * 10 ** 6), 2) + SIFS + round((FRAMESIZE * 8) / (11 * 10 ** 6), 2)
                # we are now transmitting -> set busy until we finish
                busy_time = cur_time + trans_time
                # create a new event
                new_event = Event(cur_time + nedTime(a_rate), 0, genFrameLen(), b_count)
            else:  # backoff
                new_event = Event(cur_time + backOff(t, b_count), 0, f_len, b_count + 1)
            hostBuffer[0].gel.append(new_event)

    total_time = cur_time
    print("analysis Stuff")
    print(total_bytes)
    print(total_time)
    print(total_bytes / total_time)
    print(total_frames)


def main():
    do_everything(.1, 10, 10)
    do_everything(.9, 10, 10)


main()