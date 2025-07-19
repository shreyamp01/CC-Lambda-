import docker

client = docker.from_env()

def run_python_function(code):
    container = client.containers.run(
        "python:3.9-slim",
        command=f"python3 -c \"{code}\"",
        remove=True
    )
    return container
