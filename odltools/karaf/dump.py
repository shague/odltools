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

import sys

line_num = 0
OPENER = '[{<'
CLOSER = ']}>'

def dump_karaf_log(args):
    path = args.path
    if path == '-':
        log_file = sys.stdin
    else:
        log_file = open(path, 'r')

    if args.pretty_print:
        _dump_pretty_print(log_file)
    else:
        _dump(log_file)
    log_file.close()

def _has_nested_structs(msg):
    top = -1
    for c in msg:
        if top == -1:
            top = OPENER.find(c)
        else:
            if c in OPENER:
                return True
            closer = CLOSER.find(c)
            if closer == top:
                top = -1
    return False

def _nl(indent):
    global line_num
    line_num += 1
    sys.stdout.write('\n' + indent)

def _dump(input):
    for line in input:
        print line,

def _dump_pretty_print(input):
    for l in input:
        msg = l.rstrip()

        I = '  '
        indent = ''

        in_ws = 0
        is_empty_list = 0
        last_char = 'X'
        title = ''
        title_stack = []
        in_string_constant = 0

        i = 0
        num_fields = 0
        for c in msg:
            if c == '|':
                num_fields += 1
            i += 1
            sys.stdout.write(c)
            if num_fields > 4:
                break

        msg = msg[i:]

        if not _has_nested_structs(msg):
            print msg
            continue

        for c in msg:
            if in_ws and c in ' \t': continue
            in_ws = 0

            if c in CLOSER:
                indent = indent[:-2]
                if not is_empty_list and last_char not in CLOSER: _nl(indent)
                in_ws = 1
                is_empty_list = 0
                title = ''
            elif is_empty_list:
                is_empty_list = 0
                _nl(indent)

            if last_char in CLOSER and c != ',': _nl(indent)

            sys.stdout.write(c)
            last_char = c


            if in_string_constant:
                pass

            if c == '"':
                if in_string_constant: in_string_constant = 0
                else: in_string_constant = 1

            elif c in CLOSER:
                if len(title_stack):
                    (t,ln) = title_stack.pop()
                    if (line_num - ln) > 5: sys.stdout.write(' /* ' + t.strip() + ' */')

            elif c in OPENER:
                indent += I
                in_ws = 1
                is_empty_list = 1
                if title:
                    title_stack.append((title, line_num))
                    title = ''

            elif c == ',' and not in_string_constant:
                _nl(indent)
                in_ws = 1
                title = ''
        print ''
