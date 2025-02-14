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
sizes_emb_RBF_lin = [0.0666, 0.05, 0.04, 0.033, 0.0286, 0.025, 0.02, 0.0125, 0.0105]
errors_emb_RBF_lin = [0.0108, 0.0030, 0.00226, 0.00162, 0.0011, 0.000708, 0.000475, 0.00015, 0.00011]

# Data points - RBF multiquadric
sizes_emb_RBF_invmult = [0.0666, 0.05, 0.04, 0.033, 0.0286, 0.025, 0.02, 0.0125, 0.0105]
errors_emb_RBF_invmult = [0.00657, 0.00255, 0.00176, 0.00127, 0.00091, 0.0006, 0.000405, 0.000148, 0.000121]

# Data for plotting (MLS Order 3)
sizes_emb_MLS_3 = [0.0666, 0.05, 0.04, 0.033, 0.0286, 0.025, 0.02, 0.0125, 0.0105]
errors_emb_MLS_3 = [0.0087, 0.0033, 0.00208, 0.00102, 0.000689, 0.00047, 0.00030, 0.00011, 7.852e-5]

# Data for plotting (MLS Order 2)
sizes_emb_MLS_2 = [0.0666, 0.05, 0.033, 0.0286, 0.025, 0.02, 0.0125, 0.0105]
errors_emb_MLS_2 = [0.0087, 0.0033, 0.0025, 0.00137, 0.00062, 0.00039, 0.00011, 8.527e-5]


# Slope-2 reference line
x_slope2 = np.linspace(min(sizes_emb_RBF_lin), max(sizes_emb_RBF_lin), 100)
y_slope2 = 2.0*errors_emb_RBF_lin[0] * (x_slope2 / sizes_emb_RBF_lin[0])**2 

# Create the plot
plt.figure(figsize=(6, 4))
plt.loglog(sizes_emb_RBF_lin, errors_emb_RBF_lin, 'g-s', label="RBF (linear) Gradient Interpolation")
plt.loglog(sizes_emb_RBF_invmult, errors_emb_RBF_invmult, 'b-d', label="RBF (multiquadric) Gradient Interpolation")
plt.loglog(sizes_emb_MLS_2, errors_emb_MLS_2, 'c-p', label="MLS (quadratic) Gradient Interpolation")
plt.loglog(sizes_emb_MLS_3, errors_emb_MLS_3, 'r-v', label="MLS (cubic) Gradient Interpolation")
plt.loglog(x_slope2, y_slope2, 'k--')

# Add labels, grid, and legend
plt.xlabel(r"$h$", fontsize=14)
plt.ylabel(r"$\| u - u_h \|_{L^2(\Omega)}$", fontsize=14)
#plt.title("Log-Log Plot of Size vs Error")
plt.grid(which="both", linestyle="--", linewidth=0.5)
plt.legend(fontsize=14)

# Add a small triangle to illustrate slope 2
# Position the triangle above the slope line in log-log space
triangle_x_start = 0.024  # Starting x position
triangle_y_start = 0.0027  # Starting y position above the line
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