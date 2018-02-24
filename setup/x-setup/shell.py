#!/usr/bin/env python3

import datetime
import json
import os
import time

from wrappers import digitalocean


def spin_up():
    valid_input = False
    num_tries = 10
    while not valid_input and num_tries > 0:
        user_inp = input("How many VMs?")
        num_tries -= 1
        if user_inp.isdigit():
            valid_input = True
            num_vm = int(user_inp)

            if num_vm == 0:
                print("Must be at least 1 vm, try again")
                valid_input = False

    cur_dt = datetime.datetime.now()
    time_stamp = '{0}{1}{2}_{3}{4}{5}'.\
        format(cur_dt.year, cur_dt.month, cur_dt.day, cur_dt.hour, cur_dt.minute, cur_dt.second)

    writeout_file = 'logs/build-{time_stamp}.json'.format(time_stamp=time_stamp)
    os.system('{unix_command} > {writeout_file}'
              .format(unix_command=digitalocean.builder(num_vm), writeout_file=writeout_file))
    time.sleep(60)
    return harden(writeout_file)


def harden(writeout_file):
    response = json.load(open(writeout_file))
    payloads = []
    if 'droplets' in response:
        payloads = response['droplets']
    else:
        payloads = [response['droplet']]

    ip_addresses = []
    for payload in payloads:
        ip_addresses.append(digitalocean.get_host(payload['id'], writeout_file))

    for ip_address in ip_addresses:
        os.system('ssh -o "StrictHostKeyChecking no" root@{ip_address} \'bash -s\' < procedures/remote0.sh'.format(ip_address=ip_address))
        os.system('scp /home/kenso/.ssh/id_rsa.pub root@{ip_address}:/etc/ssh/kensotrabing/authorized_keys'.format(ip_address=ip_address))
        os.system('sh -c \'echo "kensotrabing:swordfish" > /home/kenso/dotfiles/setup/.credentials\'')
        os.system('scp /home/kenso/dotfiles/setup/.credentials root@{ip_address}:/home/kensotrabing/'.format(ip_address=ip_address))
        os.system('ssh -o "StrictHostKeyChecking no" root@{ip_address} \'bash -s\' < procedures/remote1.sh'.format(ip_address=ip_address))
    os.system('rm /home/kenso/dotfiles/setup/.credentials')
    return ip_addresses

if __name__ == '__main__':
    from pprint import pprint
    pprint(spin_up())
