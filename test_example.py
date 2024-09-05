
class TestExample(unittest.TestCase):
    def test_function_with_one(self):
        result = function_to_test(1)
        assert result == expected_value_for_one

if __name__ == '__main__':
    unittest.main()
