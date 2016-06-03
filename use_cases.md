
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

    $ dedop run -c my-config l1a-source-dir
    $ dedop run -c my-config l1a-source-dir/S6_P4_SIM_RMC_L1A__20210929T064000_20210929T064019_T02.nc
    
We now have a (set of) L1B and/or L1BS netCDF files. -> What now?
    
