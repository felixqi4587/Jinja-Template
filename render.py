import yaml  # pip3 install pyyaml
from pprint import pprint
from jinja2 import Environment, FileSystemLoader  # pip3 install jinja2
import ipaddress


def get_ip_from_sub(subnet):
    ip_list = ipaddress.ip_network(subnet)
    list = []
    for ip in ip_list:
        list.append(str(ip))
    return list


def get_iso_address(ip):
    iso_t = ip.split('.')
    iso_s = ''
    for t in iso_t:
        while len(t) < 3:
            t = str(0) + t
        iso_s += t
    iso_split = [iso_s[i:i+4] for i in range(0, len(iso_s), 4)]
    return '.'.join(iso_split)


var = yaml.full_load(open('./Lesson1/varibles.yaml').read())
var_dict = var[0]  # Convert LIST to DICT

CORE01_CORE02_NET = get_ip_from_sub(var_dict['CORE01_CORE02_NET'])
var_dict['CORE01_CORE02'] = CORE01_CORE02_NET[1]
var_dict['CORE02_CORE01'] = CORE01_CORE02_NET[2]

var_dict['CORE01_ISO'] = get_iso_address(var_dict['CORE01_LOOPBACK0'])
var_dict['CORE02_ISO'] = get_iso_address(var_dict['CORE02_LOOPBACK0'])


def output():
    renderfile = './Lesson1/mop.j2'
    env = Environment(loader=FileSystemLoader(''))
    template = env.get_template(renderfile)
    for device in var:
        output = template.render(device)
        with open(renderfile.split('.')[0]+'mop.txt', 'w') as f:
            f.write(output)
    print('Template created')


if __name__ == "__main__":
    output()