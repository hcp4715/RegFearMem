## Procedure for regulating fear

This is a psychopy (based on psychopy 2) procedure used for Emotion Regulation Memory Consolidation Project.

This folder include two sub-folders: /stim & /data
      /stim ---- stimuli
      /data ---- saving rating data and timing of each trial
      
Scripts for the current experiment:
      shock_calibration.py ---- calibration shocks
      ReapDopa_fam_D1.py   ---- familarize the the procedure and stimuli before experiment
      ReapDopa_exp_D1.py   ---- procedure for day 1
      ReapDopa_exp_D2.py   ---- procedure for day 2
      
excel and csv files:
      pseudoRandomConditions.xlsx ---- pseudo randomized order for each participant
      pseudOrd_d1.csv             ---- pseudo order for day 1, part of the xlsx file
      pseudOrd_d2.csv             ---- pseudo order for day 2, part of the xlsx file
      
Scripts, files for running the procedure
      inpout32.dll      ---- this is necessary for sending trigger (parallel port)
      
      ratingscale_revised_PY2.py ---- revised ratingscale script, so that when the button is down, the marker will keep moving. Need to replace the orignal ratingscale.py in the installing folder (e.g. mine is located in C:\Program Files (x86)\PsychoPy2\Lib\site-packages\psychopy\visual).
      
      ratingscale_original.py  ---- oringal ratingscale from Psychopy 2, button need to be release and re-press to move the marker.
      
Other files:
      Maybe used for version control.