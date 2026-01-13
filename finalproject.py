"""
This is the final project "Spectral Matters" for the course Elementary
programming.
"""
import os
import numpy as np
import guilib


state = {
    "textbox": [],
    "points": [],
    "clickable": False,
    "calc_intens": False,
    "energy": [],
    "sum_of_intensities": []
}
"""
State variables that are used throughout the program. They are defined
here and mean the following: "textbox", used in the gui textbox that 
messages are printed into; "points", used in the choose_point function
to determine when to call which other function; "clickable", used to
determine when to call remove_background function within choose_points
function; "calc_intens", used same way as "clickable" but for
calculating the intensitites of peaks in the plot; "energy", used to
save the x data; "sum_of_intensities", used to save the y data.
"""

figure = None
"""
This variable is used for removing the figures before plotting a new 
one. Putting this variable in the state dictionary caused some
problems and having it here made the program work better.
"""

def read_data(folder_path):
    """
    Reads all data files from the given folder. Sums up values from
    the second column in each file to a list called measurements.
    In all data files, first column's values are the same. Creates
    a list with these values called measurement_points. Returns 
    measurement_points and measurements.
    """
    measurement_points = []
    measurements = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        try:
            temp_list = []
            temp_points = []
            with open(file_path, encoding='utf-8') as source:
                for row in source.readlines():
                    data_row = row.strip().split()
                    if len(data_row) == 2:
                        temp_points.append(float(data_row[0]))
                        temp_list.append(float(data_row[1]))
                    else:
                        raise ValueError("Row does not contain exactly 2 columns")
            if not measurements:
                measurements = temp_list
                measurement_points = temp_points
            else:
                measurements = [x + y for x, y in zip(measurements, temp_list)]
        except (FileNotFoundError, IOError,UnicodeDecodeError, ValueError) as e:
            print(f"Error processing {file_name}: {e}")
    return measurement_points, measurements

def open_folder():
    """
    A button handler that opens a dialog the user can use to choose a
    data folder. Loads data from the selected folder and returns the
    measured kinetic energy values and sum of all measurements.
    """
    energy, sum_of_intensities = read_data(guilib.open_folder_dialog("Valitse kansio"))
    if energy is not None and sum_of_intensities is not None:
        state["energy"] = energy
        state["sum_of_intensities"] = sum_of_intensities
        guilib.write_to_textbox(state["textbox"], "Data loaded succesfully", clear=False)
    else:
        guilib.write_to_textbox(state["textbox"], "Data loading unsuccesful", clear=False)

def choose_point(event):
    """
    Receives a mouse event from a mouse click and reads the x and y
    data values from it. The values are printed into a textbox, and
    saved to a list in the program's state dictionary. The function
    will call functions to modify the data and replot the new data.
    And it will also calculate the intensities for the user if called
    with the calculate_intensities funciton instead.
    """
    if state["clickable"]:
        x_data = event.xdata
        y_data = event.ydata
        if x_data is not None and y_data is not None:
            guilib.write_to_textbox(
                state["textbox"],
                f"Value at x={x_data:.2f} is {y_data:.2f}",
                clear=False
            )
            state["points"].append((x_data, y_data))
            if len(state["points"]) == 2:
                remove_noise(state["points"], state["energy"], state["sum_of_intensities"])
                clear_all_figures()
                plot_data(state["energy"], state["sum_of_intensities"])
                state["points"] = []
                state["clickable"] = False
    elif state["calc_intens"]:
        x_data = event.xdata
        y_data = event.ydata
        if x_data is not None and y_data is not None:
            guilib.write_to_textbox(
                state["textbox"],
                f"Value at x={x_data:.2f} is {y_data:.2f}",
                clear=False
            )
            state["points"].append((x_data, y_data))
            if len(state["points"]) == 2:
                start, end = find_indices(
                    state["energy"],
                    state["points"][0][0],
                    state["points"][1][0]
                )
                peak = np.trapezoid(
                    state["sum_of_intensities"][start:end],
                    state["energy"][start:end]
                )
                guilib.write_to_textbox(
                    state["textbox"],
                    f"This peak's intesity is {peak}",
                    clear=False
                )
                state["points"] = []
                state["calc_intens"] = False
    else:
        pass

def plot_data(x_axis_data=None, y_axis_data=None):
    """
    A button handler function that creates a plot on the top right
    frame of the user interface using state variables for the energy
    (x) and intensity (y).
    """
    global figure
    global canvas
    global subplot
    if figure:
        guilib.write_to_textbox(state["textbox"], "Please clear figure first", clear=False)
    else:
        x_axis_data = state.get("energy", [])
        y_axis_data = state.get("sum_of_intensities", [])
        if x_axis_data and y_axis_data:
            canvas, figure, subplot = guilib.create_figure(
                top_right_frame, choose_point, width=500, height=500
            )
            subplot.plot(
                x_axis_data,
                y_axis_data,
                'bo-',
                label='Photoionization Spectrum of Argon',
                markersize=3
            )
            subplot.set_xlabel('Binding energy (eV)')
            subplot.set_ylabel('Intensity (arbitrary units)')
            subplot.legend()
            subplot.figure.tight_layout()
            canvas.draw()
        else:
            guilib.write_to_textbox(state["textbox"], "Please load data first", clear=False)

def clear_all_figures():
    """
    A button handler function that clears all figures and updates the
    canvas.
    """
    global figure
    global canvas
    if figure:
        figure.clear()
        canvas.draw()
        canvas.get_tk_widget().pack_forget()
        canvas = None
        figure = None
        guilib.write_to_textbox(state["textbox"], "Figure cleared.", clear=False)
    else:
        guilib.write_to_textbox(state["textbox"], "No figure to clear.", clear=False)

def remove_noise(points, list_x, list_y):
    """
    Calculates the parameters of slope and intercept from the two
    points given. Produces a list of values that are the y values
    of a line with the given slope and y intercept, from a list of
    x values. Saves new data into the state variable.
    """
    first_point, second_point = points[0], points[1]
    slope = float(
        (second_point[1] - first_point[1]) / (second_point[0] - first_point[0])
    )
    intercept = float(
        (second_point[0] * first_point[1] - first_point[0] * second_point[1]) /
        (second_point[0] - first_point[0])
    )
    list_of_y_values = [slope * x + intercept for x in list_x]
    state["sum_of_intensities"] = [x - y for x, y in zip(list_y, list_of_y_values)]

def remove_background():
    """
    This function removes the background noise and plots the new data
    into the figure by turning state variable "clickable" on allowing
    the calculations and replotting to happen within the choose point
    function.
    """
    if state["energy"] and state["sum_of_intensities"]:
        if figure:
            state["clickable"] = True
            state["points"] = []
            guilib.write_to_textbox(
                state["textbox"],
                "Choose two points from the spectrum by clicking the plot.",
                clear=False
            )
        else:
            guilib.write_to_textbox(state["textbox"], "Plot the figure first", clear=False)
    else:
        guilib.write_to_textbox(state["textbox"], "You need to load data first.", clear=False)

def calculate_intensities():
    """
    This function calculates the intensities of the peaks selected by
    the user by turning state variable "calc_intens" on allowing the
    calculation happen in the choose point function.
    """
    if state["energy"] and state["sum_of_intensities"]:
        if figure:
            state["calc_intens"] = True
            state["points"] = []
            guilib.write_to_textbox(
                state["textbox"],
                (
                "Choose an interval around a peak by choosing two points "
                "from the spectrum by clicking the plot."
                ),
                clear=False
            )
        else:
            guilib.write_to_textbox(state["textbox"], "Plot the figure first", clear=False)
    else:
        guilib.write_to_textbox(
            state["textbox"],
            "There is no data to calculate. Please load data and plot it first.",
            clear=False
        )

def find_indices(measurement_point_series, min_boundary, max_boundary):
    """
    Finds two endpoints from a list of numerical data so that the
    resulting the values between the selected indices are between
    the given minimum and maximum boundaries. Returns the two indices.
    """
    if min_boundary > measurement_point_series[-1]:
        start_index = len(measurement_point_series)
        end_index = len(measurement_point_series)
    else:
        for correspond_index, value in enumerate(measurement_point_series):
            if value >= min_boundary:
                start_index = correspond_index
                break
        for correspond_index, value in enumerate(measurement_point_series):
            if value > max_boundary:
                end_index = correspond_index
                break
            if max_boundary >= measurement_point_series[-1]:
                end_index = len(measurement_point_series)
                break
    return start_index, end_index

def save_figure():
    """
    Save figure: this feature allows the user to save an image of the
    current plot. The user uses a separate dialog for select a filename
    and destination for saving the figure. matplotlib provides you with
    the necessary features to do this.
    """
    if figure:
        path = guilib.open_save_dialog("Valitse kansio minne haluat tallentaa kuvan")
        path += ".png"
        figure.savefig(path, dpi=300)
    else:
        guilib.write_to_textbox(state["textbox"], "Plot a figure first", clear=False)

def main():
    """
    Creates an application window with seven buttons on the left and a
    plot window on the top right corner and a textbox on the bottom
    right corner. 
    """
    global top_right_frame
    host_window = guilib.create_window("Spectral Matters")
    left_frame = guilib.create_frame(host_window, side=guilib.LEFT)
    right_frame = guilib.create_frame(host_window, side=guilib.RIGHT)
    top_right_frame = guilib.create_frame(right_frame, side=guilib.TOP)
    bottom_right_frame = guilib.create_frame(right_frame, side=guilib.BOTTOM)
    guilib.create_button(left_frame, "load data", open_folder)
    guilib.create_button(left_frame, "plot data", plot_data)
    guilib.create_button(left_frame, "remove linear background", remove_background)
    guilib.create_button(left_frame, "calculate intensities", calculate_intensities)
    guilib.create_button(left_frame, "clear figure", clear_all_figures)
    guilib.create_button(left_frame, "save figure", save_figure)
    guilib.create_button(left_frame, "quit", guilib.quit)
    state["textbox"] = guilib.create_textbox(bottom_right_frame)
    guilib.start()

if __name__ == "__main__":
    main()
