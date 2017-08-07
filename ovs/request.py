def debug_print(text1, data, debug=0):
    if debug:
        print "request: {}".format(text1)
        print "{}".format(data)


def get_from_file(filename, debug=0):
    lines = []
    with open(filename, 'r') as fp:
        for line in fp:
            lines.append(line.lstrip())
    debug_print(filename, lines, debug)
    return lines


def write_file(filename, lines):
    with open(filename, 'w') as fp:
        fp.writelines(lines)
