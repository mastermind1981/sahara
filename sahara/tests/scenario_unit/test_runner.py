# Copyright (c) 2015 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

import mock
import testtools

from sahara.tests.scenario import runner


class RunnerUnitTest(testtools.TestCase):

    def _isDictContainSubset(self, sub_dictionary, dictionary):
        for key in sub_dictionary:
            if sub_dictionary[key] != dictionary[key]:
                return False
        return True

    def test_set_defaults(self):
        config_without_cred_net = {
            "clusters": [
                {
                    "plugin_name": "vanilla",
                    "plugin_version": "2.7.1",
                    "image": "sahara-vanilla-2.7.1-ubuntu-14.04"
                }],
            }

        expected_default_credential = {
            "credentials": {
                "os_username": "admin",
                "os_auth_url": "http://localhost:5000/v2.0",
                "sahara_url": None,
                "sahara_service_type": "data-processing",
                "os_password": "nova",
                "os_tenant": "admin",
                "ssl_cert": None,
                "ssl_verify": True
            }
        }

        expected_default_network = {
            "network": {
                "type": "neutron",
                "private_network": "private",
                "public_network": "public",
                "auto_assignment_floating_ip": False
                },
        }

        expected_default_cluster = {
            "clusters": [
                {
                    "image": "sahara-vanilla-2.7.1-ubuntu-14.04",
                    "edp_jobs_flow": [],
                    "class_name": "vanilla2_7_1",
                    "plugin_name": "vanilla",
                    "scenario": ['run_jobs', 'scale', 'run_jobs'],
                    "plugin_version": "2.7.1",
                    "retain_resources": False,
                }],
        }

        runner.set_defaults(config_without_cred_net)

        self.assertTrue(self._isDictContainSubset(
            expected_default_credential, config_without_cred_net))
        self.assertTrue(self._isDictContainSubset(
            expected_default_network, config_without_cred_net))
        self.assertTrue(self._isDictContainSubset(
            expected_default_cluster, config_without_cred_net))

        config = {
            "credentials": {
                "os_username": "changed_admin",
                "os_auth_url": "http://127.0.0.1:5000/v2.0",
                "sahara_url": "http://127.0.0.1",
                "os_password": "changed_nova",
                "os_tenant": "changed_admin",
                "ssl_cert": "/etc/tests/cert.crt"
            },
            "network": {
                "type": "neutron",
                "private_network": "changed_private",
                "public_network": "changed_public",
                "auto_assignment_floating_ip": True,
                },
            "clusters": [
                {
                    "plugin_name": "vanilla",
                    "plugin_version": "2.7.1",
                    "image": "sahara-vanilla-2.7.1-ubuntu-14.04",
                    "edp_jobs_flow": "test_flow",
                    "retain_resources": True
                }],
            "edp_jobs_flow": {
                "test_flow": [
                    {
                        "type": "Pig",
                        "input_datasource": {
                            "type": "swift",
                            "source": "etc/edp-examples/edp-pig/top-todoers/"
                                      "data/input"
                        },
                        "output_datasource": {
                            "type": "hdfs",
                            "destination": "/user/hadoop/edp-output"
                        },
                        "main_lib": {
                            "type": "swift",
                            "source": "etc/edp-examples/edp-pig/top-todoers/"
                                      "example.pig"
                        }
                    },
                    {
                        "type": "Java",
                        "additional_libs": [
                            {
                                "type": "database",
                                "source": "sahara/tests/integration/tests/"
                                          "resources/"
                            }],
                        "configs": "edp.java.main_class: org.apache.hadoop."
                                   "examples.QuasiMonteCarlo",
                        "args": [10, 10]
                    },
                    ],
                "test_flow2": [
                    {
                        "type": "Java",
                        "additional_libs": [
                            {
                                "type": "database",
                                "source": "sahara/tests/integration/tests/"
                                          "resources/"
                            }],
                        "configs": "edp.java.main_class: org.apache.hadoop."
                                   "examples.QuasiMonteCarlo",
                        "args": [20, 20]
                    },
                ],
                },
            }

        expected_credential = {
            "credentials": {
                "os_username": "changed_admin",
                "os_auth_url": "http://127.0.0.1:5000/v2.0",
                "sahara_url": "http://127.0.0.1",
                "os_password": "changed_nova",
                "os_tenant": "changed_admin",
                "sahara_service_type": "data-processing",
                "ssl_cert": "/etc/tests/cert.crt",
                "ssl_verify": True
            },
        }

        expected_network = {
            "network": {
                "type": "neutron",
                "private_network": "changed_private",
                "public_network": "changed_public",
                "auto_assignment_floating_ip": True,
                },
        }

        expected_cluster = {
            "clusters": [
                {
                    "plugin_name": "vanilla",
                    "plugin_version": "2.7.1",
                    "image": "sahara-vanilla-2.7.1-ubuntu-14.04",
                    "retain_resources": True,
                    'edp_jobs_flow': [
                        {
                            'main_lib': {
                                'source': 'etc/edp-examples/edp-pig/'
                                          'top-todoers/example.pig',
                                'type': 'swift'
                            },
                            'type': 'Pig',
                            'input_datasource': {
                                'source': 'etc/edp-examples/edp-pig/'
                                          'top-todoers/data/input',
                                'type': 'swift'
                            },
                            'output_datasource': {
                                'type': 'hdfs',
                                'destination': '/user/hadoop/edp-output'
                            }
                        },
                        {
                            'args': [10, 10],
                            'configs': 'edp.java.main_class: org.apache.'
                                       'hadoop.examples.QuasiMonteCarlo',
                            'type': 'Java',
                            'additional_libs': [
                                {
                                    'source': 'sahara/tests/integration/'
                                              'tests/resources/',
                                    'type': 'database'
                                }]
                        }
                    ],
                    "scenario": ['run_jobs', 'scale', 'run_jobs'],
                    "class_name": "vanilla2_7_1"
                }],
        }

        runner.set_defaults(config)

        self.assertTrue(self._isDictContainSubset(
            expected_credential, config))
        self.assertTrue(self._isDictContainSubset(
            expected_network, config))
        self.assertTrue(self._isDictContainSubset(
            expected_cluster, config))

    @mock.patch('sys.exit', return_value=None)
    @mock.patch('subprocess.call', return_value=None)
    def test_runner_main(self, mock_sub, mock_sys):
        sys.argv = ['sahara/tests/scenario/runner.py',
                    'sahara/tests/scenario_unit/vanilla2_7_1.yaml']
        runner.main()

    @mock.patch('sys.exit', return_value=None)
    @mock.patch('subprocess.call', return_value=None)
    def test_runner_template_missing_varfile(self, mock_sub, mock_sys):
        sys.argv = ['sahara/tests/scenario/runner.py',
                    'sahara/tests/scenario_unit/vanilla2_7_1.yaml.mako']
        self.assertRaises(NameError, runner.main)

    @mock.patch('sys.exit', return_value=None)
    @mock.patch('subprocess.call', return_value=None)
    def test_runner_template_wrong_varfile(self, mock_sub, mock_sys):
        sys.argv = ['sahara/tests/scenario/runner.py',
                    '-V',
                    'sahara/tests/scenario_unit/templatevars_nodefault.ini',
                    'sahara/tests/scenario_unit/vanilla2_7_1.yaml.mako']
        self.assertRaises(NameError, runner.main)

    @mock.patch('sys.exit', return_value=None)
    @mock.patch('subprocess.call', return_value=None)
    def test_runner_template_incomplete_varfile(self, mock_sub, mock_sys):
        sys.argv = ['sahara/tests/scenario/runner.py',
                    '-V',
                    'sahara/tests/scenario_unit/templatevars_incomplete.ini',
                    'sahara/tests/scenario_unit/vanilla2_7_1.yaml.mako']
        self.assertRaises(NameError, runner.main)

    @mock.patch('sys.exit', return_value=None)
    @mock.patch('subprocess.call', return_value=None)
    def test_runner_template_working(self, mock_sub, mock_sys):
        sys.argv = ['sahara/tests/scenario/runner.py',
                    '-V',
                    'sahara/tests/scenario_unit/templatevars_complete.ini',
                    'sahara/tests/scenario_unit/vanilla2_7_1.yaml.mako']
        runner.main()

    @mock.patch('sys.exit', return_value=None)
    def test_runner_validate(self, mock_sys):
        sys.argv = ['sahara/tests/scenario/runner.py',
                    '--validate',
                    '-V',
                    'sahara/tests/scenario_unit/templatevars_complete.ini',
                    'sahara/tests/scenario_unit/vanilla2_7_1.yaml.mako']
        runner.main()
