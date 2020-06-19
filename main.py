#!/usr/bin/env python3
# encoding: utf-8
# ===============================================================================
#
#         FILE:
#
#        USAGE:
#
#  DESCRIPTION:
#
#      OPTIONS:  ---
# REQUIREMENTS:  ---
#         BUGS:  ---
#        NOTES:  ---
#       AUTHOR:  YOUR NAME (),
#      COMPANY:
#      VERSION:  1.0
#      CREATED:
#     REVISION:  ---
# ===============================================================================

import os
import sys
from datetime import timezone, datetime
from flask import Flask, request, Response
from collections import OrderedDict
from functools import wraps
import json
from flask_cors import CORS
from influxdb import InfluxDBClient
from elasticsearch import Elasticsearch
import schema

influxdb_ip = os.environ.get('INFLUXDB_IP', default='127.0.0.1')
influxdb_port = os.environ.get('INFLUXDB_PORT', default=8086)
influxdb_user = os.environ.get('INFLUXDB_USER', default='')
influxdb_pass = os.environ.get('INFLUXDB_PASS', default='')
influxdb_db = os.environ.get('INFLUXDB_DB', default='app')
es_group = os.environ.get("ES_TARGET", default='127.0.0.1:9200')
es_group = es_group.split(',')

try:
    influxdb_port = int(influxdb_port)
except (TypeError, ValueError):
    influxdb_port = 8086

app = Flask(__name__)
CORS(app)


def get_influxdb_instance(db=influxdb_db):
    client = InfluxDBClient(
        host=influxdb_ip,
        port=influxdb_port,
        username=influxdb_user,
        password=influxdb_pass,
        database=db
    )
    if db not in [x['name'] for x in client.get_list_database()]:
        client.create_database(db)
    return client


def get_elasticsearch_instance():
    # es = Elasticsearch()    # 默认连接本地elasticsearch
    # es = Elasticsearch(['127.0.0.1:9200'])  # 连接本地9200端口
    # es = Elasticsearch(["192.168.1.10", "192.168.1.11", "192.168.1.12"]) # 连接集群，以列表的形式存放各节点的IP地址
    es = Elasticsearch(
        es_group,
        # 连接前测试
        sniff_on_start=True,
        # 节点无响应时刷新节点
        sniff_on_connection_fail=True,
        # 设置超时时间
        sniff_timeout=60
    )
    return es


def get_std_output():
    stand = OrderedDict()
    stand['ret'] = 200
    stand['data'] = None
    stand['msg'] = ""
    return stand


def stand_output():
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            stand = get_std_output()
            if type(result) == list or type(result) == tuple:
                try:
                    stand['ret'] = int(result[0])
                except IndexError:
                    stand['ret'] = 500
                    stand['data'] = None
                    stand['msg'] = "Return String error"
                    return json.dumps(stand)
                try:
                    stand['data'] = result[1]
                except IndexError:
                    pass
                try:
                    stand['msg'] = result[2]
                except IndexError:
                    pass
            else:
                stand['data'] = result
            result = json.dumps(stand)
            return Response(result, mimetype='application/json', status=stand['ret'])
        return wrapper
    return decorate


@app.route('/elk/app1', methods=['POST'])
@stand_output()
def save_iot_log():
    es = get_elasticsearch_instance()
    data = request.get_json(silent=True)
    if not schema.verify_iot_log(data):
        return 400, None, "Json schema error"
    now = datetime.now(tz=timezone.utc)
    rt = es.index(
        index='data-iot-pi-%s' % now.strftime('%Y.%m.%d'),
        doc_type='doc',
        body=data
    )
    return 200, rt, ""


@app.route('/tsdb/schema/t', methods=['GET'])
@stand_output()
def get_t_schema():
    return 200, schema.temperature, "ok"


@app.route('/tsdb/t', methods=['GET'])
@stand_output()
def load_temperature():
    _limit = 10000
    client = get_influxdb_instance('iot')
    results = client.query("select * from temperature limit %d" % _limit)
    data = [d for d in results.get_points(measurement='temperature')]
    return 200, data, "data limit = %d" % _limit


@app.route('/tsdb/t', methods=['POST'])
@stand_output()
def save_temperature():
    client = get_influxdb_instance('iot')
    data = request.get_json(silent=True)
    if not schema.verify_temperature(data):
        return 400, None, "Json schema error"
    if 'name' in data:
        name = data['name']
    else:
        name = ''
    payload = [{
        "measurement": "temperature",
        "time": data['time'],
        "tags": {
            "uuid": data['uuid'],
            "name": name
        },
        "fields": {
            "value": data['value']
        }
    }]
    return 200, "", client.write_points(payload)


if __name__ == '__main__':
    listen = '127.0.0.1'
    port = 10080
    # print("Starting App...")
    app.run(host=listen, port=port, threaded=True)

