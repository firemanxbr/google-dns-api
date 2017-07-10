"""Open Source tool to management domains in Google Cloud DNS
    using JSON files

    more informations please consulte the README.md
"""
import time
from google.cloud import dns


def client_conn(project_id=None):
    """Create a connection with Google DNS API

    :param project_id: a project_id of Google Cloud Platform

    :returns: an object connection of Google DNS
    """
    client = dns.Client(project=project_id)
    return client


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
    """print (create_zone('product',
                       'product.example.com.',
                       'domain used of blog product.example.com'))"""
    print (create_record('product',
                         'product.example.com.',
                         '4eef4a76dfb2072eb7cba2a2263278cf.product.example.com.',
                         'CNAME',
                         3600,
                         ['388ba5b47e181376c968bf08550b68de538c1f38.comodoca.com.']))
    print (create_record('product',
                         'product.example.com.',
                         'product.example.com.',
                         'A',
                         3600,
                         ["52.0.16.118","52.1.119.170","52.1.147.205","52.1.173.203","52.4.145.119","52.4.175.111","52.4.225.124","52.4.240.221","52.4.38.70","52.5.181.79","52.6.3.192","52.6.46.142"]))
