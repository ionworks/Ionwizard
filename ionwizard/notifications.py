import subprocess

from ionwizard.library_wizard import IonWorksPipWizard


def find_outdated(library_config):
    outdated_found = False
    lib_info = {lib["library"]: lib["key"] for lib in library_config}
    lib_info.update({"ionwizard": None})
    package_names = list(lib_info.keys())
    licenses = list(lib_info.values())
    cleaned_output = ["\nThe following ionworks packages can be updated:\n"]
    for key in licenses:
        cmd = ["pip", "list", "--outdated"]
        if key:
            cmd += ["--index-url", f"{IonWorksPipWizard.get_address(key)}"]
        result = subprocess.run(
            cmd,
            capture_output=True,
        )
        output = result.stdout.decode("UTF-8").split("\n")
        for line in output:
            split_line = line.split()
            if (
                split_line
                and split_line[0] in package_names
                and line not in cleaned_output
            ):
                outdated_found = True
                cleaned_output.append("\t" + line)
    cleaned_output.append("\n")
    if outdated_found:
        print("".join(cleaned_output))
