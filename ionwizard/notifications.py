import subprocess


def find_outdated(package_names: list[str]):
    package_names.append("ionwizard")
    result = subprocess.run(["pip", "list", "--outdated"], capture_output=True)
    output = result.stdout.decode("UTF-8").split("\n")
    cleaned_output = ["\nThe following ionworks packages can be updated:\n"]
    for line in output:
        split_line = line.split()
        if split_line and split_line[0] in package_names:
            cleaned_output.append("\t" + line)
    cleaned_output.append("\n")
    print("".join(cleaned_output))
