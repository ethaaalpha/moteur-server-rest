import subprocess
from moteur_server_rest.config import get_env_variable
from moteur_server_rest.workflow_manager import get_number_running_workflows

def get_max_ram() -> int:
    grep = subprocess.run(
        ["grep", "MemTotal", "/proc/meminfo"],
        capture_output=True,
        check=True,
    )
    output = grep.stdout.decode().strip()
    value = int(output.split()[1])
    # convert result into mB
    return int(value / 1000)

def get_allowed_ram() -> int:
    total_ram = get_max_ram()
    allowed_percentage = int(get_env_variable("RAM_ALLOWED_PERCENTAGE", "80", required=False))

    return total_ram * (allowed_percentage / 100)

def is_enough_ram() -> bool:
    ram_per_worflow = int(get_env_variable("RAM_WORKFLOW", 256, required=True))

    used = get_number_running_workflows() * ram_per_worflow
    allowed = get_allowed_ram()

    return used + ram_per_worflow < allowed
