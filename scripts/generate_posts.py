"""
This script will convert jupyter notebooks into Jekyll-style markdown
files, and place them in the appropriate folder. It will also move
the images properly so that they are in their own separate directory.
It will only do this for notebook files that are NEWER than their
corresponding jekyll markdown files.
"""
import nbformat as nf
import os
import os.path as op
import subprocess
from glob import glob
from tqdm import tqdm
from datetime import datetime
import shutil as sh


def parse_meta_file(meta, run_keys={}):
    """Parse a metadata cell of a Jupyter notebok."""
    if meta['cell_type'] != 'raw':
        raise ValueError('First cell must have raw text inside')
    # A dictionary that runs the function with the value as input
    def_run_keys = {'modified': lambda a: eval(a.format(datetime.today())),  # Insert the date
                    'permalink': lambda a: a.replace('earth-analytics/', 'earth-analytics-python/')  # Correct URL paths
                    }
    run_keys.update(def_run_keys)

    # Only use lines with key: val pairs
    metalines = meta['source'].split('\n')
    for ii, ln in enumerate(metalines):
        if '---' in ln:
            continue
        split = ln.split(': ')
        if len(split) < 2:
            continue
        if len(split) > 2:
            ln_type = split[0]
            ln_val = ': '.join(split[1:])
        else:
            ln_type, ln_val = split

        # If we have a function for one of the keys, run it and replace the value
        if ln_type not in run_keys.keys():
            continue
        new_val = run_keys[ln_type](ln_val)
        metalines[ii] = ': '.join([ln_type, new_val])

    # Replace the meta cell
    meta['source'] = '\n'.join(metalines)
    return meta

# --- Set up paths ---
# Path to root of site
path_root = op.abspath('../')

# Finds the ipynb files
files = glob(op.join('..', 'notebooks', 'final-notebooks', '*', '*', '*.ipynb'))

# Where to save the MD posts
save_path = op.join('..', '_posts', 'course-materials', 'earth-analytics-python')


# --- Preprocess Jupyter Notebooks ---
# Temporary directory for jupyntbks
if not op.isdir(op.join('.', 'tmp')):
    os.makedirs(op.join('.', 'tmp'))

built, skipped = (0, 0)
for ifile in tqdm(files):
    # Find file names etc
    path = ifile.split('final-notebooks/')[-1]
    path_tmp_file = op.basename(path)
    file_name = op.splitext(path_tmp_file)[0]
    path_folders = op.dirname(path)
    path_rel_to_root = op.dirname(ifile.split('final-notebooks')[1])

    # --- Metadata ---
    # Read in notebook, pull meta cell
    ntbk = nf.read(ifile, nf.NO_CONVERT)
    meta = ntbk['cells'][0]
    ntbk['cells'][0] = parse_meta_file(meta)

    # --- Replace cell text ---
    # Change image paths to {{ site.url }}
    # Path relative to root for this notebook
    rel_path = os.path.relpath(path_root, ifile)

    for ii, cell in enumerate(ntbk['cells']):
        if cell['cell_type'] == 'markdown':
            cell['source'] = cell['source'].replace(rel_path[:-2], "{{ site.url }}%s" %os.sep)

    # --- Convert ---
    # Set paths
    path_rel_to_root_split = path_rel_to_root.split('/')
    build_path = op.join(path_root, "_posts", 'course-materials', 'earth-analytics-python', *path_rel_to_root_split)
    path_imgs_root = op.relpath(path_root, build_path)
    images_path = op.join(path_imgs_root, "images", "course-materials", "earth-analytics-python", *path_rel_to_root_split)
    path_new_file = op.join(build_path, file_name + '.md')

    # Check the file date, if md has been modified *after* notebook then don't re-build it
    if op.exists(path_new_file):
        last_modified_ntbk = op.getmtime(ifile)
        last_modified_md = op.getmtime(path_new_file)
        if last_modified_ntbk <= last_modified_md:
            skipped += 1
            continue

    # Write the file
    path_save_tmp_file = op.join('.', 'tmp', path_tmp_file)
    nf.write(ntbk, path_save_tmp_file)

    # Call nbconvert
    build_call = '--FilesWriter.build_directory={}'.format(build_path)
    images_call = '--NbConvertApp.output_files_dir={}'.format(images_path)
    subprocess.call(['jupyter', 'nbconvert',
                     '--to', 'markdown',
                     images_call, build_call, path_save_tmp_file])

    # Clean up
    os.remove(path_save_tmp_file)
    built += 1
sh.rmtree(op.join('.', 'tmp'))
print('Built {} files\nSkipped {} files'.format(built, skipped))
