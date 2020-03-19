#!/usr/bin/env python3

import argparse
import jinja2
import os
import yaml


def punssh_load(path):
    """
    Loads configuration from yaml file and returns it.
    """
    with open(path) as stream:
        return yaml.safe_load(stream)


def punssh_config(name, config, tmpldir):
    """
    Extracts a tunnel from config and applies the specified config template.
    """
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(tmpldir),
    )

    for tunnel in config.get("tunnels", []):
        if tunnel["name"] == name:
            tplname = "{:s}.config.j2".format(tunnel["template"])
            template = env.get_template(tplname)
            return template.render(**tunnel)

    raise IndexError("Tunnel not found")


def main():
    parser = argparse.ArgumentParser(
            description='prints configuration for the given tunnel to stdout')
    parser.add_argument(
            '-f', help='config file', default="punssh/config.yml")
    parser.add_argument(
            "-t", help="Template directory. Path relative to config file",
            metavar="TEMPLATES", default="templates")
    parser.add_argument(
            'name', help='name of configuration')
    args = parser.parse_args()

    if args.t.startswith("/"):
        tmpldir = args.t
    else:
        tmpldir = os.path.join(os.path.dirname(args.f), args.t)

    config = punssh_load(args.f)
    print(punssh_config(args.name, config, tmpldir))


if __name__ == "__main__":
    main()
