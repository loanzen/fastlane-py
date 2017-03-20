import base64

import requests


class FastlaneClient(object):
    def __init__(self, env, username, password):
        """
        Takes env, username and password as the parameters, where:
        evn = sandbox|production
        username & password: credentials of the API [allotted by
                            fastlaneindia.com]
        """
        self.env = env
        self.username = username
        self.password = password

    def get_vehicle_details(self, regn_no):
        """
        Takes reg_no as the parameter to get the details of the vehicle from
        fastlane apis.
        """
        if self.env == "production":
            url = "https://web.fastlaneindia.com/vin/api/v1.2/vehicle"
        elif self.env == "sandbox":
            url = "https://web.fastlaneindia.com/sandbox/api/v1.2/vehicle"
        else:
            return "invalid_env"

        querystring = {"regn_no": regn_no}
        headers = {
            'accept': "application/json",
            'authorization': "Basic " + base64.b64encode(
                self.username + ':' + self.password),
        }

        response = requests.request("GET", url, headers=headers,
                                    params=querystring)

        return response
