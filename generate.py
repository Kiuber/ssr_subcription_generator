import requests
import base64
import json
import re

def base64_encode(str):
    resstr = base64.b64encode(str.encode()).decode()
    return re.sub('\/', '_', resstr.replace('=', '').replace('+', '-'))

# ssr://server:port:protocol:method:obfs:password_base64/?params_base64
# obfsparam=obfsparam_base64&protoparam=protoparam_base64&remarks=remarks_base64&group=group_base64
def encode_ssr_config_list(config_list):
    ssr_list = []
    for config in config_list:
        fields = ['server', 'server_port', 'protocol', 'method', 'obfs']
        list = []
        for field in fields:
            if config.get(field, None) is not None:
                list.append(str(config[field]))
        config_str = ':' . join(list)

        fields = ['obfsparam', 'protocolparam', 'remarks', 'group']
        list = []
        for field in fields:
            if config.get(field, None) is not None:
                list.append(field + '=' + (base64_encode(config[field])))

        extra_config_str = '&' . join(list)
        password_str = base64_encode(config['password'])

        ssr_str = config_str + ':' + password_str + '/?' + extra_config_str
        ssr_list.append('ssr://' + base64_encode(ssr_str))
    return ssr_list

if __name__ == '__main__':

    f = open('gui-config.json', 'r')
    ssr_config = f.read()
    f.close()

    ssr_config = json.loads(ssr_config)
    config_list = encode_ssr_config_list(ssr_config['configs'])

    config_list = '\n' . join(config_list)
    print(config_list)

    base64_config_list = base64_encode(config_list)
    print(base64_config_list)
