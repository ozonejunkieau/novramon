import subprocess
import xmltodict

NOVRA_CMD_XMLSTATUS = "-xmlstatus"
NOVRA_EXECUTABLE = './novra/cmcs'

class NovraException(Exception):
    pass

class NovraReceiverNotFound(NovraException):
    pass

class Novra300:

    def __init__(self, host, password):
        self._host = host
        self._password = password

    def _cmcs_run_command(self, command_list):
        base_commands = [NOVRA_EXECUTABLE, f'-ip {self._host }', f'-pw {self._password}']
        sp_commands = base_commands + list(command_list)
        sp = subprocess.run(" ".join(sp_commands), universal_newlines=True, capture_output=True, text=True, shell=True)

        if "Unable to communicate with receiver" in sp.stdout:
            raise NovraReceiverNotFound
        return sp

    def get_status(self):
        resp = self._cmcs_run_command([NOVRA_CMD_XMLSTATUS])
        xml_response = resp.stdout
        novra_status = xmltodict.parse(xml_response)['RECEIVER_STATUS']

        return novra_status

