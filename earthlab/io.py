"""File Input/Output utilities."""

import connectortools as ct
import os.path as op
import os

DATA_URLS = {'week_05': 'https://ndownloader.figshare.com/files/7525363'}
URL_DATA = 'https://www.dropbox.com/sh/n8i01jtyhke5io4/AACK2DQh831C1zzjaY4BRe_2a?dl=1'
HOME = op.join(op.expanduser('~'))
DATA_NAME = 'data_earthlab'


class EarthlabData(object):
    """
    Data storage and retrieval functionality for Earthlab.

    Parameters
    ----------
    path : string | None
        The path where data is stored.
    """
    def __init__(self, path=None):
        if path is None:
            path = op.join(HOME, DATA_NAME)
        self.path = path
        self.data_keys = list(DATA_URLS.keys())

    def __repr__(self):
        s = 'Available Datasets: {}'.format(self.data_keys)
        return s

    def get_data(self, key=None, replace=False, zipfile=True):
        """
        Retrieve the data for a given week and return its path.

        This will retrieve data from the internet if it isn't already
        downloaded, otherwise it will only return a path to that dataset.

        Parameters
        ----------
        key : str
            The dataset to retrieve. Possible options can be found in
            ``self.data_keys``.
        replace : bool
            Whether to replace the data for this key if it is
            already downloaded.
        zipfile : bool
            Whether the dataset is a zip file.

        Returns
        -------
        path_data : str
            The path to the downloaded data.
        """
        if key is None:
            print('Available datasets: {}'.format(
                list(DATA_URLS.keys())))
        elif key not in DATA_URLS:
            raise ValueError("Don't understand key "
                             "{}\nChoose one of {}".format(
                                key, DATA_URLS.keys()))
        else:
            ct.download_file(DATA_URLS[key], key, self.path,
                             replace=replace, zipfile=zipfile)
            path_data = op.join(self.path, key)
            return path_data



def list_files(path, depth=3):
    """
    List files in a directory up to a specified depth.

    Parameters
    ----------
    path : str
        A path to a folder whose contents you want to list recursively.
    depth : int
        The depth of files / folders you want to list inside of ``path``.
    """
    depth_str_base = '  '
    if not path.endswith(os.sep):
        path = path + os.sep
    print(path)
    for ii, (i_path, folders, files) in enumerate(os.walk(path)):
        if ii == 0:
            continue
        folder_name = op.basename(i_path)
        path_wo_base = i_path.replace(path, '')
        this_depth = len(path_wo_base.split('/'))
        if this_depth > depth:
            continue

        # Define the string for this level
        depth_str = depth_str_base * this_depth
        print(depth_str + folder_name)

        if this_depth + 1 > depth:
            continue
        for ifile in files:
            print(depth_str + depth_str_base + ifile)
