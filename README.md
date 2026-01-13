# Sprectal_Matters
This is the final project called "Spectral Matters" for the course Elementary Programming in University of Oulu. This was created in the summer of 2024 and gave me the best grade of 5 in this course.

## Background
In electron spectroscopy matter is examined by radiating it with a bright light and measuring the kinetic energy of electrons that come off it. When the photonic energy of light and kinetic energy of the electrons are known, they can be used to derive the amount of force that was required to break off the electrons. This provides valuable information about the matter's electron structure, and its chemical and physical properties. This phenomenon where photons break off electrons is called photoionization, and the broken off electrons are called photoelectrons.
In this course project you'll learn how to read data into a program and how to perform small operations on the data, and how to plot data using Python libraries. Your task is to write a program for analyzing the photoionization spectrum of argon. For this purpose we have provided you with simulated data where argon atoms have been ionized and the kinetic energy of broken off electrons has been measured. 

## Program overview
The measurement has been performed multiple times, and each measurement session has been recorded into a different, numbered file. The file names are in the format measurement_i.txt. Each file contains rows of data with two floating point numbers. The first number on each line is the binding energy of electrons, derived from the measured kinetic energy (unit: electronvolt); the second number is the corresponding intensity (no specific unit; this described the amount of electrons measured with this particular binding energy). In each measurement file, the first column contains the same uniformly distributed binding energy values. Your program should add together the intensity values from each file. The purpose is to eliminate noise from the measurements. 

Due to the measuring equipment, the spectrum has a linear background. Aside from the obvious peaks it looks like a downward sloping line. The background signal that causes the sloping should be removed before analyzing the spectrum. This can be done by choosing two points from the spectrum and fitting a line between these points. After this, at each data point, values obtained from this line are subtracted from the measured intensity values.
When analyzing the spectrum our primary interest are the two rather obvious peaks in intensity; in particular, their relative intensity. The intensity of each peak is obtained by computing their area by obtaining its integral. This can obtained by using the trapezoidal rule to estimate the integral. According to theory the first peak should have approximately double the intensity of the second one.

## Program features
The program has the following features:
1. The program has a graphical user interface with all the features available for the user.
2. Load data: loads data from a user-specified location and reads it into program memory in a format that is suitable for processing. Should return one list for each column in the data. The first list should contain measured kinetic energy values (measurement points) and the second one the sums of all measurements for each row.
3. Plot data: this plots the current data (the user is prompted to load the data first if it hasn't been loaded yet). Data is plotted using matplotlib, but it is plotted inside the application window. The figure will look like the one below.
4. Remove linear background: removes the linear background from the data as described above. The user selects two points from the figure, and a line is fitted between these points. The line is then subtracted from the data. If there's no data in the program memory yet, the user is given an error message about it.
5. Calculate intensities: The intensity of peaks can be calculated. This is done with the trapz function from numpy. The use selects the interval by clicking on the figure. The result is printed somewhere inside the window. If there's no data in the program memory yet, the user is given an error message about it.
6. Save figure: this feature allows the user to save an image of the current plot. The user uses a separate dialog for select a filename and destination for saving the figure. matplotlib provides the necessary features to do this.

![Example plot of the data](examplefigure.png)

## About libraries
The course provided a library that is built on top of TkInter, and offers a heavily simplified interface to some of its features through functions. The library's docstrings describe how to use it. The lirary's main program also has a short example of how to make a simple interface. THIS IS NOT INCLUDED IN THIS REPOSITORY
