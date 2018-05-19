def add_common_args(parser):
    parser.add_argument("--path",
                        help="the directory that the parsed data is written into")
    parser.add_argument("--transport", default="http",
                        choices=["http", "https"],
                        help="transport for connections")
    parser.add_argument("-i", "--ip", default="localhost",
                        help="OpenDaylight ip address")
    parser.add_argument("-t", "--port", default="8181",
                        help="OpenDaylight restconf port, default: 8181")
    parser.add_argument("-u", "--user", default="admin",
                        help="OpenDaylight restconf username, default: admin")
    parser.add_argument("-w", "--pw", default="admin",
                        help="OpenDaylight restconf password, default: admin")
    parser.add_argument("-p", "--pretty_print", action="store_true",
                        help="json dump with pretty_print")
