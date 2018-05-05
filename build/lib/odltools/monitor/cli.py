def haha(args):
    print("tim, tim, bo-bim, banana-fana, foo-fim, tiiiimmm")


def add_parser(parsers):
    parser = parsers.add_parser("tim", description="timothy")
    parser.add_argument("tim",
                        help="say something funny!")
    parser.set_defaults(func=haha)
