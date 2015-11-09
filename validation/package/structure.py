from libtaxii.taxii_default_query import package_dir
from ..observable.address import AddressValidationInfo
from ..observable.socket_type import SocketValidationInfo
from ..observable.http_session import HTTPSessionValidationInfo


class ObservableStructureConverter(object):

    @staticmethod
    def __get_conversion_handler(object_type):
        conversion_handlers = {
            AddressValidationInfo.TYPE: ObservableStructureConverter.__address_package_to_simple,
            SocketValidationInfo.TYPE: ObservableStructureConverter.__socket_package_to_simple,
            HTTPSessionValidationInfo.TYPE: ObservableStructureConverter.__https_session_package_to_simple
        }
        return conversion_handlers.get(object_type)

    @staticmethod
    def package_to_simple(object_type, package_dict):
        converter = ObservableStructureConverter.__get_conversion_handler(object_type)
        if converter:
            return converter(package_dict)
        return package_dict

    @staticmethod
    def __address_package_to_simple(package_dict):
        # This doesn't handle more exotic structures like IP ranges...
        simple = package_dict.copy()
        address_value = simple['address_value']
        if isinstance(address_value, dict):
            simple['address_value'] = address_value['value']
        return simple

    @staticmethod
    def __socket_package_to_simple(package_dict):
        simple = {
            'port': package_dict['port']['port_value'],
            'protocol': package_dict['port']['layer4_protocol']
        }
        if package_dict.get('ip_address'):
            simple['ip_address'] = package_dict['ip_address']['address_value']
        if package_dict.get('hostname'):
            simple['hostname'] = package_dict['hostname']['hostname_value']

        return simple

    @staticmethod
    def __https_session_package_to_simple(package_dict):
        simple = package_dict.copy()
        try:
            http_request_response = simple.pop('http_request_response', {})
            simple['user_agent'] = \
                http_request_response[0]['http_client_request']['http_request_header']['parsed_header']['user_agent']
        except LookupError:
            simple['user_agent'] = None

        return simple


class IndicatorStructureConverter(object):

    @staticmethod
    def package_to_simple(package_dict):
        simple = package_dict.copy()
        try:
            simple['confidence'] = package_dict['confidence']['value']['value']
        except KeyError:
            simple['confidence'] = None

        try:
            kill_chain_phases = simple.pop('kill_chain_phases', {})
            simple['phase_id'] = kill_chain_phases['kill_chain_phases'][0]['phase_id']
        except LookupError:
            simple['phase_id'] = None

        try:
            handling_structures = package_dict['handling']
            marking_structure = handling_structures[0]['marking_structures'][0]
            simple['tlp'] = marking_structure['color']
        except LookupError:
            simple['tlp'] = None

        try:
            simple['suggested_coas'] = simple['suggested_coas']['suggested_coas']
        except KeyError:
            simple['suggested_coas'] = None

        return simple
