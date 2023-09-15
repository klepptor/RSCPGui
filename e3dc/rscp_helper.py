# -*- coding: latin-1 -*-

import datetime
import logging
import socket
import time

from e3dc._rscp_dto import RSCPDTO
from e3dc._rscp_exceptions import RSCPCommunicationError
from e3dc.e3dc import E3DC
from e3dc.rscp_tag import RSCPTag
from e3dc.rscp_type import RSCPType

logger = logging.getLogger(__name__)

class rscp_helper():
    _blocked = False

    def __init__(self, username, password, host, rscp_pass):
        self.e3dc = E3DC(username, password, host, rscp_pass)

    def get_all(self, requests=None, raw=False):
        if not requests:
            requests = []
        requests += self.getBatData(bat_index=0, dcb_indexes=[0, 1])
        requests += self.getDCDCData(dcdc_indexes=[0, 1])
        requests += self.getEMSData()
        requests += self.getPMData(pm_indexes=[0, 1])
        requests += self.getPVIData()
        # requests += self.getEmergencyStatus()
        # requests += self.getSysSpecs()
        # requests += self.getInfo()

        return self.get_data(requests, raw)

    def getUserLevel(self):
        requests = []
        requests.append(RSCPTag.RSCP_REQ_USER_LEVEL)
        return requests


    def getCheckForUpdates(self):
        requests = []
        requests.append(RSCPTag.UM_REQ_CHECK_FOR_UPDATES)

        return requests

    def getUpdateStatus(self):
        requests = []
        requests.append(RSCPTag.UM_REQ_UPDATE_STATUS)

        return requests

    def getWBCount(self):
        requests = []
        requests.append(RSCPTag.WB_REQ_CONNECTED_DEVICES)
        return requests


    def getWB(self, index=0):
        requests = []
        r = RSCPDTO(RSCPTag.WB_REQ_DATA, rscp_type=RSCPType.Container)
        r += RSCPDTO(RSCPTag.WB_INDEX, rscp_type=RSCPType.UChar8, data = index)
        r += RSCPTag.WB_REQ_STATUS
        r += RSCPTag.WB_REQ_ENERGY_ALL
        r += RSCPTag.WB_REQ_ENERGY_SOLAR
        r += RSCPTag.WB_REQ_SOC
        r += RSCPTag.WB_REQ_STATUS
        r += RSCPTag.WB_REQ_ERROR_CODE
        r += RSCPTag.WB_REQ_MODE
        r += RSCPTag.WB_REQ_APP_SOFTWARE
        r += RSCPTag.WB_REQ_BOOTLOADER_SOFTWARE
        r += RSCPTag.WB_REQ_HW_VERSION
        r += RSCPTag.WB_REQ_FLASH_VERSION
        r += RSCPTag.WB_REQ_DEVICE_ID
        r += RSCPTag.WB_REQ_DEVICE_STATE
        r += RSCPTag.WB_REQ_PM_POWER_L1
        r += RSCPTag.WB_REQ_PM_POWER_L2
        r += RSCPTag.WB_REQ_PM_POWER_L3
        r += RSCPTag.WB_REQ_PM_ACTIVE_PHASES
        r += RSCPTag.WB_REQ_PM_MODE
        r += RSCPTag.WB_REQ_PM_ENERGY_L1
        r += RSCPTag.WB_REQ_PM_ENERGY_L2
        r += RSCPTag.WB_REQ_PM_ENERGY_L3
        r += RSCPTag.WB_REQ_PM_DEVICE_ID
        r += RSCPTag.WB_REQ_PM_ERROR_CODE
        r += RSCPTag.WB_REQ_PM_DEVICE_STATE
        r += RSCPTag.WB_REQ_PM_FIRMWARE_VERSION
        r += RSCPTag.WB_REQ_DIAG_DEVICE_ID
        r += RSCPTag.WB_REQ_DIAG_BAT_CAPACITY
        r += RSCPTag.WB_REQ_DIAG_USER_PARAM
        r += RSCPTag.WB_REQ_DIAG_MAX_CURRENT
        r += RSCPTag.WB_REQ_DIAG_PHASE_VOLTAGE
        r += RSCPTag.WB_REQ_DIAG_DISPLAY_SPEECH
        r += RSCPTag.WB_REQ_DIAG_DESIGN
        r += RSCPTag.WB_REQ_DIAG_INFOS
        r += RSCPTag.WB_REQ_DIAG_WARNINGS
        r += RSCPTag.WB_REQ_DIAG_ERRORS
        r += RSCPTag.WB_REQ_DIAG_TEMP_1
        r += RSCPTag.WB_REQ_DIAG_TEMP_2
        r += RSCPTag.WB_REQ_DIAG_CP_PEGEL
        r += RSCPTag.WB_REQ_DIAG_PP_IN_A
        r += RSCPTag.WB_REQ_DIAG_STATUS_DIODE
        r += RSCPTag.WB_REQ_DIAG_DIG_IN_1
        r += RSCPTag.WB_REQ_DIAG_DIG_IN_2
        r += RSCPTag.WB_REQ_PM_MAX_PHASE_POWER
        r += RSCPTag.WB_REQ_DEVICE_NAME
        r += RSCPTag.WB_REQ_EXTERN_DATA_SUN
        r += RSCPTag.WB_REQ_EXTERN_DATA_NET
        r += RSCPTag.WB_REQ_EXTERN_DATA_ALL
        r += RSCPTag.WB_REQ_EXTERN_DATA_ALG
        r += RSCPTag.WB_REQ_PARAM_1
        r += RSCPTag.WB_REQ_PARAM_2

        requests.append(r)

        return requests

    def getModbus(self):
        requests = []
        requests.append(RSCPTag.MBS_REQ_MODBUS_ENABLED)
        requests.append(RSCPTag.MBS_REQ_MODBUS_CONNECTORS)

        return requests

    #TODO: Weiter mit Leben f�llen
    def getDB(self, start, intervall, span):
        start = int(datetime.datetime.now().timestamp())
        intervall = 3600
        span = 3600

        container = []
        container.append(RSCPDTO(tag=RSCPTag.DB_REQ_HISTORY_TIME_START, rscp_type=RSCPType.Uint64, data=start))
        container.append(RSCPDTO(tag=RSCPTag.DB_REQ_HISTORY_TIME_INTERVAL, rscp_type=RSCPType.Uint64, data=intervall))
        container.append(RSCPDTO(tag=RSCPTag.DB_REQ_HISTORY_TIME_SPAN, rscp_type=RSCPType.Uint64, data=span))
        requests = []
        requests.append(RSCPDTO(tag=RSCPTag.DB_REQ_HISTORY_DATA_DAY, rscp_type=RSCPType.Container, data=container))

        for i in requests:
            print(i)

        return requests

    def getInfoAdditional(self):
        requests = []
        requests.append(RSCPTag.INFO_REQ_MODULES_SW_VERSIONS)
        return requests

    def getInfo(self):
        requests = []
        requests.append(RSCPTag.INFO_REQ_PRODUCTION_DATE)
        requests.append(RSCPTag.INFO_REQ_SERIAL_NUMBER)
        requests.append(RSCPTag.INFO_REQ_SW_RELEASE)
        requests.append(RSCPTag.INFO_REQ_A35_SERIAL_NUMBER)
        requests.append(RSCPTag.INFO_REQ_TIME)
        requests.append(RSCPTag.INFO_REQ_TIME_ZONE)
        requests.append(RSCPTag.INFO_REQ_UTC_TIME)
        requests.append(RSCPTag.INFO_REQ_IP_ADDRESS)
        requests.append(RSCPTag.INFO_REQ_SUBNET_MASK)
        requests.append(RSCPTag.INFO_REQ_MAC_ADDRESS)
        requests.append(RSCPTag.INFO_REQ_GATEWAY)
        requests.append(RSCPTag.INFO_REQ_DNS)
        requests.append(RSCPTag.INFO_REQ_DHCP_STATUS)
        requests.append(RSCPTag.INFO_REQ_IS_RSCP_PASSWORD_SET)
        requests.append(RSCPTag.INFO_REQ_UPNP_STATUS)
        #requests.append(RSCPTag.INFO_REQ_GET_FACILITY) -> Leere Tags (INFO_NAME, INFO_STREET, INFO_STREET_NO, INFO_POSTCODE, INFO_CITY, INFO_FON, INFO_E_MAIL, INFO_COUNTRY)
        #requests.append(RSCPTag.INFO_REQ_IS_CALIBRATED) #-> Fehler (ACCESS_DENIED)
        #requests.append(RSCPTag.INFO_REQ_HW_TIME) #-> Fehler (ACCESS_DENIED)
        requests.append(RSCPTag.INFO_REQ_GET_FS_USAGE) # R�ckgabe: INFO_FS_SIZE, INFO_FS_USED, INFO_FS_AVAILABLE, INFO_FS_USE_PERCENT
        requests.append(RSCPTag.INFO_REQ_GUI_TARGET)
        #requests.append(RSCPTag.INFO_REQ_PLATFORM_TYPE) #-> Fehler (ACCESS_DENIED)
        requests.append(RSCPTag.SRV_REQ_IS_ONLINE)
        requests.append(RSCPTag.SYS_REQ_IS_SYSTEM_REBOOTING)
        requests.append(RSCPTag.RSCP_REQ_USER_LEVEL)

        return requests

    def setChargePower(self, value=None):
        requests = []
        containerData = []
        if value:
            containerData.append(RSCPDTO(tag=RSCPTag.EMS_POWER_LIMITS_USED, data=True))
            containerData.append(RSCPDTO(tag=RSCPTag.EMS_MAX_CHARGE_POWER, data=value))
        else:
            containerData.append(RSCPDTO(tag=RSCPTag.EMS_POWER_LIMITS_USED, data=False))

        requests.append(RSCPDTO(tag=RSCPTag.EMS_REQ_SET_POWER_SETTINGS, data=containerData))

        return requests

    def getBatDcbData(self, bat_index=0, bat_indexes=None):
        if not bat_indexes:
            bat_indexes = [bat_index]

        requests = []

        for bat_index in bat_indexes:
            r = RSCPDTO(tag=RSCPTag.BAT_REQ_DATA)
            r += RSCPDTO(tag=RSCPTag.BAT_INDEX, data=bat_index)
            r += RSCPTag.BAT_REQ_DCB_COUNT
            try:
                data = self.get_data([r], True)
                logger.debug('Bat #' + str(bat_index) + ' scheint aktiv zu sein, rufe weitere Daten ab')
                requests += self.getBatData(bat_index=bat_index, dcb_indexes=range(0, data['BAT_DCB_COUNT'].data))
            except:
                logger.debug('Bat #' + str(bat_index) + ' steht nicht zur Verf�gung')


        return requests

    def getBatData(self, bat_index=0, bat_indexes=None, dcb_index=0, dcb_indexes=None):
        requests = []

        if not bat_indexes:
            bat_indexes = [bat_index]
        if not dcb_indexes and dcb_index:
            dcb_indexes = [dcb_index]

        for bat_index in bat_indexes:
            r = RSCPDTO(tag=RSCPTag.BAT_REQ_DATA)
            r += RSCPDTO(tag=RSCPTag.BAT_INDEX, data=bat_index)
            r += RSCPTag.BAT_REQ_USABLE_CAPACITY
            r += RSCPTag.BAT_REQ_USABLE_REMAINING_CAPACITY
            r += RSCPTag.BAT_REQ_ASOC
            r += RSCPTag.BAT_REQ_RSOC_REAL
            r += RSCPTag.BAT_REQ_MAX_BAT_VOLTAGE
            r += RSCPTag.BAT_REQ_MAX_CHARGE_CURRENT
            r += RSCPTag.BAT_REQ_EOD_VOLTAGE
            r += RSCPTag.BAT_REQ_MAX_DISCHARGE_CURRENT
            r += RSCPTag.BAT_REQ_CHARGE_CYCLES
            r += RSCPTag.BAT_REQ_TERMINAL_VOLTAGE
            r += RSCPTag.BAT_REQ_MAX_DCB_CELL_TEMPERATURE
            r += RSCPTag.BAT_REQ_MIN_DCB_CELL_TEMPERATURE
            r += RSCPTag.BAT_REQ_READY_FOR_SHUTDOWN
            r += RSCPTag.BAT_REQ_TRAINING_MODE
            r += RSCPTag.BAT_REQ_FCC
            r += RSCPTag.BAT_REQ_RC
            r += RSCPTag.BAT_REQ_INFO
            r += RSCPTag.BAT_REQ_DCB_COUNT
            r += RSCPTag.BAT_REQ_DEVICE_NAME
            r += RSCPTag.BAT_REQ_DEVICE_STATE
            r += RSCPTag.BAT_REQ_SPECIFICATION
            r += RSCPTag.BAT_REQ_INTERNALS
            r += RSCPTag.BAT_REQ_TOTAL_USE_TIME
            r += RSCPTag.BAT_REQ_TOTAL_DISCHARGE_TIME

            if dcb_indexes:
                for dcb_index in dcb_indexes:
                    r += RSCPDTO(tag=RSCPTag.BAT_REQ_DCB_ALL_CELL_TEMPERATURES, data=dcb_index)
                    r += RSCPDTO(tag=RSCPTag.BAT_REQ_DCB_ALL_CELL_VOLTAGES, data=dcb_index)
                    r += RSCPDTO(tag=RSCPTag.BAT_REQ_DCB_INFO, data=dcb_index)

            requests.append(r)

        return requests

    def getDCDCData(self, dcdc_index=0, dcdc_indexes=None):
        requests = []

        if not dcdc_indexes:
            dcdc_indexes = [dcdc_index]

        for dcdc_index in dcdc_indexes:
            r = RSCPDTO(tag=RSCPTag.DCDC_REQ_DATA)
            r += RSCPDTO(tag=RSCPTag.DCDC_INDEX, data=dcdc_index)
            r += RSCPTag.DCDC_REQ_P_BAT
            r += RSCPTag.DCDC_REQ_P_DCL
            r += RSCPTag.DCDC_REQ_U_BAT
            r += RSCPTag.DCDC_REQ_U_DCL
            r += RSCPTag.DCDC_REQ_I_BAT
            r += RSCPTag.DCDC_REQ_I_DCL
            r += RSCPTag.DCDC_REQ_STATUS_AS_STRING
            r += RSCPTag.DCDC_REQ_FPGA_FIRMWARE
            r += RSCPTag.DCDC_REQ_FIRMWARE_VERSION
            r += RSCPTag.DCDC_REQ_SERIAL_NUMBER
            r += RSCPTag.DCDC_BOARD_VERSION
            requests.append(r)

        return requests

    def getTestData(self):
        requests = []

        requests.append(RSCPTag.EMS_REQ_AC_REACTIVE_POWER)
        requests.append(RSCPTag.EMS_REQ_MAX_DC_POWER)
        requests.append(RSCPTag.EMS_REQ_BAT_CURRENT_IN)
        requests.append(RSCPTag.EMS_REQ_BAT_CURRENT_OUT)
        requests.append(RSCPTag.EMS_REQ_EP_RESERVE)
        requests.append(RSCPTag.EMS_REQ_SEC_LIMITS)
        requests.append(RSCPTag.EMS_REQ_SEC_DEVICE_STATUS)
        requests.append(RSCPTag.EMS_REQ_SPECIFICATION_VALUES)
        requests.append(RSCPTag.EMS_REQ_ENERGY_STORAGE_MODEL)
        requests.append(RSCPTag.EMS_REQ_PV_ENERGY)
        requests.append(RSCPTag.EMS_REQ_POWER_PV_AC_OUT)
        requests.append(RSCPTag.EMS_REQ_REGULATOR_STRATEGY)
        requests.append(RSCPTag.EMS_REQ_EMERGENCY_POWER_OVERLOAD_STATUS)
        requests.append(RSCPTag.EMS_REQ_SUPPORTED_REGULATOR_MODES)
        requests.append(RSCPTag.EMS_REQ_REGULATOR_MODE)
        requests.append(RSCPTag.EMS_REQ_IDLE_PERIOD_MIN_SOC_UCB)
        requests.append(RSCPTag.EMS_REQ_IDLE_PERIOD_MAX_SOC_UCB)
        requests.append(RSCPTag.EMS_REQ_REMOTE_CONTROL_STATUS)
        requests.append(RSCPTag.EMS_REQ_EP_DELAY)
        requests.append(RSCPTag.EMS_REQ_GET_PARTIAL_GRID)

        return requests

    def getEMSSysSpecs(self):
        requests = []
        requests.append(RSCPTag.EMS_REQ_GET_SYS_SPECS)
        return requests

    def getEMSIdlePeriods(self):
        requests = []
        requests.append(RSCPTag.EMS_REQ_GET_IDLE_PERIODS)
        return requests

    def getEMSPowerSettings(self):
        requests = []
        requests.append(RSCPTag.EMS_REQ_GET_POWER_SETTINGS)
        requests.append(RSCPTag.EMS_REQ_BATTERY_BEFORE_CAR_MODE)
        requests.append(RSCPTag.EMS_REQ_BATTERY_TO_CAR_MODE)
        return requests

    def getEMSBasis(self):
        requests = []

        requests.append(RSCPTag.EMS_REQ_POWER_PV)
        requests.append(RSCPTag.EMS_REQ_POWER_BAT)
        requests.append(RSCPTag.EMS_REQ_POWER_HOME)
        requests.append(RSCPTag.EMS_REQ_POWER_GRID)
        requests.append(RSCPTag.EMS_REQ_POWER_ADD)
        requests.append(RSCPTag.EMS_REQ_BAT_SOC)
        requests.append(RSCPTag.EMS_REQ_AUTARKY)
        requests.append(RSCPTag.EMS_REQ_SELF_CONSUMPTION)
        requests.append(RSCPTag.EMS_REQ_COUPLING_MODE)

        requests.append(RSCPTag.EMS_REQ_BALANCED_PHASES)
        requests.append(RSCPTag.EMS_REQ_INSTALLED_PEAK_POWER)
        requests.append(RSCPTag.EMS_REQ_DERATE_AT_PERCENT_VALUE)
        requests.append(RSCPTag.EMS_REQ_DERATE_AT_POWER_VALUE)
        requests.append(RSCPTag.EMS_REQ_USED_CHARGE_LIMIT)
        requests.append(RSCPTag.EMS_REQ_USER_CHARGE_LIMIT)
        requests.append(RSCPTag.EMS_REQ_BAT_CHARGE_LIMIT)
        requests.append(RSCPTag.EMS_REQ_DCDC_CHARGE_LIMIT)
        requests.append(RSCPTag.EMS_REQ_USED_DISCHARGE_LIMIT)
        requests.append(RSCPTag.EMS_REQ_USER_DISCHARGE_LIMIT)
        requests.append(RSCPTag.EMS_REQ_BAT_DISCHARGE_LIMIT)
        requests.append(RSCPTag.EMS_REQ_DCDC_DISCHARGE_LIMIT)
        requests.append(RSCPTag.EMS_REQ_REMAINING_BAT_CHARGE_POWER)
        requests.append(RSCPTag.EMS_REQ_REMAINING_BAT_DISCHARGE_POWER)
        requests.append(RSCPTag.EMS_REQ_EMERGENCY_POWER_STATUS)

        requests.append(RSCPTag.EMS_REQ_MODE)
        requests.append(RSCPTag.EMS_REQ_EXT_SRC_AVAILABLE)
        #requests.append(RSCPTag.EMS_REQ_GET_GENERATOR_STATE)
        requests.append(RSCPTag.EMS_REQ_EMERGENCYPOWER_TEST_STATUS)
        requests.append(RSCPTag.EMS_REQ_STORED_ERRORS)
        #requests.append(RSCPTag.EMS_REQ_ERROR_BUZZER_ENABLED)

        requests.append(RSCPTag.EMS_REQ_POWER_WB_ALL)
        requests.append(RSCPTag.EMS_REQ_POWER_WB_SOLAR)
        requests.append(RSCPTag.EMS_REQ_ALIVE)

        requests.append(RSCPTag.EMS_REQ_GET_MANUAL_CHARGE)

        requests.append(RSCPTag.EP_REQ_IS_READY_FOR_SWITCH)
        requests.append(RSCPTag.EP_REQ_IS_GRID_CONNECTED)
        requests.append(RSCPTag.EP_REQ_IS_ISLAND_GRID)
        requests.append(RSCPTag.EP_REQ_IS_POSSIBLE)
        requests.append(RSCPTag.EP_REQ_IS_INVALID_STATE)

        requests.append(RSCPTag.EMS_REQ_STATUS)

        return requests

    def getEMSData(self):
        requests = []
        requests += self.getEMSSysSpecs()
        requests += self.getEMSIdlePeriods()
        requests += self.getEMSPowerSettings()
        requests += self.getEMSBasis()
        return requests

    def getEmergencyStatus(self):
        requests = []

        requests.append(RSCPTag.EMS_REQ_EMERGENCY_POWER_STATUS)

        return requests

    def getSysSpecs(self):
        requests = []
        requests.append(RSCPTag.EMS_REQ_GET_SYS_SPECS)

        return requests

    def getPMData(self, pm_index=0, pm_indexes=None):
        requests = []
        if not pm_indexes:
            pm_indexes = [pm_index]

        for pm_index in pm_indexes:
            r = RSCPDTO(tag=RSCPTag.PM_REQ_DATA)
            r += RSCPDTO(tag=RSCPTag.PM_INDEX, data=pm_index)  # PM INDEX 0 = Leistungsmesser Netzbezug
            r += RSCPTag.PM_REQ_POWER_L1
            r += RSCPTag.PM_REQ_POWER_L2
            r += RSCPTag.PM_REQ_POWER_L3
            r += RSCPTag.PM_REQ_VOLTAGE_L1
            r += RSCPTag.PM_REQ_VOLTAGE_L2
            r += RSCPTag.PM_REQ_VOLTAGE_L3
            r += RSCPTag.PM_REQ_ENERGY_L1
            r += RSCPTag.PM_REQ_ENERGY_L2
            r += RSCPTag.PM_REQ_ENERGY_L3
            r += RSCPTag.PM_REQ_FIRMWARE_VERSION
            r += RSCPTag.PM_REQ_ACTIVE_PHASES
            r += RSCPTag.PM_REQ_MODE
            r += RSCPTag.PM_REQ_ERROR_CODE
            r += RSCPTag.PM_REQ_TYPE
            r += RSCPTag.PM_REQ_DEVICE_ID
            r += RSCPTag.PM_REQ_COMM_STATE
            r += RSCPTag.PM_REQ_IS_CAN_SILENCE
            r += RSCPTag.PM_REQ_DEVICE_STATE

            requests.append(r)

        return requests

    def getPVIData(self, pvi_index=0, pvi_indexes=None, phase=None, string=None):
        requests = []

        phases = phase if isinstance(phase,list) else [phase] if phase else phase
        strings = string if isinstance(string, list) else [string] if string else string

        if not pvi_indexes:
            pvi_indexes = [pvi_index]

        for pvi_index in pvi_indexes:
            r = RSCPDTO(tag=RSCPTag.PVI_REQ_DATA)
            r += RSCPDTO(tag=RSCPTag.PVI_INDEX, data=pvi_index)
            r += RSCPTag.PVI_REQ_AC_MAX_PHASE_COUNT
            r += RSCPTag.PVI_REQ_TEMPERATURE_COUNT
            r += RSCPTag.PVI_REQ_DC_MAX_STRING_COUNT
            data = self.get_data([r], True)

            tempcount = int(data['PVI_TEMPERATURE_COUNT'])

            if not phases:
                phases = range(0,int(data['PVI_AC_MAX_PHASE_COUNT']))

            if not strings:
                strings = range(0,int(data['PVI_DC_MAX_STRING_COUNT']))

            r = RSCPDTO(tag=RSCPTag.PVI_REQ_DATA)
            r += RSCPDTO(tag=RSCPTag.PVI_INDEX, data=pvi_index)
            r += RSCPTag.PVI_REQ_TEMPERATURE_COUNT
            r += RSCPTag.PVI_REQ_TYPE
            r += RSCPTag.PVI_REQ_SERIAL_NUMBER
            r += RSCPTag.PVI_REQ_VERSION
            r += RSCPTag.PVI_REQ_ON_GRID
            r += RSCPTag.PVI_REQ_STATE
            r += RSCPTag.PVI_REQ_LAST_ERROR
            r += RSCPTag.PVI_REQ_COS_PHI
            r += RSCPTag.PVI_REQ_VOLTAGE_MONITORING
            r += RSCPTag.PVI_REQ_POWER_MODE
            r += RSCPTag.PVI_REQ_SYSTEM_MODE
            r += RSCPTag.PVI_REQ_FREQUENCY_UNDER_OVER
            r += RSCPTag.PVI_REQ_AC_MAX_PHASE_COUNT
            r += RSCPTag.PVI_REQ_MAX_TEMPERATURE
            r += RSCPTag.PVI_REQ_MIN_TEMPERATURE
            r += RSCPTag.PVI_REQ_AC_MAX_APPARENTPOWER
            r += RSCPTag.PVI_REQ_DEVICE_STATE

            for phase in phases:
                r += RSCPDTO(tag=RSCPTag.PVI_REQ_AC_POWER, data=phase)
                r += RSCPDTO(tag=RSCPTag.PVI_REQ_AC_VOLTAGE, data=phase)
                r += RSCPDTO(tag=RSCPTag.PVI_REQ_AC_CURRENT, data=phase)
                r += RSCPDTO(tag=RSCPTag.PVI_REQ_AC_APPARENTPOWER, data=phase)
                r += RSCPDTO(tag=RSCPTag.PVI_REQ_AC_REACTIVEPOWER, data=phase)
                r += RSCPDTO(tag=RSCPTag.PVI_REQ_AC_ENERGY_ALL, data=phase)
                r += RSCPDTO(tag=RSCPTag.PVI_REQ_AC_ENERGY_GRID_CONSUMPTION, data=phase)

            for string in strings:
                r += RSCPDTO(tag=RSCPTag.PVI_REQ_DC_POWER, data=string)
                r += RSCPDTO(tag=RSCPTag.PVI_REQ_DC_VOLTAGE, data=string)
                r += RSCPDTO(tag=RSCPTag.PVI_REQ_DC_CURRENT, data=string)
                r += RSCPDTO(tag=RSCPTag.PVI_REQ_DC_STRING_ENERGY_ALL, data=string)

            for temps in range(0,tempcount):
                r += RSCPDTO(tag=RSCPTag.PVI_REQ_TEMPERATURE, data=temps)

            requests.append(r)

        return requests

    def setCharge(self, state):
        return self.setIdlePeriod(0, state)

    def setDischarge(self, state):
        return self.setIdlePeriod(1, state)

    def setIdlePeriod(self, type=0, active=True, day=None, start='01:00', end='23:00'):
        if not day:
            day = datetime.datetime.today().weekday()
        periodData = []
        periodData.append(RSCPDTO(tag=RSCPTag.EMS_IDLE_PERIOD_TYPE, data=int(type)))
        periodData.append(RSCPDTO(tag=RSCPTag.EMS_IDLE_PERIOD_DAY, data=int(day)))
        periodData.append(RSCPDTO(tag=RSCPTag.EMS_IDLE_PERIOD_ACTIVE, data=active))
        timeData = []
        timeData.append(RSCPDTO(tag=RSCPTag.EMS_IDLE_PERIOD_HOUR, data=int(start[:2])))
        timeData.append(RSCPDTO(tag=RSCPTag.EMS_IDLE_PERIOD_MINUTE, data=int(start[3:])))
        periodData.append(RSCPDTO(tag=RSCPTag.EMS_IDLE_PERIOD_START, data=timeData))
        timeData = []
        timeData.append(RSCPDTO(tag=RSCPTag.EMS_IDLE_PERIOD_HOUR, data=int(end[:2])))
        timeData.append(RSCPDTO(tag=RSCPTag.EMS_IDLE_PERIOD_MINUTE, data=int(end[3:])))
        periodData.append(RSCPDTO(tag=RSCPTag.EMS_IDLE_PERIOD_END, data=timeData))

        data = []
        data.append(RSCPDTO(tag=RSCPTag.EMS_IDLE_PERIOD, rscp_type=RSCPType.Container, data=periodData))

        containerData = []
        containerData.append(RSCPDTO(tag=RSCPTag.EMS_REQ_SET_IDLE_PERIODS, rscp_type=RSCPType.Container, data=data))

        return containerData


    def get_blocked(self):
        return self._blocked

    def set_blocked(self, value):
        logger.debug('Setze blocking auf ' + str(value))
        self._blocked = value

    blocked = property(get_blocked, set_blocked)

    def get_data(self, requests, raw=False, block=True, waittime=0.01):
        if block:
            while self.blocked:
                logger.debug('Warte auf Freigabe der Verbindung')
                time.sleep(0.05)
            self.blocked = True

        responses = []

        try:
            responses = self.e3dc.send_requests(requests, waittime=waittime)
        except:
            if block:
                self.blocked = False
            raise

        if block:
            self.blocked = False

        if raw:
            if len(responses) == 1:
                return responses[0]
            elif len(responses) > 0:
                rscp = RSCPDTO(tag=RSCPTag.LIST_TYPE, rscp_type=RSCPType.Container, data=responses)
                return rscp
            else:
                return None
        else:
            raise Exception('Deprecated')
