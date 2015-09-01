# -*- coding: utf-8 -*-
#
# Copyright (c) 2012-2015, CRS4
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from unittest import TestCase

from clay.exceptions import InvalidMessage, SchemaException, InvalidContent
from clay.factory import MessageFactory
from clay.serializer import AvroSerializer
from clay.message import _Record

from tests import TEST_CATALOG, TEST_SCHEMA, TEST_COMPLEX_SCHEMA


class TestMessage(TestCase):
    def setUp(self):
        self.factory = MessageFactory(AvroSerializer, TEST_CATALOG)

    def test_message_instantiation(self):
        test_message = self.factory.create("TEST")
        self.assertEqual(test_message.message_type, "TEST")
        self.assertEqual(test_message.schema, TEST_SCHEMA)
        self.assertEqual(test_message.fields, ("id", "name"))
        self.assertEqual(test_message.content, {"id": None, "name": None})

        test_message = self.factory.create("TEST_COMPLEX")
        self.assertEqual(test_message.message_type, "TEST_COMPLEX")
        self.assertEqual(test_message.schema, TEST_COMPLEX_SCHEMA)
        self.assertEqual(test_message.fields, ("valid", "id", "long_id", "float_id", "double_id",
                                               "name", "array_complex_field", "matrix_field", "array_simple_field",
                                               "record_field"))
        self.assertEqual(test_message.content, {"valid": "true", "id": None, "long_id": None, "float_id": None,
                                                "double_id": None, "name": None, "array_complex_field": None,
                                                "array_simple_field": None, "record_field": None, "matrix_field": None})
        self.assertEqual(test_message.record_field.fields, ("field_1", "field_2"))
        self.assertEqual(test_message.record_field.content, None)

    def test_invalid_message_instantiation(self):
        self.assertRaises(InvalidMessage, self.factory.create, "UNK")

    def test_simple_message_value_assignment(self, m=None):
        if m is None:
            m = self.factory.create("TEST")
        self.assertEqual(m.id, None)
        self.assertEqual(m.name, None)
        m.id = 1111111
        m.name = "aaa"

        self.assertEqual(m.id, 1111111)
        self.assertEqual(m.name, "aaa")

        # with self.assertRaises(AttributeError):
        #     m.unkn = 1

    def test_wrong_schema(self):
        with self.assertRaises(SchemaException):
            self.factory.create("TEST_WRONG")

    def test_complex_message_base_type_assignment(self):
        m = self.factory.create("TEST_COMPLEX")
        self.test_simple_message_value_assignment(m)

    def test_complex_message_value_error(self):
        m = self.factory.create("TEST_COMPLEX")

        with self.assertRaises(ValueError):
            m.array_complex_field = [{"field_1": "aaa"}]

        with self.assertRaises(ValueError):
            m.record_field = {"field_1": "aaa"}

    def test_complex_message_record_array_assignment(self):
        m = self.factory.create("TEST_COMPLEX")

        # Tests on
        m.array_complex_field.add()
        self.assertEqual(len(m.array_complex_field), 1)
        self.assertIsInstance(m.array_complex_field[0], _Record)
        m.array_complex_field[0].field_1 = "bbb"
        self.assertEqual(m.array_complex_field[0].field_1, "bbb")

        m.array_complex_field.add()
        self.assertEqual(len(m.array_complex_field), 2)
        self.assertIsInstance(m.array_complex_field[1], _Record)
        m.array_complex_field[1].field_1 = "ccc"
        self.assertEqual(m.array_complex_field[1].field_1, "ccc")

        del m.array_complex_field[1]
        self.assertEqual(len(m.array_complex_field), 1)

    def test_complex_message_simple_array_assignment(self):
        m = self.factory.create("TEST_COMPLEX")

        m.array_simple_field.add()
        self.assertEqual(len(m.array_simple_field), 1)
        self.assertEqual(m.array_simple_field[0], None)
        m.array_simple_field[0] = "ccc"
        self.assertEqual(m.array_simple_field[0], "ccc")

        m.array_simple_field.add()
        self.assertEqual(len(m.array_simple_field), 2)
        self.assertEqual(m.array_simple_field[1], None)
        m.array_simple_field[1] = "ddd"
        self.assertEqual(m.array_simple_field[1], "ddd")

        del m.array_simple_field[1]
        self.assertEqual(len(m.array_simple_field), 1)

    def test_complex_message_matrix_assignment(self):
        m = self.factory.create("TEST_COMPLEX")

        m.matrix_field.add()
        self.assertEqual(len(m.matrix_field), 1)
        self.assertEqual(m.matrix_field[0], None)

        m.matrix_field[0].add()
        self.assertEqual(len(m.matrix_field[0]), 1)
        self.assertEqual(m.matrix_field[0], [None])
        self.assertEqual(m.matrix_field[0][0], None)

        m.matrix_field[0].add("test")
        self.assertEqual(len(m.matrix_field[0]), 2)
        self.assertEqual(m.matrix_field[0], [None, "test"])
        self.assertEqual(m.matrix_field[0][1], "test")

        m.matrix_field[0][0] = "test1"
        self.assertEqual(m.matrix_field[0], ["test1", "test"])
        self.assertEqual(m.matrix_field[0][0], "test1")

        m.matrix_field.add(["test_3", "test_4"])
        self.assertEqual(len(m.matrix_field), 2)
        self.assertEqual(m.matrix_field[1], ["test_3", "test_4"])

    def test_complex_message_record_assignment(self):
        m = self.factory.create("TEST_COMPLEX")

        m.record_field.field_1 = 'aaa'
        self.assertEqual(m.record_field.field_1, 'aaa')

    def test_set_content_message(self):
        content = {
            "valid": True,
            "id": 1111111,
            "long_id": 1*10e60,
            "float_id": 1.32,
            "double_id": 1*10e-60,
            "name": "aaa",
            "array_complex_field": [{
                "field_1": "bbb"
            }],
            "array_simple_field": ["ccc"],
            "matrix_field": [["test1", "test2"], ["test3"]],
            "record_field": {
                "field_1": "ddd",
                "field_2": "eee"
            }
        }

        # test for the entire message
        m = self.factory.create("TEST_COMPLEX")
        m.set_content(content)
        self.assertEqual(m.content, content)

        self.assertEqual(m.id, 1111111)
        self.assertEqual(m.name, "aaa")
        self.assertEqual(len(m.array_complex_field), 1)
        self.assertEqual(m.array_complex_field[0].field_1, "bbb")
        self.assertEqual(len(m.array_simple_field), 1)
        self.assertEqual(m.array_simple_field[0], "ccc")
        self.assertEqual(len(m.matrix_field), 2)
        self.assertEqual(m.matrix_field[0], ["test1", "test2"])
        self.assertEqual(m.record_field.field_1, "ddd")

    def test_set_content_message_wrong(self):
        content = {
            "wrong_id": 1111111,
            "wrong_name": "aaa",
            "wrong_array_complex_field": [{
                "wrong_field_1": "bbb"
            }],
            "wrong_array_simple_field": ["ccc"],
            "wrong_record_field": {
                "wrong_field_1": "ddd"
            },
            "wrong_matrix_field": ["eee"]
        }

        m = self.factory.create("TEST_COMPLEX")
        self.assertRaises(AttributeError, m.set_content, content)

    def test_set_content_complex_field_array(self):
        content = [{
            "field_1": "bbb"
        }]

        m = self.factory.create("TEST_COMPLEX")
        self.assertRaises(InvalidContent, m.array_complex_field.set_content, 1)  # 1 is not iterable

        m.array_complex_field.set_content(None)
        self.assertEqual(m.array_complex_field.content, None)
        # Type error because the array is None
        self.assertRaises(TypeError, m.array_complex_field.__getitem__, 0)
        self.assertRaises(TypeError, m.array_complex_field.__delitem__, 0)
        self.assertRaises(TypeError, m.array_complex_field.__setitem__, 0, "value")
        self.assertRaises(TypeError, len, m.array_complex_field)

        m.array_complex_field.set_content([])
        self.assertEqual(m.array_complex_field.content, [])
        m.array_complex_field.set_content(content)
        self.assertEqual(m.array_complex_field.content, [{"field_1": "bbb"}])

    def test_set_content_simple_field_array(self):
        m = self.factory.create("TEST_COMPLEX")
        self.assertRaises(InvalidContent, m.array_simple_field.set_content, "aaa")  # "aaa" is not a list or a tuple

        m.array_simple_field.set_content(None)
        # Type error because the array is None
        self.assertRaises(TypeError, m.array_simple_field.__getitem__, 0)
        self.assertRaises(TypeError, m.array_simple_field.__delitem__, 0)
        self.assertRaises(TypeError, m.array_simple_field.__setitem__, 0, "value")
        self.assertRaises(TypeError, len, m.array_simple_field)

        m.array_simple_field.set_content([])
        self.assertEqual(m.array_simple_field.content, [])
        m.array_simple_field.set_content(["aaa", "bbb"])
        self.assertEqual(m.array_simple_field.content, ["aaa", "bbb"])

    def test_set_content_matrix(self):
        m = self.factory.create("TEST_COMPLEX")
        self.assertRaises(InvalidContent, m.matrix_field.set_content, "aaa")  # "aaa" is not a list or a tuple
        self.assertRaises(InvalidContent, m.matrix_field.set_content, ["aaa", "bbb"])  # "aaa" is not a list of list

        m.matrix_field.set_content(None)
        # Type error because the array is None
        self.assertRaises(TypeError, m.matrix_field.__getitem__, 0)
        self.assertRaises(TypeError, m.matrix_field.__delitem__, 0)
        self.assertRaises(TypeError, m.matrix_field.__setitem__, 0, "value")
        self.assertRaises(TypeError, len, m.array_simple_field)

        m.matrix_field.set_content([])
        self.assertEqual(m.matrix_field.content, [])
        m.matrix_field.set_content([["aaa", "bbb"], ["ccc"]])
        self.assertEqual(m.matrix_field.content, [["aaa", "bbb"], ["ccc"]])

    def test_set_content_array_wrong(self):
        content = [{
            "wrong_field_1": "bbb"
        }]

        m = self.factory.create("TEST_COMPLEX")
        self.assertRaises(AttributeError, m.array_complex_field.set_content, content)

    def test_set_content_record(self):
        content = {
            "field_1": "ddd",
            "field_2": "eee"
        }

        m = self.factory.create("TEST_COMPLEX")

        self.assertIsNone(m.record_field.content)
        self.assertRaises(AttributeError, getattr, m.record_field, "field_1")
        self.assertRaises(AttributeError, getattr, m.record_field, "field_2")
        m.record_field.field_1 = 'ddd'
        self.assertEqual(m.record_field.field_1, "ddd")
        self.assertIsNone(m.record_field.field_2)

        m.record_field.set_content(None)
        self.assertIsNone(m.record_field.content)
        self.assertRaises(AttributeError, getattr, m.record_field, "field_1")
        self.assertRaises(AttributeError, getattr, m.record_field, "field_2")

        m.record_field.set_content(content)
        self.assertEqual(m.record_field.field_1, "ddd")
        self.assertEqual(m.record_field.field_2, "eee")

    def test_set_content_record_wrong(self):
        content = {
            "wrong_field_1": "ddd"
        }

        m = self.factory.create("TEST_COMPLEX")

        self.assertRaises(AttributeError, m.record_field.set_content, content)

    def test_message_equality(self):
        m1 = self.factory.create("TEST_COMPLEX")
        m2 = self.factory.create("TEST_COMPLEX")
        self.assertEqual(m1, m2)
        content = {
            "id": 1111111,
            "name": "aaa",
            "array_complex_field": [
                {"field_1": "bbb"},
                {"field_1": "ccc"}
            ],
            "array_simple_field": ["ccc", "ddd"],
            "record_field": {
                "field_1": "ddd"
            }
        }
        m1.set_content(content)
        m2.set_content(content)
        self.assertEqual(m1, m2)

        m2._domain = "OTHER DOMAIN"
        self.assertNotEqual(m1, m2)
        m2._domain = m1._domain  # reset domain

        m1._message_type = "OTHER MESSAGE TYPE"
        self.assertNotEqual(m1, m2)
        m2._message_type = m1._message_type  # reset message_type

    def test_fields_equality(self):
        m1 = self.factory.create("TEST_COMPLEX")
        m2 = self.factory.create("TEST_COMPLEX")

        self.assertEqual(m1.array_complex_field, None)
        self.assertEqual(m1.array_simple_field, None)
        self.assertEqual(m1.record_field, None)

        content = {
            "id": 1111111,
            "name": "aaa",
            "array_complex_field": [
                {"field_1": "bbb"},
                {"field_1": "ccc"}
            ],
            "array_simple_field": ["ccc", "ddd"],
            "record_field": {
                "field_1": "ddd"
            }
        }

        m1.set_content(content)
        m2.set_content(content)
        self.assertEqual(m1.array_complex_field, m2.array_complex_field)
        self.assertEqual(m1.array_simple_field, m2.array_simple_field)
        self.assertEqual(m1.record_field, m2.record_field)

        m1.array_complex_field[0].field_1 = "aaa"
        m1.array_simple_field[0] = "aaa"
        m1.record_field.field_1 = "aaa"
        self.assertNotEqual(m1.array_complex_field, m2.array_complex_field)
        self.assertNotEqual(m1.array_simple_field, m2.array_simple_field)
        self.assertNotEqual(m1.record_field, m2.record_field)
