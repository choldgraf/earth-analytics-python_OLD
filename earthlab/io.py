"""File Input/Output utilities."""

from download import download
import os.path as op
import os

DATA_URLS = {
    'week_05': ('https://ndownloader.figshare.com/files/7525363', 'ZIPFILE'),
    'week_02': [('https://ndownloader.figshare.com/files/7010681',
                 'boulder-precip.csv'),
                ('https://ndownloader.figshare.com/files/7010681',
                 'temperature_example.csv')],
    'week_02-hw': ('https://ndownloader.figshare.com/files/7426738', 'ZIPFILE')
}

#               destfile = "data/boulder-precip.csv"'}
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

    def get_data(self, key=None, name=None, replace=False, zipfile=True):
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
            this_data = DATA_URLS[key]
            if not isinstance(this_data, list):
                this_data = [this_data]
            data_paths = []
            for url, name in this_data:
                name = key if name is None else name
                if zipfile is True:
                    name = key
                    this_root = self.path
                else:
                    this_root = op.join(self.path, key)
                this_path = download(url, name,
                                     this_root,
                                     replace=replace, zipfile=zipfile,
                                     verbose=False)
                data_paths.append(this_path)
            if len(data_paths) == 1:
                data_paths = data_paths[0]
            return data_paths


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
