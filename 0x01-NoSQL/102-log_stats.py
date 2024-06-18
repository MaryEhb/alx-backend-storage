#!/usr/bin/env python3
'''15. Log stats - new version'''
from pymongo import MongoClient


if __name__ == '__main__':
    client = MongoClient('mongodb://127.0.0.1:27017')
    c = client.logs.nginx
    print('{} logs'.format(c.count_documents({})))
    print('Methods:')
    print('\tmethod GET: {}'.format(c.count_documents({'method': 'GET'})))
    print('\tmethod POST: {}'.format(c.count_documents({'method': 'POST'})))
    print('\tmethod PUT: {}'.format(c.count_documents({'method': 'PUT'})))
    print('\tmethod PATCH: {}'.format(c.count_documents({'method': 'PATCH'})))

    delete = c.count_documents({'method': 'DELETE'})
    print('\tmethod DELETE: {}'.format(delete))

    get_status = c.count_documents({'method': 'GET', 'path': '/status'})
    print('{} status check'.format(get_status))

    print('IPs:')
    ips = c.aggregate([
        {'$group': {'_id': '$ip', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}},
        {'$limit': 10}
    ])

    for ip in ips:
        print('\t{}: {}'.format(ip.get('_id'), ip.get('count')))
