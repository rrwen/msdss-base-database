Install
=======

1. Install `Anaconda 3 <https://www.anaconda.com/>`_ for Python
2. Install ``msdss-base-database`` via pip or through a conda environment
3. The default is to use ``postgresql`` as the database

.. code::

   conda create -n msdss-base-database python=3.8
   conda activate msdss-base-database
   pip install msdss-base-database[postgresql]

.. note::

    Optionally, you can also install other databases supported by ``sqlalchemy``:

    .. code::

        pip install msdss-base-database[mysql]
        pip install msdss-base-database[sqlite]