
Use case - ...

    $ dedop --help

    $ dedop workspace list
    my-ws-1
    test-ws
    
    $ dedop workspace create new-experiment

Download data from FTP to *l1a-source-dir*.

    $ dedop workspace add-l1a new-experiment l1a-source-dir/*.nc

Read the doc how to create a basic JSON configuration file or start from an example: *<my-config.json>*
 
    $ dedop config create my-config.json
    
Will write *my-config.json* and open the OS default editor. You can change parameters values as 
shown in the mock up.  

    $ dedop config list 
    $ dedop config add myfile.json 
    
Run processor

    $ dedop run -n R1 -c my-config l1a-source-dir
    $ dedop run -n R2 -c my-config l1a-source-dir/S6_P4_SIM_RMC_L1A__20210929T064000_20210929T064019_T02.nc
    
We now have a (set of) L1B and/or L1BS netCDF files. -> What now?
    
    $ dedop listvars 
    time
    longitude
    latitude
    altitude
    waveforms
    power
    
    $ dedop plot --recs=634,75,632 --vars=waveforms,power
    
    
will output

* overview map with trace, selected records highlighted
* variable-specific plots for selected records, may include 2D and 3D plots
* table of variable values at selected records
* anything else?
* optional: HTML page that includes all the output as a report
    
Printing of values:

    $ dedop print --vars=power --recs=634,632

Comparison:

    $ dedop cmp R1 R2 --vars=waveforms,power --recs=634,75,632 
    
