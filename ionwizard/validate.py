import sys
import platformdirs
import yaml
from pathlib import Path
import requests
from ionwizard.env_variables import KEYGEN_ACCOUNT_ID


def read_config_libraries():
    config_file = Path(platformdirs.user_config_dir("ionworks")) / "config.yml"
    if config_file.exists():
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)
        libraries = config.get("ionworks", {}).get("libraries", {})
        return libraries
    sys.tracebacklimit = 0
    raise FileNotFoundError("\nError: No ionworks configuration file was found.\n")


def get_library_key(library_name):
    """
    Get the API key from the library configuration.
    """
    libraries = read_config_libraries()
    for library in libraries:
        if library["library"] == library_name:
            return library["key"]
    return None


def license_check(library_name, custom_library_key=None):
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
    if custom_library_key is not None:
        library_key = custom_library_key
    else:
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

    # Send the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Print the response content
        data = response.json()
        if data["meta"]["code"] == "VALID":
            return {"success": True, "message": "License key is valid"}
        else:
            if data["meta"]["code"] == "EXPIRED":
                return {"success": False, "message": "Error: License key expired"}
            return {"success": False, "message": "Error: Invalid license key"}
    else:
        return {"success": False, "message": "Error: Failed to validate license key"}
