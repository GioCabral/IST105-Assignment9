import requests
from requests.auth import HTTPBasicAuth
from dnac_config import DNAC
import urllib3

urllib3.disable_warnings()


class DNAC_Manager:
    def __init__(self):
        self.token = None

    def get_auth_token(self, display_token=False):
        try:
            url = f"https://{DNAC['host']}:{DNAC['port']}/dna/system/api/v1/auth/token"
            response = requests.post(
                url,
                auth=HTTPBasicAuth(DNAC['username'], DNAC['password']),
                verify=False,
                timeout=10
            )
            response.raise_for_status()
            self.token = response.json()['Token']

            return True, self.token
        except Exception as e:
            return False, str(e)

    def get_network_devices(self):
        if not self.token:
            return False, "Please authenticate first!"

        try:
            url = f"https://{DNAC['host']}:{DNAC['port']}/api/v1/network-device"
            headers = {"X-Auth-Token": self.token}
            response = requests.get(
                url,
                headers=headers,
                verify=False,
                timeout=10
            )
            response.raise_for_status()
            return True, response.json().get('response', [])
        except Exception as e:
            return False, str(e)

    def get_device_interfaces(self, device_ip):
        if not self.token:
            return False, "Please authenticate first!"

        try:
            ok, devices = self.get_network_devices()
            if not ok:
                return False, devices

            device = next(
                (d for d in devices if d.get('managementIpAddress') == device_ip),
                None
            )
            if not device:
                return False, f"Device {device_ip} not found!"

            url = f"https://{DNAC['host']}:{DNAC['port']}/api/v1/interface"
            headers = {"X-Auth-Token": self.token}
            params = {"deviceId": device['id']}
            response = requests.get(
                url,
                headers=headers,
                params=params,
                verify=False,
                timeout=10
            )
            response.raise_for_status()
            return True, response.json().get('response', [])
        except Exception as e:
            return False, str(e)
