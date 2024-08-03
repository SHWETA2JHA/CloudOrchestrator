import subprocess
import shutil

def check_disk_space(min_space_gb=5):
    total, used, free = shutil.disk_usage("/")
    free_gb = free // (2**30)
    if free_gb < min_space_gb:
        raise Exception(f"Insufficient disk space. Only {free_gb} GB available, at least {min_space_gb} GB required.")

def docker_ls():
    check_disk_space()
    subprocess.run(['sudo', 'docker', 'image', 'ls'])

def docker_ps():
    check_disk_space()
    subprocess.run(['sudo', 'docker', 'ps'])

def docker_stop(container_id):
    check_disk_space()
    subprocess.run(['sudo', 'docker', 'container', 'rm', '-f', container_id])

def docker_sh(container_id):
    check_disk_space()
    subprocess.run(['sudo', 'docker', 'exec', '-it', container_id, '/bin/bash'])

def docker_run(port1, port2, image_name):
    check_disk_space()
    subprocess.run(['sudo', 'docker', 'run', '-p', f'{port1}:{port2}', '-d', image_name])
