import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import seaborn as sns
import warnings

def func_read_data(filename, sticklength):
    data = pd.read_table(f'./input/{filename}', sep='\s+', skiprows=24, parse_dates={'GPS Time': [0, 1]})
    data['height(m)'] = data['height(m)'] - sticklength
    return data

def haversine(lat1, lon1, lat2, lon2):     
    # Radius of the Earth in meters     
    R = 6371000  # approximately 6,371 kilometers 
    
    # Convert latitude and longitude from degrees to radians     
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])   
    
    # Differences in latitude and longitude     
    dlat = lat2 - lat1     
    dlon = lon2 - lon1
    
    # Haversine formula for distance     
    a = (math.sin(dlat / 2) ** 2) + math.cos(lat1) * math.cos(lat2) * (math.sin(dlon / 2) ** 2)     
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))     

    distance = R * c          
    return distance

def func_distance(latitudes, longitudes):
    distance_array = []

    for i in range(len(latitudes)):
        lat1 = latitudes[0]
        lon1 = longitudes[0]
        lat2 = latitudes[i]
        lon2 = longitudes[i]
        distance = haversine(lat1, lon1, lat2, lon2)
        distance_array.append(distance)
    
    return distance_array

def func_fitline(distances, elevations, waterlevel, pointname):
    degrees = np.arange(5, 21)
    errors = np.zeros(len(degrees))
    
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', np.RankWarning)
        
        for i in range(len(degrees)):
            degree = degrees[i]
            coefficients = np.polyfit(distances, elevations, degree)
            poly = np.poly1d(coefficients)
            fitted_values = poly(distances)
            errors[i] = np.sum((elevations - fitted_values) ** 2)

        best_degree_index = np.argmin(errors)
        best_degree = degrees[best_degree_index]

        best_coefficients = np.polyfit(distances, elevations, best_degree)
        best_poly = np.poly1d(best_coefficients)
        best_fitted_values = best_poly(distances)
        
    plt.clf()
    plt.scatter(distances, elevations, label='Data points')
    plt.plot(distances, best_fitted_values, label='Cross profile', color='r')
    if waterlevel != 0:
        plt.axhline(waterlevel, label='Waterlevel', linestyle='--', color='blue')
    plt.title(f'Cross profile of {pointname}')
    plt.xlabel('Distance [m]')
    plt.ylabel('Elevation [m]')
    plt.legend()
    plt.grid()
    plt.savefig(f'./output/{pointname}_crossprofile.png');
    plt.show()

    return best_fitted_values

def func_hydraulic_parameters(waterlevel, elevations, distances):
    waterlevel = waterlevel - elevations.max()
    depths = elevations - elevations.max()
    submerged_y = []
    submerged_x = []
    
    for i in range(len(depths)):
        if depths[i] <= waterlevel:
            submerged_y.append(depths[i] - waterlevel)
            submerged_x.append(distances[i])
    
    mean_depth = np.abs(np.mean(submerged_y))
    width = np.max(submerged_x) - np.min(submerged_x)
    area = np.abs(np.trapz(submerged_y, submerged_x))
    hydraulic_depth = area / width
    
    dx = np.diff(submerged_x)
    dy = np.diff(submerged_y)
    distance = 0
    a = 0
    wetted_perimeter = 0
   
    for i in range(len(submerged_x) - 1):
        distance += dx[i]
        if distance >= 0.5:
            y = np.sum(dy[a:i])
            wetted_perimeter += np.sqrt(distance**2 + y**2)
            a = i
            distance = 0
            last_i = i
        if i == len(submerged_x) - 2:
            y = np.sum(dy[a:i])
            wetted_perimeter += np.sqrt(distance**2 + y**2)
            break
        
    hydraulic_radius = np.abs(area / wetted_perimeter)
    
    array = [mean_depth, width, area, hydraulic_depth, hydraulic_radius]
    
    return array

def func_velocityprofile(filename, pointname):
    vp_file = pd.read_csv(f'./input/{filename}', delimiter=';', index_col=0)
    vp_file = vp_file.replace(',', '.', regex=True).astype(float)
    
    dL = 0.5 #m
    h1 = 0.05
    h2 = 0.25
    h3 = 0.25
    h4 = 0.24
    h5 = 0.26

    a = h1 * dL 
    b = h2 * dL # voor rij 0,25
    c = h3 * dL # voor rij 0,25
    d = h4 * dL # voor rij 0,25# voor rij 0,25
    e = h5 * dL # voor rij 0,25

    areas = np.array([a, b, c, d, e])
    areas = areas.reshape(-1, 1)  

    weighted_speeds = vp_file.mul(areas, axis=0)

    sum_weighted_speeds = weighted_speeds.sum().sum()  
    total_surface = np.nansum(areas * vp_file.notna(), axis=0).sum()
    avg_speed = sum_weighted_speeds / total_surface
    
    #ander punt dan 1? verander 0 naar 0.5
    cmap = plt.cm.viridis

    column_distances = np.arange(0, 0.5 * vp_file.shape[1], 0.5)  
    row_distances = [0.00, 0.05, 0.25, 0.50, 0.76, 1.02]

    plt.figure(figsize=(10, 6))
    sns.heatmap(vp_file, cmap=cmap, cbar=True, cbar_kws={"label": "Velocity [m/s]"}, 
                linewidths=0.5, linecolor='black', xticklabels=False, yticklabels=False)

    plt.yticks(ticks=np.linspace(0, len(row_distances) - 1, len(row_distances)), labels=row_distances)
    plt.xticks(ticks=np.arange(0.5, len(column_distances), 1), labels=column_distances, rotation=45, ha='right')

    plt.title(f'Velocity Profile {pointname}, avg speed = {avg_speed:.3f} [m/s]')
    plt.xlabel("Distance [m]")
    plt.ylabel("Water Depth [m]");

    # Toon de plot
    plt.savefig(f'./output/{pointname}_velocityprofile.png');
    
    return avg_speed

def func_slope(waterheight_values, distances):
    # Convert inputs to numpy arrays and ensure they are numeric
    waterheight_values = np.array(waterheight_values, dtype=np.float64)
    distances = np.array(distances, dtype=np.float64)

    # Create a mask to filter out NaN values from both arrays
    mask = ~np.isnan(waterheight_values) & ~np.isnan(distances)

    # Filter the arrays using the mask
    filtered_heights = waterheight_values[mask]
    filtered_distances = distances[mask]

    # Check if there are enough points to calculate a slope
    if len(filtered_heights) < 2 or len(filtered_distances) < 2:
        raise ValueError("Not enough valid data points to calculate a slope.")

    # Perform linear fit
    degree = 1
    coefficients = np.polyfit(filtered_distances, filtered_heights, degree)  # Linear fit
    slope = coefficients[0]  # Extract the slope (coefficient of x)

    return slope

def func_fitline2(distances, elevations, pointname):
    degrees = np.arange(5, 21)
    errors = np.zeros(len(degrees))
    
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', np.RankWarning)
        
        for i in range(len(degrees)):
            degree = degrees[i]
            coefficients = np.polyfit(distances, elevations, degree)
            poly = np.poly1d(coefficients)
            fitted_values = poly(distances)
            errors[i] = np.sum((elevations - fitted_values) ** 2)

        best_degree_index = np.argmin(errors)
        best_degree = degrees[best_degree_index]

        best_coefficients = np.polyfit(distances, elevations, best_degree)
        best_poly = np.poly1d(best_coefficients)
        best_fitted_values = best_poly(distances)
        
    plt.clf()
    plt.scatter(distances, elevations, label='Data points')
    plt.plot(distances, best_fitted_values, label='Cross profile', color='r')
    plt.title(f'Cross profile of {pointname}')
    plt.xlabel('Distance [m]')
    plt.ylabel('Elevation [m]')
    plt.legend()
    plt.grid()
    plt.show()

    return best_fitted_values