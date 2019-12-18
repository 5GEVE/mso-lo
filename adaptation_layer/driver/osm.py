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
        ns_list = self._client.ns_list(args=args)
        return self._ns_list_converter(ns_list)

    def create_ns(self, args=None) -> Dict:
        return self._client.ns_create(args=args)

    def get_ns(self, nsId: str, args=None) -> Dict:
        ns = self._client.ns_get(nsId, args=args)
        vnfs = [self._client.vnf_get(vnf_id) for vnf_id in ns["constituent-vnfr-ref"]]
        return self._ns_im_converter(ns, vnfs)

    def delete_ns(self, nsId: str, args: Dict = None) -> None:
        return self._client.ns_delete(nsId, args=args)

    def instantiate_ns(self, nsId: str, args=None) -> None:
        return self._client.ns_instantiate(nsId, args=args)

    def terminate_ns(self, nsId: str, args=None) -> None:
        return self._client.ns_terminate(nsId, args=args)

    def scale_ns(self, nsId: str, args=None) -> None:
        return self._client.ns_scale(nsId, args=args)

    def get_op_list(self, args: Dict = None) -> List[Dict]:
        nsId = None
        if args['args'] and len(args['args']) > 0:
            nsId = args['args']['nsInstanceId'] if 'nsInstanceId' in args['args'] else None
        return self._client.ns_op_list(nsId, args=args)

    def get_op(self, nsLcmOpId, args: Dict = None) -> Dict:
        return self._client.ns_op(nsLcmOpId, args=args)

    @staticmethod
    def _get_cp_address(cp, osm_vnf, osm_ns):
        """
        OSM does not map a connection-point to its addresses in the GET vnf_instances response.
        Given the connection-point reported in the osm_vnf, we navigate the osm_ns and the nsd field
        to retrieve the vld_id to which the connection-point is connected. We match the connection point id
        and the member-vnf-index.
        Given the vld_id we get the mac_address and ip_address of the connection-point from osm_vnf.
        """
        [vld_id] = [v["id"] for v in osm_ns["nsd"]["vld"] for cpr in v["vnfd-connection-point-ref"]
                    if cpr["vnfd-connection-point-ref"] == cp["name"]
                    and cpr["member-vnf-index-ref"] == osm_vnf["member-vnf-index-ref"]]
        try:
            [(ip_addr, mac_addr)] = [(iface["ip-address"], iface["mac-address"]) for vdur in osm_vnf["vdur"]
                                     for iface in vdur["interfaces"]
                                     if iface["ns-vld-id"] == vld_id]
        except KeyError:
            (ip_addr, mac_addr) = (None, None)
        return ip_addr, mac_addr

    def _ns_im_converter(self, osm_ns: Dict, osm_vnfs: List[Dict]) -> Dict:
        sol_ns = {
            "id": osm_ns['id'],
            "nsInstanceName": osm_ns['name'],
            "nsInstanceDescription": osm_ns['description'],
            "nsdId": osm_ns['nsd-id'],
            "nsState": osm_ns['_admin']['nsState'],
            "vnfInstance": []
        }
        for osm_vnf in osm_vnfs:
            vnf_instance = {
                "id": osm_vnf["id"],
                "vnfdId": osm_vnf["vnfd-id"],
                "vnfProductName": osm_vnf["vnfd-ref"],
                "vimId": osm_vnf["vim-account-id"],
                "instantiationState": osm_ns['_admin']['nsState'],  # same as the NS
            }
            if vnf_instance["instantiationState"] is "INSTANTIATED":
                vnf_instance["instantiatedVnfInfo"]["extCpInfo"] = []
                for cp in osm_vnf["connection-point"]:
                    ip_address, mac_address = self._get_cp_address(cp, osm_vnf, osm_ns)
                    vnf_instance["instantiatedVnfInfo"]["extCpInfo"].append({
                        "id": cp["name"],
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

    def _ns_list_converter(self, ns_list: List[Dict]):
        sol_ns_list = []
        for ns in ns_list:
            vnfs = [self._client.vnf_get(vnf_id) for vnf_id in ns["constituent-vnfr-ref"]]
            sol_ns_list.append(self._ns_im_converter(ns, vnfs))
        return sol_ns_list
