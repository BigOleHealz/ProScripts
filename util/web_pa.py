#!/usr/bin/python3
import requests, random, logging, os
import traceback
import static.credentials as creds
from static.static import device_types, device_dict

class WebpaUtils:

    webpa_sat_key = creds.webpa_sat_key
    webpa_sat_secret = creds.webpa_sat_secret
    webpa_sat_url = creds.webpa_sat_url
    webpa_base_url = creds.webpa_base_url

    @classmethod
    def get_webpa_sat_token(cls):

        try:
            headers = {
                'Content-Type': "application/json",
                'X-Client-Id': cls.webpa_sat_key,
                'X-Client-Secret': cls.webpa_sat_secret
            }

            sat_response = requests.get(cls.webpa_sat_url, headers=headers)
            service_access_token = sat_response.json()['serviceAccessToken']

            return service_access_token
        except:
            traceback.print_exc()

    @classmethod
    def ip_from_mac(cls, mac: str, device_type: str):

        product_type = device_types[device_type]
        command = device_dict[product_type]["devices"][device_type]["command"]

        try:
            access_token = cls.get_webpa_sat_token()
            request_headers = {
                'authorization': "Bearer " + access_token,
            }
            request_url = cls.webpa_base_url + mac + '/config?names=' + command
            webpa_response = requests.get(request_url, headers=request_headers)

            ip_address = webpa_response.json()['parameters'][0]['value'] if \
                webpa_response.json().get('statusCode', 0) == 200 else False
            return ip_address
        except Exception as e:
            traceback.print_exc()

        return False


    @classmethod
    def router_is_online(cls, mac: str):
        command = "Device.DeviceInfo.UpTime"
        try:
            access_token = cls.get_webpa_sat_token()
            request_headers = {
                'authorization': "Bearer " + access_token,
            }
            request_url = cls.webpa_base_url + mac + '/config?names=' + command
            webpa_response = requests.get(request_url, headers=request_headers)

            answer = True if webpa_response.json().get('statusCode', 0) == 200 else False
            return answer
        except:
            traceback.print_exc()
        return False

    @classmethod
    def __extract_tgz_file(cls, tgz_filename: str, dir_name: str):
        '''
        This method extract the tgz file in provided "dir_name".
        :param tgz_filename: tgz file name
        :param dir_name: directory path
        '''
        try:
            tar = tarfile.open(tgz_filename, 'r')
            logging.info(dir_name)
            tar.extractall(dir_name) 
            tar.close()
        except Exception:
            logging.info("couldn't extract the file")

    @classmethod
    def __stbit_rest_request(cls, url: str, output_path: str, mac: str, device_type: str) -> str:
        """
        Internal private function to handle the actual STBiT REST GET Request.
        STBiT has many quirks, which we handle. This attempts to get the file
        and output it in a directory which it returns on successful completion

        :param str url: The URL on which to run the GET Request
        :param str output_file_name: The string path where
        :return: The path to the output directory
        :rtype: str
        :raises: Exception
        """
        error_message = ''
        output_file_name = ''
        try:
            logging.info(f"In rest request url: {url}")

            resp = requests.get(url, timeout=3000)

            if 'errorDetails' in resp.text:
                error_message = "Box could be offline"
                logging.info(" [STB LIVE LOGS] Box could be offline")

            else:
                filename = os.path.join(output_path, resp.headers['Content-Disposition'].split('=')[-1].strip(
                    '"').replace(':', ''))
                logging.info("filename: ", filename)

                file_descriptor = open(filename, 'wb')
                file_descriptor.write(resp.content)
                file_descriptor.close()

                path = "{}/{}".format(output_path, device_type)
                cls.__extract_tgz_file(filename, path)

                logging.info(f" [STB LIVE LOGS] File downloaded to : %s", filename)
                logging.info(f" [STB LOGS] output path : {output_path}")
        except requests.exceptions.Timeout as errt:
            logging.exception(" [STB LOGS] STB Timeout Error: : ", exc_info=True)
            error_message=  "STB request timeout"
        except requests.exceptions.ConnectionError as conn:
            logging.exception(" [STB LOGS] STB Connection Timeout Error: : ", exc_info=True)
            error_message=  "STB Connection error"
        except Exception as e:
            logging.exception("[STB LOGS] STB Error: : ", exc_info=True)
            error_message =  "error"

        return output_path

    @classmethod
    def get_live_logs_by_ip(cls, ip_addr: str, device_type: str) -> str:
        """
        Downloads the files specified by the parameters from the specified device IP
        using the STB Infra Tool and returns the extracted path for the same
        :param str ip: The IP of the Gateway/XB Box for which to Download
        :param str files_to_get: A glob supported path to download. Ex: /opt/logs/\*\*/receiver\*
        :param str plant_id: The Plant ID on which you know MAC maybe present. Not necessary
        :param str device_type: The Device Type for which to get the logs. Can be GW or XB3 (For all XB Devices)
        :return: Returns a path string to downloaded strings
        :rtype: str
        :raises: None
        """

        device_type = device_type.upper()
        product_type = device_types[device_type]
        files_to_download = device_dict[product_type]["devices"][device_type]["logpath"]

        username = creds.USERNAME
        password = creds.PASSWORD
        baseURL = r'https://stbit02.ccp.xcal.tv/' 
        rest_url = 'stbLogs/getLogs?format=json' 
        rest_url += "&username=" + username + "&password=" + password
        rest_url += '&ipValues=' + ip_addr
        logging.info(f"Rest URL: {rest_url}")

        logging.info(f"Downloading logs of {device_type}")
        if device_type in device_dict["RDKB"]["devices"].keys():
            """Downloading logs of XB"""
            rest_url += '&inputdevices=XB3&myGroup=8'

        elif device_type == 'XI5':
            """Downloading logs of XG"""
            rest_url += '&inputdevices=CL'

        elif device_type == 'XG':
            """Downloading logs of XG"""
            rest_url += '&inputdevices=GW&myGroup=4'

        rest_url += f'&logname={files_to_download}'

        output_name = ip_addr.strip('.').upper()
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))

        output_path = os.path.join(os.getcwd(), 'CpeLogs', 'DOWNLOADED', 'LIVE')

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        url = baseURL + rest_url
        if device_type == "XI5": url += "&networkType=GRAM"
        logging.info(f"Url: {url}")

        resp = requests.get(url)

        if 'errorDetails' in resp.text:
            logging.info("[STB LIVE LOGS] Box could be offline")
            return False

        else:
            filename = os.path.join(output_path, resp.headers[
                'Content-Disposition'].split('=')[-1].strip('"').replace(':', ''))
            logging.info(f"filename: {filename}")

            file_descriptor = open(filename, 'wb')
            file_descriptor.write(resp.content)
            file_descriptor.close()        

        path = f"{output_path}/{device_type}"  
        cls.__extract_tgz_file(filename, path)

        return path

    @classmethod
    def get_live_logs_by_mac(cls, estb_mac: str, device_type: str) -> str:
        """
        Downloads the files specified by the parameters from the specified device IP
        using the STB Infra Tool and returns the extracted path for the same

        :param str ip: The IP of the Gateway/XB Box for which to Download
        :param str files_to_get: A glob supported path to download. Ex: /opt/logs/\*\*/receiver\*
        :param str plant_id: The Plant ID on which you know MAC maybe present. Not necessary
        :param str device_type: The Device Type for which to get the logs. Can be CL
        :return: Returns a path string to downloaded strings
        :rtype: str
        :raises: None
        """
        device_type = device_type.upper()
        product_type = device_types[device_type]
        files_to_download = device_dict[product_type]["devices"][device_type]["logpath"]

        username = creds.USERNAME
        password = creds.PASSWORD
        baseURL = "https://stbit02.ccp.xcal.tv/"
        rest_url = 'stbReverseSShLogs/getLogs?format=json'
        rest_url += "&username=" + username + "&password=" + password
        rest_url += '&ipValues=' + estb_mac + "&inputdevices=CL&networkType=GRAM"
        rest_url += f'&logname={files_to_download}'
        logging.info(f"{rest_url}")

        logging.info("*****************", baseURL + rest_url)
        estb_mac = estb_mac.replace(':', '').upper()
        output_path = os.path.join(os.getcwd(), 'CpeLogs', 'DOWNLOADED', 'LIVE')
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        return cls.__stbit_rest_request(url=baseURL + rest_url, output_path=output_path, mac=estb_mac, device_type=device_type)

    @staticmethod
    def ecm_to_estb(ecm_mac: str):
        mac = ecm_mac.replace(":",'').upper().strip("'")
        mac = hex(int(mac, 16) - 2).lstrip('0x').rstrip('L').upper().zfill(12)
        estb_mac = ':'.join([mac[i:i+2] for i in range(0, len(mac), 2)])
        return estb_mac

    def find_online_device(device_type: str) -> str:
        """
        Loop through some known MAC addresses (that we haev stored locally) of the 
        given device type checking if that router is online. Once we have found one 
        that is online, return that MAC address
        """
        found_one = False
        with open(f'static/device_addresses/{device_type}.txt', 'r') as file:
            macs = file.read().splitlines()
            random.shuffle(macs)

            while found_one == False:
                mac = macs.pop()
                found_one = WebpaUtils.router_is_online(mac)

                print(f'{device_type} - {mac} : {found_one}')
                if found_one: 

                    return mac


if __name__ == "__main__":
    """
    Purpose:
        Loop through device types finding one that is online and printing the MAC
        and IP addresses. Mostly for testing and debugging."""
    for device_type in device_types.keys():
        mac = find_online_device(device_type)
        online = WebpaUtils.router_is_online(mac=mac)
        print(f'Online: {online}')
        ip = WebpaUtils.ip_from_mac(mac=mac, device_type=device_type)
        print(f'ip: {ip}')