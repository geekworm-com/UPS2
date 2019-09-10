# -*- coding: UTF-8 -*-
# this is the sample python 3 code that how to view the batery information
# BQ27441 Python Library by ugeek (sp@geekworm.com)

import smbus 
import time 
import struct 
#import logging
import datetime
#Change 2500 to your battery capacity (mAh)
MY_BATTERY_CAP = 2500
#
# General Constants 常量
#
BQ27441_I2C_ADDRESS = 0x55    # Default I2C address of the BQ27441-G1A
BQ27441_UNSEAL_KEY  = 0x8000  # Secret code to unseal the BQ27441-G1A
BQ27441_DEVICE_ID   = 0x0421  # Default device ID

#
# Standard Command 标准命令
#
# The fuel gauge uses a series of 2-byte standard commands to enable system 
# reading and writing of battery information. Each command has an associated
# sequential command-code pair.
BQ27441_COMMAND_CONTROL        = 0x00
BQ27441_COMMAND_TEMP           = 0x02
BQ27441_COMMAND_VOLTAGE        = 0x04
BQ27441_COMMAND_FLAGS          = 0x06
BQ27441_COMMAND_NOM_CAPACITY   = 0x08
BQ27441_COMMAND_AVAIL_CAPACITY = 0x0A
BQ27441_COMMAND_REM_CAPACITY   = 0x0C
BQ27441_COMMAND_FULL_CAPACITY  = 0x0E
BQ27441_COMMAND_AVG_CURRENT    = 0x10
BQ27441_COMMAND_STDBY_CURRENT  = 0x12
BQ27441_COMMAND_MAX_CURRENT    = 0x14
BQ27441_COMMAND_AVG_POWER      = 0x18
BQ27441_COMMAND_SOC            = 0x1C
BQ27441_COMMAND_INT_TEMP       = 0x1E
BQ27441_COMMAND_SOH            = 0x20
BQ27441_COMMAND_REM_CAP_UNFL   = 0x28
BQ27441_COMMAND_REM_CAP_FIL    = 0x2A
BQ27441_COMMAND_FULL_CAP_UNFL  = 0x2C
BQ27441_COMMAND_FULL_CAP_FIL   = 0x2E
BQ27441_COMMAND_SOC_UNFL       = 0x30
BQ27441_COMMAND_TRUEREM_CAPACITY = 0x6A
#
# Control Sub-commands 控制子命令
#
# Issuing a Control(self) command requires a subsequent 2-byte subcommand. These
# additional bytes specify the particular control function desired. The 
# Control(self) command allows the system to control specific features of the fuel
# gauge during normal operation and additional features when the device is in 
# different access modes.

BQ27441_CONTROL_STATUS          = 0x00
BQ27441_CONTROL_DEVICE_TYPE     = 0x01
BQ27441_CONTROL_FW_VERSION      = 0x02
BQ27441_CONTROL_DM_CODE         = 0x04
BQ27441_CONTROL_PREV_MACWRITE   = 0x07
BQ27441_CONTROL_CHEM_ID         = 0x08
BQ27441_CONTROL_BAT_INSERT      = 0x0C
BQ27441_CONTROL_BAT_REMOVE      = 0x0D
BQ27441_CONTROL_SET_HIBERNATE   = 0x11
BQ27441_CONTROL_CLEAR_HIBERNATE	= 0x12
BQ27441_CONTROL_SET_CFGUPDATE   = 0x13
BQ27441_CONTROL_SHUTDOWN_ENABLE	= 0x1B
BQ27441_CONTROL_SHUTDOWN        = 0x1C
BQ27441_CONTROL_SEALED          = 0x20
BQ27441_CONTROL_PULSE_SOC_INT   = 0x23
BQ27441_CONTROL_RESET           = 0x41
BQ27441_CONTROL_SOFT_RESET      = 0x42
BQ27441_CONTROL_EXIT_CFGUPDATE  = 0x43
BQ27441_CONTROL_EXIT_RESIM      = 0x44

#
# Control Status Word - Bit Definitions 控制状态词
#
# Bit positions for the 16-bit data of CONTROL_STATUS.
# CONTROL_STATUS instructs the fuel gauge to return status information to 
# Control(self) addresses 0x00 and 0x01. The read-only status word contains status
# bits that are set or cleared either automatically as conditions warrant or
# through using specified subcommands.

BQ27441_STATUS_SHUTDOWNEN = 1 << 15
BQ27441_STATUS_WDRESET    = 1 << 14
BQ27441_STATUS_SS         = 1 << 13
BQ27441_STATUS_CALMODE    = 1 << 12
BQ27441_STATUS_CCA        = 1 << 11
BQ27441_STATUS_BCA        = 1 << 10
BQ27441_STATUS_QMAX_UP    = 1 << 9
BQ27441_STATUS_RES_UP     = 1 << 8
BQ27441_STATUS_INITCOMP   = 1 << 7
BQ27441_STATUS_HIBERNATE  = 1 << 6
BQ27441_STATUS_SLEEP      = 1 << 4
BQ27441_STATUS_LDMD       = 1 << 3
BQ27441_STATUS_RUP_DIS    = 1 << 2
BQ27441_STATUS_VOK        = 1 << 1

#
# Flag Command - Bit Definitions 标志命令
#
# Bit positions for the 16-bit data of Flags(self)
# This read-word function returns the contents of the fuel gauging status
# register, depicting the current operating status.
BQ27441_FLAG_OT        = 1 << 15
BQ27441_FLAG_UT        = 1 << 14
BQ27441_FLAG_FC        = 1 << 9
BQ27441_FLAG_CHG       = 1 << 8
BQ27441_FLAG_OCVTAKEN  = 1 << 7
BQ27441_FLAG_ITPOR     = 1 << 5
BQ27441_FLAG_CFGUPMODE = 1 << 4
BQ27441_FLAG_BAT_DET   = 1 << 3
BQ27441_FLAG_SOC1      = 1 << 2
BQ27441_FLAG_SOCF      = 1 << 1
BQ27441_FLAG_DSG       = 1 << 0

dict_flag = {'OT':BQ27441_FLAG_OT, 'UT':BQ27441_FLAG_UT, 'FC':BQ27441_FLAG_FC, \
	'CHG':BQ27441_FLAG_CHG, 'OCVTAKEN':BQ27441_FLAG_OCVTAKEN, 'ITPOR':BQ27441_FLAG_ITPOR, \
	'CFGUPMODE':BQ27441_FLAG_CFGUPMODE, 'BAT_DET':BQ27441_FLAG_BAT_DET, \
	'SOC1':BQ27441_FLAG_SOC1, 'SOCF':BQ27441_FLAG_SOCF, 'DSG':BQ27441_FLAG_DSG }
	
	
#
# Extended Data Commands 控制数据命令
#
# Extended data commands offer additional functionality beyond the standard
# set of commands. They are used in the same manner; however, unlike standard
# commands, extended commands are not limited to 2-byte words.
BQ27441_EXTENDED_OPCONFIG  = 0x3A # OpConfig(self)
BQ27441_EXTENDED_CAPACITY  = 0x3C # DesignCapacity(self)
BQ27441_EXTENDED_DATACLASS = 0x3E # DataClass(self)
BQ27441_EXTENDED_DATABLOCK = 0x3F # DataBlock(self)
BQ27441_EXTENDED_BLOCKDATA = 0x40 # BlockData(self)
BQ27441_EXTENDED_CHECKSUM  = 0x60 # BlockDataCheckSum(self)
BQ27441_EXTENDED_CONTROL   = 0x61 # BlockDataControl(self)

#
# Configuration Class, Subclass ID's # 配置类，子类的ID
#
# To access a subclass of the extended data, set the DataClass(self) function
# with one of these values.
# Configuration Classes
BQ27441_ID_SAFETY          = 2   # Safety
BQ27441_ID_CHG_TERMINATION = 36  # Charge Termination
BQ27441_ID_CONFIG_DATA     = 48  # Data
BQ27441_ID_DISCHARGE       = 49  # Discharge
BQ27441_ID_REGISTERS       = 64  # Registers
BQ27441_ID_POWER           = 68  # Power
# Gas Gauging Classes
BQ27441_ID_IT_CFG          = 80  # IT Cfg
BQ27441_ID_CURRENT_THRESH  = 81  # Current Thresholds
BQ27441_ID_STATE           = 82  # State
# Ra Tables Classes
BQ27441_ID_R_A_RAM         = 89  # R_a RAM
# Calibration Classes
BQ27441_ID_CALIB_DATA      = 104 # Data
BQ27441_ID_CC_CAL          = 105 # CC Cal
BQ27441_ID_CURRENT         = 107 # Current
# Security Classes
BQ27441_ID_CODES           = 112 # Codes

#
# OpConfig Register - Bit Definitions 选项寄存器
#
# Bit positions of the OpConfig Register
BQ27441_OPCONFIG_BIE      = 1 << 13
BQ27441_OPCONFIG_BI_PU_EN = 1 << 12
BQ27441_OPCONFIG_GPIOPOL  = 1 << 11
BQ27441_OPCONFIG_SLEEP    = 1 << 5
BQ27441_OPCONFIG_RMFCC    = 1 << 4
BQ27441_OPCONFIG_BATLOWEN = 1 << 2
BQ27441_OPCONFIG_TEMPS    = 1 << 0

def readControlWord(cmd):
	bus.write_word_data(BQ27441_I2C_ADDRESS,0x00,cmd)
	# up is below
	#bus.write_byte_data(BQ27441_I2C_ADDRESS,0x00,cmd & 0x00FF)
	#bus.write_byte_data(BQ27441_I2C_ADDRESS,0x01,cmd >> 8)
	return bus.read_word_data(BQ27441_I2C_ADDRESS, 0x00)

def executeControlWord(cmd):
	bus.write_word_data(BQ27441_I2C_ADDRESS,0x00,cmd)
	# # subCommandMSB = (cmd >> 8);
	# # subCommandLSB = (cmd & 0x00FF)
	# # command = [subCommandLSB, subCommandMSB]
	# #print "Control Word [0x%04x]" % ((subCommandLSB << 8) | subCommandMSB)
	# new_cmd = (cmd >> 8) | ((cmd & 0x00FF) << 8)
	# print "Execute Control Word [0x%04x]" % cmd
	# bus.write_word_data(BQ27441_I2C_ADDRESS,0x00,0x0001)
	# bus.write_word_data(BQ27441_I2C_ADDRESS,0x00,new_cmd)
	# #bus.write_word_data(BQ27441_I2C_ADDRESS,0x00,(subCommandLSB << 8) | subCommandMSB)
	
	# #bus.write_byte_data(BQ27441_I2C_ADDRESS,0x00,subCommandLSB) 
	# #bus.write_byte_data(BQ27441_I2C_ADDRESS,0x01,subCommandMSB) 
	
def writeExtendedCommand(addr,val):
	#print "Write Extend Command addr[0x%02x]" % addr ,", val[0x%02x]" % val
	bus.write_byte_data(BQ27441_I2C_ADDRESS,addr,val)
	#bus.write_byte_data(BQ27441_I2C_ADDRESS,0,addr)
	#bus.write_byte_data(BQ27441_I2C_ADDRESS,1,val)
	#bus.write_byte(BQ27441_I2C_ADDRESS,val)
	
	# bus.write_byte_data(BQ27441_I2C_ADDRESS, 0, addr)
	# bus.write_byte_data(BQ27441_I2C_ADDRESS, 1, val)
	

def device_id():
	return readControlWord(BQ27441_CONTROL_DEVICE_TYPE)
	
def dm_id():
	return readControlWord(BQ27441_CONTROL_DM_CODE)

def fw_version():
	return readControlWord(BQ27441_CONTROL_FW_VERSION)

def chem_id():
	return readControlWord(BQ27441_CONTROL_CHEM_ID)

def controlStatus():
	status = readControlWord(BQ27441_CONTROL_STATUS)
	return status

def softReset():
	#print "Soft Reset"
	executeControlWord(BQ27441_CONTROL_SOFT_RESET)
	
def setConfigUpdate():
	#print "Set Config Update..."
	executeControlWord(BQ27441_CONTROL_SET_CFGUPDATE)
	# bus.write_byte_data(BQ27441_I2C_ADDRESS,0x00,0x13) 
	# bus.write_byte_data(BQ27441_I2C_ADDRESS,0x01,0x00) 
def exitConfigUpdate():
	executeControlWord(BQ27441_CONTROL_EXIT_CFGUPDATE)
	
def seal():
	#print "BQ27441_CONTROL_SEALED"
	executeControlWord(BQ27441_CONTROL_SEALED)
	#executeControlWord(BQ27441_CONTROL_SEALED)

	
def unseal():
	#print "Unseal..."
	executeControlWord(BQ27441_UNSEAL_KEY)
	executeControlWord(BQ27441_UNSEAL_KEY)
	# bus.write_byte_data(BQ27441_I2C_ADDRESS,0x00,0x00) 
	# bus.write_byte_data(BQ27441_I2C_ADDRESS,0x01,0x80) 
	# bus.write_byte_data(BQ27441_I2C_ADDRESS,0x00,0x00) 
	# bus.write_byte_data(BQ27441_I2C_ADDRESS,0x01,0x80) 

def writeCap(cap):
	unseal()
	
	setConfigUpdate()
	
	writeExtendedCommand(BQ27441_EXTENDED_CONTROL,0x00)
	writeExtendedCommand(BQ27441_EXTENDED_DATACLASS,0x52)
	writeExtendedCommand(BQ27441_EXTENDED_DATABLOCK,0x00)
	
	block=bus.read_i2c_block_data(BQ27441_I2C_ADDRESS,BQ27441_EXTENDED_BLOCKDATA,32)
	block=list(struct.unpack('32B',bytearray(block)[0:32]))
	block[0x0a] = cap >> 8
	block[0x0b] = cap & 0xFF
	new_checksum = ~sum(block) & 0xFF

	bus.write_byte_data(BQ27441_I2C_ADDRESS,0x4a,cap >> 8) #writing new capacity 
	bus.write_byte_data(BQ27441_I2C_ADDRESS,0x4b,cap & 0xFF) #writing new capacity 

	time.sleep(1) 
	#write checksum
	bus.write_byte_data(BQ27441_I2C_ADDRESS,0x60,new_checksum) #trying to write on BlockDataChecksum(self) 

	time.sleep(1) 
	
	softReset()
	exitConfigUpdate()
	
	seal()
	
def availCap():
	val = bus.read_i2c_block_data(BQ27441_I2C_ADDRESS, BQ27441_COMMAND_AVAIL_CAPACITY, 2) 
	new_val = struct.unpack('H', bytearray(val)[0:2])
	return new_val[0]

def desCap():
	val = bus.read_i2c_block_data(BQ27441_I2C_ADDRESS, BQ27441_EXTENDED_CAPACITY, 2) 
	new_val = struct.unpack('H', bytearray(val)[0:2])
	return new_val[0]

def voltage():
	val = bus.read_i2c_block_data(BQ27441_I2C_ADDRESS, BQ27441_COMMAND_VOLTAGE, 2) 
	new_val = struct.unpack('H', bytearray(val)[0:2])
	return new_val[0]
	
def soc():
	val = bus.read_i2c_block_data(BQ27441_I2C_ADDRESS, BQ27441_COMMAND_SOC, 2) 
	new_val = struct.unpack('H', bytearray(val)[0:2])
	return new_val[0]

def soh():
	val = get_status_u(BQ27441_COMMAND_SOH)
	return val & 0x00FF

def get_status_u(reg):
	status = bus.read_i2c_block_data(BQ27441_I2C_ADDRESS, reg, 2) 
	(new_status, ) = struct.unpack('H', bytearray(status)[0:2])
	return new_status

def get_status(reg):
	status = bus.read_i2c_block_data(BQ27441_I2C_ADDRESS, reg, 2) 
	(new_status, ) = struct.unpack('h', bytearray(status)[0:2])
	return new_status
	
# def unseal():
	# executeControlWord(BQ27441_UNSEAL_KEY)
	# executeControlWord(BQ27441_UNSEAL_KEY)

def get_all_info():
	global status_control, status_temp, status_voltage, status_nom_capacity, \
	status_avail_capacity, status_rem_capacity, status_full_capacity, \
	status_avg_current, status_stdby_current, status_max_current, \
	status_avg_power, status_soc, status_int_temp, status_soh, \
	status_rem_cap_unfil, status_rem_cap_fil, status_full_cap_unfil, \
	status_full_cap_fil, status_soc_unfl, status_truerem_capacity
	
	status_control = get_status_u(BQ27441_COMMAND_CONTROL)
	status_temp = get_status_u(BQ27441_COMMAND_TEMP)
	status_voltage = get_status_u(BQ27441_COMMAND_VOLTAGE)
	status_nom_capacity = get_status_u(BQ27441_COMMAND_NOM_CAPACITY)
	status_avail_capacity = get_status_u(BQ27441_COMMAND_AVAIL_CAPACITY)
	status_rem_capacity = get_status_u(BQ27441_COMMAND_REM_CAPACITY)
	status_full_capacity = get_status_u(BQ27441_COMMAND_FULL_CAPACITY)
	status_avg_current = get_status(BQ27441_COMMAND_AVG_CURRENT)
	status_stdby_current = get_status(BQ27441_COMMAND_STDBY_CURRENT)
	status_max_current = get_status(BQ27441_COMMAND_MAX_CURRENT)
	status_avg_power = get_status(BQ27441_COMMAND_AVG_POWER)
	status_soc = get_status_u(BQ27441_COMMAND_SOC)
	status_int_temp = get_status_u(BQ27441_COMMAND_INT_TEMP)
	status_soh = soh()
	status_rem_cap_unfil = get_status_u(BQ27441_COMMAND_REM_CAP_UNFL)
	status_rem_cap_fil = get_status_u(BQ27441_COMMAND_REM_CAP_FIL)
	status_full_cap_unfil = get_status_u(BQ27441_COMMAND_FULL_CAP_UNFL)
	status_full_cap_fil = get_status_u(BQ27441_COMMAND_FULL_CAP_FIL)
	status_soc_unfl = get_status_u(BQ27441_COMMAND_SOC_UNFL)
	status_truerem_capacity = get_status_u(BQ27441_COMMAND_TRUEREM_CAPACITY)

def print_all_info():
	print "Control:                        ", status_control
	print "Temperature:                    ", status_temp, "0.1K"
	print "Voltage:                        ", status_voltage, "mV"
	print "Nominal Available Capacity:     ", status_nom_capacity, "mAh"
	print "Full Available Capacity:        ", status_avail_capacity, "mAh"
	print "Remaining Capacity:             ", status_rem_capacity, "mAh"
	print "Full Charge Capacity:           ", status_full_capacity, "mAh"
	print "Average Current:                ", status_avg_current, "mA"
	print "Standby Current:                ", status_stdby_current, "mA"
	print "MaxLoad Current:                ", status_max_current, "mA"
	print "Average Power:                  ", status_avg_power, "mW"
	print "State Of Charge:                ", status_soc, "%"
	print "Internal Temperature:           ", status_int_temp, "0.1K"
	print "State Of Health:                ", status_soh, "%"
	print "Remaining Capacity Unfiltered:  ", status_rem_cap_unfil, "mAh"
	print "Remaining Capacity Filtered:    ", status_rem_cap_fil, "mAh"
	print "Full Charge Capacity Unfiltered:", status_full_cap_unfil, "mAh"
	print "Full Charge Capacity Filtered:  ", status_full_cap_fil, "mAh"
	print "State Of Charge Unfiltered:     ", status_soc_unfl, "%"
	print "True Remaining Capacity:        ", status_truerem_capacity, "mAh"

def get_basic_info():
	global battery_soc, battery_voltage, battery_current ,battery_soh
	battery_soc = get_status_u(BQ27441_COMMAND_SOC)
	battery_voltage = get_status_u(BQ27441_COMMAND_VOLTAGE)
	battery_current = get_status(BQ27441_COMMAND_AVG_CURRENT)
	battery_soh = soh()

def print_basic_info():
	# print "[Basic Info]"
	# print "1.Voltage:", float(battery_voltage) / 1000, "V"
	# print "2.SOC:    ", battery_soc , "%"
	# print "3.Current:", float(battery_current) / 1000 , "A"
	# print "4.SOH:    ", battery_soh, "%"
	print "Voltage:", float(battery_voltage) / 1000, "V - " \
		"Current:", float(battery_current) / 1000 , "A - " , \
		"SOC:", battery_soc , "%"
	

def log_all_info():
	f = open('ups2_log.txt', 'a+')
	get_all_info()
	now_time = datetime.datetime.now()
	time_str = datetime.datetime.strftime(now_time,'%Y-%m-%d %H:%M:%S')
	
	f.write(time_str + ',' + str(status_control) + ',' + str(status_temp) + ',' + str(status_voltage) + ',' + str(status_nom_capacity) + ',' + \
	str(status_avail_capacity) + ',' + str(status_rem_capacity) + ',' + str(status_full_capacity) + ',' + \
	str(status_avg_current) + ',' + str(status_stdby_current) + ',' + str(status_max_current) + ',' + \
	str(status_avg_power) + ',' + str(status_soc) + ',' + str(status_int_temp) + ',' + str(status_soh) + ',' + \
	str(status_rem_cap_unfil) + ',' + str(status_rem_cap_fil) + ',' + str(status_full_cap_unfil) + ',' + \
	str(status_full_cap_fil) + ',' + str(status_soc_unfl) + ',' + str(status_truerem_capacity) + '\n')
	f.close()

def print_status():
	for dictElement in dict_flag:
	#print dict_flag[dictElement]
		if (dict_flag[dictElement] & status) is not 0:
			print dictElement

bus=smbus.SMBus(1)
time.sleep(1)
writeCap(MY_BATTERY_CAP)
#print "Now loading..."
#get_all_info()
get_basic_info()
print_basic_info()

