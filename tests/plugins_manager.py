# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest

from flask.blueprints import Blueprint
from flask_admin.menu import MenuLink, MenuView

from airflow.hooks.base_hook import BaseHook
from airflow.models import BaseOperator
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.executors.base_executor import BaseExecutor
from airflow.www.app import cached_app


class PluginsTest(unittest.TestCase):

    def test_operators(self):
        from airflow.operators.test_plugin import PluginOperator
        self.assertTrue(issubclass(PluginOperator, BaseOperator))

    def test_sensors(self):
        from airflow.sensors.test_plugin import PluginSensorOperator
        self.assertTrue(issubclass(PluginSensorOperator, BaseSensorOperator))

    def test_hooks(self):
        from airflow.hooks.test_plugin import PluginHook
        self.assertTrue(issubclass(PluginHook, BaseHook))

    def test_executors(self):
        from airflow.executors.test_plugin import PluginExecutor
        self.assertTrue(issubclass(PluginExecutor, BaseExecutor))

        from airflow.executors import GetDefaultExecutor
        self.assertTrue(issubclass(type(GetDefaultExecutor()), BaseExecutor))

        # test plugin executor import based on a name string, (like defined in airflow.cfg)
        # this is not identical to the first assertion!
        from airflow.executors import _get_executor
        self.assertTrue(issubclass(type(_get_executor('test_plugin.PluginExecutor')), BaseExecutor))

    def test_macros(self):
        from airflow.macros.test_plugin import plugin_macro
        self.assertTrue(callable(plugin_macro))

    def test_admin_views(self):
        app = cached_app()
        [admin] = app.extensions['admin']
        category = admin._menu_categories['Test Plugin']
        [admin_view] = [v for v in category.get_children()
                        if isinstance(v, MenuView)]
        self.assertEqual('Test View', admin_view.name)

    def test_flask_blueprints(self):
        app = cached_app()
        self.assertIsInstance(app.blueprints['test_plugin'], Blueprint)

    def test_menu_links(self):
        app = cached_app()
        [admin] = app.extensions['admin']
        category = admin._menu_categories['Test Plugin']
        [menu_link] = [ml for ml in category.get_children()
                       if isinstance(ml, MenuLink)]
        self.assertEqual('Test Menu Link', menu_link.name)
