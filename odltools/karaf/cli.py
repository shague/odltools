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

from odltools.karaf import dump


def add_dump_parser(parsers):
    parser = parsers.add_parser("dump", help="Dump a karaf log")
    parser.add_argument("--path", required=True,
                        help="Path to the karaf file")
    parser.add_argument("-p", "--pretty_print", action="store_true",
                        help="pretty print mdsal objects")
    parser.set_defaults(func=dump.dump_karaf_log)


def add_parser(parsers):
    parser = parsers.add_parser("karaf", description="Karaf log tools")
    subparsers = parser.add_subparsers(dest="subcommand", description="Karaf tools")
    add_dump_parser(subparsers)
