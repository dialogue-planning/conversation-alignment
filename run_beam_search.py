from time import sleep
from hovor.rollout.rollout_core import Rollout
from hovor.configuration.json_configuration_provider import JsonConfigurationProvider
from environment import initialize_local_environment
import subprocess
import requests
from requests.exceptions import ConnectionError
import json
from pathlib import Path


def run_rasa_model_server(model_path):
    #subprocess.Popen(["rasa", "run", "--enable-api", "-m", 'rollout_bot_no_system-model.tar.gz'])
    while True:
        try:
            requests.post("http://localhost:5005/model/parse", json={"text": ""})
        except ConnectionError:
            sleep(0.1)
        else:
            break

def create_rollout(output_files_path=None, domain=None):
    initialize_local_environment()
    with open ('rollout_bot_no_system_rollout_config.json') as f:
        rollout_cfg = json.load(f)

    configuration_provider = JsonConfigurationProvider('pizza')
    configuration_provider.check_all_action_builders()

    return Rollout(configuration_provider, rollout_cfg)


if __name__ == "__main__":
    create_rollout(str((Path(__file__).parent.parent / "plan4dial/output_files").resolve()), "pizza")
