import unittest
import json
from data_collector import process_data

class TestStringMethods(unittest.IsolatedAsyncioTestCase):

    async def test_ingest_4th_shell_page(self):
        with open('4shell_page.json', 'r') as file:
            page_data =  json.loads(file.read())

        await process_data(page_data)


if __name__ == '__main__':
    unittest.main()
