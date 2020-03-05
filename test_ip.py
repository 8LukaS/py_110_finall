import random
import re


def fab_privacy_net(ip_net):
    if ip_net == '192.168.0.0':
        ip_privat_net = re.compile("192\.168\.\d{1,3}\.\d{1,3}")
    elif ip_net == '10.0.0.0':
        ip_privat_net = re.compile("10\.\d{1,3}\.\d{1,3}\.\d{1,3}")

    def privacy_net(fn):
        def wrapper(*args):
            wrapper_gen = fn(*args)
            for ip in wrapper_gen:
                if ip_privat_net.search(ip) is None:
                    wrapper_filter = yield ip
                else:
                    print("Некорректный IP адрес")
                    wrapper_filter = yield None
                if wrapper_filter is not None:
                    wrapper_gen.send(wrapper_filter)
        return wrapper
    return privacy_net



@fab_privacy_net("192.168.0.0")
def ip_gen(filter_=[[], [], [], []]):
    while True:
        ip = []
        # фильтры для октетов
        for f in filter_:
            if not f:
                ip.append(str(random.randint(0, 255)))
            else:
                ip.append(str(random.choice(f)))
        filter_input = yield ".".join(ip)
        if filter_input is not None:
            filter_ = filter_input
            print(filter_)


if __name__ == "__main__":
    my_gen = ip_gen()
    for _ in range(10):
        ip = my_gen.send(None)
        print(ip)

    ip = my_gen.send([[192], [168], [], []])
    print(ip)

    for _ in range(10):
        ip = my_gen.send(None)
        print(ip)




    # my_gen = gen_ip()
    # for _ in range(10):
    #     print(my_gen.send(None))

    # def other_privat_net(decor_filter):
    #     if decor_filter == "192.168":
    #         regex = r"192\.168\.\d{1,3}\.\d{1,3}"
    #     elif decor_filter == "10":
    #         regex = r"10\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    #
    #     def privat_net(fn):
    #         def wrapper(*args):
    #             wrapper_gen = fn(*args)
    #             while True:
    #                 ip = wrapper_gen.send(None)
    #                 print(ip)
    #                 if re.match(regex, ip) is None:
    #                     yield ip
    #                 else:
    #                     yield "Недопустимый IP"
    #
    #         return wrapper
    #
    #     return privat_net
    #
    #
    # @other_privat_net("192.168")
    # def gen_ip():
    #     filter_main = [[], [], [], []]
    #     while True:
    #         ip = []
    #         for f in filter_main:
    #             if not f:
    #                 ip.append(str(random.randint(0, 255)))
    #             else:
    #                 ip.append(str(random.choice(f)))
    #         filter_input = yield ".".join(ip)
    #         if filter_input is not None:
    #             filter_main = filter_input
    #             print(filter_main)