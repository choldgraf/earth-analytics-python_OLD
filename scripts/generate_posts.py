"""
This script will convert jupyter notebooks into Jekyll-style markdown
files, and place them in the appropriate folder. It will also move
the images properly so that they are in their own separate directory.
It will only do this for notebook files that are NEWER than their
corresponding jekyll markdown files.
"""
import nbformat as nf
import os
import subprocess
from glob import glob
from tqdm import tqdm
from datetime import datetime
import shutil as sh

# --- Set up paths ---
# Path to root of site
path_root = os.path.abspath('../')

# Finds the ipynb files
files = glob('../notebooks/final-notebooks/*/*/*.ipynb')

# A dictionary that runs the function with the value as input
run_keys = {'modified': lambda a: a.format(datetime.today())}

# Where to save the MD posts
save_path = '../_posts/course-materials/earth-analytics-python/'


# --- Preprocess Jupyter Notebooks ---
# Temporary directory for jupyntbks
if not os.path.isdir(os.path.join('.', 'tmp')):
    os.makedirs(os.path.join('.', 'tmp'))

built, skipped = (0, 0)
for ifile in tqdm(files):
    # Find file names etc
    path = ifile.split('final-notebooks/')[-1]
    path_tmp_file = os.path.basename(path)
    file_name = os.path.splitext(path_tmp_file)[0]
    path_folders = os.path.dirname(path)
    path_rel_to_root = os.path.dirname(ifile.split('final-notebooks')[1])

    # Read in notebook, pull meta cell
    ntbk = nf.read(ifile, nf.NO_CONVERT)
    meta = ntbk['cells'][0]
    if meta['cell_type'] == 'raw':

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
            new_val = eval(run_keys[ln_type](ln_val))
            metalines[ii] = ': '.join([ln_type, new_val])

        # Replace the meta cell
        meta['source'] = '\n'.join(metalines)
        ntbk['cells'][0] = meta

    # --- Convert ---
    # Set paths
    build_path = os.path.join(path_root, "_posts/course-materials/earth-analytics-python{}".format(path_rel_to_root))
    path_imgs_root = os.path.relpath(path_root, build_path)
    # rather than the relative stuff, just build out the full path to ensure it's right
    images_path = os.path.join(path_root, "images/course-materials/earth-analytics-python{}".format(path_rel_to_root))
    path_new_file = os.path.join(build_path, file_name + '.md')

    # Check the file date, if md has been modified *after* notebook then don't re-build it
    if os.path.exists(path_new_file):
        last_modified_ntbk = os.path.getmtime(ifile)
        last_modified_md = os.path.getmtime(path_new_file)
        if last_modified_ntbk <= last_modified_md:
            skipped += 1
            continue

    # Write the file
    path_save_tmp_file = os.path.join('.', 'tmp', path_tmp_file)
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
sh.rmtree(os.path.join('.', 'tmp'))
print('Built {} files\nSkipped {} files'.format(built, skipped))
