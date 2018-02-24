#!/usr/bin/env python3

import json
import os
import re
# import socket

# import requests


# TODO 1: Reduce the redundancy across variables `a_header`, `c_header`, and `headers`.
# TODO 2: Port the functionality of the `curl` command to the `requests.post()` function.

def builder(params):
    endpoint = 'https://api.digitalocean.com/v2/droplets'

    hostname = params['hostname']
    payload = {}

    a_header = 'Authorization: Bearer {pa_token}'.format(pa_token=params['pa_token'])  # TODO 1
    c_header = 'Content-Type: application/json'                             # TODO 1

    vm_count = int(params['num_vm'])
    if vm_count == 1:
        payload['name'] = '{0}-{1}'.format(hostname, 0)
    else:
        payload['names'] = ['{hostname}-{n}'.format(hostname=hostname, n=i)
                            for i in range(vm_count)]

    payload['region'] = params['region']
    payload['size']   = params['size']
    payload['image']  = 'ubuntu-16-04-x64'
    # headers = {
    #     'Authorization': 'Bearer {pa_token}'.format(pa_token=pa_token),
    #     'Content-Type': 'application/json'
    # }                                                             # TODO 1
    # headers['Authorization'] = 'Bearer {pa_token}'.format(pa_token=pa_token) # TODO 1
    # headers['Content-Type'] = 'application/json'                             # TODO 1
    # keys = json.loads(requests.get('https://api.digitalocean.com/v2/account/keys', headers=headers).text)['ssh_keys']
    # payload['ssh_keys'] = [str(key['id']) for key in keys if key['name'] == socket.gethostname()]
    payload['ssh_keys'] = [get_key_id(params['pa_token'], params['working_dir'])]

    # print('ssh_keys:', payload['ssh_keys'])

    payload['tags'] = [params['tag']]
    endstate = 'curl -X POST "{endpoint}"            \
                -d \'{payload}\'                     \
                -H "{a_header}"                      \
                -H "{c_header}"'                     \
                .format(endpoint=endpoint,
                        payload=json.dumps(payload),
                        a_header=a_header.strip(),
                        c_header=c_header)   # TODO 2
    return re.sub(' +', ' ', endstate)       # TODO 2


def get_host(droplet_id, writeout_file, params):
    writeout_file_i = '{0}-{1}.json'. \
        format(writeout_file.split('.')[0], str(droplet_id))

    os.system('curl -X GET "https://api.digitalocean.com/v2/droplets/{droplet_id}" \
                -H "Content-Type: application/json" \
                -H "Authorization: Bearer {pa_token}" > {writeout_file_i}'
              .format(droplet_id=droplet_id,
                      pa_token=params['pa_token'],
                      writeout_file_i=writeout_file_i))

    payload = json.load(open(writeout_file_i))
    ip_address = payload['droplet']['networks']['v4'][0]['ip_address']
    return ip_address


def get_key_id(token, working_dir):
    cmd = 'curl -X GET -H "Content-Type: application/json" ' \
        + '-H "Authorization: Bearer {0}" '.format(token) \
        + '"https://api.digitalocean.com/v2/account/keys" > ' \
        + '{working_dir}/curl_out.txt'.format(working_dir=working_dir)

    # print(cmd)
    os.system(cmd)

    filnm = '{working_dir}/curl_out.txt'.format(working_dir=working_dir)
    json_data = open(filnm).read()
    values = json.loads(json_data)

    return values['ssh_keys'][0]['id']
