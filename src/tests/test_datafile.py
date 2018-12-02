import json
import os
from unittest import TestCase

from utils.data_parser import parse_title, create_page
from app import App


class DataFileTest(TestCase):
    def setUp(self):
        self.app = App()

    def tearDown(self):
        self.app.exit(0)

    def test_str_and_widget(self):
        data_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 '../data/categories.json'))
        with open(data_path, 'r') as f:
            data_content = json.load(f)
            for node in data_content:
                self._test_node(node)
                children = node.get('children', None)
                if children:
                    for child in children:
                        self._test_node(child)

    def _test_node(self, node):
        title = parse_title(node.get('title', None))
        self.assertIsNotNone(title)
        print('title ok:', title)
        widget_cls = node.get('widget', None)
        if widget_cls:
            widget = create_page(widget_cls)
            self.assertIsNotNone(widget)
            print('widget ok:', widget_cls)

