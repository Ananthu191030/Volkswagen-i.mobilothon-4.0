import open3d as o3d
import numpy as np


def create_car_parts_visualization(parts_status):
    # Initialize a visualization window
    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window("Car Parts VR Simulation")

    # Define colors for part status
    status_colors = {
        "good": [0, 1, 0],  # Green
        "damaged": [1, 0, 0]  # Red
    }

    # Text geometry setup
    text_labels = []

    # Create and add parts to the visualization
    for idx, (part, details) in enumerate(parts_status.items()):
        # Create a geometric shape for the part
        if part == "engine":
            part_geometry = o3d.geometry.TriangleMesh.create_box(width=1.5, height=1, depth=1)
        elif part == "brakes":
            part_geometry = o3d.geometry.TriangleMesh.create_sphere(radius=0.5)
        elif part == "transmission":
            part_geometry = o3d.geometry.TriangleMesh.create_cylinder(radius=0.3, height=1.0)
        else:
            part_geometry = o3d.geometry.TriangleMesh.create_box(width=1, height=1, depth=1)

        # Set the part's position
        translation = np.array([2 * idx, 0, 0])
        part_geometry.translate(translation)

        # Set the color based on part status
        color = status_colors.get(details["status"], [0.5, 0.5, 0.5])  # Default to gray
        part_geometry.paint_uniform_color(color)

        # Add the part to the visualization
        vis.add_geometry(part_geometry)

        # Add a label for the part's problem
        label_text = f"{part.capitalize()}:\n{details['problem'] or 'No problems'}"
        text_label = create_text_label(label_text, translation + [0, 0.7, 0])  # Offset above the part
        text_labels.append(text_label)

    # Render text labels (workaround using LineSet for each text line)
    for label in text_labels:
        vis.add_geometry(label)

    # Run the visualization
    vis.run()
    vis.destroy_window()


def create_text_label(text, position):
    """
    Create a 3D label from text as a series of line geometries.
    """
    text_lines = text.split('\n')
    label_geometry = o3d.geometry.LineSet()
    vertices = []
    lines = []
    color = [0, 0, 0]  # Black text

    # Font size control
    spacing = 0.1  # Line spacing
    line_offset = 0.0

    for line in text_lines:
        line_vertices, line_lines = text_to_line_geometry(line, position + np.array([0, -line_offset, 0]))
        line_offset += spacing
        vertices.extend(line_vertices)
        lines.extend(line_lines)

    label_geometry.points = o3d.utility.Vector3dVector(vertices)
    label_geometry.lines = o3d.utility.Vector2iVector(lines)
    label_geometry.colors = o3d.utility.Vector3dVector([color] * len(lines))

    return label_geometry


def text_to_line_geometry(text, position):
    """
    Create geometry for a single line of text using placeholder points and lines.
    In a real-world VR system, a text rendering library would be used.
    """
    vertices = []
    lines = []

    # Simulate text width based on character count
    length = len(text) * 0.1
    start = position
    end = position + np.array([length, 0, 0])

    # Add a line representing the text (placeholder)
    vertices.append(start)
    vertices.append(end)
    lines.append([len(vertices) - 2, len(vertices) - 1])

    return vertices, lines


if __name__ == "__main__":
    # Simulated part statuses
    car_parts = {
        "engine": {"status": "good", "problem": None},
        "brakes": {"status": "damaged", "problem": "Worn brake pads"},
        "transmission": {"status": "damaged", "problem": "Fluid leakage detected"}
    }

    # Start visualization
    create_car_parts_visualization(car_parts)
