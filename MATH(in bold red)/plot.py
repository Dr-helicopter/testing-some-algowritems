import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from Vectors import Vector3


class Plot3D:
    @staticmethod
    def plot_point(vector: Vector3, color='b'):
        # Set up a 3D plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Plot the origin and the Vector3 point
        ax.scatter([0], [0], [0], color='gray', label='Origin')  # Origin
        ax.scatter([vector.x], [vector.y], [vector.z], color=color, label='Point')

        # Customize plot
        ax.set_xlabel('X Axis')
        ax.set_ylabel('Y Axis')
        ax.set_zlabel('Z Axis')
        ax.legend()
        plt.show()