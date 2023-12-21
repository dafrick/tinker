# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
# for auto-reloading external modules
# see http://stackoverflow.com/questions/1907993/autoreload-of-modules-in-ipython
# %load_ext autoreload
# %autoreload 2

# %%
import logging
logging.basicConfig(level=logging.INFO)

# %%
import sys, os, pathlib
assert os.getenv('NB_WORKSPACE') is not None
WORK_DIRECTORY = pathlib.Path(f"{os.getenv('NB_WORKSPACE')}")
sys.path.insert(1, (WORK_DIRECTORY).as_posix())
import blurber

# %%
example = blurber.FileParser('articles_to_process.md', max_blurbs = 50)

# %%
print([[e.title, e.authors, e.publisher] for e in example.blurbers])
