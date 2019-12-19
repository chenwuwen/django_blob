import json

import requests
from django.http import HttpResponse

from common.consul_config import ConsulConf

# 实例化ConsulConf()对象
consul = ConsulConf()


# 调用NODE-SERVICE远程服务
def node_micro_service(request):
    ip, port = consul.get_ip_port('NODE-SERVICE')
    print(f"从Consul得到nodeMicroService的地址是：{ip}:{port}")
    address = 'http://' + str(ip) + ":" + str(port)
    address += "/search/users/bar"
    print(f"从Consul取到服务地址：{address}")
    # 使用requests请求返回的是Response对象(requests.models.Response),不能直接返回
    r = requests.get(address)
    print(type(r))
    return HttpResponse(json.dumps(r.text, ensure_ascii=False), content_type="application/json,charset=utf-8")
