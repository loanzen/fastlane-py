import base64

import requests

from attrdict import AttrDict

import copy


class FastlaneApiException(Exception):

    def __init__(self, status, description):
        self.status = status
        self.description = description
        super(FastlaneApiException, self).__init__(description)


class FastlaneClient(object):
    def __init__(self, env, username, password):
        """
        Takes env, username and password as the parameters, where:
        evn = sandbox|production
        username & password: credentials of the API [allotted by
                                                    fastlaneindia.com]
        """
        self.username = username
        self.password = password
        if env == "production":
            self.url = "https://web.fastlaneindia.com/vin/api/v1.2/vehicle"
        elif env == "sandbox":
            self.url = "https://web.fastlaneindia.com/sandbox/api/v1.2/vehicle"
        else:
            raise ValueError('Invalid Environment %s', env)

    def convert_format(self, vehicle_rto, replacement_map):
        replacement_map_default = {'vehicle': {'regn_dt': 'registration_date', 'purchase_dt': 'purchase_date','regn_no':'registration_no',
                                               'state_cd': 'state', 'rto_cd': 'rto_code', 'rto_name': 'rto_name',
                                               'chasi_no': 'chasis_no', 'eng_no': 'engine_no', 'fla_vh_class_desc': 'vehicle_class_desc',
                                               'owner_sr': 'owner_serial_no', 'owner_cd_desc': 'owner_code', 'regn_type_desc': 'registration_type_desc',
                                               'vehicle_cd': 'vehicle_code', 'fla_maker_desc': 'make', 'fla_model_desc': 'model',
                                               'fla_variant': 'variant', 'fla_sub_variant': 'sub_variant', 'fla_fuel_type_desc': 'fuel_type',
                                               'fla_cubic_cap': 'cubic_cap', 'manu_yr': 'manufacture_year', 'fla_seat_cap': 'seat_cap'
                                               },
                                   'hypth': {'hp_type': 'hypth_type'},
                                   'insurance': {'comp_cd_desc': 'company_code'}
                                   }
        replacement_map = replacement_map if replacement_map is not None else replacement_map_default
        vehicle_rto_old = vehicle_rto
        vehicle_rto_new = copy.deepcopy(vehicle_rto)
        for i in range(len(vehicle_rto_new['results'])):
            for parent_key in vehicle_rto_new['results'][i].keys():
                for key in vehicle_rto_new['results'][i][parent_key].keys():
                    if parent_key in replacement_map and key in replacement_map[parent_key]:
                        if key != replacement_map[parent_key][key]:
                            vehicle_rto_new['results'][i][parent_key][replacement_map[parent_key][key]] = vehicle_rto_old['results'][i][parent_key][key]
                            vehicle_rto_new['results'][i][parent_key].pop(key, None)
        return AttrDict(vehicle_rto_new)

    def get_vehicle_details(self, regn_no, **kwargs):
        """
        Takes reg_no as the parameter to get the details of the vehicle from
        fastlane apis.
        """

        replacement_map = kwargs.get('replacement_map', None)
        querystring = {"regn_no": regn_no}
        headers = {
            'accept': "application/json",
            'authorization': "Basic " + base64.b64encode(
                self.username + ':' + self.password),
        }

        response = requests.request("GET", self.url, headers=headers,
                                    params=querystring)
        if response.status_code is not 200:
            raise FastlaneApiException(response.status_code, response.text)
        elif response.json()['status'] == 101:
            raise FastlaneApiException(response.status_code, response.json()['description'])

        return self.convert_format(response.json(), replacement_map)
