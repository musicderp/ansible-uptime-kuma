#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Lucas Held <lucasheld@hotmail.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r'''
---
extends_documentation_fragment:
  - lucasheld.uptime_kuma.uptime_kuma

module: monitor_info
author: Lucas Held (@lucasheld)
short_description: Retrieves facts about a monitor.
description: Retrieves facts about a monitor.

options:
  id:
    description: The id of the monitor to inspect.
    type: int
  name:
    description: The name of the monitor to inspect.
    type: str
'''

EXAMPLES = r'''
- name: get all monitors
  lucasheld.uptime_kuma.monitor_info:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
  register: result
'''

RETURN = r'''
monitors:
  description: The monitors as list
  returned: always
  type: complex
  contains:
    id:
      description: The id of the monitor.
      returned: always
      type: int
      sample: 1
    name:
      description: The name of the monitor.
      returned: always
      type: str
      sample: 'test'
    url:
      description: The url of the monitor.
      returned: always
      type: str
      sample: 'https://google.com'
    method:
      description: The http method of the monitor.
      returned: always
      type: str
      sample: 'GET'
    hostname:
      description: The hostname of the monitor.
      returned: always
      type: str
      sample: None
    port:
      description: The port of the monitor.
      returned: always
      type: int
      sample: 53
    maxretries:
      description: The retries of the monitor.
      returned: always
      type: int
      sample: 0
    weight:
      description: The weight of the monitor.
      returned: always
      type: int
      sample: 2000
    active:
      description: True if upside down mode is active.
      returned: always
      type: bool
      sample: True
    type:
      description: The type of the monitor.
      returned: always
      type: str
      sample: 'http'
    interval:
      description: The heartbeat interval of the monitor.
      returned: always
      type: int
      sample: 60
    retryInterval:
      description: The heartbeat retry interval of the monitor.
      returned: always
      type: int
      sample: 60
    keyword:
      description: The keyword of the monitor.
      returned: always
      type: str
      sample: None
    expiryNotification:
      description: True if certificate expiry notification is enabled.
      returned: always
      type: bool
      sample: False
    ignoreTls:
      description: True if ignore tls error is enabled.
      returned: always
      type: bool
      sample: False
    upsideDown:
      description: True if upside down mode is enabled.
      returned: always
      type: bool
      sample: False
    maxredirects:
      description: The max redirects of the monitor.
      returned: always
      type: int
      sample: 10
    accepted_statuscodes:
      description: The accepted status codes of the monitor.
      returned: always
      type: list
      sample: ['200-299']
    dns_resolve_type:
      description: The dns resolve type of the monitor.
      returned: always
      type: str
      sample: 'A'
    dns_resolve_server:
      description: The dns resolve server of the monitor.
      returned: always
      type: str
      sample: '1.1.1.1'
    dns_last_result:
      description: The dns last result of the monitor.
      returned: always
      type: str
      sample: None
    proxyId:
      description: The proxy id of the monitor.
      returned: always
      type: int
      sample: 1
    notificationIDList:
      description: The notification ids of the monitor.
      returned: always
      type: list
      sample: [1,3]
    tags:
      description: The tags of the monitor.
      returned: always
      type: list
      sample: []
    mqttUsername:
      description: The mqtt username of the monitor.
      returned: always
      type: str
      sample: None
    mqttPassword:
      description: The mqtt password of the monitor.
      returned: always
      type: str
      sample: None
    mqttTopic:
      description: The mqtt topic of the monitor.
      returned: always
      type: str
      sample: None
    mqttSuccessMessage:
      description: The mqtt success message of the monitor.
      returned: always
      type: str
      sample: None
    databaseConnectionString:
      description: The sqlserver connection string of the monitor.
      returned: always
      type: str
      sample: 'Server=<hostname>,<port>;Database=<your database>;User Id=<your user id>;Password=<your password>;Encrypt=<true/false>;TrustServerCertificate=<Yes/No>;Connection Timeout=<int>'
    databaseQuery:
      description: The database query of the monitor.
      returned: always
      type: str
      sample: None
    authMethod:
      description: The auth method of the monitor.
      returned: always
      type: str
      sample: ''
    authWorkstation:
      description: The auth workstation of the monitor.
      returned: always
      type: str
      sample: None
    authDomain:
      description: The auth domain of the monitor.
      returned: always
      type: str
      sample: None
    headers:
      description: The http headers of the monitor.
      returned: always
      type: str
      sample: None
    body:
      description: The http body of the monitor.
      returned: always
      type: str
      sample: None
    basic_auth_user:
      description: The basic auth user of the monitor.
      returned: always
      type: str
      sample: None
    basic_auth_pass:
      description: The basic auth pass of the monitor.
      returned: always
      type: str
      sample: None
    pushToken:
      description: The push token of the monitor.
      returned: always
      type: str
      sample: None
'''

import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import common_module_args, get_monitor_by_name
from ansible.module_utils.basic import missing_required_lib

try:
    from uptime_kuma_api import UptimeKumaApi
    HAS_UPTIME_KUMA_API = True
except ImportError:
    HAS_UPTIME_KUMA_API = False


def run(api, params, result):
    if params["id"]:
        monitor = api.get_monitor(params["id"])
        monitors = [monitor]
    elif params["name"]:
        monitor = get_monitor_by_name(api, params["name"])
        monitors = [monitor]
    else:
        monitors = api.get_monitors()

    for monitor in monitors:
        # notificationIDList dict to list[int]
        notification_ids = []
        for notification_id, notification_enabled in monitor["notificationIDList"].items():
            if notification_enabled:
                notification_id = int(notification_id)
                notification_ids.append(notification_id)
        monitor["notificationIDList"] = notification_ids

    result["monitors"] = monitors


def main():
    module_args = dict(
        id=dict(type="int"),
        name=dict(type="str"),
    )
    module_args.update(common_module_args)

    module = AnsibleModule(module_args, supports_check_mode=True)
    params = module.params

    if not HAS_UPTIME_KUMA_API:
        module.fail_json(msg=missing_required_lib("uptime_kuma_api"))

    api = UptimeKumaApi(params["api_url"])
    api_token = params.get("api_token")
    if api_token:
      api.login_by_token(api_token)
    else:
      api.login(params["api_username"], params["api_password"])

    result = {
        "changed": False
    }

    try:
        run(api, params, result)

        api.disconnect()
        module.exit_json(**result)
    except Exception:
        api.disconnect()
        error = traceback.format_exc()
        module.fail_json(msg=error, **result)


if __name__ == '__main__':
    main()
