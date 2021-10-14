# _*_ coding: utf-8 _*_
"""
# @Time : 2021/9/30 10:39 
# @Author : lijun7 
# @File : soa_create_order.py
# @desc :
"""
import json

import pika


# 生成消息入口处
def get_message():
    # for i in range(10):  # 生成10条消息
    #     message = json.dumps({'id': "10000%s" % i, "amount": 100 * i, "name": "mhec", "createTime": str(datetime.datetime.now())})

    with open('./resource/zf_order_info.json', 'r', encoding='utf-8') as st:
        message = json.load(st)
        message = json.dumps(message)
    producter(message)


# 消息生产者
def producter(message):  # 消息生产者
    # 获取与rabbitmq 服务的连接，虚拟队列需要指定参数 virtual_host，如果是默认的可以不填（默认为/)，也可以自己创建一个
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='127.0.0.1',
            port=5672,
            credentials=pika.PlainCredentials('guest', 'guest')
        )
    )
    # 创建一个 AMQP 信道（Channel）,建造一个大邮箱，隶属于这家邮局的邮箱
    channel = connection.channel()
    # 声明消息队列firstTester，消息将在这个队列传递，如不存在，则创建
    channel.queue_declare(queue='firstTester')
    # 向队列插入数值 routing_key的队列名为firstTester，body 就是放入的消息内容，exchange指定消息在哪个队列传递，这里是空的exchange但仍然能够发送消息到队列中，因为我们使用的是我们定义的空字符串“”exchange（默认的exchange）
    channel.basic_publish(exchange='', routing_key='firstTester', body=message)
    # 关闭连接
    connection.close()


if __name__ == "__main__":
    get_message()  # 程序执行入口
