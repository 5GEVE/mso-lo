#  Copyright 2020 Telcaria Ideas S.L.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from __future__ import absolute_import

import datetime
import os
import unittest
import uuid
from typing import Dict, Tuple, List

import requests
import json
import re

from adaptation_layer.error_handler import ResourceNotFound, NsNotFound, \
  BadRequest, ServerError, NsOpNotFound, NsdNotFound
from .interface import Driver, Headers, BodyList, Body

from urllib.parse import urlencode

import logging
logger = logging.getLogger('app.driver.fivegr_so')

TESTING = os.environ.get("TESTING", False)
PRISM_ALIAS = os.environ.get("PRISM_ALIAS", "prism-fivegr-so")


class FIVEGR_SO(Driver):
  """
   ETSI SOL 005 (https://www.etsi.org/deliver/etsi_gs/NFV-SOL/001_099/005/02.06.01_60/gs_NFV-SOL005v020601p.pdf)
   to IFA 003 (https://www.etsi.org/deliver/etsi_gs/NFV-IFA/001_099/013/02.01.01_60/gs_NFV-IFA013v020101p.pdf)
   API translator
  """

  def __init__(self, nfvo_cred):
    self._nfvoId = nfvo_cred["nfvo_id"]
    self._host = nfvo_cred["host"]
    self._port = nfvo_cred["port"] if "port" in nfvo_cred else 8080
    self._headers = {"Content-Type": "application/json",
                     "Accept": "application/json"}
    logger.debug("_host:{} _port:{}".format(self._host, self._port))
    if TESTING is False:
      self._base_path = 'http://{0}:{1}/5gt/so/v1'.format(self._host, self._port)
    else:
      self._base_path = 'http://{0}:{1}'.format(PRISM_ALIAS, 9999)

  def _exec_delete(self, url=None, params=None, headers=None):

    try:
      resp = requests.delete(url, params=params, verify=False, headers=headers)
    except Exception as e:
      raise ServerError(str(e))

    if resp.status_code in (200, 201, 202, 206):
      if 'application/json' in resp.headers['content-type']:
        return resp.json(), resp.headers
      else:
        return resp.text, resp.headers
    elif resp.status_code == 204:
      return None, resp.headers
    elif resp.status_code == 400:
      raise BadRequest()
    elif resp.status_code == 404:
      raise ResourceNotFound()
    else:
      error = resp.json()
      raise ServerError(error)

  def _exec_post(self, url=None, data=None, json=None, headers=None):

    try:
      resp = requests.post(url, data=data, json=json, verify=False, headers=headers)
    except Exception as e:
      raise ServerError(str(e))

    if resp.status_code in (200, 201, 202, 206):
      if 'application/json' in resp.headers['content-type']:
        return resp.json(), resp.headers
      else:
        return resp.text, resp.headers
    elif resp.status_code == 204:
      return None, resp.headers
    elif resp.status_code == 400:
      raise BadRequest()
    elif resp.status_code == 404:
      raise ResourceNotFound()
    else:
      if 'application/json' in resp.headers['content-type']:
        error = resp.json()
      else:
        error = resp.text
      raise ServerError(error)

  def _exec_get(self, url=None, params=None, headers=None):

    try:
      resp = requests.get(url, params=params, verify=False, headers=headers)
    except Exception as e:
      raise ServerError(str(e))

    if resp.status_code in (200, 201, 202, 206):
      if 'application/json' in resp.headers['content-type']:
        return resp.json(), resp.headers
      else:
        return resp.text, resp.headers
    elif resp.status_code == 204:
      return None, resp.headers
    elif resp.status_code == 400:
      raise BadRequest()
    elif resp.status_code == 404:
      raise ResourceNotFound()
    else:
      error = resp.json()
      raise ServerError(error)

  def _exec_put(self, url=None, data=None, json=None, params=None, headers=None):

    try:
      resp = requests.put(url, params=params, verify=False, headers=headers, json=json)
    except Exception as e:
      raise ServerError(str(e))

    if resp.status_code in (200, 201, 202, 206):
      if 'application/json' in resp.headers['content-type']:
        return resp.json(), resp.headers
      else:
        return resp.text, resp.headers
    elif resp.status_code == 204:
      return None, resp.headers
    elif resp.status_code == 400:
      raise BadRequest()
    elif resp.status_code == 404:
      raise ResourceNotFound()
    else:
      error = resp.json()
      raise ServerError(error)

  @staticmethod
  def _build_url_query(base, args=None):
    if args and args['args']:
      url_query = urlencode(args['args'])
      return "{0}?{1}".format(base, url_query)
    return base

  def get_ns_list(self, args: Dict = None) -> Tuple[BodyList, Headers]:
    raise NotImplementedError('get_ns_list is not implemented: 5gr-so does not support retrieving multiple NS')

  def create_ns(self, args: Dict = None) -> Tuple[Body, Headers]:
    logger.info("creating_ns")
    _url = '{0}/ns'.format(self._base_path)
    _url = self._build_url_query(_url, args)
    if 'payload' not in args:
      raise BadRequest()
    try:
      nsIdRaw, resp_headers = self._exec_post(
        _url, json=args['payload'], headers=self._headers)
      nsId = nsIdRaw['nsId']
      logger.debug("nsId:{}".format(nsId))
      # nsInstance, resp_headers = self.get_ns(nsId)  # FIXME get_ns without instantiation does not work in 5gr-so
      sol005NsInstance = SOL005NSInstance(id=nsId, nsInstanceName=args['payload']['nsName'], nsInstanceDescription=args['payload']['nsDescription'], nsState="NOT_INSTANTIATED")

      nsInstance = to_dict(sol005NsInstance)
    except ResourceNotFound:
      nsd_Id = args['payload']['nsdId']
      raise NsdNotFound(nsd_id=nsd_Id)
    headers = self._build_instance_header(nsId)
    logger.info("created_ns")
    return nsInstance, headers

  def get_ns(self, nsId: str, args: Dict = None) -> Tuple[Body, Headers]:
    logger.info("retrieving_ns")
    _url = '{0}/ns/{1}'.format(self._base_path, nsId)
    _url = self._build_url_query(_url, args)
    try:
      nsInfoDict, resp_headers = self._exec_get(_url, headers=self._headers)
      nsInfoDict = nsInfoDict["queryNsResult"][0]
      nsInfo = IFA013NsInfo(**nsInfoDict)
      nsInstance = ifa013nsinfo_to_sol005nsinstance(nsInfo)
    except ResourceNotFound:
      raise NsNotFound(ns_id=nsId)
    headers = {}
    logger.info("retrieved_ns")
    return to_dict(nsInstance), headers

  def delete_ns(self, nsId: str, args: Dict = None) -> Tuple[None, Headers]:
    raise NotImplementedError('delete_ns is not implemented: 5gr-so does not support deleting NS')

  def instantiate_ns(self, nsId: str, args: Dict = None) -> Tuple[None, Headers]:
    logger.info("instantiating_ns")
    _url = '{0}/ns/{1}/instantiate'.format(self._base_path, nsId)
    _url = self._build_url_query(_url, args)
    if 'payload' not in args:
      raise BadRequest(description="Payload not found for id: {}".format(nsId))
    sol005InstantiateNsRequest = SOL005InstantiateNsRequest(**args['payload'])
    ifa013InstantiateNsRequest = sol005InstantiateNsRequest_to_ifa013InstantiateNsRequest(sol005InstantiateNsRequest)
    ifa013InstantiateNsRequestDict = to_dict(ifa013InstantiateNsRequest)
    try:
      operationIdRaw, resp_headers = self._exec_put(
        _url, headers=self._headers, json=ifa013InstantiateNsRequestDict)
    except ResourceNotFound:
      raise NsNotFound(ns_id=nsId)
    operationId = operationIdRaw["operationId"]
    headers = self._build_lcm_op_occs_header(operationId)
    logger.debug("operationId:{}".format(operationId))
    logger.info("instantiating_ns operation submitted")
    return None, headers

  def terminate_ns(self, nsId: str, args: Dict = None) -> Tuple[None, Headers]:
    logger.info("terminating_ns")
    _url = '{0}/ns/{1}/terminate'.format(self._base_path, nsId)
    _url = self._build_url_query(_url, args)
    try:
      operationIdRaw, resp_headers = self._exec_put(
        _url)
    except ResourceNotFound:
      raise NsNotFound(ns_id=nsId)
    operationId = operationIdRaw["operationId"]
    headers = self._build_lcm_op_occs_header(operationId)
    logger.debug("operationId:{}".format(operationId))
    logger.info("terminating_ns operation submitted")
    return None, headers

  def scale_ns(self, nsId: str, args: Dict = None) -> Tuple[None, Headers]:
    logger.info("scaling_ns")
    _url = "{0}/ns/{1}/scale".format(
      self._base_path, nsId)
    _url = self._build_url_query(_url, args)
    sol005ScaleNsRequest = SOL005ScaleNsRequest(**args['payload'])
    ifa013ScaleNsRequest = sol005ScaleNsRequest_to_ifa013ScaleNsRequest(nsId, sol005ScaleNsRequest)
    ifa013ScaleNsRequestDict = to_dict(ifa013ScaleNsRequest)
    try:
      operationIdRaw, resp_headers = self._exec_put(
        _url, json=ifa013ScaleNsRequestDict, headers=self._headers)
    except ResourceNotFound:
      raise NsNotFound(ns_id=id)
    operationId = operationIdRaw["operationId"]
    headers = self._build_lcm_op_occs_header(operationId)
    logger.debug("operationId:{}".format(operationId))
    logger.info("scaling_ns operation submitted")
    return None, headers

  def get_op_list(self, args: Dict = None) -> Tuple[BodyList, Headers]:
    raise NotImplementedError('get_op_list is not implemented: 5gr-so does not support querying multiple operations')

  def get_op(self, nsLcmOpId, args: Dict = None) -> Tuple[Body, Headers]:
    _url = '{0}/operation/{1}'.format(self._base_path, nsLcmOpId)
    _url = self._build_url_query(_url, args)
    try:
      lcmOpStatusRaw, resp_headers = self._exec_get(_url, headers=self._headers)
    except ResourceNotFound:
      raise NsOpNotFound(ns_op_id=nsLcmOpId)
    lcmOpStatus = lcmOpStatusRaw["status"]
    sol005NsLcmOpOcc = ifa013OperationStatus_to_sol005NsLcmOpOcc(nsLcmOpId, lcmOpStatus)
    headers = {}
    return to_dict(sol005NsLcmOpOcc), headers

  def _build_instance_header(self, instance_id):
    headers = {'location': '/nfvo/{0}/ns_instances/{1}'.format(
      self._nfvoId, instance_id)}
    return headers

  def _build_lcm_op_occs_header(self, operation_id):
    headers = {'location': '/nfvo/{0}/ns_lcm_op_occs/{1}'.format(
      self._nfvoId, operation_id)}
    return headers


# IFA 013 - Information Model

class IFA013SapData:
  def __init__(self, sapdId="", sapName="", description="", address="", **kwargs):
    self.sapdId: str = sapdId
    self.sapName: str = sapName
    self.description: str = description
    self.address: str = address


class IFA013PnfExtCpInfo:
  def __init__(self, cpdId="", address="", **kwargs):
    self.cpdId: str = cpdId
    self.address: str = address


class IFA013PnfInfo:
  def __init__(self, pnfName="", pnfdinfoId="", cpInfo=None, **kwargs):
    self.pnfName: str = pnfName
    self.pnfdinfoId: str = pnfdinfoId
    self.cpInfo: List[IFA013PnfExtCpInfo] = []
    [self.cpInfo.append(IFA013PnfExtCpInfo(**element)) for element in cpInfo or []]


class IFA013VnfInstanceData:
  def __init__(self, vnfInstanceId="", vnfProfileId="", **kwargs):
    self.vnfInstanceId: str = vnfInstanceId
    self.vnfProfileId: str = vnfProfileId


class IFA013VnfLocationConstraint:
  def __init__(self, vnfProfileId="", locationConstraints="", **kwargs):
    self.vnfProfileId: str = vnfProfileId
    self.locationConstraints: str = locationConstraints


class IFA013ParamsForVnf:
  def __init__(self, vnfProfileId="", additionalParam=None, **kwargs):
    self.vnfProfileId: str = vnfProfileId
    self.additionalParam: Dict = {}
    if additionalParam is not None: self.additionalParam = additionalParam


class IFA013AffinityOrAntiAffinityRule:
  def __init__(self, descriptorId="", vnfInstanceId="", affinityOrAntiAffinity=True, scope="", **kwargs):
    self.descriptorId: str = descriptorId
    self.vnfInstanceId: str = vnfInstanceId
    self.affinityOrAntiAffinity: bool = affinityOrAntiAffinity
    self.scope: str = scope


class IFA013ResourceHandle:
  def __init__(self, vimId="", resourceProviderId="", resourceId="", **kwargs):
    self.vimId: str = vimId
    self.resourceProviderId: str = resourceProviderId
    self.resourceId: str = resourceId


class IFA013NsLinkPort:
  def __init__(self, resourceHandle=None, cpId="", **kwargs):
    self.resourceHandle: IFA013ResourceHandle = IFA013ResourceHandle()
    if resourceHandle is not None:
      self.resourceHandle: IFA013ResourceHandle = IFA013ResourceHandle(**resourceHandle)
    self.cpId: str = cpId


class IFA013NsVirtualLinkInfo:
  def __init__(self, nsVirtualLinkDescId="", resourceHandle=None, linkPort=None, **kwargs):
    self.nsVirtualLinkDescId: str = nsVirtualLinkDescId
    self.resourceHandle: List[IFA013ResourceHandle] = []  # IFA013ResourceHandle
    [self.resourceHandle.append(IFA013ResourceHandle(**element)) for element in resourceHandle or []]
    self.linkPort: List[IFA013NsLinkPort] = []  # NsLinkPort
    [self.linkPort.append(IFA013NsLinkPort(**element)) for element in linkPort or []]


class UserAccessInfo:
  def __init__(self, address="", sapdId="", vnfdId="", **kwargs):
    self.address: str = address
    self.sapdId: str = sapdId
    self.vnfdId: str = vnfdId


class IFA013SapInfo:
  def __init__(self, sapInstanceId="", sapdId="", sapName="", description="", address="", userAccessInfo=None, **kwargs):
    self.sapInstanceId: str = sapInstanceId
    self.sapdId: str = sapdId
    self.sapName: str = sapName
    self.description: str = description
    self.address: str = address
    self.userAccessInfo: List[UserAccessInfo] = []
    [self.userAccessInfo.append(UserAccessInfo(**element)) for element in userAccessInfo or []]


class IFA013Nfp:
  def __init__(self, nfpId="", cpId=None, totalCp=0, nfpRule="", nfpState="", **kwargs):
    self.nfpId: str = nfpId
    self.cpId: List[str] = cpId  # String
    self.totalCp: int = totalCp
    self.nfpRule: str = nfpRule  # Rule
    self.nfpState: str = nfpState


class IFA013VnffgInfo:
  def __init__(self, vnffgId="", vnffgdId="", vnfId=None, pnfId=None, virtualLinkId=None, cpId=None, nfp=None, **kwargs):
    self.vnffgId: str = vnffgId
    self.vnffgdId: str = vnffgdId
    self.vnfId: List[str] = []  # String
    [self.vnfId.append(element) for element in vnfId or []]
    self.pnfId: List[str] = []  # String
    [self.pnfId.append(element) for element in pnfId or []]
    self.virtualLinkId: List[str] = []  # String
    [self.virtualLinkId.append(element) for element in virtualLinkId or []]
    self.cpId: List[str] = []  # String
    [self.cpId.append(element) for element in cpId or []]
    self.nfp: List[IFA013Nfp] = []  # Nfp
    [self.nfp.append(IFA013Nfp(**element)) for element in nfp or []]


class IFA013NsScaleInfo:
  def __init__(self, nsScalingAspectId="", nsScaleLevelId="", **kwargs):
    self.nsScalingAspectId: str = nsScalingAspectId
    self.nsScaleLevelId: str = nsScaleLevelId


class IFA013ScaleNsByStepsData:
  def __init__(self, scalingDirection="", aspectId="", numberOfSteps=1, **kwargs):
    self.scalingDirection: str = scalingDirection
    self.aspectId: str = aspectId
    self.numberOfSteps: int = numberOfSteps


class IFA013ScaleNsToLevelData:
  def __init__(self, nsInstantiationLevel="", nsScaleInfo=None, **kwargs):
    self.nsInstantiationLevel: str = nsInstantiationLevel
    self.nsScaleInfo: List[IFA013NsScaleInfo] = []  # NsScaleInfo
    [self.nsScaleInfo.append(IFA013NsScaleInfo(**element)) for element in nsScaleInfo or []]


class IFA013ScaleNsData:
  def __init__(self, vnfInstanceToBeAdded=None, vnfInstanceToBeRemoved=None, scaleNsByStepsData=None,
               scaleNsToLevelData=None, additionalParamForNs=None, **kwargs):
    self.vnfInstanceToBeAdded: List[IFA013VnfInstanceData] = []  # VnfInstanceData
    [self.vnfInstanceToBeAdded.append(IFA013VnfInstanceData(**element)) for element in vnfInstanceToBeAdded or []]
    self.vnfInstanceToBeRemoved: List[str] = []  # String
    [self.vnfInstanceToBeRemoved.append(element) for element in vnfInstanceToBeRemoved or []]
    self.scaleNsByStepsData: IFA013ScaleNsByStepsData = IFA013ScaleNsByStepsData()
    if scaleNsByStepsData is not None:
      self.scaleNsByStepsData: IFA013ScaleNsByStepsData = IFA013ScaleNsByStepsData(**scaleNsByStepsData)
    self.scaleNsByStepsData: IFA013ScaleNsToLevelData = IFA013ScaleNsToLevelData()
    if scaleNsToLevelData is not None:
      self.scaleNsToLevelData: IFA013ScaleNsToLevelData = IFA013ScaleNsToLevelData(**scaleNsToLevelData)
    self.additionalParamForNs: Dict = {}
    if additionalParamForNs is not None: self.additionalParamForNs = additionalParamForNs


class IFA013ScaleInfo:
  def __init__(self, aspectId="", scaleLevel=0, **kwargs):
    self.aspectId: str = aspectId
    self.scaleLevel: int = scaleLevel


class IFA013ScaleToLevelData:
  def __init__(self, instantiationLevelId="", scaleInfo=None, additionalParam=None, **kwargs):
    self.instantiationLevelId: str = instantiationLevelId
    self.scaleInfo: List[IFA013ScaleInfo] = []  # ScaleInfo
    [self.scaleInfo.append(IFA013ScaleInfo(**element)) for element in scaleInfo or []]
    self.additionalParam: Dict = {}
    if additionalParam is not None: self.additionalParam = additionalParam


class IFA013ScaleByStepData:
  def __init__(self, type="", aspectId="", numberOfSteps=1, additionalParam=None, **kwargs):
    self.type: str = type
    self.aspectId: str = aspectId
    self.numberOfSteps: int = numberOfSteps
    self.additionalParam: Dict = {}
    if additionalParam is not None: self.additionalParam = additionalParam


class IFA013ScaleVnfData:
  def __init__(self, vnfInstanceId="", type="", scaleToLevelData=None, scaleByStepData=None, **kwargs):
    self.vnfInstanceId: str = vnfInstanceId
    self.type: str = type
    if scaleToLevelData is not None:
      self.scaleToLevelData: IFA013ScaleToLevelData = IFA013ScaleToLevelData(**scaleToLevelData)
    if scaleByStepData is not None:
      self.scaleByStepData: IFA013ScaleByStepData = IFA013ScaleByStepData(**scaleByStepData)


class IFA013ScaleNsRequest:
  def __init__(self, nsInstanceId="", scaleType="", scaleNsData=None, scaleVnfData=None, scaleTime=None, **kwargs):
    self.nsInstanceId: str = nsInstanceId
    self.scaleType: str = scaleType
    if scaleNsData is not None:
      self.scaleNsData: IFA013ScaleNsData = IFA013ScaleNsData(**scaleNsData)
    if scaleVnfData is not None:
      self.scaleVnfData: List[IFA013ScaleVnfData] = []  # ScaleVnfData
      [self.scaleVnfData.append(IFA013ScaleVnfData(**element)) for element in scaleVnfData or []]
    self.scaleTime: str = scaleTime


class IFA013NsInfo:
  def __init__(self, nsInstanceId="", nsName="", description="", nsdId="", flavourId="", vnfInfoId=None, pnfInfo=None,
               virtualLinkInfo=None, vnffgInfo=None, sapInfo=None, nestedNsInfoId=None, nsState="", nsScaleStatus=None,
               additionalAffinityOrAntiAffinityRule=None, **kwargs):
    self.nsInstanceId: str = nsInstanceId
    self.nsName: str = nsName
    self.description: str = description
    self.nsdId: str = nsdId
    self.flavourId: str = flavourId
    self.vnfInfoId: List[str] = []  # String
    [self.vnfInfoId.append(**element) for element in vnfInfoId or []]
    self.pnfInfo: List[IFA013PnfInfo] = []  # PnfInfo
    [self.pnfInfo.append(IFA013PnfInfo(**element)) for element in pnfInfo or []]
    self.virtualLinkInfo: List[IFA013NsVirtualLinkInfo] = []  # NsVirtualLinkInfo
    [self.virtualLinkInfo.append(IFA013NsVirtualLinkInfo(**element)) for element in virtualLinkInfo or []]
    self.vnffgInfo: List[IFA013VnffgInfo] = []  # VnffgInfo
    [self.vnffgInfo.append(IFA013VnffgInfo(**element)) for element in vnffgInfo or []]
    self.sapInfo: List[IFA013SapInfo] = []  # SapInfo
    [self.sapInfo.append(IFA013SapInfo(**element)) for element in sapInfo or []]
    self.nestedNsInfoId: List[str] = []  # String
    [self.nestedNsInfoId.append(element) for element in nestedNsInfoId or []]
    self.nsState: str = nsState
    self.nsScaleStatus: List[IFA013NsScaleInfo] = []  # NsScaleInfo
    [self.nsScaleStatus.append(IFA013NsScaleInfo(**element)) for element in nsScaleStatus or []]
    self.additionalAffinityOrAntiAffinityRule: List[IFA013AffinityOrAntiAffinityRule] = []  # AffinityOrAntiAffinityRule
    [self.additionalAffinityOrAntiAffinityRule.append(IFA013AffinityOrAntiAffinityRule(**element)) for element in
     additionalAffinityOrAntiAffinityRule or []]


class IFA013QueryNsRequest:
  def __init__(self, filter="", attributeSelector=None, **kwargs):
    self.filter: str = filter
    self.attributeSelector: List[str] = []  # String
    [self.attributeSelector.append(element) for element in attributeSelector or []]


class IFA013QueryNsResponse:
  def __init__(self, queryNsResult=None, **kwargs):
    self.queryNsResult: List[IFA013NsInfo] = []  # NsInfo
    [self.queryNsResult.append(IFA013NsInfo(**element)) for element in queryNsResult or []]


class IFA013CreateNsIdentifierRequest:
  def __init__(self, nsdId="", nsName="", nsDescription="", **kwargs):
    self.nsdId: str = nsdId
    self.nsName: str = nsName
    self.nsDescription: str = nsDescription


class IFA013InstantiateNsRequest:
  def __init__(self, nsInstanceId="", flavourId="", sapData=None, pnfInfo=None, vnfInstanceData=None,
               nestedNsInstanceId="", locationConstraints=None, additionalParamForNs=None, additionalParamForVnf=None,
               startTime="", nsInstantiationLevelId="", additionalAffinityOrAntiAffiniityRule=None, **kwargs):
    self.nsInstanceId: str = nsInstanceId
    self.flavourId: str = flavourId
    self.sapData: List[IFA013SapData] = []
    [self.sapData.append(IFA013SapData(**element)) for element in sapData or []]
    self.pnfInfo: List[IFA013PnfInfo] = []
    [self.pnfInfo.append(IFA013PnfInfo(**element)) for element in pnfInfo or []]
    self.vnfInstanceData: List[IFA013VnfInstanceData] = []
    [self.vnfInstanceData.append(IFA013VnfInstanceData(**element)) for element in vnfInstanceData or []]
    self.nestedNsInstanceId: str = nestedNsInstanceId
    self.locationConstraints: List[IFA013VnfLocationConstraint] = []
    [self.locationConstraints.append(IFA013VnfLocationConstraint(**element)) for element in locationConstraints or []]
    self.additionalParamForNs: Dict = {}
    if additionalParamForNs is not None: self.additionalParamForNs = additionalParamForNs
    self.additionalParamForVnf: List[IFA013ParamsForVnf] = []
    [self.additionalParamForVnf.append(IFA013ParamsForVnf(**element)) for element in additionalParamForVnf or []]
    self.startTime: str = startTime
    self.nsInstantiationLevelId: str = nsInstantiationLevelId
    self.additionalAffinityOrAntiAffiniityRule: List[IFA013AffinityOrAntiAffinityRule] = []
    [self.additionalAffinityOrAntiAffiniityRule.append(IFA013AffinityOrAntiAffinityRule(**element)) for element in
     additionalAffinityOrAntiAffiniityRule or []]


# SOL 005 - Information Model


class SOL005CreateNsIdentifierRequest:
  def __init__(self, nsdId="", nsName="", nsDescription="", **kwargs):
    self.nsdId: str = nsdId
    self.nsName: str = nsName
    self.nsDescription: str = nsDescription


class SOL005IpOverEthernetAddressData:
  def __init__(self, macAddress="", ipAddresses=None, **kwargs):
    self.macAddress: str = macAddress
    self.ipAddresses: List[str] = []
    [self.ipAddresses.append(element) for element in ipAddresses or []]


class SOL005CpProtocolData:
  def __init__(self, layerProtocol="", ipOverEthernet=None, **kwargs):
    self.layerProtocol: str = layerProtocol
    self.ipOverEthernet: SOL005IpOverEthernetAddressData = SOL005IpOverEthernetAddressData()
    if ipOverEthernet is not None:
      self.ipOverEthernet: SOL005IpOverEthernetAddressData = SOL005IpOverEthernetAddressData(**ipOverEthernet)


class SOL005PnfExtCpInfo:
  def __init__(self, cpInstanceId="", cpdId="", cpProtocolData="", **kwargs):
    self.cpInstanceId: str = cpInstanceId
    self.cpdId: str = cpdId
    self.cpProtocolData: List[SOL005CpProtocolData] = []  # CpProtocolData
    [self.cpProtocolData.append(SOL005CpProtocolData(**element)) for element in cpProtocolData or []]


class SOL005PnfInfo:
  def __init__(self, pnfId="", pnfName="", pnfdId="", pnfdInfoId="", pnfProfileId="", cpInfo=None, **kwargs):
    self.pnfId: str = pnfId
    self.pnfName: str = pnfName
    self.pnfdId: str = pnfdId
    self.pnfdInfoId: str = pnfdInfoId
    self.pnfProfileId: str = pnfProfileId
    self.cpInfo: List[SOL005PnfExtCpInfo] = []  # PnfExtCpInfo
    [self.cpInfo.append(SOL005PnfExtCpInfo(**element)) for element in cpInfo or []]


class SOL005VnfInstance:
  def __init__(self, id="", vnfInstanceName="", vnfInstanceDescription="", vnfdId="", vnfProvider="", vnfProductName="",
               vnfSoftwareVersion="", vnfdVersion="", vnfPkgId="", vnfConfigurableProperties=None, vimId="",
               instantiationState="", instantiatedVnfInfo="", **kwargs):
    self.id: str = id
    self.vnfInstanceName: str = vnfInstanceName
    self.vnfInstanceDescription: str = vnfInstanceDescription
    self.vnfdId: str = vnfdId
    self.vnfProvider: str = vnfProvider
    self.vnfProductName: str = vnfProductName
    self.vnfSoftwareVersion: str = vnfSoftwareVersion
    self.vnfdVersion: str = vnfdVersion
    self.vnfPkgId: str = vnfPkgId
    self.vnfConfigurableProperties: Dict = {}
    if vnfConfigurableProperties is not None: self.additionalParamForNs = vnfConfigurableProperties
    self.vimId: str = vimId
    self.instantiationState: str = instantiationState
    self.instantiatedVnfInfo: str = instantiatedVnfInfo


class SOL005ResourceHandle:
  def __init__(self, vimId="", resourceProviderId="", resourceId="", vimLevelResourceType="", **kwargs):
    self.vimId: str = vimId
    self.resourceProviderId: str = resourceProviderId
    self.resourceId: str = resourceId
    self.vimLevelResourceType: str = vimLevelResourceType


class SOL005NsCpHandle:
  def __init__(self, vnfInstanceId="", vnfExtCpInstanceId="", pnfInfoId="", pnfExtCpInstanceId="", nsInstanceId="",
               nsSapInstanceId="", **kwargs):
    self.vnfInstanceId: str = vnfInstanceId
    self.vnfExtCpInstanceId: str = vnfExtCpInstanceId
    self.pnfInfoId: str = pnfInfoId
    self.pnfExtCpInstanceId: str = pnfExtCpInstanceId
    self.nsInstanceId: str = nsInstanceId
    self.nsSapInstanceId: str = nsSapInstanceId


class SOL005NsLinkPortInfo:
  def __init__(self, id="", resourceHandle=None, nsCpHandle=None, **kwargs):
    self.id: str = id
    self.resourceHandle: SOL005ResourceHandle = SOL005ResourceHandle()
    if resourceHandle is not None:
      self.resourceHandle: SOL005ResourceHandle = SOL005ResourceHandle(**resourceHandle)
    self.nsCpHandle: SOL005NsCpHandle = SOL005NsCpHandle()
    if nsCpHandle is not None:
      self.nsCpHandle: SOL005NsCpHandle = SOL005NsCpHandle(**nsCpHandle)


class SOL005NsVirtualLinkInfo:
  def __init__(self, id="", nsVirtualLinkDescId="", nsVirtualLinkProfileId="", resourceHandle=None, linkPort=None, **kwargs):
    self.id: str = id
    self.nsVirtualLinkDescId: str = nsVirtualLinkDescId
    self.nsVirtualLinkProfileId: str = nsVirtualLinkProfileId
    self.resourceHandle: List[SOL005ResourceHandle] = []
    [self.resourceHandle.append(SOL005ResourceHandle(**element)) for element in resourceHandle or []]
    self.linkPort: List[SOL005NsLinkPortInfo] = []
    [self.linkPort.append(SOL005NsLinkPortInfo(**element)) for element in linkPort or []]


class SOL005CpPairInfo:
  def __init__(self, vnfExtCpIds=None, pnfExtCpIds=None, sapIds=None, **kwargs):
    self.vnfExtCpIds: List[str] = []
    [self.vnfExtCpIds.append(element) for element in vnfExtCpIds or []]
    self.pnfExtCpIds: List[str] = []
    [self.pnfExtCpIds.append(element) for element in pnfExtCpIds or []]
    self.sapIds: List[str] = []
    [self.sapIds.append(element) for element in sapIds or []]


class SOL005ForwardingBehaviourInputParameters:
  def __init__(self, algortihmName="", algorithmWeights=None, **kwargs):
    self.algortihmName: str = algortihmName
    self.algorithmWeights: List[int] = []
    [self.algorithmWeights.append(element) for element in algorithmWeights or []]


class SOL005CpGroupInfo:
  def __init__(self, cpPairInfo=None, forwardingBehaviour="", forwardingBehaviourInputParameters=None, **kwargs):
    self.cpPairInfo: SOL005CpPairInfo = SOL005CpPairInfo()
    if cpPairInfo is not None:
      self.cpPairInfo: SOL005CpPairInfo = SOL005CpPairInfo(**cpPairInfo)
    self.forwardingBehaviour: str = forwardingBehaviour
    self.forwardingBehaviourInputParameters: SOL005ForwardingBehaviourInputParameters = SOL005ForwardingBehaviourInputParameters()
    if forwardingBehaviourInputParameters is not None:
      self.forwardingBehaviourInputParameters: SOL005ForwardingBehaviourInputParameters = SOL005ForwardingBehaviourInputParameters(
        **forwardingBehaviourInputParameters)


class SOL005NfpRule:
  def __init__(self, etherDestinationAddress="", etherSourceAddress="", etherType="", vlanTag="", protocol="", dscp="",
               sourcePortRange="", destinationPortRange="", sourceIpAddressPrefix="", destinationIpAddressPrefix="",
               extendedCriteria="", **kwargs):
    self.etherDestinationAddress: str = etherDestinationAddress
    self.etherSourceAddress: str = etherSourceAddress
    self.etherType: str = etherType
    self.vlanTag: str = vlanTag
    self.protocol: str = protocol
    self.dscp: str = dscp
    self.sourcePortRange: str = sourcePortRange
    self.destinationPortRange: str = destinationPortRange
    self.sourceIpAddressPrefix: str = sourceIpAddressPrefix
    self.destinationIpAddressPrefix: str = destinationIpAddressPrefix
    self.extendedCriteria: str = extendedCriteria


class SOL005NfpInfo:
  def __init__(self, id="", nfpdId="", nfpName="", description="", cpGroup=None, totalCp="", nfpRule=None, nfpState="", **kwargs):
    self.id: str = id
    self.nfpdId: str = nfpdId
    self.nfpName: str = nfpName
    self.description: str = description
    self.cpGroup: SOL005CpGroupInfo = SOL005CpGroupInfo()
    if cpGroup is not None:
      self.cpGroup: SOL005CpGroupInfo = SOL005CpGroupInfo(**cpGroup)
    self.totalCp: str = totalCp
    self.nfpRule: SOL005NfpRule = SOL005NfpRule()
    if nfpRule is not None:
      self.nfpRule: SOL005NfpRule = SOL005NfpRule(**nfpRule)
    self.nfpState: str = nfpState


class SOL005VnffgInfo:
  def __init__(self, id="", vnffgdId="", vnfInstanceId="", pnfInfoId="", nsVirtualLinkInfoId="", nsCpHandle=None,
               nfpInfo=None, **kwargs):
    self.id: str = id
    self.vnffgdId: str = vnffgdId
    self.vnfInstanceId: str = vnfInstanceId
    self.pnfInfoId: str = pnfInfoId
    self.nsVirtualLinkInfoId: str = nsVirtualLinkInfoId
    self.nsCpHandle: SOL005NsCpHandle = SOL005NsCpHandle()
    if nsCpHandle is not None:
      self.nsCpHandle: SOL005NsCpHandle = SOL005NsCpHandle(**nsCpHandle)
    self.nfpInfo: SOL005NfpInfo = SOL005NfpInfo()
    if nfpInfo is not None:
      self.nfpInfo: SOL005NfpInfo = SOL005NfpInfo(**nfpInfo)


class SOL005IpOverEthernetAddressInfo:
  def __init__(self, macAddress="", ipAddresses=None, **kwargs):
    self.macAddress: str = macAddress
    self.ipAddresses: List[str] = []
    [self.ipAddresses.append(element) for element in ipAddresses or []]


class SOL005CpProtocolInfo:
  def __init__(self, layerProtocol="IP_OVER_ETHERNET", ipOverEthernet=None, **kwargs):
    self.layerProtocol: str = layerProtocol
    self.ipOverEthernet: SOL005IpOverEthernetAddressInfo = SOL005IpOverEthernetAddressInfo()
    if ipOverEthernet is not None:
      self.ipOverEthernet: SOL005IpOverEthernetAddressInfo = SOL005IpOverEthernetAddressInfo(**ipOverEthernet)


class SOL005SapInfo:
  def __init__(self, id="", sapdId="", sapName="", description="", sapProtocolInfo=None, **kwargs):
    self.id: str = id
    self.sapdId: str = sapdId
    self.sapName: str = sapName
    self.description: str = description
    self.sapProtocolInfo: List[SOL005CpProtocolInfo] = []
    [self.sapProtocolInfo.append(element) for element in sapProtocolInfo or []]
    #self.userAccessInfo: List[UserAccessInfo] = []
    #[self.userAccessInfo.append(element) for element in userAccessInfo or []]


class SOL005NsScaleInfo:
  def __init__(self, nsScalingAspectId="", nsScaleLevelId="", **kwargs):
    self.nsScalingAspectId: str = nsScalingAspectId
    self.nsScaleLevelId: str = nsScaleLevelId


class SOL005AffinityOrAntiAffinityRule:
  def __init__(self, vnfdId="", vnfProfileId="", vnfInstanceId="", affinityOrAntiAffinity="", scope="", **kwargs):
    self.vnfdId: str = vnfdId
    self.vnfProfileId: str = vnfProfileId
    self.vnfInstanceId: str = vnfInstanceId
    self.affinityOrAntiAffinity: str = affinityOrAntiAffinity
    self.scope: str = scope


class SOL005NSInstance:
  def __init__(self, id="", nsInstanceName="", nsInstanceDescription="", nsdId="", nsdInfoId="", flavourId="",
               vnfInstance=None, pnfInfo=None, virtualLinkInfo=None, vnffgInfo=None, sapInfo=None,
               nestedNsInstanceId=None, nsState="", monitoringParameter=None, nsScaleStatus=None,
               additionalAffinityOrAntiAffinityRule=None, **kwargs):
    self.id: str = id
    self.nsInstanceName: str = nsInstanceName
    self.nsInstanceDescription: str = nsInstanceDescription
    self.nsdId: str = nsdId
    self.nsdInfoId: str = nsdInfoId
    self.flavourId: str = flavourId
    self.vnfInstance: List[SOL005VnfInstance] = []
    [self.vnfInstance.append(SOL005VnfInstance(**element)) for element in vnfInstance or []]
    self.pnfInfo: List[SOL005PnfInfo] = []
    [self.pnfInfo.append(SOL005PnfInfo(**element)) for element in pnfInfo or []]
    self.virtualLinkInfo: List[SOL005NsVirtualLinkInfo] = []
    [self.virtualLinkInfo.append(SOL005NsVirtualLinkInfo(**element)) for element in virtualLinkInfo or []]
    self.vnffgInfo: List[SOL005VnffgInfo] = []
    [self.vnffgInfo.append(SOL005VnffgInfo(**element)) for element in vnffgInfo or []]
    self.sapInfo: List[SOL005SapInfo] = []
    [self.sapInfo.append(SOL005SapInfo(**element)) for element in sapInfo or []]
    self.nestedNsInstanceId: List[str] = []
    [self.nestedNsInstanceId.append(element) for element in nestedNsInstanceId or []]
    self.nsState: str = nsState
    self.monitoringParameter = monitoringParameter
    self.nsScaleStatus: List[SOL005NsScaleInfo] = []
    [self.nsScaleStatus.append(SOL005NsScaleInfo(**element)) for element in nsScaleStatus or []]
    self.additionalAffinityOrAntiAffinityRule: List[SOL005AffinityOrAntiAffinityRule] = []
    [self.additionalAffinityOrAntiAffinityRule.append(SOL005AffinityOrAntiAffinityRule(**element)) for element in additionalAffinityOrAntiAffinityRule or []]


class SOL005SapData:
  def __init__(self, sapdId="", sapName="", description="", sapProtocolData=None, **kwargs):
    self.sapdId: str = sapdId
    self.sapName: str = sapName
    self.description: str = description
    self.sapProtocolData: List[SOL005CpProtocolData] = []
    [self.sapProtocolData.append(SOL005CpProtocolData(**element)) for element in sapProtocolData or []]


class SOL005PnfExtCpData:
  def __init__(self, cpInstanceI16, cpdId, cpProtocolData=None, **kwargs):
    self.cpInstanceI16: str = cpInstanceI16
    self.cpdId: str = cpdId
    self.cpProtocolData: List[SOL005CpProtocolData] = []
    [self.cpProtocolData.append(SOL005CpProtocolData(**element)) for element in cpProtocolData or []]


class SOL005AddPnfData:
  def __init__(self, pnfId="", pnfName="", pnfdId="", pnfProfileId="", cpData=None, **kwargs):
    self.pnfId: str = pnfId
    self.pnfName: str = pnfName
    self.pnfdId: str = pnfdId
    self.pnfProfileId: str = pnfProfileId
    self.cpData: List[SOL005PnfExtCpData] = []
    [self.cpData.append(SOL005PnfExtCpData(**element)) for element in cpData or []]


class SOL005VnfInstanceData:
  def __init__(self, vnfInstanceId="", vnfProfileId="", **kwargs):
    self.vnfInstanceId: str = vnfInstanceId
    self.vnfProfileId: str = vnfProfileId


class SOL005NestedNsInstanceData:
  def __init__(self, nestedNsInstanceId="", nsProfileId="", **kwargs):
    self.nestedNsInstanceId: str = nestedNsInstanceId
    self.nsProfileId: str = nsProfileId


class SOL005LocationConstraints:
  def __init__(self, countryCode="", civicAddressElement="", **kwargs):
    self.countryCode: str = countryCode
    self.civicAddressElement: str = civicAddressElement


class SOL005VnfLocationConstraint:
  def __init__(self, vnfProfileId="", locationConstraints=None, **kwargs):
    self.vnfProfileId: str = vnfProfileId
    self.locationConstraints: SOL005LocationConstraints = SOL005LocationConstraints()
    if locationConstraints is not None:
      self.locationConstraints: SOL005LocationConstraints = SOL005LocationConstraints(**locationConstraints)


class SOL005ParamForNestedNs:
  def __init__(self, nsProfileId="", additionalParam=None, **kwargs):
    self.nsProfileId: str = nsProfileId
    self.additionalParam: Dict = {}
    if additionalParam is not None: self.additionalParam = additionalParam


class SOL005ParamsForVnf:
  def __init__(self, vnfProfileId="", additionalParams=None, **kwargs):
    self.vnfProfileId: str = vnfProfileId
    self.additionalParams: Dict = {}
    if additionalParams is not None: self.additionalParams = additionalParams


class SOL005InstantiateNsRequest:
  def __init__(self, nsFlavourId="", sapData=None, addpnfData=None, vnfInstanceData=None, nestedNsInstanceData=None,
               locationConstraints=None, additionalParamsForNs=None, additionalParamForNestedNs=None,
               additionalParamsForVnf=None, startTime="", nsInstantiationLevelId=None,
               additionalAffinityOrAntiAffinityRule=None, **kwargs):
    self.nsFlavourId: str = nsFlavourId
    self.sapData: List[SOL005SapData] = []
    [self.sapData.append(SOL005SapData(**element)) for element in sapData or []]
    self.addpnfData: List[SOL005AddPnfData] = []
    [self.addpnfData.append(SOL005AddPnfData(**element)) for element in addpnfData or []]
    self.vnfInstanceData: List[SOL005VnfInstanceData] = []
    [self.vnfInstanceData.append(SOL005VnfInstanceData(**element)) for element in vnfInstanceData or []]
    self.nestedNsInstanceData: List[SOL005NestedNsInstanceData] = []
    [self.nestedNsInstanceData.append(SOL005NestedNsInstanceData(**element)) for element in nestedNsInstanceData or []]
    self.locationConstraints: List[SOL005VnfLocationConstraint] = []
    [self.locationConstraints.append(SOL005VnfLocationConstraint(**element)) for element in locationConstraints or []]
    self.additionalParamsForNs: Dict = {}
    if additionalParamsForNs is not None: self.additionalParamsForNs = additionalParamsForNs
    self.additionalParamForNestedNs: List[SOL005ParamForNestedNs] = []
    [self.additionalParamForNestedNs.append(SOL005ParamForNestedNs(**element)) for element in
     additionalParamForNestedNs or []]
    self.additionalParamsForVnf: List[SOL005ParamsForVnf] = []
    [self.additionalParamsForVnf.append(SOL005ParamsForVnf(**element)) for element in additionalParamsForVnf or []]
    self.startTime: str = startTime
    self.nsInstantiationLevelId: str = nsInstantiationLevelId
    self.additionalAffinityOrAntiAffinityRule: List[SOL005AffinityOrAntiAffinityRule] = []
    [self.additionalAffinityOrAntiAffinityRule.append(SOL005AffinityOrAntiAffinityRule(**element)) for element in
     additionalAffinityOrAntiAffinityRule or []]


class SOL005ScaleNsByStepsData:
  def __init__(self, scalingDirection="", aspectId="", numberOfSteps=1, **kwargs):
    self.scalingDirection: str = scalingDirection
    self.aspectId: str = aspectId
    self.numberOfSteps: int = numberOfSteps


class SOL005ScaleNsToLevelData:
  def __init__(self, nsInstantiationLevel="", nsScaleInfo=None, **kwargs):
    self.nsInstantiationLevel: str = nsInstantiationLevel
    self.nsScaleInfo: List[SOL005NsScaleInfo] = []
    [self.nsScaleInfo.append(SOL005NsScaleInfo(**element)) for element in nsScaleInfo or []]


class SOL005ScaleNsData:
  def __init__(self, vnfInstanceToBeAdded=None, vnfInstanceToBeRemoved=None, scaleNsByStepsData=None,
               scaleNsToLevelData=None, additionalParamsForNs=None, additionalParamsForVnf=None,
               locationConstraints=None, **kwargs):
    self.vnfInstanceToBeAdded: List[SOL005VnfInstanceData] = []
    [self.vnfInstanceToBeAdded.append(SOL005VnfInstanceData(**element)) for element in vnfInstanceToBeAdded or []]
    self.vnfInstanceToBeRemoved: List[str] = []
    [self.vnfInstanceToBeRemoved.append(element) for element in vnfInstanceToBeRemoved or []]
    self.scaleNsByStepsData: SOL005ScaleNsByStepsData = SOL005ScaleNsByStepsData()
    if scaleNsByStepsData is not None:
      self.scaleNsByStepsData: SOL005ScaleNsByStepsData = SOL005ScaleNsByStepsData(**scaleNsByStepsData)
    self.scaleNsToLevelData: SOL005ScaleNsToLevelData = SOL005ScaleNsToLevelData()
    if scaleNsToLevelData is not None:
      self.scaleNsToLevelData: SOL005ScaleNsToLevelData = SOL005ScaleNsToLevelData(**scaleNsToLevelData)
    self.additionalParamsForNs: Dict = {}
    if additionalParamsForNs is not None: self.additionalParamsForNs = additionalParamsForNs
    self.additionalParamsForVnf: List[SOL005ParamsForVnf] = []
    [self.additionalParamsForVnf.append(SOL005ParamsForVnf(**element)) for element in additionalParamsForVnf or []]
    self.locationConstraints: List[SOL005VnfLocationConstraint] = []
    [self.locationConstraints.append(SOL005VnfLocationConstraint(**element)) for element in locationConstraints or []]


class SOL005VnfScaleInfo:
  def __init__(self, aspectlId="", scaleLevel=0, **kwargs):
    self.aspectlId: str = aspectlId
    self.scaleLevel: int = scaleLevel


class SOL005ScaleToLevelData:
  def __init__(self, vnfInstantiationLevelId="", vnfScaleInfo=None, additionalParams=None, **kwargs):
    self.vnfInstantiationLevelId: str = vnfInstantiationLevelId
    self.vnfScaleInfo: List[SOL005VnfScaleInfo] = []
    [self.vnfScaleInfo.append(SOL005VnfScaleInfo(**element)) for element in vnfScaleInfo or []]
    self.additionalParams: Dict = {}
    if additionalParams is not None: self.additionalParams = additionalParams


class SOL005ScaleByStepData:
  def __init__(self, aspectId="", numberOfSteps=1, additionalParams=None, **kwargs):
    self.aspectId: str = aspectId
    self.numberOfSteps: int = numberOfSteps
    self.additionalParams: Dict = {}
    if additionalParams is not None: self.additionalParams = additionalParams


class SOL005ScaleVnfData:
  def __init__(self, vnfInstanceid="", scaleVnfType="", scaleToLevelData=None, scaleByStepData=None, **kwargs):
    self.vnfInstanceid: str = vnfInstanceid
    self.scaleVnfType: str = scaleVnfType
    if scaleToLevelData is not None:
      self.scaleToLevelData: SOL005ScaleToLevelData = SOL005ScaleToLevelData(**scaleToLevelData)
    if scaleByStepData is not None:
      self.scaleByStepData: SOL005ScaleByStepData = SOL005ScaleByStepData(**scaleByStepData)


class SOL005ScaleNsRequest:
  def __init__(self, scaleType="", scaleNsData=None, scaleVnfData=None, scaleTime="", **kwargs):
    self.scaleType: str = scaleType
    if scaleNsData is not None:
      self.scaleNsData: SOL005ScaleNsData = SOL005ScaleNsData(**scaleNsData)
    if scaleVnfData is not None:
      self.scaleVnfData: List[SOL005ScaleVnfData] = []
      [self.scaleVnfData.append(SOL005ScaleVnfData(**element)) for element in scaleVnfData or []]
    self.scaleTime: str = scaleTime


class SOL005NsLcmOpOcc:
  def __init__(self, id="", operationState="", stateEnteredTime="", nsInstanceId="", lcmOperationType="", startTime="", isAutomaticInvocation=False, operationParams=None, isCancelPending=False, cancelMode="", error=None, resourceChanges=None, **kwargs):
    self.id = id
    self.operationState = operationState
    self.stateEnteredTime = stateEnteredTime  # Not fully compliant with SOL005 specification "statusEnteredTime"
    self.nsInstanceId = nsInstanceId
    self.lcmOperationType = lcmOperationType
    self.startTime = startTime
    self.isAutomaticInvocation = isAutomaticInvocation
    self.operationParams = operationParams
    self.isCancelPending = isCancelPending
    self.cancelMode = cancelMode
    self.error = error
    self.resourceChanges: Dict = {}
    if resourceChanges is not None: self.resourceChanges = resourceChanges


# SOL005 to IFA 013 Translator functions

def sol005ScaleNsRequest_to_ifa013ScaleNsRequest(nsInstanceId: str,
                                                 sol005ScaleNsRequest: SOL005ScaleNsRequest) -> IFA013ScaleNsRequest:
  ifa013ScaleNsRequest = IFA013ScaleNsRequest()
  ifa013ScaleNsRequest.nsInstanceId = nsInstanceId
  ifa013ScaleNsRequest.scaleType = sol005ScaleNsRequest.scaleType
  if hasattr(sol005ScaleNsRequest, 'scaleNsData') and sol005ScaleNsRequest.scaleNsData is not None:
    ifa013ScaleNsRequest.scaleNsData = sol005ScaleNsData_to_ifa013ScaleNsData(sol005ScaleNsRequest.scaleNsData)
  if hasattr(sol005ScaleNsRequest, 'scaleVnfData') and sol005ScaleNsRequest.scaleVnfData is not None:
    ifa013ScaleNsRequest.scaleVnfData = sol005ScaleVnfData_to_ifa013ScaleVnfData(sol005ScaleNsRequest.scaleVnfData)
  ifa013ScaleNsRequest.scaleTime = sol005ScaleNsRequest.scaleTime
  return ifa013ScaleNsRequest


def sol005ScaleNsData_to_ifa013ScaleNsData(sol005ScaleNsData: SOL005ScaleNsData) -> IFA013ScaleNsData:
  ifa013ScaleNsData = IFA013ScaleNsData()
  ifa013ScaleNsData.vnfInstanceToBeAdded = sol005VnfInstanceData_to_ifa013VnfInstanceData(
    sol005ScaleNsData.vnfInstanceToBeAdded)
  ifa013ScaleNsData.vnfInstanceToBeRemoved = sol005ScaleNsData.vnfInstanceToBeRemoved
  ifa013ScaleNsData.scaleNsByStepsData = sol005ScaleNsByStepsData_to_ifa013ScaleNsByStepsData(
    sol005ScaleNsData.scaleNsByStepsData)
  ifa013ScaleNsData.scaleNsToLevelData = sol005ScaleNsToLevelData_to_ifa013ScaleNsToLevelData(
    sol005ScaleNsData.scaleNsToLevelData)
  ifa013ScaleNsData.additionalParamsForNs = sol005ScaleNsData.additionalParamsForNs
  ifa013ScaleNsData.additionalParamsForVnf = sol005ParamsForVnf_to_ifa013ParamsForVnf(
    sol005ScaleNsData.additionalParamsForVnf)
  ifa013ScaleNsData.locationConstraints = sol005LocationConstraints_to_ifa013VnfLocationConstraint(
    sol005ScaleNsData.locationConstraints)
  return ifa013ScaleNsData


def sol005ScaleNsToLevelData_to_ifa013ScaleNsToLevelData(
  sol005ScaleNsToLevelData: SOL005ScaleNsToLevelData) -> IFA013ScaleNsToLevelData:
  ifa013ScaleNsToLevelData = IFA013ScaleNsToLevelData()
  ifa013ScaleNsToLevelData.nsInstantiationLevel = sol005ScaleNsToLevelData.nsInstantiationLevel
  ifa013ScaleNsToLevelData.nsScaleInfo = sol005NsScaleInfo_to_ifa013NsScaleInfo(sol005ScaleNsToLevelData.nsScaleInfo)
  return ifa013ScaleNsToLevelData


def sol005ScaleNsByStepsData_to_ifa013ScaleNsByStepsData(
  sol005ScaleNsByStepsData: SOL005ScaleNsByStepsData) -> IFA013ScaleNsByStepsData:
  ifa013ScaleNsByStepsData = IFA013ScaleNsByStepsData()
  ifa013ScaleNsByStepsData.scalingDirection = sol005ScaleNsByStepsData.scalingDirection
  ifa013ScaleNsByStepsData.aspectId = sol005ScaleNsByStepsData.aspectId
  ifa013ScaleNsByStepsData.numberOfSteps = sol005ScaleNsByStepsData.numberOfSteps
  return ifa013ScaleNsByStepsData


def sol005NsScaleInfo_to_ifa013NsScaleInfo(sol005NsScaleInfoArray: List[SOL005NsScaleInfo]) -> List[IFA013NsScaleInfo]:
  ifa013NsScaleInfoArray: List[IFA013NsScaleInfo] = []
  for sol005NsScaleInfo in sol005NsScaleInfoArray:
    ifa013NsScaleInfo = IFA013NsScaleInfo()
    ifa013NsScaleInfo.nsScalingAspectId = sol005NsScaleInfo.nsScalingAspectId
    ifa013NsScaleInfo.nsScaleLevelId = sol005NsScaleInfo.nsScaleLevelId
    ifa013NsScaleInfoArray.append(ifa013NsScaleInfo)
  return ifa013NsScaleInfoArray


def sol005ScaleVnfData_to_ifa013ScaleVnfData(sol005ScaleVnfDataArray: List[SOL005ScaleVnfData]) -> List[
  IFA013ScaleVnfData]:
  ifa013ScaleVnfDataArray: List[IFA013ScaleVnfData] = []
  for sol005ScaleVnfData in sol005ScaleVnfDataArray:
    ifa013ScaleVnfData = IFA013ScaleVnfData()
    ifa013ScaleVnfData.vnfInstanceId = sol005ScaleVnfData.vnfInstanceid
    ifa013ScaleVnfData.type = sol005ScaleVnfData.scaleVnfType
    if hasattr(sol005ScaleVnfData, 'scaleToLevelData') and sol005ScaleVnfData.scaleToLevelData is not None:
      ifa013ScaleVnfData.scaleToLevelData = sol005ScaleToLevelData_to_ifa013ScaleToLevelData(
        sol005ScaleVnfData.scaleToLevelData)
    if hasattr(sol005ScaleVnfData, 'scaleByStepData') and sol005ScaleVnfData.scaleByStepData is not None:
      ifa013ScaleVnfData.scaleByStepData = sol005ScaleByStepData_to_ifa013ScaleByStepData(
      sol005ScaleVnfData.scaleByStepData, sol005ScaleVnfData.scaleVnfType)
    ifa013ScaleVnfDataArray.append(ifa013ScaleVnfData)
  return ifa013ScaleVnfDataArray


def sol005ScaleToLevelData_to_ifa013ScaleToLevelData(
  sol005ScaleToLevelData: SOL005ScaleToLevelData) -> IFA013ScaleToLevelData:
  ifa013ScaleToLevelData = IFA013ScaleToLevelData()
  ifa013ScaleToLevelData.instantiationLevelId = sol005ScaleToLevelData.vnfInstantiationLevelId
  ifa013ScaleToLevelData.scaleInfo = sol005VnfScaleInfo_to_ifa013VnfScaleInfo(sol005ScaleToLevelData.vnfScaleInfo)
  ifa013ScaleToLevelData.additionalParam = sol005ScaleToLevelData.additionalParams
  return ifa013ScaleToLevelData


def sol005VnfScaleInfo_to_ifa013VnfScaleInfo(sol005VnfScaleInfoArray: List[SOL005VnfScaleInfo]) -> List[
  IFA013ScaleInfo]:
  ifa013ScaleInfoArray: List[IFA013ScaleInfo] = []
  for sol005VnfScaleInfo in sol005VnfScaleInfoArray:
    ifa013ScaleInfo = IFA013ScaleInfo()
    ifa013ScaleInfo.aspectId = sol005VnfScaleInfo.aspectlId
    ifa013ScaleInfo.scaleLevel = sol005VnfScaleInfo.scaleLevel
    ifa013ScaleInfoArray.append(ifa013ScaleInfo)
  return ifa013ScaleInfoArray


def sol005ScaleByStepData_to_ifa013ScaleByStepData(
  sol005ScaleByStepData: SOL005ScaleByStepData, type: str) -> IFA013ScaleByStepData:
  ifa013ScaleByStepData = IFA013ScaleByStepData()
  ifa013ScaleByStepData.type = type  # FIXME SOL005ScaleByStepData does not specify scaling type (scale in or scale out)
  ifa013ScaleByStepData.aspectId = sol005ScaleByStepData.aspectId
  ifa013ScaleByStepData.numberOfSteps = sol005ScaleByStepData.numberOfSteps
  ifa013ScaleByStepData.additionalParam = sol005ScaleByStepData.additionalParams
  return ifa013ScaleByStepData

def sol005InstantiateNsRequest_to_ifa013InstantiateNsRequest(
  sol005InstantiateNsRequest: SOL005InstantiateNsRequest) -> IFA013InstantiateNsRequest:
  ifa013InstantiateNsRequest = IFA013InstantiateNsRequest()
  ifa013InstantiateNsRequest.nsInstanceId = None  # FIXME: get it from URI
  ifa013InstantiateNsRequest.flavourId = sol005InstantiateNsRequest.nsFlavourId
  ifa013InstantiateNsRequest.sapData = sol005SapData_to_ifa013SapData(sol005InstantiateNsRequest.sapData)  # FIXME
  ifa013InstantiateNsRequest.pnfInfo = sol005AddPnfData_to_ifa013PnfInfo(
    sol005InstantiateNsRequest.addpnfData)  # FIXME
  ifa013InstantiateNsRequest.vnfInstanceData = sol005InstantiateNsRequest.vnfInstanceData  # FIXME
  ifa013InstantiateNsRequest.nestedNsInstanceId = sol005NestedNsInstanceData_to_ifa013NestedNsInstanceId(
    sol005InstantiateNsRequest.nestedNsInstanceData)  # FIXME
  ifa013InstantiateNsRequest.locationConstraints = sol005LocationConstraints_to_ifa013VnfLocationConstraint(
    sol005InstantiateNsRequest.locationConstraints)  # FIXME
  ifa013InstantiateNsRequest.additionalParamForNs = sol005InstantiateNsRequest.additionalParamsForNs
  ifa013InstantiateNsRequest.additionalParamForVnf = sol005ParamsForVnf_to_ifa013ParamsForVnf(
    sol005InstantiateNsRequest.additionalParamsForVnf)  # FIXME
  ifa013InstantiateNsRequest.startTime = sol005InstantiateNsRequest.startTime
  ifa013InstantiateNsRequest.nsInstantiationLevelId = sol005InstantiateNsRequest.nsInstantiationLevelId
  ifa013InstantiateNsRequest.additionalAffinityOrAntiAffinityRule = sol005AffinityOrAntiAffinityRule_to_ifa013AffinityOrAntiAffinityRule(
    sol005InstantiateNsRequest.additionalAffinityOrAntiAffinityRule)  # FIXME
  return ifa013InstantiateNsRequest


def sol005CpProtocolData_to_ifa013Address(sol005SapData: SOL005CpProtocolData) -> str:
  """
  FIXME: SOL005CpProtocolData can come as an array, while in IFA address is only expecting one entry
  """
  pass


def sol005CpProtocolDataArray_to_ifa013Address(sol005SapDataArray: List[SOL005CpProtocolData]) -> str:
  ifaAddressArray: List[str] = []
  for sol005SapData in sol005SapDataArray:
    ifa013Address = sol005CpProtocolData_to_ifa013Address(sol005SapData)
    ifaAddressArray.append(ifa013Address)
  return ifaAddressArray[0]  # FIXME get first occurrence of address


def sol005SapData_to_ifa013SapData(sol005SapDataArray: List[SOL005SapData]) -> List[IFA013SapData]:
  ifa013SapDataArray = []
  for sol005SapData in sol005SapDataArray:
    ifa013SapData = IFA013SapData()
    ifa013SapData.sapdId = sol005SapData.sapdId
    ifa013SapData.sapName = sol005SapData.sapName
    ifa013SapData.description = sol005SapData.description
    ifa013SapData.address = sol005CpProtocolDataArray_to_ifa013Address(sol005SapData.sapProtocolData)
    ifa013SapDataArray.append(ifa013SapData)
  return ifa013SapDataArray


def sol005PnfExtCpData_to_ifa013PnfExtCpInfo(sol005PnfExtCpDataArray: List[SOL005PnfExtCpData]) -> List[
  IFA013PnfExtCpInfo]:
  ifa013PnfExtCpInfoArray: List[IFA013PnfExtCpInfo] = []
  for sol005PnfExtCpData in sol005PnfExtCpDataArray:
    ifa013PnfExtCpInfo = IFA013PnfExtCpInfo()
    ifa013PnfExtCpInfo.cpdId = sol005PnfExtCpData.cpdId
    ifa013PnfExtCpInfo.address = sol005CpProtocolDataArray_to_ifa013Address(sol005PnfExtCpData.cpProtocolData)
    ifa013PnfExtCpInfoArray.append(ifa013PnfExtCpInfo)
  return ifa013PnfExtCpInfoArray


def sol005AddPnfData_to_ifa013PnfInfo(sol005AddPnfDataArray: List[SOL005AddPnfData]) -> List[IFA013PnfInfo]:
  ifa013PnfInfoArray: List[IFA013PnfInfo] = []
  for sol005AddPnfData in sol005AddPnfDataArray:
    ifa013PnfInfo = IFA013PnfInfo()
    ifa013PnfInfo.pnfName = sol005AddPnfData.pnfName
    ifa013PnfInfo.pnfdinfoId = sol005AddPnfData.pnfId
    ifa013PnfInfo.cpInfo = sol005PnfExtCpData_to_ifa013PnfExtCpInfo(sol005AddPnfData.cpData)
    ifa013PnfInfoArray.append(ifa013PnfInfo)
  return ifa013PnfInfoArray


def sol005VnfInstanceData_to_ifa013VnfInstanceData(sol005VnfInstanceDataArray: List[SOL005VnfInstanceData]) -> List[
  IFA013VnfInstanceData]:
  ifa013VnfInstanceDataArray: List[IFA013VnfInstanceData] = []
  for sol005VnfInstanceData in sol005VnfInstanceDataArray:
    ifa013VnfInstanceData = IFA013VnfInstanceData()
    ifa013VnfInstanceData.vnfInstanceId = sol005VnfInstanceData.vnfInstanceId
    ifa013VnfInstanceData.vnfProfileId = sol005VnfInstanceData.vnfProfileId
    ifa013VnfInstanceDataArray.append(ifa013VnfInstanceData)
  return ifa013VnfInstanceDataArray


def sol005NestedNsInstanceData_to_ifa013NestedNsInstanceId(
  sol005NestedNsInstanceDataArray: List[SOL005NestedNsInstanceData]) -> List[str]:
  ifa013NestedNsInstanceIdArray: List[str] = []
  for sol005NestedNsInstanceData in sol005NestedNsInstanceDataArray:
    ifa013NestedNsInstanceId = sol005NestedNsInstanceData.nestedNsInstanceId
    ifa013NestedNsInstanceIdArray.append(ifa013NestedNsInstanceId)
  return ifa013NestedNsInstanceIdArray


def sol005LocationConstraints_to_ifa013VnfLocationConstraint(
  sol005LocationConstraintsArray: List[SOL005VnfLocationConstraint]) -> List[IFA013VnfLocationConstraint]:
  ifa013vnfLocationConstraintArray: List[IFA013VnfLocationConstraint] = []
  for sol005LocationConstraints in sol005LocationConstraintsArray:
    ifa013vnfLocationConstraint = IFA013VnfLocationConstraint()
    ifa013vnfLocationConstraint.vnfProfileId = sol005LocationConstraints.vnfProfileId
    ifa013vnfLocationConstraint.locationConstraints = None  # FIXME IFA does not specify such attribute
    ifa013vnfLocationConstraintArray.append(ifa013vnfLocationConstraint)
  return ifa013vnfLocationConstraintArray


def sol005ParamsForVnf_to_ifa013ParamsForVnf(sol005ParamsForVnfArray: List[SOL005ParamsForVnf]) -> List[
  IFA013ParamsForVnf]:
  ifa013ParamsForVnfArray: List[IFA013ParamsForVnf] = []
  for sol005ParamsForVnf in sol005ParamsForVnfArray:
    ifa013ParamsForVnf = IFA013ParamsForVnf()
    ifa013ParamsForVnf.vnfProfileId = sol005ParamsForVnf.vnfProfileId
    ifa013ParamsForVnf.additionalParam = sol005ParamsForVnf.additionalParams
    ifa013ParamsForVnfArray.append(ifa013ParamsForVnf)
  return ifa013ParamsForVnfArray


def sol005AffinityOrAntiAffinityRule_to_ifa013AffinityOrAntiAffinityRule(
  sol005AffinityOrAntiAffinityRuleArray: List[SOL005AffinityOrAntiAffinityRule]) -> List[
  IFA013AffinityOrAntiAffinityRule]:
  ifa013AffinityOrAntiAffinityRuleArray: List[IFA013AffinityOrAntiAffinityRule] = []
  for sol005AffinityOrAntiAffinityRule in sol005AffinityOrAntiAffinityRuleArray:
    ifa013AffinityOrAntiAffinityRule = IFA013AffinityOrAntiAffinityRule()
    ifa013AffinityOrAntiAffinityRule.descriptorId = sol005AffinityOrAntiAffinityRule.vnfdId
    ifa013AffinityOrAntiAffinityRule.vnfInstanceId = sol005AffinityOrAntiAffinityRule.vnfInstanceId
    if sol005AffinityOrAntiAffinityRule.affinityOrAntiAffinity == "AFFINITY":
      ifa013AffinityOrAntiAffinityRule.affinityOrAntiAffinity = True
    else:
      ifa013AffinityOrAntiAffinityRule.affinityOrAntiAffinity = False
    ifa013AffinityOrAntiAffinityRule.scope = sol005AffinityOrAntiAffinityRule.scope
    ifa013AffinityOrAntiAffinityRuleArray.append(ifa013AffinityOrAntiAffinityRule)
  return ifa013AffinityOrAntiAffinityRuleArray


# IFA 013 to SOL005 Translator functions

def ifa013nsinfo_to_sol005nsinstance(nsInfo: IFA013NsInfo) -> SOL005NSInstance:
  nsInstance = SOL005NSInstance()
  nsInstance.id = nsInfo.nsInstanceId
  nsInstance.nsInstanceName = nsInfo.nsName
  nsInstance.nsInstanceDescription = nsInfo.description
  nsInstance.nsdId = nsInfo.nsdId
  nsInstance.nsdInfoId = None
  nsInstance.flavourId = nsInfo.flavourId
  nsInstance.vnfInstance = []  # FIXME unsupported, as ifa only supports using id as vnfinstance and 5GROWTH implementation does not include an endpoint to query VNF instances
  nsInstance.pnfInfo = ifa013PnfInfo_to_sol005PnfInfo(nsInfo.pnfInfo)
  nsInstance.virtualLinkInfo = ifa013NsVirtualLinkInfo_to_sol005NsVirtualLinkInfo(nsInfo.virtualLinkInfo)
  nsInstance.vnffgInfo = ifa013VnffgInfo_to_sol005VnffgInfo(nsInfo.vnffgInfo)
  nsInstance.sapInfo = ifa013SapInfo_to_sol005Sapinfo(nsInfo.sapInfo)
  nsInstance.nestedNsInstanceId = nsInfo.nestedNsInfoId
  nsInstance.nsState = nsInfo.nsState
  nsInstance.monitoringParameter = None
  nsInstance.nsScaleStatus = nsInfo.nsScaleStatus
  nsInstance.additionalAffinityOrAntiAffinityRule = ifa013AffinityOrAntiAffinityRule_to_sol005AffinityOrAntiAffinityRule(
    nsInfo.additionalAffinityOrAntiAffinityRule)
  return nsInstance


def ifa013SapInfo_to_sol005Sapinfo(ifaSapInfoArray: List[IFA013SapInfo]) -> List[SOL005SapInfo]:
  sol005SapInfoArray = []
  for ifaSapInfo in ifaSapInfoArray:
    sol005SapInfo = SOL005SapInfo()
    sol005SapInfo.id = ifaSapInfo.sapInstanceId
    sol005SapInfo.sapdId = ifaSapInfo.sapdId
    sol005SapInfo.sapName = ifaSapInfo.sapName
    sol005SapInfo.description = ifaSapInfo.description
    # Ifa cpProtocolInfo to SOL005 cpProtocolInfo
    sol005cpProtocolInfo = SOL005CpProtocolInfo()
    sol005cpProtocolInfo.ipOverEthernet = SOL005IpOverEthernetAddressInfo()
    if "." in ifaSapInfo.address:  # Ip address
      sol005cpProtocolInfo.ipOverEthernet.ipAddresses.append(ifaSapInfo.address)
    else:  # Mac address
      sol005cpProtocolInfo.ipOverEthernet.macAddress = ifaSapInfo.address
    sol005SapInfo.sapProtocolInfo.append(sol005cpProtocolInfo)
    #sol005SapInfo.userAccessInfo = ifaSapInfo.userAccessInfo
    sol005SapInfoArray.append(sol005SapInfo)
  return sol005SapInfoArray


def ifa013PnfInfo_to_sol005PnfInfo(ifa013PnfInfoArray: List[IFA013PnfInfo]) -> List[SOL005PnfInfo]:
  sol005PnfInfoArray = []
  for ifaPnfInfo in ifa013PnfInfoArray:
    sol005PnfInfo = SOL005PnfInfo()
    sol005PnfInfo.pnfName = ifaPnfInfo.pnfName
    sol005PnfInfo.pnfdInfoId = ifaPnfInfo.pnfdinfoId
    sol005PnfInfo.cpInfo = ifa013PnfExtCpInfo_to_sol005PnfExtCpInfo(ifaPnfInfo.cpInfo)
    sol005PnfInfoArray.append(sol005PnfInfo)
  return sol005PnfInfoArray


def ifa013PnfExtCpInfoAddress_to_sol005CpProtocolData(address: str) -> SOL005CpProtocolData:
  sol005cpProtocolData = SOL005CpProtocolData()
  sol005cpProtocolData.ipOverEthernet = SOL005IpOverEthernetAddressData()
  if "." in address:  # Ip address
    sol005cpProtocolData.ipOverEthernet.ipAddresses.append(address)
  else:  # Mac address
    sol005cpProtocolData.ipOverEthernet.macAddress = address

  return sol005cpProtocolData


def ifa013PnfExtCpInfo_to_sol005PnfExtCpInfo(ifa013PnfExtCpInfoArray: List[IFA013PnfExtCpInfo]) -> List[
  SOL005PnfExtCpInfo]:
  sol005PnfExtCpInfoArray = []
  for ifa013PnfExtCpInfo in ifa013PnfExtCpInfoArray:
    sol005PnfExtCpInfo = SOL005PnfExtCpInfo()
    sol005PnfExtCpInfo.cpdId = ifa013PnfExtCpInfo.cpdId
    sol005cpProtocolData = ifa013PnfExtCpInfoAddress_to_sol005CpProtocolData(ifa013PnfExtCpInfo.address)
    sol005PnfExtCpInfo.cpProtocolData.append(sol005cpProtocolData)
    sol005PnfExtCpInfoArray.append(sol005PnfExtCpInfo)
  return sol005PnfExtCpInfoArray


def ifa013cpIds_to_sol005nsCpHandle(cpIds: List[str]) -> List[SOL005NsCpHandle]:
  sol005NsCpHandleArray = []
  for cpId in cpIds:
    sol005NsCpHandle = ifa013cpId_to_sol005nsCpHandle(cpId)
    sol005NsCpHandleArray.append(sol005NsCpHandle)
  return sol005NsCpHandleArray


def ifa013cpId_to_sol005nsCpHandle(cpId: str) -> SOL005NsCpHandle:
  """
  FIXME: cpId is an identifier pointing to the two pointers required for SOL005 NsCpHandle, 5gr-so does not support in its api querying VnfExtCpInfo, PnfExtCpInfo or SapInfo from its cpId
  cpId: Identifier (Reference to VnfExtCpInfo or PnfExtCpInfo or SapInfo)
  SOL005 NSCpHandle
  NOTE 1: For the VNF external CP instance, both vnfInstanceId and vnfExtCpInstanceId shall be present as a pair.
  NOTE 2: For the PNF external CP instance, both pnfInfoId and PnfExtCpInstanceId shall be present as a pair.
  NOTE 3: For the SAP instance, both nsInstanceId and nsSapInstanceId shall be present as a pair.
  NOTE 4: One pair of identifiers (VNF external CP, PNF external CP or SAP) shall be present. 
  """
  return SOL005NsCpHandle()


def ifa013NsLinkPort_to_sol005NsLinkPortInfo(ifa013NsLinkPortArray: List[IFA013NsLinkPort]) -> List[
  SOL005NsLinkPortInfo]:
  sol005NsLinkPortInfoArray = []
  for ifa013NsLinkPort in ifa013NsLinkPortArray:
    sol005NsLinkPortInfo = SOL005NsLinkPortInfo()
    sol005NsLinkPortInfo.id = None
    sol005NsLinkPortInfo.resourceHandle = ifa013NsLinkPort.resourceHandle
    sol005NsLinkPortInfo.nsCpHandle = ifa013cpId_to_sol005nsCpHandle(ifa013NsLinkPort.cpId)
    sol005NsLinkPortInfoArray.append(sol005NsLinkPortInfo)
  return sol005NsLinkPortInfoArray


def ifa013NsVirtualLinkInfo_to_sol005NsVirtualLinkInfo(ifa013NsVirtualLinkInfoArray: List[IFA013NsVirtualLinkInfo]) -> \
  List[SOL005NsVirtualLinkInfo]:
  sol005NsVirtualLinkInfoArray = []
  for ifa013NsVirtualLinkInfo in ifa013NsVirtualLinkInfoArray:
    sol005NsVirtualLinkInfo = SOL005NsVirtualLinkInfo()
    sol005NsVirtualLinkInfo.id = None
    sol005NsVirtualLinkInfo.nsVirtualLinkDescId = ifa013NsVirtualLinkInfo.nsVirtualLinkDescId
    sol005NsVirtualLinkInfo.nsVirtualLinkProfileId = None
    sol005NsVirtualLinkInfo.resourceHandle = ifa013ResourceHandle_to_sol005ResourceHandle(
      ifa013NsVirtualLinkInfo.resourceHandle)
    sol005NsVirtualLinkInfo.linkPort = ifa013NsVirtualLinkInfo.linkPort
    sol005NsVirtualLinkInfoArray.append(sol005NsVirtualLinkInfo)
  return sol005NsVirtualLinkInfoArray


def ifa013ResourceHandle_to_sol005ResourceHandle(ifa013ResourceHandleArray: List[IFA013ResourceHandle]) -> List[
  SOL005ResourceHandle]:
  sol005ResourceHandleArray = []
  for ifa013ResourceHandle in ifa013ResourceHandleArray:
    sol005ResourceHandle = SOL005ResourceHandle()
    sol005ResourceHandle.vimId = ifa013ResourceHandle.vimId
    sol005ResourceHandle.resourceProviderId = ifa013ResourceHandle.resourceProviderId
    sol005ResourceHandle.resourceId = ifa013ResourceHandle.resourceId
    sol005ResourceHandle.vimLevelResourceType = None
    sol005ResourceHandleArray.append(sol005ResourceHandle)
  return sol005ResourceHandleArray


def ifa013VnffgInfo_to_sol005VnffgInfo(ifa013VnffgInfoArray: List[IFA013VnffgInfo]) -> List[SOL005VnffgInfo]:
  sol005VnffgInfoArray = []
  for ifa013VnffgInfo in ifa013VnffgInfoArray:
    sol005VnffgInfo = SOL005VnffgInfo()
    sol005VnffgInfo.id = ifa013VnffgInfo.vnffgId
    sol005VnffgInfo.vnffgdId = ifa013VnffgInfo.vnffgdId
    sol005VnffgInfo.vnfInstanceId = ifa013VnffgInfo.vnfId
    sol005VnffgInfo.pnfInfoId = ifa013VnffgInfo.pnfId
    sol005VnffgInfo.nsVirtualLinkInfoId = ifa013VnffgInfo.virtualLinkId
    sol005VnffgInfo.nsCpHandle = ifa013cpIds_to_sol005nsCpHandle(ifa013VnffgInfo.cpId)
    sol005VnffgInfo.nfpInfo = ifa013Nfp_to_sol005NfpInfo(ifa013VnffgInfo.nfp)
    sol005VnffgInfoArray.append(sol005VnffgInfo)
  return sol005VnffgInfoArray


def ifa013Nfp_to_sol005NfpInfo(ifa013NfpArray: List[IFA013Nfp]) -> List[SOL005NfpInfo]:
  sol005NfpInfoArray = []
  for ifa013Nfp in ifa013NfpArray:
    sol005NfpInfo = SOL005NfpInfo()
    sol005NfpInfo.id = ifa013Nfp.nfpId
    sol005NfpInfo.nfpdId = None
    sol005NfpInfo.nfpName = None
    sol005NfpInfo.description = None
    sol005NfpInfo.cpGroup = None
    sol005NfpInfo.totalCp = ifa013Nfp.totalCp
    sol005NfpInfo.nfpRule = None
    sol005NfpInfo.nfpState = ifa013Nfp.nfpState
    sol005NfpInfoArray.append(sol005NfpInfo)
  return sol005NfpInfoArray


def ifa013AffinityOrAntiAffinityRule_to_sol005AffinityOrAntiAffinityRule(
  ifa013AffinityOrAntiAffinityRuleArray: List[IFA013AffinityOrAntiAffinityRule]) -> List[
  SOL005AffinityOrAntiAffinityRule]:
  sol005AffinityOrAntiAffinityRuleArray = []
  for ifa013AffinityOrAntiAffinityRule in ifa013AffinityOrAntiAffinityRuleArray:
    sol005AffinityOrAntiAffinityRule = SOL005AffinityOrAntiAffinityRule()
    sol005AffinityOrAntiAffinityRule.vnfdId = ifa013AffinityOrAntiAffinityRule.descriptorId
    sol005AffinityOrAntiAffinityRule.vnfProfileId = None
    sol005AffinityOrAntiAffinityRule.vnfInstanceId = ifa013AffinityOrAntiAffinityRule.vnfInstanceId
    if ifa013AffinityOrAntiAffinityRule.affinityOrAntiAffinity:
      sol005AffinityOrAntiAffinityRule.affinityOrAntiAffinity = "AFFINITY"
    else:
      sol005AffinityOrAntiAffinityRule.affinityOrAntiAffinity = "ANTI_AFFINITY"

    sol005AffinityOrAntiAffinityRule.scope = ifa013AffinityOrAntiAffinityRule.scope  # TODO: Check if string match
    sol005AffinityOrAntiAffinityRuleArray.append(sol005AffinityOrAntiAffinityRule)
  return sol005AffinityOrAntiAffinityRuleArray


def ifa013OperationStatus_to_sol005NsLcmOpOcc(ifa013NSLCMOpId, ifa013OperationStatus):
  """
  IFA: (1)PROCESSING, (2)SUCCESFULLY_DONE, (3)FAILED, CANCELLED
  SOL: (1)PROCESSING, (2)COMPLETED, PARTIALLY_COMPLETED, FAILED_TEMP, (3)FAILED, ROLLING_BACK, ROLLED_BACK
  """
  sol005NsLcmOpOcc = SOL005NsLcmOpOcc()
  if ifa013OperationStatus == "SUCCESSFULLY_DONE":
    sol005NsLcmOpOcc.operationState = "COMPLETED"
  elif ifa013OperationStatus == "PROCESSING":
    sol005NsLcmOpOcc.operationState = "PROCESSING"
  elif ifa013OperationStatus == "FAILED":
    sol005NsLcmOpOcc.operationState = "FAILED"
  else:  # by default use "PROCESSING"
    sol005NsLcmOpOcc.operationState = "PROCESSING"
  sol005NsLcmOpOcc.id = ifa013NSLCMOpId

  sol005NsLcmOpOcc.nsInstanceId = str(uuid.uuid4())  # FIXME: Not supported by 5gr-so NBI
  sol005NsLcmOpOcc.lcmOperationType = "INSTANTIATE"  # FIXME: Not supported by 5gr-so NBI

  d = datetime.datetime.utcnow()
  currentDateTime = d.isoformat("T") + "Z"
  sol005NsLcmOpOcc.statusEnteredTime = currentDateTime  # FIXME: Not supported by 5gr-so NBI
  sol005NsLcmOpOcc.startTime = currentDateTime  # FIXME: Not supported by 5gr-so NBI

  return sol005NsLcmOpOcc


def to_dict(obj):
  """
    Nested objects to dictionary representation
  """
  original = json.loads(json.dumps(obj, default=lambda o: o.__dict__))
  return {k: v for k, v in original.items() if v is not None}
