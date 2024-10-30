Welcome to the Data Processor package! 

This file gives a brief introduction to all the files and folders in this package and an instruction on how to work with the package.

NOTE: A detailed instruction on how to work with the package is given in Appendix F of the manual.

-----

The folder structure is as follows:

Data Processor package
├── BACKGROUND_PYTHON_SCRIPTS
│   ├── FUNCTIONS
│   │   └─── Import_functions.py
│   │         Interactive_plot.py
│   │         my_functions.py
│   └── Data_trim_tool.ipynb
│        GNSS_import.ipynb
│   ├── INPUT
│   │   └─── input.xlsx
│   ├── OUTPUT
│   └─── RUN_THIS_NOTEBOOK.ipynb
│		  INDIVIDUAL_CROSS_SECTION.ipynb
│	      SLOPE_DETERMINATION.ipynb
│		  README.txt


IMPORTANT: Don't change anything to this structure. Otherwise the package doesn't work anymore.

----- 

How to work with the package?

1. Fill in the input.xlsx file with all the information.
2. Load all the files (which you noted down in input.xlsx file) in the INPUT folder.
3. Run the RUN_THIS_NOTEBOOK.ipynb notebook.
4. Run the SLOPE_DETERMINATION.ipynb notebook. 
4. Analyse the output in the OUTPUT folder.
5. Does one specific cross section need additional work? Use the INDIVIDUAL_CROSS_SECTION.ipynb notebook. 
