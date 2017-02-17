# Markham Thomas  Jan 22, 2017
#
# Odroid c1 (or RPI) wiring TO RF1100se (CC1100 TI chip) 7-wires total
# pin1  (3.3v) <--> VDD, pin6  (gnd)  <--> GND
# pin19 (mosi) <--> SI,  pin21 (miso) <--> SO
# pin24 (ceo)  <--> CSN, pin23 (SCLK) <--> SCK
# pin22 (wpi6) <--> GDO2      This is used to detect chip ready
#
# defines constants used by rf110se.py
# NOTES:  the green PCB boards listed as 'CC1101 RF1101SE'
#         are only capable of using the 433mhz frequencies
#         There are blue PCB boards listed as CC1101 that
#         support 315/433/868/915mhz frequencies

class Bunch(dict):
    def __init__(self, d = {}):
        dict.__init__(self, d)
        self.__dict__.update(d)
    def __setattr__(self, name, value):
        dict.__setitem__(self, name, value)
        object.__setattr__(self, name, value)
    def __setitem__(self, name, value):
        dict.__setitem__(self, name, value)
        object.__setattr__(self, name, value)
    def copy(self):
        return Bunch(dict.copy(self))

CONFIGREG = {
	'IOCFG2'  : 0x00         ,	# GDO2 output pin configuration
	'IOCFG1'  : 0x01         ,	# GDO1 output pin configuration
	'IOCFG0'  : 0x02         ,	# GDO0 output pin configuration
	'FIFOTHR' : 0x03         ,	# RX FIFO and TX FIFO thresholds
	'SYNC1'   : 0x04         ,	# Sync word, high byte
	'SYNC0'   : 0x05         ,	# Sync word, low byte
	'PKTLEN'  : 0x06         ,	# Packet length
	'PKTCTRL1': 0x07         ,	# Packet automation control
	'PKTCTRL0': 0x08         ,	# Packet automation control
	'ADDR'    : 0x09         ,	# Device address
	'CHANNR'  : 0x0A         ,	# Channel number
	'FSCTRL1' : 0x0B         ,	# Frequency synthesizer control
	'FSCTRL0' : 0x0C         ,	# Frequency synthesizer control
	'FREQ2'   : 0x0D         ,	# Frequency control word, high byte
	'FREQ1'   : 0x0E         ,	# Frequency control word, middle byte
	'FREQ0'   : 0x0F         ,	# Frequency control word, low byte
	'MDMCFG4' : 0x10         ,	# Modem configuration
	'MDMCFG3' : 0x11         ,	# Modem configuration
	'MDMCFG2' : 0x12         ,	# Modem configuration
	'MDMCFG1' : 0x13         ,	# Modem configuration
	'MDMCFG0' : 0x14         ,	# Modem configuration
	'DEVIATN' : 0x15         ,	# Modem deviation setting
	'MCSM2'   : 0x16         ,	# Main Radio Cntrl State Machine config
	'MCSM1'   : 0x17         ,	# Main Radio Cntrl State Machine config
	'MCSM0'   : 0x18         ,	# Main Radio Cntrl State Machine config
	'FOCCFG'  : 0x19         ,	# Frequency Offset Compensation config
	'BSCFG'   : 0x1A         ,	# Bit Synchronization configuration
	'AGCCTRL2': 0x1B         ,	# AGC control
	'AGCCTRL1': 0x1C         ,	# AGC control
	'AGCCTRL0': 0x1D         ,	# AGC control
	'WOREVT1' : 0x1E         ,	# High byte Event 0 timeout
	'WOREVT0' : 0x1F         ,	# Low byte Event 0 timeout
	'WORCTRL' : 0x20         ,	# Wake On Radio control
	'FREND1'  : 0x21         ,	# Front end RX configuration
	'FREND0'  : 0x22         ,	# Front end TX configuration
	'FSCAL3'  : 0x23         ,	# Frequency synthesizer calibration
	'FSCAL2'  : 0x24         ,	# Frequency synthesizer calibration
	'FSCAL1'  : 0x25         ,	# Frequency synthesizer calibration
	'FSCAL0'  : 0x26         ,	# Frequency synthesizer calibration
	'RCCTRL1' : 0x27         ,	# RC oscillator configuration
	'RCCTRL0' : 0x28         ,	# RC oscillator configuration
	'FSTEST'  : 0x29         ,	# Frequency synthesizer cal control
	'PTEST'   : 0x2A         ,	# Production test
	'AGCTEST' : 0x2B         ,	# AGC test
	'TEST2'	  : 0x2C		,
	'TEST1'	  : 0x2D		,
	'TEST0'	  : 0x2E		,}
rf_config_reg = Bunch(CONFIGREG)

CC1100_RW_TYPE = {
	'WRITE_SINGLE_BYTE'	: 0x00,
	'WRITE_BURST'		: 0x40,
	'READ_SINGLE_BYTE' 	: 0x80,
	'READ_BURST'       	: 0xC0,}
rf_cc1100_rw_type = Bunch(CC1100_RW_TYPE)

CC1100_FIFO = {
	'TXFIFO_BURST'			: 0x7F    ,	# write burst only
	'TXFIFO_SINGLE_BYTE'	: 0x3F    ,	# write single only
	'RXFIFO_BURST'			: 0xFF    ,	# read burst only
	'RXFIFO_SINGLE_BYTE'	: 0xBF    ,	# read single only
	'PATABLE_BURST'			: 0x7E    ,	# power control read/write
	'PATABLE_SINGLE_BYTE'	: 0xFE    ,}# power control read/write
rf_cc1100_fifo = Bunch(CC1100_FIFO)

CC1100_MISC = {
	 'CFG_REGISTER'				: 0x2F  ,
	 'FIFOBUFFER'				: 0x42  ,	# size of Fifo Buffer
	 'RSSI_OFFSET_868MHZ'		: 0x4E  ,	# dec : 74
	 'TX_RETRIES_MAX'			: 0x05  ,	# tx_retries_max
	 'CC1100_COMPARE_REGISTER'	: 0x00  ,	# register compare 0:no compare 1:compare
	 'BROADCAST_ADDRESS'		: 0x00  ,	# broadcast address
	 'CC1100_FREQ_315MHZ'		: 0x01  ,
	 'CC1100_FREQ_434MHZ'		: 0x02  ,
	 'CC1100_FREQ_868MHZ'		: 0x03  ,
	 'CC1100_FREQ_915MHZ'		: 0x04  ,}
rf_cc1100_misc = Bunch(CC1100_MISC)

CC1100_CMD_STROBE = {
	 'SRES'		: 0x30          ,	# Reset chip
	 'SFSTXON'	: 0x31          ,	# Enable/calibrate freq synthesizer
	 'SXOFF'	: 0x32          ,	# Turn off crystal oscillator.
	 'SCAL'		: 0x33          ,	# Calibrate freq synthesizer & disable
	 'SRX'		: 0x34          ,	# Enable RX.
	 'STX'		: 0x35          ,	# Enable TX.
	 'SIDLE'	: 0x36          ,	# Exit RX / TX
	 'SAFC'		: 0x37          ,	# AFC adjustment of freq synthesizer
	 'SWOR'		: 0x38          ,	# Start automatic RX polling sequence
	 'SPWD'		: 0x39          ,	# Enter pwr down mode when CSn goes hi
	 'SFRX'		: 0x3A          ,	# Flush the RX FIFO buffer.
	 'SFTX'		: 0x3B          ,	# Flush the TX FIFO buffer.
	 'SWORRST'	: 0x3C          ,	# Reset real time clock.
	 'SNOP'		: 0x3D          ,}	# No operation.
rf_cc1100_cmd_strobe = Bunch(CC1100_CMD_STROBE)

CC1100_STATUS_REG = {
	 'PARTNUM'			: 0xF0	,	# Part number
	 'VERSION'			: 0xF1	,	# Current version number
	 'FREQEST'			: 0xF2	,	# Frequency offset estimate
	 'LQI'				: 0xF3	,	# Demodulator estimate for link quality
	 'RSSI'				: 0xF4	,	# Received signal strength indication
	 'MARCSTATE'		: 0xF5	,	# Control state machine state
	 'WORTIME1'			: 0xF6	,	# High byte of WOR timer
	 'WORTIME0'			: 0xF7	,	# Low byte of WOR timer
	 'PKTSTATUS'		: 0xF8	,	# Current GDOx status and packet status
	 'VCO_VC_DAC'		: 0xF9	,	# Current setting from PLL cal module
	 'TXBYTES'			: 0xFA	,	# Underflow and ,	# of bytes in TXFIFO
	 'RXBYTES'			: 0xFB	,	# Overflow and ,	# of bytes in RXFIFO
	 'RCCTRL1_STATUS'	: 0xFC	,	# Last RC Oscillator Calibration Result
	 'RCCTRL0_STATUS'	: 0xFD	,}	# Last RC Oscillator Calibration Result
rf_cc1100_status_reg = Bunch(CC1100_STATUS_REG)

# NOTE:  modulation format 2-FSK
# Address Config : No address check 
# Base Frequency : 433.999969 
# CRC Autoflush : false 
# CRC Enable : true 
# Carrier Frequency : 433.999969 
# Channel Number : 0 
# Channel Spacing : 199.951172 
# Data Format : Normal mode 
# Data Rate : 2.39897 
# Deviation : 5.157471 
# Device Address : 0 
# Manchester Enable : false 
# Modulated : true 
# Modulation Format : 2-FSK 
# PA Ramping : false 
# Packet Length : 255 
# Packet Length Mode : Variable packet length mode. Packet length configured by the first byte after sync word 
# Preamble Count : 4 
# RX Filter BW : 58.035714 
# Sync Word Qualifier Mode : 30/32 sync word bits detected 
# TX Power : 0 
# Whitening : false 

FSK2_433_2_4k = {
	'IOCFG0'     : 0x06,
	'PKTCTRL0'   : 0x05,
	'FSCTRL1'    : 0x06,
	'FREQ2'      : 0x10,
	'FREQ1'      : 0xB1,
	'FREQ0'      : 0x3B,
	'MDMCFG4'    : 0xF6,
	'MDMCFG3'    : 0x83,
	'MDMCFG2'    : 0x03,
	'DEVIATN'    : 0x15,
	'MCSM0'      : 0x18,
	'FOCCFG'     : 0x16,
	'FSCAL3'     : 0xE9,
	'FSCAL2'     : 0x2A,
	'FSCAL1'     : 0x00,
	'FSCAL0'     : 0x1F,
	'TEST2'      : 0x81,
	'TEST1'      : 0x35,
	'TEST0'      : 0x09, }
rf_fsk2_433_2_4k = Bunch(FSK2_433_2_4k)

# NOTE: GFSK modulation
# Address Config : No address check 
# Base Frequency : 433.999969 
# CRC Autoflush : false 
# CRC Enable : true 
# Carrier Frequency : 433.999969 
# Channel Number : 0 
# Channel Spacing : 199.951172 
# Data Format : Normal mode 
# Data Rate : 2.39897 
# Deviation : 5.157471 
# Device Address : 0 
# Manchester Enable : false 
# Modulated : true 
# Modulation Format : GFSK 
# PA Ramping : false 
# Packet Length : 255 
# Packet Length Mode : Variable packet length mode. Packet length configured by the first byte after sync word 
# Preamble Count : 4 
# RX Filter BW : 58.035714 
# Sync Word Qualifier Mode : 30/32 sync word bits detected 
# TX Power : 0 
# Whitening : false 

GFSK_433_2_4k = {
	 'IOCFG0'     : 0x06,
	 'PKTCTRL0'   : 0x05,
	 'FSCTRL1'    : 0x06,
	 'FREQ2'      : 0x10,
	 'FREQ1'      : 0xB1,
	 'FREQ0'      : 0x3B,
	 'MDMCFG4'    : 0xF6,
	 'MDMCFG3'    : 0x83,
	 'MDMCFG2'    : 0x13,
	 'DEVIATN'    : 0x15,
	 'MCSM0'      : 0x18,
	 'FOCCFG'     : 0x16,
	 'FSCAL3'     : 0xE9,
	 'FSCAL2'     : 0x2A,
	 'FSCAL1'     : 0x00,
	 'FSCAL0'     : 0x1F,
	 'TEST2'      : 0x81,
	 'TEST1'      : 0x35,
	 'TEST0'      : 0x09, }
rf_gfsk_433_2_4k = Bunch(GFSK_433_2_4k)

#NOTE:  modulation is ASK/OOK
# Address Config : No address check 
# Base Frequency : 433.999969 
# CRC Autoflush : false 
# CRC Enable : true 
# Carrier Frequency : 433.999969 
# Channel Number : 0 
# Channel Spacing : 199.951172 
# Data Format : Normal mode 
# Data Rate : 2.39897 
# Deviation : 5.157471 
# Device Address : 0 
# Manchester Enable : false 
# Modulation Format : ASK/OOK 
# PA Ramping : false 
# Packet Length : 255 
# Packet Length Mode : Variable packet length mode. Packet length configured by the first byte after sync word 
# Preamble Count : 4 
# RX Filter BW : 58.035714 
# Sync Word Qualifier Mode : 30/32 sync word bits detected 
# TX Power : 0 
# Whitening : false 

ASKOOK_433_2_4k = {
	'IOCFG0'     : 0x06,
	'PKTCTRL0'   : 0x05,
	'FSCTRL1'	 : 0x06,
	'FREQ2'      : 0x10,
	'FREQ1'      : 0xB1,
	'FREQ0'      : 0x3B,
	'MDMCFG4'    : 0xF6,
	'MDMCFG3'    : 0x83,
	'MDMCFG2'    : 0x33,
	'DEVIATN'    : 0x15,
	'MCSM0'      : 0x18,
	'FOCCFG'     : 0x16,
	'FREND0'     : 0x11,
	'FSCAL3'     : 0xE9,
	'FSCAL2'     : 0x2A,
	'FSCAL1'     : 0x00,
	'FSCAL0'     : 0x1F,
	'TEST2'      : 0x81,
	'TEST1'      : 0x35,
	'TEST0'      : 0x09, }
rf_askook_433_2_4k = Bunch(ASKOOK_433_2_4k)

#NOTE:  modulation MSK
# Address Config : No address check 
# Base Frequency : 433.999969 
# CRC Autoflush : false 
# CRC Enable : true 
# Carrier Frequency : 433.999969 
# Channel Number : 0 
# Channel Spacing : 199.951172 
# Data Format : Normal mode 
# Data Rate : 2.39897 
# Device Address : 0 
# Manchester Enable : false 
# Modulated : true 
# Modulation Format : MSK 
# PA Ramping : false 
# Packet Length : 255 
# Packet Length Mode : Variable packet length mode. Packet length configured by the first byte after sync word 
# Phase Transition Time : 0 
# Preamble Count : 4 
# RX Filter BW : 58.035714 
# Sync Word Qualifier Mode : 30/32 sync word bits detected 
# TX Power : 0 
# Whitening : false 

MSK_433_2_4k = {
	'IOCFG0'     : 0x06,
	'PKTCTRL0'   : 0x05,
	'FSCTRL1'    : 0x06,
	'FREQ2'      : 0x10,
	'FREQ1'      : 0xB1,
	'FREQ0'      : 0x3B,
	'MDMCFG4'    : 0xF6,
	'MDMCFG3'    : 0x83,
	'MDMCFG2'    : 0x73,
	'DEVIATN'    : 0x10,
	'MCSM0'      : 0x18,
	'FOCCFG'     : 0x16,
	'FSCAL3'     : 0xE9,
	'FSCAL2'     : 0x2A,
	'FSCAL1'     : 0x00,
	'FSCAL0'     : 0x1F,
	'TEST2'      : 0x81,
	'TEST1'      : 0x35,
	'TEST0'      : 0x09,}
rf_msk_433_2_4k = Bunch(MSK_433_2_4k)

#NOTE: modulation 2-fsk at 250kbaud
# Address Config : No address check 
# Base Frequency : 433.999969 
# CRC Autoflush : false 
# CRC Enable : true 
# Carrier Frequency : 433.999969 
# Channel Number : 0 
# Channel Spacing : 199.951172 
# Data Format : Normal mode 
# Data Rate : 249.939 
# Deviation : 1.586914 
# Device Address : 0 
# Manchester Enable : false 
# Modulated : true 
# Modulation Format : 2-FSK 
# PA Ramping : false 
# Packet Length : 255 
# Packet Length Mode : Variable packet length mode. Packet length configured by the first byte after sync word 
# Preamble Count : 4 
# RX Filter BW : 541.666667 
# Sync Word Qualifier Mode : 30/32 sync word bits detected 
# TX Power : 0 
# Whitening : false 

FSK2_433_250k = {
	'IOCFG0'     : 0x06,
	'PKTCTRL0'   : 0x05,
	'FSCTRL1'    : 0x0A,
	'FREQ2'      : 0x10,
	'FREQ1'      : 0xB1,
	'FREQ0'      : 0x3B,
	'MDMCFG4'    : 0x2D,
	'MDMCFG3'    : 0x3B,
	'MDMCFG2'    : 0x03,
	'DEVIATN'    : 0x00,
	'MCSM0'      : 0x18,
	'FOCCFG'     : 0x1D,
	'BSCFG'      : 0x1C,
	'AGCCTRL2'   : 0xC7,
	'AGCCTRL1'   : 0x00,
	'AGCCTRL0'   : 0xB0,
	'FREND1'     : 0xB6,
	'FSCAL3'     : 0xEA,
	'FSCAL2'     : 0x2A,
	'FSCAL1'     : 0x00,
	'FSCAL0'     : 0x1F,
	'TEST0'      : 0x09,}
rf_fsk2_433_250k = Bunch(FSK2_433_250k)

#NOTE: modulation GFSK at 250k baud
# Address Config : No address check 
# Base Frequency : 433.999969 
# CRC Autoflush : false 
# CRC Enable : true 
# Carrier Frequency : 433.999969 
# Channel Number : 0 
# Channel Spacing : 199.951172 
# Data Format : Normal mode 
# Data Rate : 249.939 
# Deviation : 1.586914 
# Device Address : 0 
# Manchester Enable : false 
# Modulated : true 
# Modulation Format : GFSK 
# PA Ramping : false 
# Packet Length : 255 
# Packet Length Mode : Variable packet length mode. Packet length configured by the first byte after sync word 
# Preamble Count : 4 
# RX Filter BW : 541.666667 
# Sync Word Qualifier Mode : 30/32 sync word bits detected 
# TX Power : 0 
# Whitening : false 

GFSK_433_250k = {
	'IOCFG0'     : 0x06,
	'PKTCTRL0'   : 0x05,
	'FSCTRL1'    : 0x0A,
	'FREQ2'      : 0x10,
	'FREQ1'      : 0xB1,
	'FREQ0'      : 0x3B,
	'MDMCFG4'    : 0x2D,
	'MDMCFG3'    : 0x3B,
	'MDMCFG2'    : 0x13,
	'DEVIATN'    : 0x00,
	'MCSM0'      : 0x18,
	'FOCCFG'     : 0x1D,
	'BSCFG'      : 0x1C,
	'AGCCTRL2'   : 0xC7,
	'AGCCTRL1'   : 0x00,
	'AGCCTRL0'   : 0xB0,
	'FREND1'     : 0xB6,
	'FSCAL3'     : 0xEA,
	'FSCAL2'     : 0x2A,
	'FSCAL1'     : 0x00,
	'FSCAL0'     : 0x1F,
	'TEST0'      : 0x09,}
rf_gfsk_433_250k = Bunch(GFSK_433_250k)

#NOTE: modulation ASK/OOK at 250k baud
# Address Config : No address check 
# Base Frequency : 433.999969 
# CRC Autoflush : false 
# CRC Enable : true 
# Carrier Frequency : 433.999969 
# Channel Number : 0 
# Channel Spacing : 199.951172 
# Data Format : Normal mode 
# Data Rate : 249.939 
# Deviation : 1.586914 
# Device Address : 0 
# Manchester Enable : false 
# Modulation Format : ASK/OOK 
# PA Ramping : false 
# Packet Length : 255 
# Packet Length Mode : Variable packet length mode. Packet length configured by the first byte after sync word 
# Preamble Count : 4 
# RX Filter BW : 541.666667 
# Sync Word Qualifier Mode : 30/32 sync word bits detected 
# TX Power : 0 
# Whitening : false 

ASKOOK_433_250k = {
	'IOCFG0'     : 0x06,
	'PKTCTRL0'   : 0x05,
	'FSCTRL1'    : 0x0A,
	'FREQ2'      : 0x10,
	'FREQ1'      : 0xB1,
	'FREQ0'      : 0x3B,
	'MDMCFG4'    : 0x2D,
	'MDMCFG3'    : 0x3B,
	'MDMCFG2'    : 0x33,
	'DEVIATN'    : 0x00,
	'MCSM0'      : 0x18,
	'FOCCFG'     : 0x1D,
	'BSCFG'      : 0x1C,
	'AGCCTRL2'   : 0xC7,
	'AGCCTRL1'   : 0x00,
	'AGCCTRL0'   : 0xB0,
	'FREND1'     : 0xB6,
	'FREND0'     : 0x11,
	'FSCAL3'     : 0xEA,
	'FSCAL2'     : 0x2A,
	'FSCAL1'     : 0x00,
	'FSCAL0'     : 0x1F,
	'TEST0'      : 0x09,}
rf_askook_433_250k = Bunch(ASKOOK_433_250k)

#NOTE: modulation is MSK at 250k baud
# Address Config : No address check 
# Base Frequency : 433.999969 
# CRC Autoflush : false 
# CRC Enable : true 
# Carrier Frequency : 433.999969 
# Channel Number : 0 
# Channel Spacing : 199.951172 
# Data Format : Normal mode 
# Data Rate : 249.939 
# Device Address : 0 
# Manchester Enable : false 
# Modulated : true 
# Modulation Format : MSK 
# PA Ramping : false 
# Packet Length : 255 
# Packet Length Mode : Variable packet length mode. Packet length configured by the first byte after sync word 
# Phase Transition Time : 0 
# Preamble Count : 4 
# RX Filter BW : 541.666667 
# Sync Word Qualifier Mode : 30/32 sync word bits detected 
# TX Power : 0 
# Whitening : false 

MSK_433_250k = {
	'IOCFG0'     : 0x06,
	'PKTCTRL0'   : 0x05,
	'FSCTRL1'    : 0x0A,
	'FREQ2'      : 0x10,
	'FREQ1'      : 0xB1,
	'FREQ0'      : 0x3B,
	'MDMCFG4'    : 0x2D,
	'MDMCFG3'    : 0x3B,
	'MDMCFG2'    : 0x73,
	'DEVIATN'    : 0x00,
	'MCSM0'      : 0x18,
	'FOCCFG'     : 0x1D,
	'BSCFG'      : 0x1C,
	'AGCCTRL2'   : 0xC7,
	'AGCCTRL1'   : 0x00,
	'AGCCTRL0'   : 0xB0,
	'FREND1'     : 0xB6,
	'FSCAL3'     : 0xEA,
	'FSCAL2'     : 0x2A,
	'FSCAL1'     : 0x00,
	'FSCAL0'     : 0x1F,
	'TEST0'      : 0x09,}
rf_msk_433_250k = Bunch(MSK_433_250k)

#NOTE: 902 Mhz 2-FSK modulation with 250k baud
# Address Config : No address check 
# Base Frequency : 902.000000 
# CRC Autoflush : false 
# CRC Enable : true 
# Carrier Frequency : 905.999023 
# Channel Number : 20 
# Channel Spacing : 199.951172 
# Data Format : Normal mode 
# Data Rate : 249.939 
# Deviation : 1.586914 
# Device Address : 0 
# Manchester Enable : false 
# Modulated : true 
# Modulation Format : 2-FSK 
# PA Ramping : false 
# Packet Length : 255 
# Packet Length Mode : Variable packet length mode. Packet length configured by the first byte after sync word 
# Preamble Count : 4 
# RX Filter BW : 541.666667 
# Sync Word Qualifier Mode : 30/32 sync word bits detected 
# TX Power : 0 
# Whitening : false 

FSK2_902_250k = {
	'IOCFG0'     : 0x06,
	'PKTCTRL0'   : 0x05,
	'CHANNR'     : 0x14,
	'FSCTRL1'    : 0x0A,
	'FREQ2'      : 0x22,
	'FREQ1'      : 0xB1,
	'FREQ0'      : 0x3B,
	'MDMCFG4'    : 0x2D,
	'MDMCFG3'    : 0x3B,
	'MDMCFG2'    : 0x03,
	'DEVIATN'    : 0x00,
	'MCSM0'      : 0x18,
	'FOCCFG'     : 0x1D,
	'BSCFG'      : 0x1C,
	'AGCCTRL2'   : 0xC7,
	'AGCCTRL1'   : 0x00,
	'AGCCTRL0'   : 0xB0,
	'FREND1'     : 0xB6,
	'FSCAL3'     : 0xEA,
	'FSCAL2'     : 0x2A,
	'FSCAL1'     : 0x00,
	'FSCAL0'     : 0x1F,
	'TEST0'      : 0x09,}
rf_fsk2_902_250k = Bunch(FSK2_902_250k)

#NOTE: 902Mhz GFSK modulation with 250k baud
# Address Config = No address check 
# Base Frequency = 902.000000 
# CRC Autoflush = false 
# CRC Enable = true 
# Carrier Frequency = 905.999023 
# Channel Number = 20 
# Channel Spacing = 199.951172 
# Data Format = Normal mode 
# Data Rate = 249.939 
# Deviation = 1.586914 
# Device Address = 0 
# Manchester Enable = false 
# Modulated = true 
# Modulation Format = GFSK 
# PA Ramping = false 
# Packet Length = 255 
# Packet Length Mode = Variable packet length mode. Packet length configured by the first byte after sync word 
# Preamble Count = 4 
# RX Filter BW = 541.666667 
# Sync Word Qualifier Mode = 30/32 sync word bits detected 
# TX Power = 0 
# Whitening = false 

GFSK_902_250k = {
	'IOCFG0'     : 0x06,
	'PKTCTRL0'   : 0x05,
	'CHANNR'     : 0x14,
	'FSCTRL1'    : 0x0A,
	'FREQ2'      : 0x22,
	'FREQ1'      : 0xB1,
	'FREQ0'      : 0x3B,
	'MDMCFG4'    : 0x2D,
	'MDMCFG3'    : 0x3B,
	'MDMCFG2'    : 0x13,
	'DEVIATN'    : 0x00,
	'MCSM0'      : 0x18,
	'FOCCFG'     : 0x1D,
	'BSCFG'      : 0x1C,
	'AGCCTRL2'   : 0xC7,
	'AGCCTRL1'   : 0x00,
	'AGCCTRL0'   : 0xB0,
	'FREND1'     : 0xB6,
	'FSCAL3'     : 0xEA,
	'FSCAL2'     : 0x2A,
	'FSCAL1'     : 0x00,
	'FSCAL0'     : 0x1F,
	'TEST0'      : 0x09,}
rf_gfsk_902_250k = Bunch(GFSK_902_250k)

#NOTE: modulation is ask/ook at 250k baud
# Address Config = No address check 
# Base Frequency = 902.000000 
# CRC Autoflush = false 
# CRC Enable = true 
# Carrier Frequency = 905.999023 
# Channel Number = 20 
# Channel Spacing = 199.951172 
# Data Format = Normal mode 
# Data Rate = 249.939 
# Deviation = 1.586914 
# Device Address = 0 
# Manchester Enable = false 
# Modulation Format = ASK/OOK 
# PA Ramping = false 
# Packet Length = 255 
# Packet Length Mode = Variable packet length mode. Packet length configured by the first byte after sync word 
# Preamble Count = 4 
# RX Filter BW = 541.666667 
# Sync Word Qualifier Mode = 30/32 sync word bits detected 
# TX Power = 0 
# Whitening = false 

ASKOOK_902_250k = {
	'IOCFG0'     : 0x06,
	'PKTCTRL0'   : 0x05,
	'CHANNR'     : 0x14,
	'FSCTRL1'    : 0x0A,
	'FREQ2'      : 0x22,
	'FREQ1'      : 0xB1,
	'FREQ0'      : 0x3B,
	'MDMCFG4'    : 0x2D,
	'MDMCFG3'    : 0x3B,
	'MDMCFG2'    : 0x33,
	'DEVIATN'    : 0x00,
	'MCSM0'      : 0x18,
	'FOCCFG'     : 0x1D,
	'BSCFG'      : 0x1C,
	'AGCCTRL2'   : 0xC7,
	'AGCCTRL1'   : 0x00,
	'AGCCTRL0'   : 0xB0,
	'FREND1'     : 0xB6,
	'FREND0'     : 0x11,
	'FSCAL3'     : 0xEA,
	'FSCAL2'     : 0x2A,
	'FSCAL1'     : 0x00,
	'FSCAL0'     : 0x1F,
	'TEST0'      : 0x09,}
rf_askook_902_250k = Bunch(ASKOOK_902_250k)

#NOTE: MSK modulation at 250k
# Address Config = No address check 
# Base Frequency = 902.000000 
# CRC Autoflush = false 
# CRC Enable = true 
# Carrier Frequency = 905.999023 
# Channel Number = 20 
# Channel Spacing = 199.951172 
# Data Format = Normal mode 
# Data Rate = 249.939 
# Device Address = 0 
# Manchester Enable = false 
# Modulated = true 
# Modulation Format = MSK 
# PA Ramping = false 
# Packet Length = 255 
# Packet Length Mode = Variable packet length mode. Packet length configured by the first byte after sync word 
# Phase Transition Time = 0 
# Preamble Count = 4 
# RX Filter BW = 541.666667 
# Sync Word Qualifier Mode = 30/32 sync word bits detected 
# TX Power = 0 
# Whitening = false 

MSK_902_250k = {
	'IOCFG0'     : 0x06,
	'PKTCTRL0'   : 0x05,
	'CHANNR'     : 0x14,
	'FSCTRL1'    : 0x0A,
	'FREQ2'      : 0x22,
	'FREQ1'      : 0xB1,
	'FREQ0'      : 0x3B,
	'MDMCFG4'    : 0x2D,
	'MDMCFG3'    : 0x3B,
	'MDMCFG2'    : 0x73,
	'DEVIATN'    : 0x00,
	'MCSM0'      : 0x18,
	'FOCCFG'     : 0x1D,
	'BSCFG'      : 0x1C,
	'AGCCTRL2'   : 0xC7,
	'AGCCTRL1'   : 0x00,
	'AGCCTRL0'   : 0xB0,
	'FREND1'     : 0xB6,
	'FSCAL3'     : 0xEA,
	'FSCAL2'     : 0x2A,
	'FSCAL1'     : 0x00,
	'FSCAL0'     : 0x1F,
	'TEST0'      : 0x09,}
rf_msk_902_250k = Bunch(MSK_902_250k)

#NOTE: CC1101 115k baud, Mod: GFSK, 915Mhz, power 10
# Address Config = No address check 
# Base Frequency = 915.000000 
# CRC Autoflush = false 
# CRC Enable = true 
# Carrier Frequency = 915.000000 
# Channel Number = 0 
# Channel Spacing = 199.951172 
# Data Format = Normal mode 
# Data Rate = 115.051 
# Deviation = 47.607422 
# Device Address = 0 
# Manchester Enable = false 
# Modulated = true 
# Modulation Format = GFSK 
# PA Ramping = false 
# Packet Length = 255 
# Packet Length Mode = Variable packet length mode. Packet length configured by the first byte after sync word 
# Preamble Count = 4 
# RX Filter BW = 270.833333 
# Sync Word Qualifier Mode = 30/32 sync word bits detected 
# TX Power = 10 
# Whitening = false 

GFSK_915_115k = {
	'IOCFG0'     : 0x06,
	'FIFOTHR'    : 0x47,
	'PKTCTRL0'   : 0x05,
	'FSCTRL1'    : 0x08,
	'FREQ2'      : 0x23,
	'FREQ1'      : 0x31,
	'FREQ0'      : 0x3B,
	'MDMCFG4'    : 0x6C,
	'MDMCFG2'    : 0x13,
	'MCSM0'      : 0x18,
	'FOCCFG'     : 0x1D,
	'AGCCTRL2'   : 0xC7,
	'AGCCTRL1'   : 0x00,
	'AGCCTRL0'   : 0xB2,
	'WORCTRL'    : 0xFB,
	'FREND1'     : 0xB6,
	'FSCAL3'     : 0xEA,
	'FSCAL2'     : 0x2A,
	'FSCAL1'     : 0x00,
	'FSCAL0'     : 0x1F,
	'TEST2'      : 0x81,
	'TEST1'      : 0x35,
	'TEST0'      : 0x09,}
rf_gfsk_915_115k = Bunch(GFSK_915_115k)
