#!/usr/bin/python
# %%
import sys

with open("providers.txt") as f:
    providers = [l.strip() for l in f.readlines()]
# %%
with open("base_config.yaml") as f:
    for l in f.readlines():
        print(l, end="")
# %%
print(
    """
proxies:

proxy-groups:
  - name: loc
    type: select
    url: 'http://www.gstatic.com/generate_204'
    proxies:
      - from_ALL
      - from_US
      - from_NUS
  - name: Relay
    type: relay
    url: 'http://www.gstatic.com/generate_204'
    proxies:
      - loc
      - loc
  - name: proxy
    type: select
    url: 'http://www.gstatic.com/generate_204'
    proxies:
      - loc
      - Relay
      - DIRECT
  - name: Default
    type: select
    proxies:
      - DIRECT
      - proxy
""")

# %%
for l in ["US", "NUS"]:
    print("""
  - name: from_{0}
    type: load-balance
    url: 'http://www.gstatic.com/generate_204'
    strategy: round-robin # consistent-hashing or round-robin
    use:
{1}
""".format(l,
        "\n".join(["      - %s_%s" % (p,l) for p in providers])
    ))
# %%
print("""
  - name: from_ALL
    type: load-balance
    url: 'http://www.gstatic.com/generate_204'
    strategy: round-robin # consistent-hashing or round-robin
    use:
{0}
""".format("\n".join(["      - %s_%s" % (p,l) for p in providers for l in ["US", "NUS"]])))
# %%
print(
    """
proxy-providers:
"""
)
for i in providers:
    for (suffix,param) in [("US","c=US"),("NUS","nc=US")] :
        print("""
  {0}_{1}:
    type: http
    url: "http://{0}/clash/proxies?{2}"
    interval: 86400
    path: providers/{0}_{1}
    health-check:
      enable: true
      interval: 3600
      url: https://i.ytimg.com/generate_204
""".format(
            i, suffix, param
        )
    )

# %%
with open("rules.yaml", "rt") as f:
    for l in f.readlines():
        print(l, end="")
# %%
