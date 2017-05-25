"""
This script is meant to parse RMarkdown files, and do some quick
processing to quickly turn them into Jupyter Notebooks.

It will not convert any of the code to python, it merely breaks up the
narrative sections / code sections and turns them into cells of the
appropriate type in the ipynb file.

It will also create a header, stored as raw text in the first cell
of the output notebook.
"""
import nbformat as nbf
from copy import deepcopy
from glob import glob
import os.path as op
import os
from tqdm import tqdm

# Read our template notebook
master_ntbk = nbf.read('../notebooks/utils/template_notebook.ipynb',
                       nbf.NO_CONVERT)

# These are the strings that will define code blocks
startswith_strings = ['```{', '``` {', '```  {']


def lines_to_sections(lines):
    on = False
    ix = 0
    sections = []
    for ii, line in enumerate(lines):
        if on is True:
            if line.startswith('```'):
                on = False
                sections.append(lines[ix: ii + 1])
                ix = ii
        elif any(line.startswith(istr) for istr in startswith_strings):
            on = True
            sections.append(lines[ix + 1: ii])
            ix = ii
    if len(sections) == 0:
        # No r cells
        sections = [lines]
    else:
        # Re-insert first line
        sections[0].insert(0, '---\n')

    # Split apart the metadata and first section
    ix_meta = [ii for ii, line in enumerate(sections[0]) if line.startswith('---\n')]
    meta = sections[0][ix_meta[0]: ix_meta[1] + 1]
    first = sections[0][ix_meta[1] + 1:]
    sections.pop(0)
    sections.insert(0, first)
    sections.insert(0, meta)
    return sections


def sections_to_notebook(sections):
    ntbk = deepcopy(master_ntbk)
    ntbk.cells = []
    for ii, section in enumerate(sections):
        if len(section) == 0:
            # Skip a section with empty code
            continue
        if any(section[0].startswith(istr) for istr in startswith_strings):
            # Code cell for R blocks
            this_cell = deepcopy(master_ntbk['cells'][1])
        elif ii == 0:
            # Raw for metadata
            this_cell = deepcopy(master_ntbk['cells'][2])
        else:
            # Markdown for everything else
            this_cell = deepcopy(master_ntbk['cells'][0])
        this_cell['source'] = '\n'.join(section)
        ntbk['cells'].append(this_cell)
    return ntbk


def fix_metadata(notebook, custom_cells=None):
    """Modify the metadata of an Rmd header so it works with python.

    Parameters
    ----------
    notebook : instance of nbf NotebookNode.
    custom_cells : dictionary
        Any key found in the first cell of `notebook` will have its
        corresponding text replaced by `value` in this dictionary.
    """
    if custom_cells is None:
        custom_cells = {'modified': "'{:%Y-%m-%d}'.format(datetime.now())"}
    meta = notebook['cells'][0]['source']
    lines = meta.split('\n\n')
    for ii, line in enumerate(lines):
        has_key = [key for key in custom_cells.keys()
                   if line.startswith(key)]
        if len(has_key) == 0:
            continue

        key = has_key[0]
        if isinstance(custom_cells[key], str):
            parts = line.split(': ')
            parts[-1] = custom_cells[key]
            line = ': '.join(parts)
        lines[ii] = line.strip()
    notebook['cells'][0]['source'] = '\n'.join(lines)
    return notebook


# Now convert the new notebooks

# Path to the RMarkdown files
rfiles = glob('../notebooks/templates/*/*/*.Rmd')

# Save path
path_save = '../notebooks/template-notebooks'

for ifile in tqdm(rfiles):
    path, filename = op.split(ifile)
    path_extras = path.split('templates/')[1]

    with open(ifile, 'r') as ff:
        lines = ff.readlines()
    # Break up by ```r sections
    sections = lines_to_sections(lines)

    # Create a notebook with these sections
    notebook = sections_to_notebook(sections)

    # Add metadata to the first cell
    notebook = fix_metadata(notebook)

    # Save in a `python_templates` folder
    newfilename = filename.split('.')[0] + '.ipynb'
    folderpath = op.join(path_save, path_extras)
    if not op.exists(folderpath):
        os.makedirs(folderpath)
    nbf.write(notebook, op.join(folderpath, newfilename))
