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

RABBIT_EXCHANGE = 'test_exchange'

RABBIT_QUEUE = 'TESTS'

TEST_SCHEMA = {
    "namespace": RABBIT_QUEUE,
    "name": "TEST",
    "type": "record",
    "fields": [
        {"name": "id", "type": "int"},
        {"name": "name", "type": "string"},
    ]
}

TEST_COMPLEX_SCHEMA = {
    "namespace": RABBIT_QUEUE,
    "name": "TEST_COMPLEX",
    "type": "record",
    "fields": [
        {"name": "valid", "type": "boolean", "default": "true"},
        {"name": "id", "type": "int"},
        {"name": "long_id", "type": "long"},
        {"name": "float_id", "type": "float"},
        {"name": "double_id", "type": "double"},
        {"name": "name", "type": "string"},
        {"name": "array_complex_field",
         "type": [{
             "type": "array",
             "items": {
                 "type": "record",
                     "name": "items_type",
                     "fields": [
                         {"name": "field_1", "type": "string"},
                     ]
                 }}, "null"]},
        {"name": "matrix_field",
         "type": {
             "type": "array",
             "items": {
                 "type": "array",
                 "items": "string"
             }
         }},
        {"name": "array_simple_field",
         "type": [{
             "type": "array",
             "items": "string"}, "null"]},
        {"name": "record_field", "type": [{
            "type": "record",
            "name": "complex_record",
            "fields": [
                 {"name": "field_1", "type": "string"},
                 {"name": "field_2", "type": ["string", "null"]}
             ]},
         "null"]}
    ]
}

TEST_COMPLEX_SCHEMA_WITH_NULL = {
    "namespace": RABBIT_QUEUE,
    "name": "TEST_COMPLEX_WITH_NULL",
    "type": "record",
    "fields": [
        {"name": "arr", "type": [{
            "type": "array",
            "items": "string"
        }, "null"]},
        {"name": "rec", "type": [{
            "type": "record",
            "name": "REC",
            "fields": [{"name": "field", "type": "string"}]
        }, "null"]}
    ]
}

TEST_WRONG_SCHEMA = {
    "namespace": RABBIT_QUEUE,
    "name": "TEST_WRONG",
    "type": "record",
    "fields": [
        {"name": "id", "type": ["int", "string"]},
        {"name": "name", "type": "string"},
    ]
}

TEST_CATALOG = {
    "version": 1,
    "name": "TEST_CATALOG",
    0: TEST_SCHEMA,
    1: TEST_COMPLEX_SCHEMA,
    2: TEST_WRONG_SCHEMA,
    3: TEST_COMPLEX_SCHEMA_WITH_NULL
}