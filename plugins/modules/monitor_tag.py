#!/usr/bin/python
from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.basic import AnsibleModule

from uptimekumaapi import UptimeKumaApi

__metaclass__ = type


# TODO:
# monitor tag edit


DOCUMENTATION = r'''
'''

EXAMPLES = r'''
- name: Add monitor tag
  uptime_kuma_monitor_tag:
    monitor_name: Peer 1
    tag_name: Tag 1
    value: Tag Value
    state: present
- name: Remove monitor tag
  uptime_kuma_monitor_tag:
    monitor_name: Peer 1
    tag_name: Tag 1
    value: Tag Value
    state: absent
'''

RETURN = r'''
'''


def get_monitor_by_name(api, name):
    monitors = api.get_monitors()
    for monitor_data in monitors.values():
        if monitor_data["name"] == name:
            return monitor_data


def get_tag_by_name(api, name):
    r = api.get_tags()
    tags = r["tags"]
    for tag in tags:
        if tag["name"] == name:
            return tag


def get_monitor_tag(monitor, tag, value):
    for monitor_tag in monitor["tags"]:
        if monitor_tag["name"] == tag["name"] and monitor_tag["color"] == tag["color"] and monitor_tag["value"] == value:
            return monitor_tag


def main():
    module_args = {
        "api_url": {
            "type": str,
            "required": True
        },
        "api_username": {
            "type": str,
            "required": True
        },
        "api_password": {
            "type": str,
            "required": True,
            "no_log": True
        },
        "monitor_name": {
            "type": str,
            "required": True
        },
        "tag_name": {
            "type": str,
            "required": True
        },
        "value": {
            "type": str,
            "required": True
        },
        "state": {
            "default": "present",
            "choices": [
                "present",
                "absent"
            ]
        }
    }
    module = AnsibleModule(module_args)
    params = module.params

    api = UptimeKumaApi(params["api_url"])
    api.login(params["api_username"], params["api_password"])

    monitor_name = params["monitor_name"]
    tag_name = params["tag_name"]
    value = params["value"]
    state = params["state"]

    monitor = get_monitor_by_name(api, monitor_name)
    tag = get_tag_by_name(api, tag_name)

    tag_id = tag["id"]
    monitor_id = monitor["id"]

    monitor_tag = get_monitor_tag(monitor, tag, value)

    changed = False
    failed_msg = False
    result = {}
    if state == "present":
        if not monitor_tag:
            r = api.add_monitor_tag(tag_id, monitor_id, value)
            if not r["ok"]:
                failed_msg = r["msg"]
            changed = True
    elif state == "absent":
        if monitor_tag:
            r = api.delete_monitor_tag(tag_id, monitor_id, value)
            if not r["ok"]:
                failed_msg = r["msg"]
            changed = True
    api.disconnect()

    if failed_msg:
        module.fail_json(msg=failed_msg, **result)

    result["changed"] = changed
    module.exit_json(**result)


if __name__ == '__main__':
    main()
