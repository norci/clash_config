#!/usr/bin/python3

import yaml

with open("base_config.yaml") as hl:
    config = yaml.safe_load(hl)
providers = config["extra"]["providers"]
HC=config["extra"]["health-check"]
for i in range(2):
    config["proxy-groups"][i].update({"use":providers})#, "interval": 3600, "url": HC["url"]})

config["proxy-providers"]={}
for p in providers:
    pp = yaml.safe_load("""
{0}:
  type: http
  url: "http://{0}/clash/proxies"
  interval: 86400
  path: providers/{0}
""".format(p))
    pp[p]["health-check"]=HC
    config["proxy-providers"].update(pp)

RULE_PREFIX = [
"http://127.0.0.1:8080/",
"http://192.168.3.2:8080/",
"https://cdn.jsdelivr.net/gh/norci/clash_config@clash.meta/",
"https://raw.githubusercontent.com/norci/clash_config/clash.meta/",
][1] + "rules/"
config["rule-providers"] = {}
for action in ["REJECT","DIRECT", "PROXY"]:
    for behavior in ["classical","domain"]:
        rn = "%s-%s" % (behavior, action)
        pp = {
"behavior": behavior,
"type": "http",
"url": RULE_PREFIX + rn + ".yaml",
"interval": 86400,
"path": "rules/" + rn + ".yaml"}
        config["rule-providers"][rn] = pp
        config["rules"].append("RULE-SET,%s,%s"%(rn,action))

config["rule-providers"]["whitelist"] = {
"behavior": "domain",
"type": "http",
"url": RULE_PREFIX + "whitelist.yaml",
"interval": 86400,
"path": "rules/" + "whitelist.yaml"
}
config["rules"].append("MATCH,GLOBAL")
config.pop("extra")
with open("../config.yaml", "wt") as hl:
    yaml.dump(config, hl)
