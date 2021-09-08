def parse_base(parser):
    parser.add_argument('worksheet', help="Parameterization worksheet path")
    parser.add_argument("--login",
                        "-l",
                        required=True,
                        metavar="EMAIL",
                        help="Login email")
    parser.add_argument("--empresa", "-e", required=True, help="Company Name")
    parser.add_argument(
        "--empresaid",
        "-eid",
        type=int,
        default=0,
        help="Company id (if have some companies with same name)")
    parser.add_argument("--filial", "-f", help="Branch name (if any)")
    parser.add_argument("--password",
                        "-p",
                        default="123456",
                        help="Access password (default = 123456)")
    parser.add_argument("-W",
                        "--no-warning",
                        action="store_true",
                        help="Suppress warnings")
    return parser
