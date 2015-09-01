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

from clay.exceptions import SchemaException
from clay.factory import MessageFactory
from clay.serializer.avro_serializer import AvroSerializer
from clay.serializer.pyavroc_serializer import AvroSerializer as PyAvrocSerializer

from tests import TEST_CATALOG


class TestAvroSerializer(TestCase):
    def setUp(self):
        self.avro_factory = MessageFactory(AvroSerializer, TEST_CATALOG)
        self.pyavroc_factory = MessageFactory(PyAvrocSerializer, TEST_CATALOG)
        self.factories = (self.avro_factory, self.pyavroc_factory)

        self.simple_msg_content = {"id": 1111111, "name": u"aaa"}
        self.complex_msg_content = {
            "valid": True,
            "id": 1111111,
            "long_id": 10**18,
            "float_id": 1.232,
            "double_id": 1e-60,
            "name": "aaa",
            "record_field": {
                "field_2": u"eee",
                "field_1": u"ddd"
            },
            "array_simple_field": ["ccc"],
            "array_complex_field": [
                {"field_1": "bbb"}
            ],
            "matrix_field": [["aaa", "bbb"], ["ccc", "ddd"]]
        }

        self.avro_simple = self.avro_factory.create("TEST")
        self.pyavroc_simple = self.pyavroc_factory.create("TEST")

        self.avro_simple.set_content(self.simple_msg_content)
        self.pyavroc_simple.set_content(self.simple_msg_content)
        self.simple_encoded = "\x00\x10\x8e\xd1\x87\x01\x06aaa"

        self.avro_complex = self.avro_factory.create("TEST_COMPLEX")
        self.pyavroc_complex = self.pyavroc_factory.create("TEST_COMPLEX")

        self.avro_complex.set_content(self.complex_msg_content)
        self.pyavroc_complex.set_content(self.complex_msg_content)
        self.complex_encoded = '\x02\x98\x01\x01\x8e\xd1\x87\x01\x80\x80\xa0\xf6\xf4\xac\xdb\xe0\x1b-\xb2\x9d?&\xa6' \
                               '\xac\xaa\x04\xb6y3\x06aaa\x00\x02\x06bbb\x00\x04\x04\x06aaa\x06bbb\x00\x04\x06ccc' \
                               '\x06ddd\x00\x00\x00\x02\x06ccc\x00\x00\x06ddd\x00\x06eee'

    def test_retrieve(self):
        for factory in self.factories:
            m = factory.retrieve(self.complex_encoded)

            self.assertEqual(m.valid, True)
            self.assertEqual(m.id, 1111111)
            self.assertEqual(m.long_id, 10**18)
            self.assertEqual(round(m.float_id, 3), 1.232)  # TODO: Avro seems to have wrong behavior with float
            self.assertEqual(m.double_id, 1e-60)
            self.assertEqual(m.name, "aaa")
            self.assertEqual(len(m.array_complex_field), 1)
            self.assertEqual(m.array_complex_field[0].field_1, "bbb")
            self.assertEqual(len(m.array_simple_field), 1)
            self.assertEqual(m.array_simple_field[0], "ccc")
            self.assertEqual(m.record_field.field_1, "ddd")
            self.assertEqual(m.record_field.field_2, "eee")
            self.assertEqual(m.matrix_field, [["aaa", "bbb"], ["ccc", "ddd"]])

    def test_avro_serializer(self):
        for m in (self.avro_simple, self.pyavroc_simple):
            value = m.serialize()
            self.assertEqual(value, self.simple_encoded)

        for m in (self.avro_complex, self.pyavroc_complex):
            value = m.serialize()
            self.assertEqual(value, self.complex_encoded)

    def test_wrong_schema(self):
        for m in (self.avro_complex, self.pyavroc_complex):
            # setting wrong type for the value (it should be int)
            m.id = "111111"
            self.assertRaises(SchemaException, m.serialize)

    def test_utf8_encoding(self):
        target = "\x00\x10\x02\x0ctest\xc3\xa0"
        for factory in self.factories:
            for s in u"testà", "testà":
                m = factory.create("TEST")
                m.id = 1
                m.name = s
                self.assertEqual(m.serialize(), target)
