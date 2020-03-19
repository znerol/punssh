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


def punssh_auth(host, config, tmpldir, **opts):
    """
    Extracts tunnel entries matching `host` from config and applies the
    specified auth template.
    """
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(tmpldir),
    )

    for tunnel in config.get("tunnels", []):
        if tunnel["host"] == host:
            tplname = "{:s}.auth.j2".format(tunnel["template"])
            template = env.get_template(tplname)
            variables = dict(opts)
            variables.update(tunnel)
            yield template.render(**variables)


def main():
    parser = argparse.ArgumentParser(
            description="prints authorized_keys for given tunnels to stdout")
    parser.add_argument(
            "-f", help="config file",
            metavar="CONFIG", default="punssh/config.yml")
    parser.add_argument(
            "-t", help="Template directory. Path relative to config file",
            metavar="TEMPLATES", default="templates")
    parser.add_argument(
            "-c", help="punssh-config command",
            metavar="CMD", default="punssh-config")
    parser.add_argument(
            "host", help="host of destination host")
    args = parser.parse_args()

    if args.t.startswith("/"):
        tmpldir = args.t
    else:
        tmpldir = os.path.join(os.path.dirname(args.f), args.t)

    confcmd = "{:s} -f {:s} -t {:s}".format(args.c, args.f, args.t)
    config = punssh_load(args.f)
    for line in punssh_auth(args.host, config, tmpldir, command=confcmd):
        print(line)


if __name__ == "__main__":
    main()
