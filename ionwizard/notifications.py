import subprocess


def find_outdated(package_names: list[str]):
    cmd = (
            ["pip", "list", "--outdated"]
    )
    subprocess.run(cmd)