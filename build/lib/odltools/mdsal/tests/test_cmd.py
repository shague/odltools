# Copyright 2018 Red Hat, Inc. and others. All Rights Reserved.
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

import logging
import os
import shutil
import unittest
from odltools import logg
from odltools.mdsal import cmd
from odltools.mdsal.tests import Args


@unittest.skip("skipping")
class TestCmd(unittest.TestCase):
    def setUp(self):
        logg.Logger(logging.INFO, logging.INFO)
        self.args = Args(path="/tmp/testmodels", pretty_print=True)

    def test_get_all_dumps(self):
        # Ensure odl is running at localhost:8181
        # Remove an existing directory
        if os.path.exists(self.args.path):
            if os.path.islink(self.args.path):
                os.unlink(self.args.path)
            else:
                shutil.rmtree(self.args.path)

        cmd.get_all_dumps(self.args)

        # assert each model has been saved to a file
        for res in cmd.DSMAP.values():
            store = res[cmd.DSM_DSTYPE]
            model_path = res[cmd.DSM_PATH]
            path_split = cmd.split_model_path(model_path)
            filename = cmd.make_filename(self.args.path, store, path_split.name, path_split.container)
            self.assertTrue(os.path.isfile(filename))


if __name__ == '__main__':
    unittest.main()
