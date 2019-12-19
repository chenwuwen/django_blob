"""
Consul配置
"""

from consul import Consul

import consul

'''
django配置
'''
django_config_dic = {
    'SERVICE_NAME': 'django_service',
    'ip': '127.0.0.1',
    'port': 8000
}

'''
consul配置
'''
consul_config_dic = {
    'ip': '127.0.0.1',
    'port': 8500
}


class ConsulConf:

    # 初始化，指定consul主机，端口，和token
    def __init__(self):
        self.service_name = django_config_dic['SERVICE_NAME']
        self.host = django_config_dic['ip']  # django运行 主机
        self.port = django_config_dic['port']  # django运行 端口
        print(f"ConsulConf类 __init__()方法开始初始化Consul连接,连接信息：服务名: {self.service_name} IP: {self.host} 端口号：{self.port}")
        self.consul = Consul(host=consul_config_dic['ip'], port=consul_config_dic['port'])
        print("成功连接到Consul!")

    # 注册到consul
    def register(self):
        # 连接consul 服务器，默认是127.0.0.1，可用host参数指定host
        print(f"开始注册服务{self.service_name}")
        # 健康检查的ip，端口，检查时间
        check = consul.Check.tcp(self.host, self.port, "10s")
        # 注册服务部分
        self.consul.agent.service.register(self.service_name,
                                           f"{self.service_name}-{self.host}-{self.port}",
                                           address=self.host, port=self.port, check=check)
        print(f"注册服务{self.service_name}成功")

    # 取消注册到consul
    def deregister(self):
        print(f"开始退出服务{self.service_name}")
        self.consul.agent.service.deregister(f'{self.service_name}-{self.host}-{self.port}')
        self.consul.agent.check.deregister(f'{self.service_name}-{self.host}-{self.port}')

    # 通过服务名,查询出可用的一个ip，和端口
    def get_ip_port(self, service_name):
        # 得到注册在consul上服务
        all_service = self.consul.agent.services()
        # 返回的是字典类型
        print(type(all_service))
        # print(all_service[service_name]['Address'])
        # python中的三元运算符是这样的,如果没有找到对应的service_name则返回None(这里不用的原因是三元运算符不支持多个值,具体可看单元测试)
        # return None, None if all_service[service_name] is None else all_service[service_name]['Address'], \
        #        all_service[service_name]['Port']
        if all_service[service_name] is None:
            return None, None
        return all_service[service_name]['Address'], all_service[service_name]['Port']


if __name__ == '__main__':
    c = ConsulConf()
    print('单元测试consul')
    print('python三元运算符,不支持多个值')
    # g, f = 'c', 'd' if 2 > 1 else 'a', 'b'
    # print(f"g的值是{g},f的值是{f}")
