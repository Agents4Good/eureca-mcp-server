import argparse

def parse():
    parser = argparse.ArgumentParser(description="Command line parser for transport config")
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="stdio",
        help="The transport method to run the server, default is 'stdio'"
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host for HTTP transport, default is '127.0.0.1'"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for HTTP transport, default is '8000'"
    )
    return parser.parse_args()

def args_config(args):
    if args.transport == "http":
        return { "transport": "http", "host": args.host, "port": args.port }
    return { "transport": "stdio" }