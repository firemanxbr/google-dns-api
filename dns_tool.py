"""Google Cloud Platform DNS Tool

    This is an open source tool to management domains
    in Google Cloud DNS using JSON files as reference

    more informations please consulte the README.md
"""
import json
import time

from argparse import ArgumentParser

try:
    from google.cloud import dns
except ImportError:
    print('please check the requeriments.txt and README.md')
    exit()


def client_conn(project_id=None):
    """Create a connection with Google DNS API

    :param project_id: a project_id of Google Cloud Platform

    :returns: an object connection of Google DNS
    """
    client = dns.Client(project=project_id)
    return client


def check_zone(name):
    """Check if the zone exists

    :param name: a name of the new zone
    
    :returns: True if the zone name exist
    """
    client = client_conn()
    zones = client.list_zones()
    for zone in zones:
        if zone.name == name:
            return True


def create_zone(name, dns_name, description):
    """Create a new zone

    :param name: a name of the new zone
    :param dns_name: domain of this zone, don't forget final point '.'
    :param description: a description about this zone or ""

    :returns: a false if not created or true
    """
    client = client_conn()
    zone = client.zone(name=name,
                       dns_name=dns_name,
                       description=description)
    zone.create()
    return zone.exists()


def create_record(name, dns_name, record_name, record_type, ttl, value):
    """Create a new record with a existent zone

    :param name: a name of zone
    :param dns_name: domain of the zone
    :param record_name: reference of the new record, for example:
                        'record_name'.zone-domain.extension
    :param record_type: type of record on DNS, for example:
                        'A', 'AAAA', 'CAA', 'CNAME', 'MX', 'NAPTR',
                        'NS', 'PTR', 'SPF', 'SRV' & 'TXT'
    :param ttl: ttl in seconds, default is 3600 seconds = 5 min (not string)
    :param value: any value of record single or multiple,
                  for example: ["value"] or ["8.8.8.8", "8.8.4.4"]

    :returns: log_records with all records about this zone
    """
    client = client_conn()
    zone = client.zone(name=name, dns_name=dns_name)

    record_set = zone.resource_record_set(record_name, record_type, ttl, value)
    changes = zone.changes()
    changes.add_record_set(record_set)

    try:
        changes.create()

        while changes.status != 'done':
            time.sleep(1)
            changes.reload()

        records = zone.list_resource_record_sets()
        log_records = [(record.name, record.record_type, record.ttl, record.rrdatas)
                       for record in records]

        return log_records

    except BaseException:
        return "the record %s already exists" % record_name



if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-f', '--file', help="your json file", required=True)
    args = parser.parse_args()

    if args.file:

        with open(args.file, 'r') as f:
            data = json.load(f)

            if check_zone(name=data['name']) is not True:
                create_zone(name=data['name'],
                            dns_name=data['zone'],
                            description=data['description'])

            for reg in range(len(data['records'])):
                create_record(name=data['name'],
                              dns_name=data['zone'],
                              record_name=data['records'][reg]['name'],
                              record_type=data['records'][reg]['type'],
                              ttl=data['records'][reg]['ttl'],
                              value=data['records'][reg]['value'])
