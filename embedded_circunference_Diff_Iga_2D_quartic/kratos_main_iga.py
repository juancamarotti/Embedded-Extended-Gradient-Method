import sys
import time
import importlib

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata


import KratosMultiphysics 
import KratosMultiphysics.IgaApplication

def CreateAnalysisStageWithFlushInstance(cls, global_model, parameters):
    class AnalysisStageWithFlush(cls):

        def __init__(self, model,project_parameters, flush_frequency=10.0):
            super().__init__(model,project_parameters)
            self.flush_frequency = flush_frequency
            self.last_flush = time.time()
            sys.stdout.flush()

        def Initialize(self):
            super().Initialize()
            sys.stdout.flush()

        def FinalizeSolutionStep(self):
            super().FinalizeSolutionStep()

            if self.parallel_type == "OpenMP":
                now = time.time()
                if now - self.last_flush > self.flush_frequency:
                    sys.stdout.flush()
                    self.last_flush = now

    return AnalysisStageWithFlush(global_model, parameters)

if __name__ == "__main__":

    with open("ProjectParameters.json", 'r') as parameter_file:
        parameters = KratosMultiphysics.Parameters(parameter_file.read())

    analysis_stage_module_name = parameters["analysis_stage"].GetString()
    analysis_stage_class_name = analysis_stage_module_name.split('.')[-1]
    analysis_stage_class_name = ''.join(x.title() for x in analysis_stage_class_name.split('_'))

    analysis_stage_module = importlib.import_module(analysis_stage_module_name)
    analysis_stage_class = getattr(analysis_stage_module, analysis_stage_class_name)

    global_model = KratosMultiphysics.Model()
    simulation = CreateAnalysisStageWithFlushInstance(analysis_stage_class, global_model, parameters)
    simulation.Run()

    model_part = global_model.GetModelPart("IgaBackgroundMeshModelPart")

    active_elements = model_part.GetSubModelPart("active_elements")
    
    # Listas para almacenar los datos
    x_coords = []
    y_coords = []
    solutions = []

    # Loop over the elements and print the results
    for element in model_part.Elements:
        element_geometry = element.GetGeometry()

        N = element_geometry.ShapeFunctionsValues()
        index = 0
        solution = 0.0

        for node in element.GetNodes():
            nodal_solution = node.GetSolutionStepValue(KratosMultiphysics.TEMPERATURE)

            solution += nodal_solution * N[0,index]
            index += 1
        
        x = element_geometry.Center().X
        y = element_geometry.Center().Y


         # Guarda las coordenadas y la solución en las listas
        x_coords.append(x)
        y_coords.append(y)
        solutions.append(solution)

    # Loop over the conditions and print the results
    for condition in model_part.Conditions:
        condition_geometry = condition.GetGeometry()

        N = condition_geometry.ShapeFunctionsValues()
        index = 0
        solution = 0.0

        for node in condition.GetNodes():
            nodal_solution = node.GetSolutionStepValue(KratosMultiphysics.TEMPERATURE)

            solution += nodal_solution * N[0,index]
            index += 1
        
        x = condition_geometry.Center().X
        y = condition_geometry.Center().Y

         # Guarda las coordenadas y la solución en las listas
        x_coords.append(x)
        y_coords.append(y)
        solutions.append(solution)

# Convertir listas a arrays de numpy
x_coords = np.array(x_coords)
y_coords = np.array(y_coords)
solutions = np.array(solutions)

# Crear una cuadrícula para el contour plot
grid_x, grid_y = np.mgrid[min(x_coords):max(x_coords):100j, min(y_coords):max(y_coords):100j]
grid_solution = griddata((x_coords, y_coords), solutions, (grid_x, grid_y), method='cubic')

# Graficar el contour plot
plt.figure(figsize=(8, 6))
contour = plt.contourf(grid_x, grid_y, grid_solution, levels=20, cmap="viridis",vmin = -1, vmax = 1)
plt.colorbar(contour, label="Solution Field (Temperature)")
plt.xlabel("x-coordinate")
plt.ylabel("y-coordinate")
plt.title("Contour Plot of Temperature Solution")

# Guardar la figura en un archivo (por ejemplo, "contour_plot.png")
plt.savefig("contour_plot.png", dpi=300, bbox_inches='tight', format='png')  # Cambia el formato si es necesario

# Mostrar la figura (opcional)
plt.show()



