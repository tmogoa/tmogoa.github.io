Getting CHPC Right the First Time
====================================

Using the resources provided by South Africa's Center for High Performance Computing (CHPC) for the first time can prove difficult.
This is despite its `documentation wiki <https://wiki.chpc.ac.za/start>`__ being quite detailed, perhaps even too detailed.
I intend this guide to be a guiding star to the sometimes rough sea that is the CHPC cluster and its wiki.
If the CHPC wiki is some classic piece of literature that is difficult to read, then this is a companion guide to navigate it.

Caution
-------
This guide is written for based on a Linux Debian distributions hence not everything transfers cleanly to different operating systems.
But that is not a problem since this is a companion guide to the official wiki.
So you will always know what to do for your specific environment by following the referals to the wiki.

Absolute Beginnings
-------------------
I recommended watching all the tutorial videos if possible interactively to ease yourself in. Find them `here <https://wiki.chpc.ac.za/quick:start#video_tutorials_for_newcomers>`__.

Storage
-------
It is important to read up on storage `here <https://wiki.chpc.ac.za/guide:filesystems>`__. On important piece of information is that the working directory for all your job scripts must be on *Lustre*.
Also note that:

- "*The CHPC’s official policies allow us to remove data that has not been used in the preceding 90 days.*"
- There is no data backup whatsoever.

Authentication
--------------
Firstly work through the `this official guide <https://wiki.chpc.ac.za/quick:login>`__. Ignore the "DTN node access" section for now. In summary the process is roughly:

1. (Done once) Follow `this guide <https://wiki.chpc.ac.za/guide:sshkeys>`__ to generate your SSH keys. It will be along the lines of:

.. code-block:: sh

    ssh-keygen -t ed25519 -C "your_username@lengau"

If you follow the guide well, at some point you will submit your public key into the `this form <https://users.chpc.ac.za/ssh-user/>`__.

2. (Done once) Follow this guide to set up VPN: https://users.chpc.ac.za/vpn/

3. Start the VPN

.. code-block:: sh

    sudo wg-quick up your_username

4. Log in to Lengau 

.. code-block:: sh
    
    ssh your_username@lengau.chpc.ac.za

5. To hop on to other service nodes use the following command:

.. code-clock:: sh
    sh  ssh -i .ssh/id_hpc_mpi dtn

Where ``dtn`` is a service node. Watch `this video <https://www.youtube.com/watch?v=Fq6xT-KjlQ0>`__ for an in depth tutorial. That video link can be found on this `wiki page <https://wiki.chpc.ac.za/quick:login#process>`__ (context might help). Why service nodes?


Service Nodes
---------------

Nodes ``chpcviz1``, ``login1``, ``dtn``, and ``chpclic1`` have internet
access.

Note ``chpcviz1`` does not have git but can access lustre. For
``chpclic1`` it is the converse.

One can use ``login1`` (scp.chpc.ac.za). But installing packages using
``conda`` on ``login1`` frustratingly fails most likely due to some
network configuration/restriction, proof of which is that when using the
–offline flag installation is able to proceed.

``dtn`` seems a formidable alternative but ``conda env create`` as
stalls on ``dtn``. Once needs to write to the help desk to get access to
``dtn``, setup the Google Authenticator App as described
`here <https://wiki.chpc.ac.za/quick:login#dtn_node_access>`__.

Once catch is that I was not able to ssh directly into ``dtn``. So login
via ``scp`` or ``lengau`` (dont forget the ``-A`` flag) then hop into
``dtn`` like so:

.. code:: sh

   ssh dtn

So what has worked is installing on the home directory on ``chpclic1``
the copy the repo directory over to ``lustre\`` later. Inconvenient but
works. Not too bad; hop over as needed then copy files over.

::

   cp -r landscape-analysis-lottery-tickets/ lustre/

or copy only what has changed

::

   rsync -av --ignore-existing landscape-analysis-lottery-tickets/ lustre/

Installing on ``dtn`` succeeded but when it likely installed the wrong
versions. Importing ``torch`` results in the following error:

.. code:: py

   ImportError: /lib64/libm.so.6: version `GLIBC_2.27' not found (required by/site-packages/torch/lib/../../../../libcurand.so.10)

It turns out that on CHPC GLIB_2.17 is what is installed. But it seems
one can make a newer installation, see
`this <https://wiki.chpc.ac.za/howto:compiling_gcc#setting_up_the_latest_gnu_binutils_and_libtool>`__.

Github
------

1. Generate ssh key:
   ``ssh-keygen -t ed25519 -C "mogoa.tonny@gmail.com"``

2. Add it to GitHub
   (https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)

3. Or, use a token
   ``sh     git clone https://<token>@github.com/tmogoa/landscape-analysis-lottery-tickets.git``
   This was easier, no SSH battles.

Python
------

src: `wiki page <https://wiki.chpc.ac.za/guide:python>`__

Check for available Python versions

.. code:: sh

   module avail chpc/python

Anaconda is the preferred module. Standalone Python versions currently
installed are outdated i.e. Python 3.7.

Update: anaconda is actually quite useless. Using pip.

Load a module

.. code:: sh

   module load chpc/python/anaconda/3-2024.10.1
   python3 --version

Using pip or virtualenv with anaconda is not recommended so to create a
virtual environment do the following:

1. Load ``module load chpc/python/anaconda/3-2024.10.1``

2. (Once) Initialise bash shell ``conda init bash`` Log out and then log
   back in.

3. (Once) Create the virtual environment
   ``conda create --prefix /home/your_username/.venv python=3.12 anaconda``

   OR (`refer
   to <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file>`__)

   ::

      conda env create --prefix ./.venv python=3.12 -f requirements.yml

   The first line of the .yml file sets the new environment’s name.

   To update when .yml file changes:
   ``conda env update --prefix ./.venv -f requirements.yml``

4. For a bash script add the following:
   ``eval "$(conda shell.bash hook)"`` This prepares the bash
   environment in a subshell so that commands such as ``conda activate``
   become available.

5. Activate the env ``conda activate /home/USERNAME/.venv/``

6. Deactivate ``sh     conda deactivate /home/USERNAME/.venv/`` ## GPU
   Use

Be sure to install pytorch with CUDA, otherwise you can’t use the GPUs.
Check if you have Pytorch CUDA installed using:

.. code:: sh

   python -c "import torch; print('CUDA Version:', torch.version.cuda)"

I added ``pytorch-cuda`` to my requirements.yml file.

PBS
---
On the week, the subject of jobs is well treated `here <https://wiki.chpc.ac.za/quick:start#scheduler>`` (in general) and `here <https://wiki.chpc.ac.za/guide:gpu#gpu_job_scripts>`__ (for GPUs).

Find a nice intro to PBS
`here <https://gist.github.com/willprice/6569d1123fb30a57a54b3ff1595df1a2>`__.

Prevent re-running:

.. code:: sh

   #PBS -r n

Submit a job:

.. code:: sh

   qsub example.job

Check for queued jobs:

.. code:: sh

   qstat -au your_username

All info for a specific job:

.. code:: sh

   qstat -f 7429553.sched01 

See the nodes assigned ssh into them

.. code:: sh

   qstat -n1 7429553.sched01

   ssh cnode0247
   htop


Long running CLI task?
----------------------

Sometimes you want some long running CLI command to continue running while you are away from your PC. Use ``screen``, a CLI utility that allows you to run your bash sessions "in the background". So a long running task will continue running even if you disconnect from Lengau. See `this guide <https://www.geeksforgeeks.org/linux-unix/screen-command-in-linux-with-examples/>`__ for a full tour.

To start a session:

.. code:: sh

   screen

If you get the error below do what follows:

.. code:: sh

   Directory '/var/run/screen' must have mode 777.

Create a directory named ``.screen`` in your home directory and assign
the appropriate permissions:

::

   mkdir ~/.screen && chmod 700 ~/.screen

Update environment variable ``SCREENDIR`` using the following:

::

   export SCREENDIR=$HOME/.screen

Or better add it to ~/.bashrc to make it permanent.

To list existing sessions:

.. code:: sh

   screen -ls

To detach a session press ``CTRL-A + D``, where ``D`` refers to "detach".

To reattach a session:

.. code:: sh

   screen -r <insert id>