import re
import tables


class Flows:
    cookie = "cookie"
    duration = "duration"
    table = "table"
    n_packets = "n_packets"
    n_bytes = "n_bytes"
    matches = "matches"
    actions = "actions"
    idle_timeout = "idle_timeout"
    send_flow_removed = "send_flow_rem"
    priority = "priority"
    goto = "goto"
    resubmit = "resubmit"

    def __init__(self, data):
        self.data = data
        self.pdata = None

    def process_data(self):
        self.pdata = []
        for line in self.data[1:]:
            pline = {}
            tokens = line.split(" ")
            for token in tokens:
                splits = token.split("=", 1)
                if len(splits) == 1:
                    if token == Flows.send_flow_removed:
                        pline[token] = token
                    else:
                        pline[Flows.matches] = token.rstrip(",")
                elif len(splits) == 2:
                    pline[splits[0]] = splits[1].rstrip(",")
            self.pdata.append(pline)
        return self.pdata

    def format_data(self, mode=0):
        if mode == 0:
            return self.format_data0()
        elif mode == 1:
            return self.format_data1()
        else:
            return None

    def format_data0(self):
        flines = [self.data[0]]
        for line in self.pdata:
            if Flows.send_flow_removed in line:
                send_flow_rem = " {} ".format(line[Flows.send_flow_removed])
            else:
                send_flow_rem = ""
            if Flows.idle_timeout in line:
                idle_timeo = "{}={}, ".format(Flows.idle_timeout, line[Flows.idle_timeout])
            else:
                idle_timeo = ""

            fline = "cookie={}, duration={}, table={}, n_packets={}, n_bytes={}, {}{}priority={} actions={}"\
                .format(line[Flows.cookie], line[Flows.duration], tables.get_table_name(int(line[Flows.table])),
                        line[Flows.n_packets], line[Flows.n_bytes],
                        idle_timeo, send_flow_rem,
                        line[Flows.priority], line[Flows.actions])
            flines.append(fline)
        return flines

    def format_data12(self):
        header = "{:9} {:8} {:13}     {:6} {:12} {}... {}... {} {}"\
            .format(Flows.cookie, Flows.duration, Flows.table, "n_pack", Flows.n_bytes, Flows.matches, Flows.actions,
                    Flows.idle_timeout, Flows.duration)

        regex = re.compile(r"(goto_table:\d{1,3})")
        flines = [header]
        for line in self.pdata:
            if Flows.send_flow_removed in line:
                send_flow_rem = " {} ".format(line[Flows.send_flow_removed])
            else:
                send_flow_rem = ""
            if Flows.idle_timeout in line:
                idle_timeo = " {}={}".format(Flows.idle_timeout, line[Flows.idle_timeout])
            else:
                idle_timeo = ""
            nactions = regex.sub(r"\1(" + regex.groups[0] + ")", line[Flows.actions])

            fline = "{:9} {:8} {:3} {:13} {:6} {:12} priority={} actions={}{}{}" \
                .format(line[Flows.cookie], line[Flows.duration],
                        line[Flows.table], tables.get_table_name(int(line[Flows.table])),
                        line[Flows.n_packets], line[Flows.n_bytes],
                        line[Flows.priority], nactions,
                        idle_timeo, send_flow_rem,)
            flines.append(fline)
        return flines

    def reg_table(self, match):
        if match.group(Flows.goto) is not None:
            table_id = int(match.group(Flows.goto))
        elif match.group(Flows.resubmit) is not None:
            table_id = int(match.group(Flows.resubmit))
        else:
            table_id = 256

        rep = "{}({})".format(match.group(), tables.get_table_name(table_id))
        return rep

    def format_data1(self):
        header = "{:9} {:8} {:13}     {:6} {:12} {}... {}... {} {}" \
            .format(Flows.cookie, Flows.duration, Flows.table, "n_pack", Flows.n_bytes, Flows.matches, Flows.actions,
                    Flows.idle_timeout, Flows.duration)

        regex_gt = re.compile(r"goto_table:(?P<goto>\d{1,3})|"
                              r"resubmit\(,(?P<resubmit>\d{1,3})\)")
        flines = [header]
        for line in self.pdata:
            if Flows.send_flow_removed in line:
                send_flow_rem = " {} ".format(line[Flows.send_flow_removed])
            else:
                send_flow_rem = ""
            if Flows.idle_timeout in line:
                idle_timeo = " {}={}".format(Flows.idle_timeout, line[Flows.idle_timeout])
            else:
                idle_timeo = ""
            nactions = regex_gt.sub(self.reg_table, line[Flows.actions])

            fline = "{:9} {:8} {:3} {:13} {:6} {:12} priority={} actions={}{}{}" \
                .format(line[Flows.cookie], line[Flows.duration],
                        line[Flows.table], tables.get_table_name(int(line[Flows.table])),
                        line[Flows.n_packets], line[Flows.n_bytes],
                        line[Flows.priority], nactions,
                        idle_timeo, send_flow_rem,)
            flines.append(fline)
        return flines
