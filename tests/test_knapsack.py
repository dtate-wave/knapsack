# Copyright 2021 D-Wave Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import sys
import unittest
import subprocess
import numpy as np
from io import StringIO
from contextlib import redirect_stdout
from knapsack import build_knapsack_cqm, parse_inputs, parse_solution
import dimod

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TestBuildCQM(unittest.TestCase):
    """Verify correct construction of CQM for very_small.csv data with weight 10."""
    def test_build_cqm1(self):
        cqm = build_knapsack_cqm([10, 1], [5, 7], 10)
        self.assertEqual(cqm.objective.linear, {0: -10.0, 1: -1.0})
        self.assertEqual(cqm.constraints["capacity"].lhs.linear, {0: 5.0, 1: 7.0})
        self.assertEqual(cqm.constraints["capacity"].rhs, 10)

class TestParsing(unittest.TestCase):
    """Verify input and output handling."""
    def test_parse_input1(self):
        file1 = os.path.join(root_dir, "data", "small.csv")
        costs, weights, capacity = parse_inputs(file1, 10)

        self.assertEqual(capacity, 10)
        self.assertEqual(sum(costs), 405)
        self.assertEqual(sum(weights), 112)

class TestIntegration(unittest.TestCase):
    @unittest.skipIf(os.getenv('SKIP_INT_TESTS'), "Skipping integration test.")
    def test_integration(self):
        """Test integration of demo script."""

        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        demo_file = os.path.join(project_dir, 'knapsack.py')

        output = subprocess.check_output([sys.executable, demo_file])
        output = output.decode('utf-8') # Bytes to str
        output = output.lower()

        self.assertIn('building a cqm', output)
        self.assertIn('submitting cqm to solver', output)
        self.assertIn('found best solution', output)
        self.assertIn('selected item numbers', output)
        self.assertIn('selected item weights', output)
        self.assertIn('selected item costs', output)
        self.assertNotIn('traceback', output)
