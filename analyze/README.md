# Analysis Programs
These files are used to visualize results from the extracted radiomic features. **I cannot guarantee that all of these files still work as intended.** The important ones should, but not all of them have been maintained as file structures have changed.  Below is a simple explanation of what each file *should* do, listed approximately in order of importance.

* ITV_viewer.py
  * Displays values and trendlines for radiomic features taken from the ITV and Random_ITV.  Plots are displayed with feature value on the y-axis and days before diagnosis on the x-axis, ITV plotted in blue and Random_ITV plotted in red.

* PTV_viewer.py
  * Does the same as ITV_viewer, but using data taken from the PTV and Random_PTV
  
* Stats1.py
  * Displays a scatter plot representing the statistical significance of the trendline in each radiomic feature.  The y-axis is the p-value that the best-fit line to the ITV data (as seen in ITV_viewer.py) is non-zero, while the x-asis is the p-value that the best-fit line to the Random_ITV data is non-zero.  Each dot represents one radiomic feature, color coded by class, and a line has been drawn at y = 0.05 for reference.
  
* Stats1_PTV.py
  * The same as Stats1, but uses data from the PTV and Random_PTV.
 
* Time_Plot.py
  * This program does the same statistical analysis as Stats1.py, but systematically throws out the data from scans taken before a given date.  By progressing this cut-off date backwards through time, it lets us see how the statistical significance of features' trends vary with time-before diagnosis.  In the plot produced by this program, the x-asis is days before diagnosis, any data taken from scans before this time is not considered.  On the y-axis is the p-value that the best-fit lines of the ITV and Random_ITV have *different slopes*.  The program only displays lines for the five most significant features.
  
* Volume_ITV.py
  * Simmilar to ITV_viewer, but plots the features against the ROI volume rather than against time.  This visualizes whether a feature is strongly correlated with ROI volume.

* heatmap1.py
  * Displays a heatmap showing the r<sup>2</sup> ccorrelation between features in each feature class.

* heatmap2.py
  * Takes in a float between zero and one as a command line argument, returns the given proportion of radiomic features in each class (see Heatmap1) with the lowest correlation to other featuers.
