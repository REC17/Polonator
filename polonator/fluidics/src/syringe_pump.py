"""
--------------------------------------------------------------------------------
 Author: Richard Terry.
 Date: February 12, 2008.
 Modified by: Mirko Palla
 Date: March 5, 2008.

 For: G.007 polony sequencer design [fluidics software] at the Church Lab - 
 Genetics Department, Harvard Medical School.
 
 Purpose: This program contains the complete code for class Syringe_pump, 
 containing Cavro XCalibur syringe pump communication subroutines in Python.

 This software may be used, modified, and distributed freely, but this
 header may not be modified and must appear at the top of this file. 
------------------------------------------------------------------------------- 
"""
import logging

log=logging.getLogger("syr_pump")


class Syringe_pump:

    global serport

    def __init__(self, config, serial_port, mux, logger=None):
        "Initialize Cavro XCalibur syringe pump object with default parameters."

        #- Serial configuration --

        self._baud_rate = int(config.get("communication","syringe_pump_baud"))
        self._read_length = int(config.get("communication","read_length"))
        self._sleep_time = float(config.get("communication","sleep_time"))

        self.serport = serial_port        
        self.mux = mux
        self.state = 'syringe pump initialized'
        #self.initialize_syringe()

        #log.debug("---\t-\t--> SP: Syringe pump object constructed")


    """
    Added by Greg Porreca 01-23-2009

    Call this function to pull an arbitraty volume with the syringe; if the
    volume specified is greater than the syringe volume, this iteratively
    does full strokes then pulls the remainder
    waste port is assumed to be port 3 unless specified
    """
    def draw(self, volume, flowcell, draw_speed, return_speed, waste_port=3):
        # volume of syringe full stroke
        syringe_volume = 1000
        
        # initialize i so remainder calculation works even if we
        # don't enter the for: loop
        i = -1

        # set the mux to the syringe pump hardware
        self.mux.setToDevice('SP')

        # iterate over the total volume to pull; if it is more than the
        # syringe barrel volume, do multiple full-stroke pulls
        for i in range(0, int(volume / syringe_volume)):
            self.draw_simple(syringe_volume, flowcell, draw_speed, \
                return_speed, waste_port)

        # pull the remainder
        self.draw_simple(int(volume - ((i+1)*syringe_volume)), flowcell, \
            draw_speed, return_speed, waste_port)



    # Call this function to pull a volume <= the syringe volume
    def draw_simple(self, volume, flowcell, draw_speed, return_speed, \
        waste_port=3):

        self.set_valve_position(flowcell + 1)
        self.set_speed(draw_speed)
        self.set_absolute_volume(volume)

        if(flowcell == 0):
            self.set_valve_position_CCW(waste_port)
        else:
            self.set_valve_position(waste_port)
        self.set_speed(return_speed)
        self.set_absolute_volume(0)


    """
    Cavro XCalibur syringe pump 
    FUNCTIONS
    Performs low-level functional commands (e.g. set pump flow rate, draw 
    volume, etc). 
    Each command implemented here must know the command set of the hardware 
    being controlled, but does not need to know how to communicate with the 
    device (how to poll it, etc). Each functional command will block until 
    execution is complete.

    BASIC SETTINGS
    """
    def initialize_syringe(self):    
        """
        Initializes syringe pump with default operation settings.
        """
                     
        log.debug("---\t-\t--> SP: initialize syringe pump")
        self.serport.set_baud(self._baud_rate)

        # Initialize syringe dead volume
        self.serport.write_serial('/1k5R\r')
        self.serport.read_serial(3)

        find_string = chr(96)
        response_string_size = 4
        self.serport.parse_read_string('/1QR\r', find_string, \
            response_string_size)

        # Initialize move to zero position, full dispense, full force
        self.serport.write_serial('/1Z0,4,3R\r')
        self.serport.read_serial(3)

        find_string = chr(96)
        response_string_size = 4
        self.serport.parse_read_string('/1QR\r', find_string, \
            response_string_size)

        # Initialize speed, range is 0-40, the maximum speed is 0 
        # (1.25 strokes/second)
        self.serport.write_serial('/1S20R\r')
        self.serport.read_serial(3)

        find_string = chr(96)
        response_string_size = 4
        self.serport.parse_read_string('/1QR\r', find_string, \
            response_string_size)

        # log.debug("---\t-\t--> SP: initialized syringe pump object")

    def set_valve_position(self, valve_position):
        "Sets to given syringe pump valve position, an integer"
                     
        # log.info("---\t-\t--> SP: set syringe pump valve position to %i" % \
        #    valve_position)
        self.serport.set_baud(self._baud_rate)

        self.serport.write_serial('/1I' + str(valve_position) + 'R\r')
        response = self.serport.read_serial(3)
        # log.info("---\t-\t--> SP: received <%d> <%d> <%d>" % \
        #   (ord(response[0]), ord(response[1]), ord(response[2])))

        find_string = chr(96)
        response_string_size = 4
        response = self.serport.parse_read_string('/1QR\r', find_string, \
            response_string_size)
        # log.info("---\t-\t--> SP: received <%d> <%d> <%d> <%d>" % \
        #    (ord(response[0]), ord(response[1]), ord(response[2]), \
        #       ord(response[3])))


    def set_valve_position_CCW(self, valve_position):
        "Sets to given syringe pump valve position, an integer"

        # log.info("---\t-\t--> SP: set syringe pump valve position CCW to %i"\
        #     % valve_position)
        self.serport.set_baud(self._baud_rate)

        self.serport.write_serial('/1O' + str(valve_position) + 'R\r')
        response = self.serport.read_serial(3)
        #log.info("---\t-\t--> SP: received <%d> <%d> <%d>" % \
        #   (ord(response[0]), ord(response[1]), ord(response[2])))

        find_string = chr(96)
        response_string_size = 4
        response = self.serport.parse_read_string('/1QR\r', find_string, \
            response_string_size)
        #log.info("---\t-\t--> SP: received <%d> <%d> <%d> <%d>" % \
        #    (ord(response[0]), ord(response[1]), ord(response[2]), \
        #       ord(response[3])))

        
        #log.debug("---\t-\t--> Set syringe pump valve position to %i" % \
        #    valve_position)

    def set_speed(self, speed):
        """
        Sets syringe pump move speed (an integer) in range of 0-40, where the
        maximum speed is 0 equivalent to 1.25 strokes/second = 1250 ul/s.
        """

        #log.debug("---\t-\t--> SP: set syringe pump speed to %i" % speed)
        self.serport.set_baud(self._baud_rate)

        self.serport.write_serial('/1S' + str(speed) + 'R\r')
        self.serport.read_serial(3)

        find_string = chr(96)
        response_string_size = 4
        self.serport.parse_read_string('/1QR\r', find_string, \
            response_string_size)


    def set_absolute_volume(self, absolute_volume):
        """
        Sets syringe pump absolute volume (an integer) in ragne of 0-1000, 
        where 0 is the syringe initial position and the maximum filling volume \
        is the stroke of the syringe (1000 ul).
        """

        #log.debug("---\t-\t--> SP: set syringe pump absolute volume to %i" % \
        #   absolute_volume)
        self.serport.set_baud(self._baud_rate)

        # Increments = (pump resolution * volume ul) / (syringe size ml * ul/ml)
        absolute_steps = (3000 * absolute_volume) / (1 * 1000)

        # 'P' command for relative pick-up, 'A' for absolute position 
        self.serport.write_serial('/1A' + str(absolute_steps) + 'R\r')
        self.serport.read_serial(3)

        find_string = chr(96)
        response_string_size = 4
        self.serport.parse_read_string('/1QR\r', find_string, \
            response_string_size)


