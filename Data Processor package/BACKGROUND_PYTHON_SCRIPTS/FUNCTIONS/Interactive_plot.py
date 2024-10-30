# Import packages
import matplotlib.pyplot as plt
import pandas as pd
import ipywidgets as widgets

# Function to update the plot when the slider is used
def update_plot(point_name, data, start, stop, plot_output):
    # Plot_output is the visiulisation created by this function
    with plot_output:
        plot_output.clear_output(wait=True)

        # Extract columns
        latitude = data['latitude(deg)']
        longitude = data['longitude(deg)']
        height = data['actual_height(m)']
        measurement_no = data['no.']

        # Define the points based on threshold range
        points_before_range = measurement_no < start
        points_in_range = (measurement_no >= start) & (measurement_no <= stop)
        points_after_range = measurement_no > stop

        # Create the figure and subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))

        # Scatter plot for latitude vs longitude
        ax1.scatter(longitude[points_in_range], latitude[points_in_range], label='Measurement', color='blue')
        ax1.scatter(longitude[points_before_range], latitude[points_before_range], label='To be removed', color='red')
        ax1.scatter(longitude[points_after_range], latitude[points_after_range], color='red')
        ax1.set_xlabel('Longitude (degrees)')
        ax1.set_ylabel('Latitude (degrees)')
        ax1.set_title(f"Scatterplot of point '{point_name}'")
        ax1.grid(True)
        ax1.legend()

        # Set limits for scatter plot
        x_margin = (longitude.max() - longitude.min()) * 0.1
        y_margin = (latitude.max() - latitude.min()) * 0.1
        ax1.set_xlim(longitude.min() - x_margin, longitude.max() + x_margin)
        ax1.set_ylim(latitude.min() - y_margin, latitude.max() + y_margin)

        # Height profile plot
        ax2.plot(measurement_no[points_before_range], height[points_before_range], color='red', label='To be removed')
        ax2.plot(measurement_no[points_in_range], height[points_in_range], color='blue', label='Measurement')
        ax2.plot(measurement_no[points_after_range], height[points_after_range], color='red')
        ax2.set_xlabel('Measurement no.')
        ax2.set_ylabel('Height (m)')
        ax2.set_title(f"Height Profile of '{point_name}'")
        ax2.grid(True)
        ax2.legend()

        # Set limits for height profile plot
        h_margin = (height.max() - height.min()) * 0.1
        no_margin = (measurement_no.max() - measurement_no.min()) * 0.1
        ax2.set_xlim(measurement_no.min() - no_margin, measurement_no.max() + no_margin)
        ax2.set_ylim(height.min() - h_margin, height.max() + h_margin)     
        
        # Show the figure
        plt.tight_layout()
        plt.show()


# Function to create widgets and set up interactions
def create_interactive_plot_widget(measurement_start, measurement_stop, data, widget_container, plot_output, point_name, data_store_cut):
    # Widget container is the export for the interactive widgets
    with widget_container:
        widget_container.clear_output()

        # Slider to select start and stop values
        range_slider = widgets.FloatRangeSlider(
            value=[measurement_start, measurement_stop],
            min=measurement_start,
            max=measurement_stop,
            step=1,
            description='Threshold Range:',
            layout={'width': '800px'}
        )

        # Text inputs for manual start and stop entries
        start_text = widgets.FloatText(
            value=measurement_start,
            description='Start:',
            layout={'width': '400px'}
        )
        stop_text = widgets.FloatText(
            value=measurement_stop,
            description='Stop:',
            layout={'width': '400px'}
        )

        # Button to cut the dataset based on selected range
        cut_button = widgets.Button(description="Cut Dataset")

        # Function to cut the dataset
        def cut_dataset():
            start, stop = range_slider.value
            data_cut = data[(data['no.'] >= start) & (data['no.'] <= stop)]
            
            # Store data_cut in the global dictionary passed as an argument
            data_store_cut['data_cut'] = data_cut
            
            # Display the message in plot_output widget
            with plot_output:
                plot_output.clear_output(wait=True)
                print(f"Dataset cut from measurement no. {start:.0f} to {stop:.0f}.")

        # Function to update the plot based on slider or text inputs
        def update_from_slider_or_text(start, stop):
            update_plot(point_name, data, start, stop, plot_output)

        # Synchronize slider and text inputs
        def on_slider_change(change):
            start, stop = change['new']
            start_text.value = start
            stop_text.value = stop
            update_from_slider_or_text(start, stop)

        def on_start_text_change(change):
            range_slider.value = (change['new'], range_slider.value[1])
            update_from_slider_or_text(change['new'], range_slider.value[1])

        def on_stop_text_change(change):
            range_slider.value = (range_slider.value[0], change['new'])
            update_from_slider_or_text(range_slider.value[0], change['new'])

        # Observe changes
        range_slider.observe(on_slider_change, names='value')
        start_text.observe(on_start_text_change, names='value')
        stop_text.observe(on_stop_text_change, names='value')

        # Attach the function to the cut button
        cut_button.on_click(lambda b: cut_dataset())

        # Display the created widgets along with the cut button
        display(widgets.VBox([range_slider, widgets.HBox([start_text, stop_text, cut_button])]))

