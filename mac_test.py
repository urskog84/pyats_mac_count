
import logging
from tabulate import tabulate
from ats import aetest
from ats.log.utils import banner

# Genie Imports
from genie.conf import Genie
from genie.abstract import Lookup
from genie.libs import ops  # noqa
from pprint import pprint

# Get your logger for your script
log = logging.getLogger(__name__)


###################################################################
#                  COMMON SETUP SECTION                           #
###################################################################

class common_setup(aetest.CommonSetup):
    """ Common Setup section """

    # CommonSetup have subsection.
    # You can have 1 to as many subsection as wanted

    # Connect to each device in the testbed
    @aetest.subsection
    def connect(self, testbed):
        genie_testbed = Genie.init(testbed)
        self.parent.parameters['testbed'] = genie_testbed
        device_list = []
        for device in genie_testbed.devices.values():
            log.info(banner(
                "Connect to device '{d}'".format(d=device.name)))
            try:
                device.connect()
            except Exception as e:
                self.failed("Failed to establish connection to '{}'".format(
                    device.name))

            device_list.append(device)

        # Pass list of devices the to testcases
        self.parent.parameters.update(dev=device_list)

###################################################################
#                     TESTCASES SECTION                           #
###################################################################

# Testcase name : vxlan_consistency_check


class MAC_address_count_check(aetest.Testcase):
    """ This is user Testcases section """

    # First test section
    @ aetest.test
    def parse_macaddresses(self):
        """ Sample test section. Only print """

        for device in self.parent.parameters['dev']:
            log.info(banner("Gathering mac address tabel from {}".format(
                device.name)))
            macaddresses = device.parse("show mac address-table")
            self.all_mac = macaddresses
            self.name = device.name

    # Second test section
    @ aetest.test
    def check_mac_count(self):
        antalx = 3
        mega_dict = {}
        mega_tabular = []
        for vlan, mac_list in self.all_mac['mac_table']['vlans'].items():
            mega_dict[vlan] = {}
            mac_len = len(mac_list['mac_addresses'])
            if mac_len > antalx:
                mega_dict[vlan] = mac_len
                smaller_tabular = []
                smaller_tabular.append(self.name)
                smaller_tabular.append(vlan)
                smaller_tabular.append(str(mac_len))
                smaller_tabular.append('Passed')
            else:
                mega_dict[vlan] = mac_len
                smaller_tabular = []
                smaller_tabular.append(self.name)
                smaller_tabular.append(vlan)
                smaller_tabular.append(str(mac_len))
                smaller_tabular.append('Failed')
            mega_tabular.append(smaller_tabular)

        mega_tabular.append(['-'*sum(len(i) for i in smaller_tabular)])

        log.info(tabulate(mega_tabular,
                          headers=['DeviceName', 'VlanID', 'Antal', 'Passed/Failed'],
                          tablefmt='orgtbl'))

        for vlan, antal in mega_dict.items():
            if antal < antalx:
                self.failed("vlan {d}: har bara {a} mac addresser, det måste vara fler en {x}".format(
                    d=vlan, a=antal, x=antalx))

        self.passed("All devices' vlan have more then {x} mac addresses".format(
            x=antalx
        ))

######################################################################
###                       COMMON CLEANUP SECTION                 ###
######################################################################


# This is how to create a CommonCleanup
# You can have 0 , or 1 CommonCleanup.
# CommonCleanup can be named whatever you want :)
class common_cleanup(aetest.CommonCleanup):
    """ Common Cleanup for Sample Test """

    # CommonCleanup follow exactly the same rule as CommonSetup regarding
    # subsection
    # You can have 1 to as many subsections as wanted
    # here is an example of 1 subsection

    @aetest.subsection
    def clean_everything(self):
        """ Common Cleanup Subsection """
        log.info("Aetest Common Cleanup ")


if __name__ == '__main__':  # pragma: no cover
    aetest.main()
