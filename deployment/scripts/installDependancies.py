import os
import subprocess



def main():

    path_to_save = os.getcwd() + "/deployment/lib"
    requirements_file_path = os.getcwd() + "/deployment/requirements.txt"

    commands = [
        "python -m pip install -t {path_to_save} -r {requirements_file_path} --platform manylinux2014_x86_64 --python-version 3.11  --implementation cp --abi cp311 --only-binary :all:".format(
            path_to_save=path_to_save, requirements_file_path=requirements_file_path
        )]

    for command in commands:
        subprocess.run(command, shell=True)


if __name__ == "__main__":
    main()
