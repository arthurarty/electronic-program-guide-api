import os
import subprocess
import shutil


def clone_git_repo(repo_url: str, folder_path: str, root_path: str, destination_folder: str):
    # Change to the desired directory
    os.chdir(folder_path)
    repo_folder = f'{folder_path}/webgrabplus-siteinipack'
    print(os.getcwd())
    if os.path.exists(repo_folder):
        print('Directory found, doing a git pull')
        os.chdir(repo_folder)
        subprocess.run(['git', 'pull'])
        print("Git repository updated successfully.")
        os.getcwd()
    else:
        print('Doing a git clone')
        subprocess.run(['git', 'clone', repo_url])
        print("Git repository cloned successfully.")
    os.chdir(root_path)
    print(os.getcwd())
    print('Replacing the siteini.pack file')
    copy_and_replace_folder(f'{repo_folder}/siteini.pack', destination_folder)


def copy_and_replace_folder(source_folder, destination_folder):
    if os.path.exists(destination_folder):
        # If the destination folder already exists, delete it first
        shutil.rmtree(destination_folder)

    # Copy the entire source folder to the destination folder
    shutil.copytree(source_folder, destination_folder)
    print(f"Folder '{source_folder}' copied and replaced as '{destination_folder}'.")
