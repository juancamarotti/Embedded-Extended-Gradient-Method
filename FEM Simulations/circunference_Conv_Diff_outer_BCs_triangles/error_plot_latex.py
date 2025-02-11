import numpy as np
import matplotlib.pyplot as plt

# Activate pgf output in matplotlib
plt.rcParams.update({
    "pgf.texsystem": "pdflatex",
    "font.family": "serif",   # Use LaTeX's default serif font
    "text.usetex": True,      # Use LaTeX for rendering text
    "pgf.rcfonts": False,     # Don't use matplotlib's own fonts
})

# Data points - RBF linear
sizes_emb_RBF_lin = [0.0964, 0.0707, 0.0424, 0.0316, 0.028, 0.023, 0.022, 0.0202]
errors_emb_RBF_lin = [0.00614, 0.0029, 0.00094, 0.00050, 0.000425, 0.00027, 0.000219, 0.000189]

# Data points - RBF multiquadric
sizes_emb_RBF_mult = [0.0964, 0.0707, 0.0424, 0.0316, 0.028, 0.023, 0.0202]
errors_emb_RBF_mult = [0.0154, 0.00615, 0.0022, 0.00129, 0.00113, 0.00069, 0.00045]

# Data for plotting (LINEAR TRIANGLE - MLS Order 2)
sizes_emb_MLS_2 = [0.0964, 0.0707, 0.0424, 0.0316, 0.028, 0.023, 0.0202]
errors_emb_MLS_2 = [0.0067, 0.00252, 0.00072, 0.000379, 0.000303, 0.000197, 0.000146]

# Data for plotting (LINEAR TRIANGLE - MLS Order 3)
sizes_emb_MLS_3 = [0.0964, 0.0707, 0.0424, 0.0316, 0.028, 0.023, 0.0202]
errors_emb_MLS_3 = [0.00438, 0.00212, 0.00079, 0.000311, 0.000306, 0.00020, 0.000151]


# Slope-2 reference line
x_slope2 = np.linspace(min(sizes_emb_RBF_lin), max(sizes_emb_RBF_lin), 100)
y_slope2 = 4.0*errors_emb_RBF_lin[0] * (x_slope2 / sizes_emb_RBF_lin[0])**2 

# Create the plot
plt.figure(figsize=(6, 4))
plt.loglog(sizes_emb_RBF_lin, errors_emb_RBF_lin, 'b-v', label="RBF (linear) Gradient Interpolation")
plt.loglog(sizes_emb_RBF_mult, errors_emb_RBF_mult, 'g-^', label="RBF (multiquadric) Gradient Interpolation")
plt.loglog(sizes_emb_MLS_2, errors_emb_MLS_2, 'r-s', label="MLS (quadratic) Gradient Interpolation")
plt.loglog(sizes_emb_MLS_3, errors_emb_MLS_3, 'c-p', label="MLS (cubic) Gradient Interpolation")
plt.loglog(x_slope2, y_slope2, 'k--')

# Add labels, grid, and legend
plt.xlabel(r"$h$")
plt.ylabel(r"$\| u - u_h \|_{L^2(\Omega)}$")
#plt.title("Log-Log Plot of Size vs Error")
plt.grid(which="both", linestyle="--", linewidth=0.5)
plt.legend()

# Add a small triangle to illustrate slope 2
# Position the triangle above the slope line in log-log space
triangle_x_start = 0.024  # Starting x position
triangle_y_start = 0.0015 # Starting y position above the line
triangle_scale = 0.15  # Scale factor for triangle size

# Calculate triangle vertices in log-log space
triangle_x_end = triangle_x_start * (1 + triangle_scale)  # Horizontal side
triangle_y_end = triangle_y_start * (triangle_x_end / triangle_x_start)**2  # Vertical side for slope 2

# Triangle coordinates
triangle_x = [triangle_x_start, triangle_x_end, triangle_x_end]
triangle_y = [triangle_y_start, triangle_y_start, triangle_y_end]

# Plot the triangle
plt.plot(triangle_x[:2], triangle_y[:2], 'k-', linewidth=1.5)  # Horizontal line
plt.plot(triangle_x[1:], triangle_y[1:], 'k-', linewidth=1.5)  # Vertical line
plt.plot([triangle_x[0], triangle_x[2]], [triangle_y[0], triangle_y[2]], 'k-', linewidth=1.5)  # Hypotenuse

# Add a slope label inside the triangle
plt.text(triangle_x_end * 0.93, triangle_y_start * 0.84, "1", fontsize=10, ha="center", color="black")
plt.text(triangle_x_end * 1.03, triangle_y_start * 1.05, "2", fontsize=10, ha="center", color="black")

# Save the plot as a .pgf file for use in LaTeX
plt.savefig("error_plot.pgf", bbox_inches="tight")

# Show the plot for verification
plt.show()