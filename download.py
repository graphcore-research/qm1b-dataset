# Copyright (c) 2023 Graphcore Ltd. All rights reserved.
import hashlib
import json
import os
import os.path as osp

import requests
from jsonargparse import CLI
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map


def download_item(url: str, dst: str, chunk_size: int = 1024 * 1024):
    response = requests.get(url, stream=True)
    filename = osp.basename(dst)
    check_md5 = hashlib.md5()

    with open(dst, mode="wb") as file:
        with tqdm(
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            miniters=1,
            desc=filename,
            total=int(response.headers.get("content-length", 0)),
        ) as pbar:
            for chunk in response.iter_content(chunk_size=chunk_size):
                file.write(chunk)
                check_md5.update(chunk)
                pbar.update(len(chunk))

    return check_md5.hexdigest()


def download(root: str, max_threads: int = 8):
    """
    Downloads the QM1B dataset to a local folder

    Args:
        root (str): the root folder for storing a local copy of QM1B
        max_threads (int): the maximum number of threads for parallel downloading.
    """
    with open("figshare_listing.json") as f:
        file_list = json.load(f)

    dst_root = osp.abspath(root)
    folders = ["", "validation", *["training"] * (len(file_list) - 2)]
    dst_files = [osp.join(dst_root, d, f["name"]) for f, d in zip(file_list, folders)]

    os.makedirs(osp.join(root, "validation"), exist_ok=True)
    os.makedirs(osp.join(root, "training"), exist_ok=True)
    urls = [f["download_url"] for f in file_list]
    actual_md5 = list(
        thread_map(download_item, urls, dst_files, max_workers=max_threads)
    )
    expect_md5 = [f["computed_md5"] for f in file_list]

    if not all(a == b for a, b in zip(actual_md5, expect_md5)):
        raise RuntimeError(
            (
                "Downloaded version differs from expected checksum.\n"
                "Please retry this download and raise an issue in\n\n"
                "https://github.com/graphcore-research/qm1b-dataset/issues."
            )
        )


if __name__ == "__main__":
    CLI(download)
