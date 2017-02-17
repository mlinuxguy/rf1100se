#!/usr/bin/python
# Markham Thomas   Jan 22, 2017
# Python support for TI CC1101   433mhz (RF1101SE transceiver)
#  and   support for RF1100SE with 315/433/868/915 mhz
#
#  Many of the cheap cc1101 modules available online only work at 433mhz due to missing resistors
#  on the board, make sure if you want frequencies other than 433Mhz they state it supports them 
#
# device: Wireless RF Transceiver Module 433Mhz CC1101 RF1101SE matched with Antenna
# wiring diagram is in rfconstants.py
# notes: the RF1101SE appears to work in:
#    spi.mode zero
#    cshigh = False
#    lsbfirst = False   (msb is first)
#    4-wire mode (SO SI not shared)
#	 bits_per_word = 8
# notes:  xfer  (CS will be released and reactivated between blocks)
#         xfer2 (CS held active between blocks)
#		readbytes - read(len)
#		writebytes - write([values])
import time
import sys
import spidev
import binascii
import wiringpi2 as wiringpi		# Odroid-c1, using wiring PI to read GDO2 for chip ready
#import wiringpi as wiringpi		# raspberry PI
from rfconstants import *

DEBUG = False

TXCOUNTER = 50			# sometimes it appears to miss the STX strobe so retry
RXCOUNTER = 50			#  "" for SRX
IDLE_COUNTER = 50		# 
SYNCWORD = 0xEEEE		# test sync word
MYADDRESS  = 0x02		# device address
DEVICECHAN = 0x01		# device channel

# set maximum packet size for variable length packets, since CRC autoflush enabled
# it must be set to 61 
MAXIMUM_PACKET_SIZE = 61

GDO2_PIN = 6			# using pin22 or wiringPi 6 for GDO2 chip ready

def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj]

# print byte array in human readable format (hex)
def BytesToHex(Bytes):
	return ''.join(["0x%02X " % x for x in Bytes]).strip()

# This setup on the Odroid-C1 reads proper reset register values on the TI chip
def setup_spi():
	spi = spidev.SpiDev()
	spi.open(0,0)
#	spi.max_speed_hz=5000000		# defaults or these work fine
#	spi.cshigh = False
#	spi.lsbfirst = False
#	spi.bits_per_word = 8
	return(spi)

# uses the default setting for gd02 as chip ready (0 when ready)
def wait_chip_ready():
	b = 1
	while (b):
		b = wiringpi.digitalRead(6)
#		print "Pin: ",b

def reset_cc1100(spi):
	a = spi.xfer([rf_cc1100_cmd_strobe['SRES']]) # reset chip
	wait_chip_ready()
	a = spi.xfer([rf_cc1100_cmd_strobe['SIDLE']]) # idle chip
	wait_chip_ready()
	a = spi.xfer([rf_cc1100_cmd_strobe['SFTX']]) # flush TX FIFO
	wait_chip_ready()
	a = spi.xfer([rf_cc1100_cmd_strobe['SFRX']]) # flush RX FIFO
	wait_chip_ready()
	a = spi.xfer([rf_cc1100_cmd_strobe['SRX']]) # enable RX
	wait_chip_ready()

# dump specified TI registers
def dump_ti_reg(spi,reglist):
	print "Dumping TI register values for: ", namestr(reglist, globals())
	for item in reglist:
		y = reglist[item] | rf_cc1100_rw_type['READ_SINGLE_BYTE']
		a = spi.xfer([y,0])[1:]
		print '\t',item,'= ' ,  format(a[0], '#04x')

def test_reg(spi):		# testing various options
	a = spi.xfer([rf_config_reg['TEST1'],0x35])
	a = spi.xfer([rf_config_reg['TEST1']|rf_cc1100_rw_type['READ_SINGLE_BYTE'],0])
	print "returned", hex(a[1])

def setup_config_register(spi,reglist):
	if DEBUG:
		print "updating config register for: ", namestr(reglist, globals())
	for item in reglist:
		y = rf_config_reg[item] | rf_cc1100_rw_type['WRITE_SINGLE_BYTE']
		wait_chip_ready()
		a = spi.xfer2([y,reglist[item]])
		if DEBUG:
			print '\t', item, '=', format(reglist[item], '#04x')

def bytes_in_rx(spi):
	y = rf_cc1100_status_reg['RXBYTES'] | rf_cc1100_rw_type['READ_SINGLE_BYTE']
	wait_chip_ready()
	a = spi.xfer([y,0])[1]
	return a

# ask for IDLE state and wait for it to enter that state
def idle(spi):
	if DEBUG:
		print "entering idle mode"
	count = 0
	wait_chip_ready()
	a = spi.xfer([rf_cc1100_cmd_strobe['SIDLE']])
	marcstate = 0xFF
	marc_reg = rf_cc1100_status_reg['MARCSTATE'] | rf_cc1100_rw_type['READ_SINGLE_BYTE']
	while (marcstate != 0x01):
		wait_chip_ready()
		marcstate = spi.xfer2([marc_reg,0])[1] & 0x1f
		count += 1
		if (count > IDLE_COUNTER):
			count = 0
			a = spi.xfer([rf_cc1100_cmd_strobe['SIDLE']])	# try to restart IDLE mode

def get_chip_info(spi):
	y = rf_cc1100_status_reg['PARTNUM'] | rf_cc1100_rw_type['READ_SINGLE_BYTE']
	partnumber = spi.xfer([y,0])[1]
	y = rf_cc1100_status_reg['VERSION'] | rf_cc1100_rw_type['READ_SINGLE_BYTE']
	chipversion = spi.xfer([y,0])[1]
	return partnumber, chipversion

# return main radio control state machine state
def get_marcstate(spi):
	marc_reg = rf_cc1100_status_reg['MARCSTATE'] | rf_cc1100_rw_type['READ_SINGLE_BYTE']
	marcstate = spi.xfer([marc_reg,0])[1] & 0x1f
	return marcstate

# used in packet (if enabled) to sync 
def set_syncword(spi,syncw):
	y = rf_config_reg['SYNC1'] | rf_cc1100_rw_type['WRITE_SINGLE_BYTE']
	b = (syncw & 0xff00)		# sync1 is high byte
	b = b >> 8
	spi.xfer2([y,b]) 
	y = rf_config_reg['SYNC0'] | rf_cc1100_rw_type['WRITE_SINGLE_BYTE']
	b = (syncw & 0x00ff)		# sync0 is low byte
	spi.xfer2([y,b]) 

# for fixed packet length, must be non-zero, if variable len then max packet size
def set_packet_length(spi, pkt_len):
	y = rf_config_reg['PKTLEN'] | rf_cc1100_rw_type['WRITE_SINGLE_BYTE']
	spi.xfer2([y,pkt_len]) 

# where pkt_ctrl1 = 7:5 preamble qual, 4 na, 3 autoflush, 2 append status, 1:0 addr check
# addr check 3 (11) is check address and 0 and 0xff (broadcasts)
# 0000 1111 = no preamble, enable flush if crc no match, status bytes appended, addr + broadcast
def set_packet_ctrl1(spi, pkt_ctrl1):
	y = rf_config_reg['PKTCTRL1'] | rf_cc1100_rw_type['WRITE_SINGLE_BYTE']
	spi.xfer2([y,pkt_ctrl1]) 

# where pkt_ctrl0 = 6 white data, 5:4 format of tx/rx, 2 (if 1 crc), 1:0 packet len
# 0100 0100 = white, fifo normal for tx/rx, crc, fixed packet len
# 0100 0101 = white, fifo normal for tx/rx, crc, variable packet len (len follows sync byte)
def set_packet_ctrl0(spi, pkt_ctrl2):
	y = rf_config_reg['PKTCTRL0'] | rf_cc1100_rw_type['WRITE_SINGLE_BYTE']
	spi.xfer2([y,pkt_ctrl2]) 

# switch cc1101 into receive mode
def receive(spi):
	idle(spi)
	count = 0
	wait_chip_ready()
	a = spi.xfer([rf_cc1100_cmd_strobe['SRX']])
	marcstate = 0xFF
	marc_reg = rf_cc1100_status_reg['MARCSTATE'] | rf_cc1100_rw_type['READ_SINGLE_BYTE']
	while (marcstate != 0x0D):
		wait_chip_ready()
		marcstate = spi.xfer2([marc_reg,0])[1] & 0x1f
		count += 1
		if (count > RXCOUNTER):
			count = 0
			a = spi.xfer([rf_cc1100_cmd_strobe['SRX']])	# try to restart RX mode

# load tx fifo register, with data packet prior to telling cc1100 to send it
# in variable packet len mode, packet length is defined as: payload data excluding len byte and CRC
def load_tx(spi,buff,length):
#	y = rf_cc1100_fifo['TXFIFO_BURST'] | rf_cc1100_rw_type['WRITE_BURST']
	y = rf_cc1100_fifo['TXFIFO_SINGLE_BYTE'] | rf_cc1100_rw_type['WRITE_SINGLE_BYTE']
	for x in range(length+1):		# ensure get last byte
		wait_chip_ready()
		spi.xfer2([y,buff[x]]) 
	
# switch cc1101 into transmit mode, need TX buffer loaded first
def transmit(spi):
	idle(spi)
	count = 0		
	wait_chip_ready()
	a = spi.xfer([rf_cc1100_cmd_strobe['STX']])
	marcstate = 0xFF
	marc_reg = rf_cc1100_status_reg['MARCSTATE'] | rf_cc1100_rw_type['READ_SINGLE_BYTE']
	while (marcstate != 0x13):
		wait_chip_ready()
		marcstate = spi.xfer2([marc_reg,0])[1] & 0x1f  
		count += 1
		if (count > TXCOUNTER):
			count = 0
			a = spi.xfer([rf_cc1100_cmd_strobe['STX']])	# try to restart TX mode

# this checks the received signal strenth register versus what is appended to a packet
def check_rssi(spi):
	rssi = rf_cc1100_status_reg['RSSI'] | rf_cc1100_rw_type['READ_SINGLE_BYTE']
	a = spi.xfer([rssi,0])[1]
	if (a >= 128):
		rssi_dbm = (a -256)/2 - 74
	elif (a < 128):
		rssi_dbm = (a/2) - 74
	return rssi_dbm

# current GD0x status and packet status
# bit 7 = CRC OK, 6 = carrier sense, 5 preamble qual reached, 4 = channel is clear
# 3 = start of frame delim, 2 = GDO2, 1=n/a, 0 = GDO0
def check_packet_status(spi):
	pkt_stat = rf_cc1100_status_reg['PKTSTATUS'] | rf_cc1100_rw_type['READ_SINGLE_BYTE']
	a = spi.xfer([pkt_stat,0])[1]
	return a

# displays AGC register values, cross-ref to CC1100 manual
def read_agc_control(spi):
	y = rf_config_reg['AGCCTRL0'] | rf_cc1100_rw_type['READ_SINGLE_BYTE']
	a = spi.xfer([y,0])[1]
	print "AGCCTRL0: ", hex(a)
	y = rf_config_reg['AGCCTRL1'] | rf_cc1100_rw_type['READ_SINGLE_BYTE']
	a = spi.xfer([y,0])[1]
	print "AGCCTRL1: ", hex(a)
	y = rf_config_reg['AGCCTRL2'] | rf_cc1100_rw_type['READ_SINGLE_BYTE']
	a = spi.xfer([y,0])[1]
	print "AGCCTRL2: ", hex(a)
	y = rf_config_reg['AGCCTRL2'] | rf_cc1100_rw_type['WRITE_SINGLE_BYTE']
	a = spi.xfer([y,0x38])

# sets device address (used for filtration) and channel
def device_address_and_channel(spi,addr,chan):  # 1-254, or 0 and 255 for broadcast
	y = rf_config_reg['ADDR'] | rf_cc1100_rw_type['WRITE_SINGLE_BYTE']
	a = spi.xfer2([y,addr]) 
	y = rf_config_reg['CHANNR'] | rf_cc1100_rw_type['WRITE_SINGLE_BYTE']
	a = spi.xfer2([y,chan]) 

def disable_pre_sync(spi):	# disable preamble and sync detection
	y = rf_config_reg['MDMCFG2'] | rf_cc1100_rw_type['READ_SINGLE_BYTE']
	a = spi.xfer([y,0])[1]
	y = rf_config_reg['MDMCFG2'] | rf_cc1100_rw_type['WRITE_SINGLE_BYTE']
	a = (a & 0b11111000) 
	a = spi.xfer2([y,a]) 

# if any bytes in RX FIFO this will return them
def read_rx_fifo(spi):
	data = []
	b = bytes_in_rx(spi)
	if (b != 0):
		y = rf_cc1100_fifo['RXFIFO_SINGLE_BYTE'] | rf_cc1100_rw_type['READ_SINGLE_BYTE']
		for x in xrange(0, b):
			wait_chip_ready()
			a = spi.xfer2([y,0])[1]
			data.append(a)
		return data
	else:
		return []

# Varible packet length test read loop
# designed for appended RSSI and LQI to packet
def read_loop(spi):
	while True:
		rssi = check_rssi(rfspi)
		receive(rfspi)
		data = read_rx_fifo(rfspi)
		if (data):
			hexdata = BytesToHex(data)
			a = data[-2]				# get RSSI from status bytes
			if (a >= 128):
				rssi_dbm = (a-256)/2 - 74
				print "rssi dbm: ", rssi_dbm
			elif (a < 128):
				rssi_dbm = (a/2) - 74
				print "rssi dbm: ", rssi_dbm
			lqi = data[-1] & 0x7f		# strip off CRC bit (1=good CRC)
			print "LQI: ", lqi			# lower value indicates better link quality
			print hexdata				# dump of packet 
			print map(chr, data[0:-2])	# string data sent, cut off status bytes
			print
		p_stat = check_packet_status(rfspi)
		time.sleep(1)	

# Varible packet length test transmit loop with optional address byte
def transmit_loop(spi, myaddr):
	count = 0
	print "Starting beacon transmitting loop"
	while True:
		alist = bytearray([])
		count = count + 1
#		msg = 'hello world ' + str(count)
		msg = str(count)	# doing a beacon counter
		strlen = len(msg) 
		strlen += 1						# str size includes address byte, but not strlen
		alist = bytearray(msg)
		alist.insert(0,chr(strlen))		# load length of string
		alist.insert(1,chr(myaddr))
		load_tx(spi,alist,strlen)
		transmit(rfspi)
		time.sleep(5)

# dump a few ti registers
def dump_regs(spi):
	dump_ti_reg(rfspi,rf_config_reg)
	dump_ti_reg(rfspi,rf_cc1100_misc)
	dump_ti_reg(rfspi,rf_cc1100_status_reg)

wiringpi.wiringPiSetup()
wiringpi.pinMode(GDO2_PIN,0)	# chip ready 1=not ready, 0=ready
rfspi = setup_spi()
reset_cc1100(rfspi)
a = get_chip_info(rfspi)
print "chip info: ", a
setup_config_register(rfspi,rf_msk_433_250k)
#setup_config_register(rfspi,rf_fsk2_433_2_4k)
device_address_and_channel(rfspi,MYADDRESS,DEVICECHAN)
#set_syncword(rfspi,SYNCWORD)	# setting this breaks transmission/reception
set_packet_length(rfspi, MAXIMUM_PACKET_SIZE)
set_packet_ctrl1(rfspi, 0x07)		# append 2 status bytes (RSSI+LQI), addr+broad
set_packet_ctrl0(rfspi, 0x45)		# variable packet length
#disable_pre_sync(rfspi)
#read_loop(rfspi)
transmit_loop(rfspi,MYADDRESS)
#dump_regs(rfspi)
