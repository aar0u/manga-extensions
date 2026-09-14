import sys
from pathlib import Path

import yaml


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: prepare-extension-tasks.py <extensions.yml>")

    config_path = Path(sys.argv[1])
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    extensions = config.get("extensions") if isinstance(config, dict) else None
    if not isinstance(extensions, list):
        raise SystemExit("extensions.yml must contain an extensions list")

    tasks = []
    for extension in extensions:
        if not isinstance(extension, dict) or not isinstance(extension.get("module"), str):
            raise SystemExit("each extension must define a string module")

        pre_build = extension.get("preBuild")
        if pre_build is not None:
            if not isinstance(pre_build, str):
                raise SystemExit("preBuild must be a Python script string")
            exec(compile(pre_build, f"{config_path}:preBuild", "exec"), {"__name__": "__main__"})

        module = extension["module"]
        tasks.extend((f"{module}:generateSourceInfo", f"{module}:packageRelease"))

    print("\n".join(tasks))


if __name__ == "__main__":
    main()
