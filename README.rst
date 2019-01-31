===============================
mro-migrator
===============================

Tool to migrate MRO conda environments to use Anaconda R
--------------------------------------------------------

Say you have an MRO-based conda environment for doing data science with R. You
want to shift over to the Anaconda R world, though, for fixing library problems
or for updates of some sort. You can't just use conda:

``conda install r-base``

You'll get unsatisfiable errors, because the MRO packages that exist in your
environment can't coexist with their Anaconda R counterparts. They're not
compatible, and the metadata is designed to prevent this coexistence. You could
just create a new environment, but that might be tedious, depending on how many
dependencies you have.

What this tool does is remove all MRO-specific packages, then updates your
remaining packages to use Anaconda R instead of MRO. That remove-update cycle
takes care of the unsatisfiability.

To use this tool, run its command line:

``mro-migrator ~/miniconda3/envs/your-r-env``

The default behavior is just to tell you which MRO-only packages will be
removed. The tool does not change anything by default.  To actually execute a migration, pass the ``--execute`` flag:

``mro-migrator --execute ~/miniconda3/envs/your-r-env``

There's very little error handling in this tool. If your environment is not
readily reproducible, it's wise to back it up before you run this tool.
