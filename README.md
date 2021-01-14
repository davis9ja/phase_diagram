# PHASE DIAGRAM

The purpose of this code is to solve a pairing model parameter mesh using the reference-ensemble-optimized IM-SRG-TN. For all mesh points, the energy space parameter $\delta$ is set to 1.0.

### FILES:

`generate_mesh.py`: generate pairs of (`g`, `pb`), where `g` is pairing strength and `pb` is pair-breaking strength; these are input parameters stored as pickled arrays in `mesh_points/`

`run_phase_parallel.py`: run optimization on single mesh point

`plot_phase_parallel.py`: plot all solved mesh points in a heatmap

`opt_job.sb`: generate parallel tasks to solve all mesh points