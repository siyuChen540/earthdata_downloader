#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Downloader Script
Description:
  This script downloads files from a list of URLs provided in a text file.
  It handles authentication, manages redirects, and ensures that files are not
  re-downloaded if they already exist in the specified directory.
@Author: Ceres Chan
@Email : chensy57@mail2.sysu.edu.cn
@EditTime : 2024/09/29 15:03
@Usage:
    python downloader.py --save-dir <SAVE_DIR> \
                        --username <USERNAME> \
                        --password <PASSWORD> \
                        --txt-dir <TXT_FILE_PATH>

@Example:
    python downloader.py --save-dir ./downloads \
                        --username myuser \
                        --password mypass \
                        --txt-dir urls.txt
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from typing import List

import requests
import pandas as pd
from tqdm import tqdm

# Constants
AUTH_HOST = 'urs.earthdata.nasa.gov'
LOG_FILE = "download.log"
CHUNK_SIZE = 1024 * 1024  # 1 MB
MAX_RETRIES = 5

def setup_logging(log_path: Path) -> None:
    """
    Configures the logging settings.

    Args:
        log_path (Path): Path to the log file.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler(sys.stdout)
        ]
    )

class SessionWithHeaderRedirection(requests.Session):
    """
    Custom requests.Session that handles redirection without passing 
    authentication headers to unrelated hosts.
    """
    def __init__(self, username: str, password: str):
        """
        Initializes the session with authentication.

        Args:
            username (str): Earthdata username.
            password (str): Earthdata password.
        """
        super().__init__()
        self.auth = (username, password)

    def rebuild_auth(self, prepared_request, response):
        """
        Overrides the method to prevent sending auth headers to different hosts.

        Args:
            prepared_request (requests.PreparedRequest): The prepared request.
            response (requests.Response): The response received.
        """
        super().rebuild_auth(prepared_request, response)
        original_host = requests.utils.urlparse(response.request.url).hostname
        redirect_host = requests.utils.urlparse(prepared_request.url).hostname

        if (original_host != redirect_host and
            redirect_host != AUTH_HOST and
            original_host != AUTH_HOST):
            if 'Authorization' in prepared_request.headers:
                del prepared_request.headers['Authorization']
                logging.debug(f"Removed Authorization header for host: {redirect_host}")

class Downloader:
    """
    Handles downloading of files from a list of URLs.
    """
    def __init__(self, save_dir: Path, username: str, password: str, txt_dir: Path):
        """
        Initializes the downloader.

        Args:
            save_dir (Path): Directory to save downloaded files.
            username (str): Earthdata username.
            password (str): Earthdata password.
            txt_dir (Path): Path to the text file containing URLs.
        """
        self.save_dir = save_dir
        self.username = username
        self.password = password
        self.txt_dir = txt_dir

        self.session = SessionWithHeaderRedirection(self.username, self.password)
        self.session.headers.update({'User-Agent': 'Downloader/1.0'})

        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.urls = self.load_urls()
        self.to_download = self.filter_existing_files()

    def load_urls(self) -> List[str]:
        """
        Loads URLs from the provided text file.

        Returns:
            List[str]: List of URLs to download.
        """
        try:
            df = pd.read_csv(self.txt_dir, header=None, dtype=str)
            urls = df.iloc[:, 0].dropna().tolist()
            logging.info(f"Loaded {len(urls)} URLs from {self.txt_dir}")
            return urls
        except Exception as e:
            logging.error(f"Failed to read URLs from {self.txt_dir}: {e}")
            sys.exit(1)

    def filter_existing_files(self) -> List[str]:
        """
        Filters out URLs whose corresponding files already exist.

        Returns:
            List[str]: List of URLs that need to be downloaded.
        """
        to_download = []
        for url in self.urls:
            filename = self.save_dir / Path(url).name
            if filename.exists():
                logging.info(f"File already exists, skipping: {filename}")
            else:
                to_download.append(url)
        logging.info(f"{len(to_download)} files to download.")
        return to_download

    def download_all(self) -> None:
        """
        Initiates the download process for all filtered URLs.
        """
        for url in tqdm(self.to_download, desc="Downloading", unit="file"):
            self.download_with_retries(url)

    def download_with_retries(self, url: str) -> None:
        """
        Downloads a file with retry logic.

        Args:
            url (str): The URL of the file to download.
        """
        filename = self.save_dir / Path(url).name
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                with self.session.get(url, stream=True, timeout=30) as response:
                    response.raise_for_status()
                    with open(filename, 'wb') as file_handle:
                        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                            if chunk:
                                file_handle.write(chunk)
                logging.info(f"Successfully downloaded: {filename}")
                break  # Exit the retry loop on success
            except requests.exceptions.RequestException as e:
                logging.error(f"Attempt {attempt} failed for {url}: {e}")
                if attempt == MAX_RETRIES:
                    logging.error(f"Max retries reached. Failed to download: {url}")
                else:
                    logging.info(f"Retrying ({attempt}/{MAX_RETRIES})...")
    
def remove_proxy_env_vars() -> None:
    """
    Removes HTTP and HTTPS proxy environment variables if they exist.
    """
    proxies_removed = False
    for proxy in ['http_proxy', 'https_proxy']:
        if proxy in os.environ:
            del os.environ[proxy]
            logging.info(f"Removed environment variable: {proxy}")
            proxies_removed = True
    if not proxies_removed:
        logging.info("No proxy environment variables to remove.")

def parse_arguments() -> argparse.Namespace:
    """
    Parses command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Download files from a list of URLs.")
    parser.add_argument(
        '--save-dir', 
        type=Path, 
        required=True, 
        help='Directory to save downloaded files.'
    )
    parser.add_argument(
        '--username', 
        type=str, 
        required=True, 
        help='Earthdata username.'
    )
    parser.add_argument(
        '--password', 
        type=str, 
        required=True, 
        help='Earthdata password.'
    )
    parser.add_argument(
        '--txt-dir', 
        type=Path, 
        required=True, 
        help='Path to the text file containing URLs.'
    )
    return parser.parse_args()

def main():
    # Parse command-line arguments
    args = parse_arguments()

    # Setup logging
    log_path = Path.cwd() / LOG_FILE
    setup_logging(log_path)

    logging.info("Starting the downloader script.")

    # Remove proxy environment variables
    remove_proxy_env_vars()

    # Initialize and start the downloader
    downloader = Downloader(
        save_dir=args.save_dir,
        username=args.username,
        password=args.password,
        txt_dir=args.txt_dir
    )
    downloader.download_all()

    logging.info("Downloader script completed successfully.")

if __name__ == "__main__":
    main()
