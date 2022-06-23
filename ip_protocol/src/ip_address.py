import netifaces
from typing import Tuple


def get_available_interfaces() -> list[str]:
    return netifaces.interfaces()


def get_ip_addr_and_mask(interface: str = 'wlan0') -> Tuple[str, str]:
    try:
        ip_data = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]
        return ip_data['addr'], ip_data['netmask']
    except ValueError:
        interfaces = get_available_interfaces()
        print(
            'Invalid interface name. Please use one of {0}'.format(
                ', '.join(interfaces)
            )
        )
        raise


def output_ip_addr_and_mask(ipaddr: str, mask: str):
    print(
        'IP-addr: {ipaddr}, mask: {mask}'.format(
            ipaddr=ipaddr,
            mask=mask,
        )
    )


if __name__ == '__main__':
    from sys import argv
    if len(argv) == 1:
        output_ip_addr_and_mask(*get_ip_addr_and_mask())
    elif len(argv) == 2:
        if argv[1] == '--help':
            print('Usage: python ip_address.py [interface name]')
        else:
            output_ip_addr_and_mask(*get_ip_addr_and_mask(argv[1]))
    else:
        print('Invalid arguments. See --help.')
