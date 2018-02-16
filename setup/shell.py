#!/usr/bin/env python3

import datetime
import json
import os
# import sys
import time

from wrappers import digitalocean


# TODO 1: Write a module for AWS Lightsail.
# TODO 2: Write an error handler.

def spin_up(params):
    # timestamp_utc = time.time()

    now = datetime.datetime.now()
    timestamp_local = '{0}{1}{2}_{3}{4}{5}'.\
        format(now.year, now.month, now.day, now.hour, now.minute, now.second)

    writeout_file = '{working_dir}/build-{timestamp_local}.json'.\
        format(working_dir=params['working_dir'], timestamp_local=timestamp_local)
    aws_lightsail = ['awsl', 'aws lightsail']
    digital_ocean = ['do', 'digital ocean']

    for vendor_choice in params['platforms']:
        if vendor_choice in aws_lightsail:
            pass     # TODO 1
        elif vendor_choice in digital_ocean:
            os.system('{unix_command} > {writeout_file}'
                      .format(unix_command=digitalocean.builder(params),
                              writeout_file=writeout_file))
            time.sleep(60)
            return harden(writeout_file, params)
    else:
        pass     # TODO 2


def harden(writeout_file, params):
    response = json.load(open(writeout_file))
    payloads = []
    if 'droplets' in response:
        payloads = response['droplets']
    else:
        payloads = [response['droplet']]

    ip_addresses = []
    for payload in payloads:
        ip_addresses.append(digitalocean.get_host(payload['id'], writeout_file, params))

    # print('ip_addresses:', ip_addresses)

    for ip_address in ip_addresses:
        # print('remote0.sh')
        os.system('ssh -o "StrictHostKeyChecking no" root@{ip_address} \'bash -s\' < procedures/remote0.sh'
                  .format(ip_address=ip_address))

        # print('id_rsa.pub')
        os.system('scp /home/steve/.ssh/id_rsa.pub root@{ip_address}:/etc/ssh/steve/authorized_keys'
                  .format(ip_address=ip_address))

        # print('credentials')
        os.system('sh -c \'echo "steve:swordfish" > {working_dir}/.credentials\''.
                  format(working_dir=params['working_dir']))

        # print('scp credentials')
        os.system('scp {working_dir}/.credentials root@{ip_address}:/home/steve/'
                  .format(working_dir=params['working_dir'], ip_address=ip_address))

        # print('remote1.sh')
        os.system('ssh -o "StrictHostKeyChecking no" root@{ip_address} \'bash -s\' < procedures/remote1.sh'
                  .format(ip_address=ip_address))

        # print('remove credentials')
        os.system('rm {working_dir}/.credentials'.format(working_dir=params['working_dir']))

    return ip_addresses


def get_params():
    with open('./params.json', 'r') as handle:
        params = json.load(handle)

    # make sure working directory exists
    if not os.path.exists(params['working_dir']):
        os.makedirs(params['working_dir'])

    # print(json.dumps(params, indent=4, sort_keys=True))
    pa_token = open('{pat_path}'.format(pat_path=params['pat_path'])).read().strip()
    params['pa_token'] = pa_token

    return params


def main():
    from pprint import pprint
    # params contains things like platforms, number of vm's and vm properties
    params = get_params()
    # print(json.dumps(params, indent=4, sort_keys=True))

    if params['num_vm'] <= 0:
        print('Error: You cannot spin up less than one server.')
    else:
        pprint(spin_up(params))


if __name__ == '__main__':
    main()
