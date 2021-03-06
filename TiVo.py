""" 
   Author: Originally Surendra Kane
   Edited by: shrocky2
  Script to control your TiVo using a Amazon Echo.
  This script originally was used to control the gpio ports on the raspberry pi, so you will see remnants of that code. 
"""

import fauxmo
import logging
import time
#Telnet Added Information
import getpass
import sys
import telnetlib
#End Telnet Added Information

from debounce_handler import debounce_handler

logging.basicConfig(level=logging.DEBUG)

print " Control+C to exit program"
#Edit this section to personalize your TV Channels. The channel number is listed after each station.
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
gpio_ports = {'TiVo Pause':10000,
              'A.B.C.':6.1,
              'N.B.C.':10.1,
              'C.B.S.':3.1,
              'Fox':47.1,
              'Comedy Central':754,
              'T.B.S.':767,
              'HGTV':762,
              'ESPN':800,
              'The CW':787,
              'A and E':795,
              'Cartoon Network':872}
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------


class device_handler(debounce_handler):
    """Triggers on/off based on 'device' selected.
       Publishes the IP address of the Echo making the request.
    """
    TRIGGERS = {"TiVo Pause":50001,
                "A.B.C.":50002,
                "N.B.C.":50003,
                "C.B.S.":50004,
                "Fox":50005,
                "Comedy Central":50006,
                "T.B.S.":50007,
                "HGTV":50008,
                "ESPN":50009,
                "The CW":50010,
                "A and E":50011,
                "Cartoon Network":50012}

    def trigger(self,port,state):
      TiVo_IP_Address = "192.168.0.47"
      print 'port:',  port,  "   state:", state
      if state == True: #If the ON command is given, it will run this code
        if port < 10000: #Numbers Less Than 10000 are channels, numbers above 10000 are Services like Netflix
                try:
                        tn = telnetlib.Telnet(TiVo_IP_Address, "31339")
                        tn.write('SETCH '+ str(port).replace("."," ") + '\r')
                        tn.close()
                        print "Channel Changed to", port
                except:
                        print "Telnet Error, Check TiVo IP Address"
                print " "
        else:
                if port == 10000: #TiVo Paused
                        try:
                         tn = telnetlib.Telnet(TiVo_IP_Address, "31339")
                         tn.write("IRCODE PAUSE\r")
                         tn.close()
                         print "TiVo Paused"
                        except:
                         print "Telnet Error, Check TiVo IP Address"

                          
                if port == 10001: #Netflix
                        try:
                         tn = telnetlib.Telnet(TiVo_IP_Address, "31339")
                         tn.write("IRCODE TIVO\r")
                         time.sleep(.4)
                         tn.write("IRCODE DOWN\r")
                         time.sleep(.4)
                         tn.write("IRCODE DOWN\r")
                         time.sleep(.4)
                         tn.write("IRCODE RIGHT\r")
                         time.sleep(1)
                         tn.write("IRCODE SELECT\r")
                         tn.close()
                         print "TiVo App Netflix is Starting"
                        except:
                         print "Telnet Error, Check TiVo IP Address"

                if port == 10002: #Hulu
                        print "Hulu Code Needed"
                if port == 10003: #YouTube
                        try:
                         tn = telnetlib.Telnet(TiVo_IP_Address, "31339")
                         tn.write("IRCODE TIVO\r")
                         time.sleep(.4)
                         tn.write("IRCODE DOWN\r")
                         time.sleep(.4)
                         tn.write("IRCODE DOWN\r")
                         time.sleep(1)
                         tn.write("IRCODE RIGHT\r")
                         time.sleep(1)
                         tn.write("IRCODE DOWN\r")
                         time.sleep(.4)
                         tn.write("IRCODE DOWN\r")
                         time.sleep(.4)
                         tn.write("IRCODE DOWN\r")
                         time.sleep(.4)
                         tn.write("IRCODE SELECT\r")
                         tn.close()
                         print "TiVo App YouTube is Starting"
                        except:
                         print "Telnet Error, Check TiVo IP Address"
                print " "
               
      else: #If the OFF command is given, it will run this code
        if port == 10001 or port == 10002 or port == 10003: #Netflix, Hulu, or YoutTube OFF command is given
                try:
                        tn = telnetlib.Telnet(TiVo_IP_Address, "31339")
                        tn.write("IRCODE LIVETV\r")
                        tn.close()
                        print "TiVo LiveTv Button Pressed"
                except:
                        print "Telnet Error, Check TiVo IP Address"
        print " "


    def act(self, client_address, state, name):
        print "State", state, "on", name, "from client @", client_address, "port:",gpio_ports[str(name)]
        self.trigger(gpio_ports[str(name)],state)
        return True

if __name__ == "__main__":
    # Startup the fauxmo server
    fauxmo.DEBUG = True
    p = fauxmo.poller()
    u = fauxmo.upnp_broadcast_responder()
    u.init_socket()
    p.add(u)

    # Register the device callback as a fauxmo handler
    d = device_handler()
    for trig, port in d.TRIGGERS.items():
        fauxmo.fauxmo(trig, u, p, None, port, d)

    # Loop and poll for incoming Echo requests
    logging.debug("Entering fauxmo polling loop")
    print " "
    while True:
        try:
            # Allow time for a ctrl-c to stop the process
            p.poll(100)
            time.sleep(0.1)
        except Exception, e:
            logging.critical("Critical exception: " + str(e))
            break
