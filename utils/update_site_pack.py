import os
import shutil
import subprocess

from common.custom_logging import logger


def clone_git_repo(repo_url: str, folder_path: str, root_path: str, destination_folder: str):
    os.chdir(folder_path)
    repo_folder = f'{folder_path}/webgrabplus-siteinipack'
    logger.info('Current folder: %s',os.getcwd())
    if os.path.exists(repo_folder):
        logger.info('Directory found, doing a git pull')
        os.chdir(repo_folder)
        subprocess.run(['git', 'pull'])
        logger.info("Git repository updated successfully.")
        os.getcwd()
    else:
        logger.info('Doing a git clone')
        subprocess.run(['git', 'clone', repo_url])
        logger.info("Git repository cloned successfully.")
    os.chdir(root_path)
    logger.info('Current folder: %s',os.getcwd())
    logger.info('Replacing the siteini.pack file')
    copy_and_replace_folder(f'{repo_folder}/siteini.pack', destination_folder)


def copy_and_replace_folder(source_folder: str, destination_folder: str):
    if os.path.exists(destination_folder):
        # If the destination folder already exists, delete it first
        shutil.rmtree(destination_folder)

    # Copy the entire source folder to the destination folder
    shutil.copytree(source_folder, destination_folder)
    logger.info(
        "Folder '%s' copied and replaced as '%s'.", source_folder, destination_folder
    )
