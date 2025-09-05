# infrastructure/sandbox_executor.py

import os
import subprocess
import tempfile

from assistant.config import SANDBOX_IMAGE


class SandboxExecutor:
    def execute(self, code: str) -> list[str]:
        workdir = tempfile.mkdtemp()
        path = os.path.join(workdir, "script.py")
        with open(path, "w") as f:
            f.write(code)
        cmd = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{workdir}:/app",
            "-w",
            "/app",
            SANDBOX_IMAGE,
            "python",
            "script.py",
        ]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return [line.decode().rstrip() for line in proc.stdout]
