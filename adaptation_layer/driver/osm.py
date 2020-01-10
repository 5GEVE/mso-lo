from typing import Dict, List

from client.osm import Client as Osmclient
from .interface import Driver


class OSM(Driver):

    def __init__(self, nfvo_auth):
        self._nfvo_auth = nfvo_auth
        self._client = Osmclient(**self._nfvo_auth)

    def get_vnf_list(self, args=None) -> list:
        return self._client.vnf_list(args=args)

    def get_vnf(self, vnfId: str, args=None) -> list:
        return self._client.vnf_get(vnfId, args=args)

    def get_ns_list(self, args=None) -> List[Dict]:
        osm_ns_list = self._client.ns_list(args=args)
        sol_ns_list = []
        for osm_ns in osm_ns_list:
            sol_ns_list.append(self._ns_im_converter(osm_ns))
        return sol_ns_list

    def create_ns(self, args=None) -> Dict:
        return self._client.ns_create(args=args)

    def get_ns(self, nsId: str, args=None) -> Dict:
        osm_ns = self._client.ns_get(nsId, args=args)
        return self._ns_im_converter(osm_ns)

    def delete_ns(self, nsId: str, args: Dict = None) -> None:
        return self._client.ns_delete(nsId, args=args)

    def instantiate_ns(self, nsId: str, args=None) -> None:
        return self._client.ns_instantiate(nsId, args=args)

    def terminate_ns(self, nsId: str, args=None) -> None:
        return self._client.ns_terminate(nsId, args=args)

    def scale_ns(self, nsId: str, args=None) -> None:
        return self._client.ns_scale(nsId, args=args)

    def get_op_list(self, args: Dict = None) -> List[Dict]:
        nsId = args['args']['nsInstanceId'] if args['args'] and 'nsInstanceId' in args['args'] else None
        osm_op_list = self._client.ns_op_list(nsId, args=args)
        sol_op_list = []
        for op in osm_op_list:
            sol_op_list.append(self._op_im_converter(op))
        return sol_op_list

    def get_op(self, nsLcmOpId, args: Dict = None) -> Dict:
        op = self._client.ns_op(nsLcmOpId, args=args)
        return self._op_im_converter(op)

    def _ns_im_converter(self, osm_ns: Dict) -> Dict:
        sol_ns = {
            "id": osm_ns['id'],
            "nsInstanceName": osm_ns['name'],
            "nsInstanceDescription": osm_ns['description'],
            "nsdId": osm_ns['nsd-id'],
            "nsState": osm_ns['_admin']['nsState'],
            "vnfInstance": []
        }
        
        osm_vnfs = []
        if 'constituent-vnfr-ref' in osm_ns:
            osm_vnfs = [self._client.vnf_get(vnf_id) for vnf_id in osm_ns["constituent-vnfr-ref"]]
            
        for osm_vnf in osm_vnfs:
            vnf_instance = {
                "id": osm_vnf["id"],
                "vnfdId": osm_vnf["vnfd-id"],
                "vnfProductName": osm_vnf["vnfd-ref"],
                "vimId": osm_vnf["vim-account-id"],
                "instantiationState": osm_ns['_admin']['nsState'],  # same as the NS
            }
            if vnf_instance["instantiationState"] == "INSTANTIATED":
                vnf_instance["instantiatedVnfInfo"] = {"extCpInfo": []}
                vnfpkg = self._client.vnfpkg_get(osm_vnf["vnfd-id"])
                for vdur in osm_vnf["vdur"]:
                    for if_vdur in vdur["interfaces"]:
                        [if_pkg] = [if_pkg for vdu in vnfpkg["vdu"] for if_pkg in vdu["interface"]
                                    if vdu["id"] == vdur["vdu-id-ref"] and if_pkg["name"] == if_vdur["name"]]
                        [cp] = [val for key, val in if_pkg.items() if key.endswith("-connection-point-ref")]
                        try:
                            (ip_address, mac_address) = (if_vdur["ip_address"], if_vdur["mac_address"])
                        except KeyError:
                            (ip_address, mac_address) = (None, None)
                        vnf_instance["instantiatedVnfInfo"]["extCpInfo"].append({
                            "id": cp,
                            "cpProtocolInfo": [
                                {
                                    "layerProtocol": "IP_OVER_ETHERNET",
                                    "ipOverEthernet": {
                                        "macAddress": mac_address,
                                        "ipAddresses": [
                                            {
                                                "type": "IPV4",
                                                "addresses": [ip_address]
                                            }
                                        ]
                                    }
                                }
                            ]
                        })
            sol_ns["vnfInstance"].append(vnf_instance)
        return sol_ns

    @staticmethod
    def _op_im_converter(osm_op):
        sol_op = {
            "id": osm_op["id"],
            "operationState": osm_op["operationState"].upper(),
            "stateEnteredTime": osm_op["statusEnteredTime"],
            "nsInstanceId": osm_op["nsInstanceId"],
            "lcmOperationType": osm_op["lcmOperationType"].upper(),
            "startTime": osm_op["startTime"]
        }
        return sol_op
