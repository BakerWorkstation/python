import sys
from PyQt5.Qt import *
from PyQt5.uic import loadUi
from confluent_kafka.admin import AdminClient
from confluent_kafka import Consumer, KafkaError, TopicPartition


def connect_kafka(broker_list):
    consume = Consumer({
                        'bootstrap.servers': broker_list,
                        'group.id': "test_1",
                        'enable.auto.commit': False,
                        'max.poll.interval.ms': 10000000,
                        'default.topic.config': {'auto.offset.reset': 'smallest'}
    })
    return consume

def list_topic(broker_list):
    kadmin = AdminClient({'bootstrap.servers': broker_list})
    topics = kadmin.list_topics().topics
    return topics.keys()

def list_partitiion(broker_list, topic):
    kadmin = AdminClient({'bootstrap.servers': broker_list})
    partition = kadmin.list_topics().topics[topic].partitions
    total = []
    consume = Consumer({
                        'bootstrap.servers': broker_list,
                        'group.id': 'tool_group',
    })
    print(dir(consume))
    for eachpart, eachmessage in partition.items():
        tp_c = TopicPartition(topic, eachpart, 0)
        # 获取数据对应最小offset 与 redis记录中的offset比较
        kafka_offset = consume.get_watermark_offsets(tp_c)
        data = [str(eachpart), str(eachmessage.leader), ','.join(map(lambda x:str(x), eachmessage.replicas)), ','.join(map(lambda x:str(x), eachmessage.isrs)), str(kafka_offset[0]), str(kafka_offset[-1])]
        total.append(data)
    return total



class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('直接加载ui文件')
        self.resize(500, 500)
        self.move(400, 200)
        self.set_ui()
        self.count = 0
        

    def set_ui(self):
        a=loadUi('./redis.ui', self)
        self.open.clicked.connect(self.connect)
        self.flushtopic.clicked.connect(self.connect)
        self.comboBox.activated.connect(self.parts)
    
    def parts(self):
        topic = self.comboBox.currentText()
        total = list_partitiion(self.broker, topic)
        self.tableWidget.clearContents()
        if self.count:
            for line in range(self.count):
                self.tableWidget.removeRow(line)
        for eachline in total:
            self.tableWidget.insertRow(0)
            for index, item in enumerate(eachline):
                self.tableWidget.setItem(0, index, QTableWidgetItem(item))
            self.tableWidget.update()
        count = self.tableWidget.rowCount()
        self.count = count



    def connect(self):
        """
        点击登录的按钮事件
        :return:
        """
        self.broker = self.address.toPlainText()
        self.topics = list_topic(self.broker)
        self.progressBar.setValue(100)
        print(self.topics)
        self.comboBox.addItems(self.topics)
        self.parts()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())