import sys
import platformdirs
import yaml
from pathlib import Path
import requests
from ionwizard.env_variables import KEYGEN_ACCOUNT_ID
import machineid


def read_config_file():
    config_file = Path(platformdirs.user_config_dir("ionworks")) / "config.yml"
    if config_file.exists():
        with open(config_file) as f:
            config = yaml.safe_load(f)
        return config.get("ionworks", {})
    sys.tracebacklimit = 0
    print("")
    raise FileNotFoundError("No ionworks configuration file was found.\n")


def read_config_libraries():
    return read_config_file().get("libraries", {})


def get_library_key(library_name):
    """
    Get the API key from the library configuration.
    """
    libraries = read_config_libraries()
    for library in libraries:
        if library["library"] == library_name:
            return library["key"]
    return None


def license_check(library_name, custom_library_key=None, check_machine_id=True):
    """
    Check if the license for the library is valid.

    Parameters:
    -----------
    library_name: str
        The name of the library to check the license for.
    custom_library_key: str, optional
        The library key to use for the license check. If not provided, the library key
        will be retrieved from the library configuration.
    """
    if check_machine_id:
        machine_id_check()

    if custom_library_key is not None:
        config = {}
        library_key = custom_library_key
    else:
        config = read_config_file()
        library_key = get_library_key(library_name)

    if library_key is None:
        return {"success": False, "message": "Error: No license key found"}

    # URL for the POST request
    url = f"https://api.keygen.sh/v1/accounts/{KEYGEN_ACCOUNT_ID}/licenses/actions/validate-key"

    # Headers for the request
    headers = {
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json",
    }

    # Data to send in the POST request
    data = {"meta": {"key": library_key}}

    # Some keys are scoped to a user email
    user_email = config.get("user_email")
    if user_email is not None:
        data["meta"]["scope"] = {"user": user_email}

    # Send the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if data["meta"]["code"] == "VALID":
            return {"success": True, "message": "License key is valid"}
        else:
            if data["meta"]["code"] == "EXPIRED":
                return {"success": False, "message": "Error: License key expired"}
            return {"success": False, "message": "Error: Invalid license key"}
    else:
        return {"success": False, "message": "Error: Failed to validate license key"}


def machine_id_check():
    config = read_config_file()
    machine_id = machineid.id()
    if config.get("machine_id") != machine_id:
        return {"success": False, "message": "Error: Machine ID mismatch"}
    return {"success": True, "message": "Machine ID is valid"}


if __name__ == "__main__":
    print(license_check("ionworkspipeline"))
