ARG BASE_CONTAINER=jupyter/datascience-notebook:7a0c7325e470
FROM $BASE_CONTAINER

LABEL maintainer="Damian Frick <damian@damianfrick.com>"

RUN conda install --quiet --yes -c conda-forge \
    'jupytext=1.3.1' \
    'papermill=1.2.1' \
    && \
    conda clean --all -f -y && \
    jupyter lab build && \
    npm cache clean --force && \
    rm -rf $CONDA_DIR/share/jupyter/lab/staging && \
    rm -rf /home/$NB_USER/.cache/yarn && \
    rm -rf /home/$NB_USER/.node-gyp && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

RUN echo 'c.NotebookApp.contents_manager_class="jupytext.TextFileContentsManager"' > ~/.jupyter/jupyter_notebook_config.py
RUN echo 'c.ContentsManager.default_jupytext_formats = ".ipynb,.Rmd"' > ~/.jupyter/jupyter_notebook_config.py
