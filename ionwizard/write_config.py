import yaml
import uuid
import pathlib
import machineid


class WriteConfig:
    def save_config(self, config, path: str | pathlib.Path):
        if "user_id" not in config:
            config["user_id"] = str(uuid.uuid4())
        config["machine_id"] = machineid.id()

        with open(path, "w") as f:
            yaml.dump({"ionworks": config}, f)
