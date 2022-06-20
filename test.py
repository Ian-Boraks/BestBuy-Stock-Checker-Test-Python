proxy_dict_list = []

with open("proxies") as f:
    d = {}
    for line in f:
        d['http'] = line.strip()
        proxy_dict_list.append(dict(d))
print(proxy_dict_list)
