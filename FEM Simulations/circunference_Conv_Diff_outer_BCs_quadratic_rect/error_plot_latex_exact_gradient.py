import numpy as np
import matplotlib.pyplot as plt

# Activate pgf output in matplotlib
plt.rcParams.update({
    "pgf.texsystem": "pdflatex",
    "font.family": "serif",   # Use LaTeX's default serif font
    "text.usetex": True,      # Use LaTeX for rendering text
    "pgf.rcfonts": False,     # Don't use matplotlib's own fonts
})

# Data for plotting (Exact gradient)
sizes_emb_exact_grad = [0.067, 0.05, 0.033, 0.02, 0.014, 0.011, 0.0091]
errors_emb_exact_grad = [4.312e-5, 1.864e-5, 5.528e-6, 1.662e-6, 6.92e-7, 5.751e-7, 4.457e-7]


# Data for plotting (MLS Order 3)
sizes_emb_MLS_3 = [0.067, 0.05, 0.033, 0.02, 0.014, 0.011, 0.0091]
errors_emb_MLS_3 = [0.00556, 0.00152, 0.00035, 3.652e-5, 1.289e-5, 6.929e-6, 3.225e-6]


# Slope-2 reference line
x_slope2 = np.linspace(min(sizes_emb_MLS_3), max(sizes_emb_MLS_3), 100)
y_slope2 = 2.0*errors_emb_MLS_3[0] * (x_slope2 / sizes_emb_MLS_3[0])**3

# Create the plot
plt.figure(figsize=(6, 4))
plt.loglog(sizes_emb_exact_grad, errors_emb_exact_grad, 'b-v', label="Exact Gradient Imposition")
plt.loglog(sizes_emb_MLS_3, errors_emb_MLS_3, 'c-p', label="MLS (cubic) Gradient Interpolation")
plt.loglog(x_slope2, y_slope2, 'k--')

# Add labels, grid, and legend
plt.xlabel(r"$h$",fontsize=14)
plt.ylabel(r"$\| u - u_h \|_{L^2(\Omega)}$", fontsize=14)
#plt.title("Log-Log Plot of Size vs Error")
plt.grid(which="both", linestyle="--", linewidth=0.5)
plt.legend(fontsize=14)

## Position the triangle above the slope line in log-log space
triangle_x_start = 0.035  # Starting x position
triangle_y_start = 0.0015 # Starting y position above the line
triangle_scale = 0.15  # Scale factor for triangle size

# Calculate triangle vertices in log-log space
triangle_x_end = triangle_x_start * (1 + triangle_scale)  # Horizontal side
triangle_y_end = triangle_y_start * (triangle_x_end / triangle_x_start)**3  # Vertical side for slope 2

# Triangle coordinates
triangle_x = [triangle_x_start, triangle_x_end, triangle_x_end]
triangle_y = [triangle_y_start, triangle_y_start, triangle_y_end]

# Plot the triangle
plt.plot(triangle_x[:2], triangle_y[:2], 'k-', linewidth=1.5)  # Horizontal line
plt.plot(triangle_x[1:], triangle_y[1:], 'k-', linewidth=1.5)  # Vertical line
plt.plot([triangle_x[0], triangle_x[2]], [triangle_y[0], triangle_y[2]], 'k-', linewidth=1.5)  # Hypotenuse

# Add a slope label inside the triangle
plt.text(triangle_x_end * 0.93, triangle_y_start * 0.8, "1", fontsize=10, ha="center", color="black")
plt.text(triangle_x_end * 1.03, triangle_y_start * 1.1, "3", fontsize=10, ha="center", color="black")

# Save the plot as a .pgf file for use in LaTeX
plt.savefig("error_plot.pgf", bbox_inches="tight")

# Show the plot for verification
plt.show()