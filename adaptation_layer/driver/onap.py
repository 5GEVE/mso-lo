from typing import Dict, List
from client.onap import Client as ONAPclient
from client.onap import AgentClient as AGENTclient
# from .interface import Driver #sometimes it has to be in commend like  ONAP(Driver)
import json

# Driver = 'onap'
# class ONAP(Driver):


class ONAP(object):

    def __init__(self):
        self._client = ONAPclient()
        self._agent = AGENTclient()
        # self._client = ONAPclient(**self)

    def create_ns(self, args: Dict = None) -> Dict:
        ns_name = self._client.check_ns_name(args['payload']['nsdId'])  # to change nsdId to name of NS
        return self._agent.ns_create(ns_name['name'], args=args)

        # variable
        # nsdId = args['payload']['nsdId']
        # nsName = args['payload']['nsName']
        # nsDescription = args['payload']['nsDescription']

        # response = self._agent.ns_create(ns_name['name'])  # instantiate NS with given name

        # # return self.instantiate_converter(response)  # response without one parameters value
        # # second option of response format
        # ns_Id = response["service_id"]  # information from ns_instantiation_server
        # ns = self._client.ns_get(ns_Id, args=args)
        # return self._ns_converter(ns)

    def get_ns_list(self, args=None) -> List[Dict]:
        ns = self._client.ns_list()
        return self._ns_converter(ns)

    def get_ns(self, nsId: str, args=None) -> Dict:
        ns = self._client.ns_get(nsId, args=args)
        return self._ns_converter(ns)

    def delete_ns(self, nsId: str, args: Dict = None) -> None:
        service_type = self._client.check_instance_ns_name(nsId)  # check service type
        return self._agent.ns_delete(nsId, args=args)

    def instantiate_ns(self, nsId: str, args: Dict = None) -> None:
        return self._agent.ns_instantiate(nsId, args=args)

    #
    # def scale_ns(self, nsId: str, args: Dict = None) -> None:
    #     pass
    #

    def terminate_ns(self, nsId: str, args: Dict = None) -> None:
        return self._agent.ns_terminate(nsId, args=args)

    def _ns_converter(self, ns):

        if type(ns) is dict:
            result = {
                "id": ns["id"],
                "nsInstanceName": ns['name'],
                "nsInstanceDescription": 'null',
                "nsdId": ns['serviceSpecification']['id'],
                "nsState": 'INSTANTIATED'
            }

        elif type(ns) is list:
            result = []
            for element in ns:
                result.append({
                    "id": element['id'],
                    "nsInstanceName": element['name'],
                    # In ONAP - no description id NS Instance
                    "nsInstanceDescription": 'null',
                    "nsdId": element['serviceSpecification']['id'],
                    # permitted value of nsState: NOT_INSTANTIATED, INSTANTIATED
                    # In ONAP all listed NS are instantiated
                    "nsState": 'INSTANTIATED'
                    })

        return result

    # def instantiate_converter(self, response):  # for first option of response format for ns_create function
    #
    #     vnf_payload = response['vnf_info']["vnf_payload"]
    #     vnf_payload = json.loads(vnf_payload)
    #
    #     result = {
    #             "id": response["instance_id"]["instance_id"],
    #             "nsInstanceName": 'check list of NS instances',
    #             "nsInstanceDescription": 'null',
    #             # nsdId - its better to get that info from get_ls_list function - may cause errors - for tests only
    #             "nsdId": vnf_payload["requestDetails"]["relatedInstanceList"][0]['relatedInstance']['modelInfo']['modelVersionId'],
    #             "nsState": 'INSTANTIATED'
    #         }
    #     return result
