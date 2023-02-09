import unittest
from time import sleep

from ticos_device_mqtt import TicosDeviceMqttClient


class TicosDeviceMqttClientTests(unittest.TestCase):
    """
    Before running tests, do the next steps:
    1. Create device "Example Name" in Ticos
    2. Add shared attribute "attr" with value "hello" to created device
    3. Add client attribute "atr3" with value "value3" to created device
    """

    client = None

    shared_attribute_name = 'attr'
    shared_attribute_value = 'hello'

    client_attribute_name = 'atr3'
    client_attribute_value = 'value3'

    request_attributes_result = None
    subscribe_to_attribute = None
    subscribe_to_attribute_all = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TicosDeviceMqttClient('127.0.0.1', 1883, 'TEST_DEVICE_TOKEN')
        cls.client.connect(timeout=1)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.client.disconnect()

    @staticmethod
    def on_attributes_change_callback(result, exception=None):
        if exception is not None:
            TicosDeviceMqttClientTests.request_attributes_result = exception
        else:
            TicosDeviceMqttClientTests.request_attributes_result = result

    @staticmethod
    def callback_for_specific_attr(result, *args):
        TicosDeviceMqttClientTests.subscribe_to_attribute = result

    @staticmethod
    def callback_for_everything(result, *args):
        TicosDeviceMqttClientTests.subscribe_to_attribute_all = result

    def test_request_attributes(self):
        self.client.request_attributes(shared_keys=[self.shared_attribute_name],
                                       callback=self.on_attributes_change_callback)
        sleep(3)
        self.assertEqual(self.request_attributes_result,
                         {'shared': {self.shared_attribute_name: self.shared_attribute_value}})

        self.client.request_attributes(client_keys=[self.client_attribute_name],
                                       callback=self.on_attributes_change_callback)
        sleep(3)
        self.assertEqual(self.request_attributes_result,
                         {'client': {self.client_attribute_name: self.client_attribute_value}})

    def test_send_telemetry_and_attr(self):
        telemetry = {"temperature": 41.9, "humidity": 69, "enabled": False, "currentFirmwareVersion": "v1.2.2"}
        self.assertEqual(self.client.send_telemetry(telemetry, 0).get(), 0)

        attributes = {"sensorModel": "DHT-22", self.client_attribute_name: self.client_attribute_value}
        self.assertEqual(self.client.send_attributes(attributes, 0).get(), 0)

    def test_subscribe_to_attrs(self):
        sub_id_1 = self.client.subscribe_to_attribute(self.shared_attribute_name, self.callback_for_specific_attr)
        sub_id_2 = self.client.subscribe_to_all_attributes(self.callback_for_everything)

        sleep(1)
        value = input("Updated attribute value: ")

        self.assertEqual(self.subscribe_to_attribute_all, {self.shared_attribute_name: value})
        self.assertEqual(self.subscribe_to_attribute, {self.shared_attribute_name: value})

        self.client.unsubscribe_from_attribute(sub_id_1)
        self.client.unsubscribe_from_attribute(sub_id_2)


if __name__ == '__main__':
    unittest.main('ticos_device_mqtt_client_tests')
