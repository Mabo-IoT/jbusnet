import unittest

from context import calculate_crc, PDU, Request, Response, generate_contents, make_response_bytes

class Test_utils(unittest.TestCase):
    def test_calculate_crc(self):
        """
        test calculate_crc 
        egg.
        01 03 00 00 00 10 = 0x44 0x06
        01 03 00 12 00 10 = 0xE4 0x03

        """
        
        bytes_data1  = memoryview(bytearray([0x01, 0x03, 0x00,0x00,0x00,0x10])).tobytes()
        crc_data1 = memoryview(bytearray([0x44, 0x06])).tobytes()
        self.assertEqual(calculate_crc(bytes_data1), crc_data1)

        bytes_data2  = memoryview(bytearray([0x01, 0x03, 0x00,0x12,0x00,0x10])).tobytes()
        crc_data2 = memoryview(bytearray([0xe4, 0x03])).tobytes()
        self.assertEqual(calculate_crc(bytes_data2), crc_data2)


class TestPDU(unittest.TestCase):
    def setUp(self):
        """
        init PDU instance
        """
        self.pdu = PDU.make_request_pdu(function_code=0x03, address=0x00, length=0x10)

    def tearDown(self):
        del(self.pdu)

    def test_bytes(self):
        """
        test PDU bytes method
        """
        bytes_data = memoryview(bytearray([0x03, 0x00, 0x00, 0x00, 0x10])).tobytes()
        self.assertEqual(bytes_data, self.pdu.bytes)


class TestRequest(unittest.TestCase):
    def setUp(self):
        """
        init request instance
        """
        self.request = Request(unit=0x01,function_code=0x03, address=0x00, length=0x10)

    def tearDown(self):
        del(self.request)
    
    def test_bytes(self):
        """
        test request bytes method
        """
        bytes_data = memoryview(bytearray([0x01,0x03,0x00,0x00, 0x00,0x10, 0x44, 0x06])).tobytes()

        self.assertEqual(bytes_data, self.request.bytes)
    
class TestReponse(unittest.TestCase):
    def setUp(self):
        """
        init response instance
        egg.
        11 04 02 000A F8F4
        """
        bytes_data = memoryview(bytearray([0x11, 0x04, 0x02, 0x00, 0x0a, 0xf8, 0xf4])).tobytes()
        self.response =  Response.make_response(bytes_data)
    
    def test_init(self):
        """
        test classmethod make_response
        """
        unit = int(0x11).to_bytes(1, 'big')
        length = int(0x02).to_bytes(1, 'big')
        function_code = int(0x04).to_bytes(1, 'big')
        contents = memoryview(bytearray([0x00, 0x0a])).tobytes()

        self.assertEqual(unit, self.response.unit)
        self.assertEqual(length, self.response.length)
        self.assertEqual(function_code, self.response.function_id)
        self.assertEqual(contents, self.response.contents)

    def test_check_crc(self):
        """
        test response check_crc method
        """
        bytes_data = memoryview(bytearray([0x11, 0x04, 0x02, 0x00, 0x0a, 0xf8, 0xf4])).tobytes()
        crc = bytes_data[-2:]
        function_specific_data = bytes_data[:-2]
        self.assertEqual(True, self.response.check_crc(function_specific_data, crc))
    
    def test_registers(self):
        """
        test response registers
        """
        # test one element 
        registers = [0x000a]
        self.assertIsInstance(self.response.registers, list)
        self.assertEqual(registers, self.response.registers)

        # test more than one element
        bytes_data = memoryview(bytearray([0x11, 0x04, 0x04, 0x00, 0x0a, 0xf8, 0xf4, 0x88, 0x00])).tobytes()
        self.response =  Response.make_response(bytes_data)
        registers = [0x000a, 0xf8f4]
        self.assertIsInstance(self.response.registers, list)
        self.assertEqual(registers, self.response.registers)
        
        # re init self.response
        self.tearDown()
        self.setUp()
    
    def test_unit_id(self):
        """for i in range(length):
        test response unit_id
        """
        unit_id = 0x11
        self.assertEqual(unit_id, self.response.unit_id)
    
    def test_function_code(self):
        """
        test response unit_id
        """
        function_code = 0x04
        self.assertEqual(function_code, self.response.function_code)
    

class TestSimulator(unittest.TestCase):
    def test_generate_contents(self):
        """
        test jbushandler generate_contents method
        """
        length = 10 
        self.assertIsInstance(generate_contents(length), bytes)
        self.assertEqual(len(generate_contents(length)), length)
    
    def test_make_response_bytes(self):
        """
        test jbushandler ma
        """
        unit = int(0x11).to_bytes(1, 'big')
        length = int(0x0a).to_bytes(1, 'big')
        function_code = int(0x04).to_bytes(1, 'big')
        
        length_number = 0x0a * 2 + 3 + 2
        res_bytes = make_response_bytes(unit, function_code, length)
        print(res_bytes)
        self.assertIsInstance(res_bytes, bytes)
        self.assertEqual(len(res_bytes), length_number)
        
    

if __name__ == '__main__':
    suite = unittest.TestSuite()

    tests = [Test_utils("test_calculate_crc"), TestPDU("test_bytes"), TestRequest("test_bytes"), TestReponse("test_init"),
    TestReponse("test_check_crc"), TestReponse("test_registers"), TestReponse("test_unit_id"), TestReponse("test_function_code"),
    TestSimulator("test_generate_contents"), TestSimulator("test_make_response_bytes")]
    suite.addTests(tests)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
    