#pylint: disable=C0103
"""KITNewSearch module"""
import sys
import logging
import yaml
import requests
import timeit

class KITNewSearch(object):
    """Module for searching data in ETP Measurement DB.    """
    def __init__(self, cred=None, meas_key="measurement_keys.yml"):
        """
        cred (dict or path): {"url": "...", "token": "..."}
        """
        self.log = logging.getLogger(__class__.__name__)
        self.log.setLevel(logging.DEBUG)
        if self.log.hasHandlers() is False:
            format_string = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
            formatter = logging.Formatter(format_string)
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.log.addHandler(console_handler)

        self.url = None
        self.token = None
        self.connection = False
        if cred is not None:
            if isinstance(cred, str):
                with open(cred, "r") as crx:
                    cred = yaml.load(crx, Loader=yaml.FullLoader)
            self.set_credentials(cred)

        with open(meas_key, "r") as stream:
            self.meas_key = yaml.load(stream, Loader=yaml.FullLoader)


    def set_credentials(self, cred):
        try:
            self.url = cred["url"]
            self.token = {"Authorization":  "Token {}".format(cred["token"])}
        except Exception:
            raise Exception("Couldn't load credentials from credentials file.")

    def check_connection(self):
        data = requests.get("http://{!s}/measurements/".format(self.url),
                 headers=self.token)
        if data.status_code == 200:
            return True
        else:
            return False


    def search_pid(self, pid):
        data = requests.get("http://{!s}/measurement/{!s}/json".format(self.url, pid),
                 headers=self.token).json()
        return data

    def extract_data(self, data):
        m_type = data["header"]["measurementtype"]
        try:
            new_dic = {
                "name": data["header"]["sensorname"],
                "dataX": [dic[self.meas_key[m_type][0]]["value"] for dic in data["data"]],
                "dataY": [dic[self.meas_key[m_type][1]]["value"] for dic in data["data"]],
                "dataZ": [],
                "err": [],
                "bias_cur": [],
                "time": [],
                "temp": [dic["temperature"]["value"] for dic in data["data"]],
                "rh": [dic["humidity"]["value"] for dic in data["data"]],
                "paraX": self.meas_key[m_type][0],
                "paraY": self.meas_key[m_type][1],
                "name": data["header"]["sensorname"],
                "project": data["header"]["sensorgroup"],
                "fluence": data["header"]["fluence"],
                "particletype": [],
                "t0": data["header"]["header"]["temperature"],
                "h0": data["header"]["header"]["humidity"]}
            return new_dic
        except (KeyError, TypeError):
            self.log.error(
                "The requested measurement is of type '%s' which "\
                "cannot be digested by KITData", m_type)
            sys.exit()


if __name__ == '__main__':
    from functools import partial

    with open("..\\..\\db.cfg", "r") as crx:
        cred = yaml.load(crx, Loader=yaml.FullLoader)
    KNS = KITNewSearch(cred["new DB"])
    # KNS.check_connection()
    DATA = KNS.search_pid(18608)
    # print(KNS.extract_data(DATA))
    print(timeit.timeit(partial(KNS.extract_data, DATA), number=1000))