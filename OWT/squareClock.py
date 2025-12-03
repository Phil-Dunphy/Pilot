import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class SquareClock:
    def __init__(self, size=400):
        """
        Initialize the square clock generator

        Parameters:
        size: Size of the square in pixels
        """
        self.size = size
        self.positions = 8  # 8 positions around the square

    def generate_clock(self, start_number=1, visible_numbers=None, pointer_position=3,
                       output_file='clock.png', theme="light"):
        # ✅ Farbmodus steuern
        if theme == "dark":
            bg_color = "black"
            fg_color = "white"
        else:
            bg_color = "white"
            fg_color = "black"

        # Zahlenfolge (gleich wie bei RoundClock)
        numbers = [(start_number + i - 1) % 8 + 1 for i in range(8)]

        if visible_numbers is None:
            visible_numbers = numbers[:]

        fig, ax = plt.subplots(1, 1, figsize=(6, 6))
        ax.set_aspect('equal')
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.axis('off')
        fig.patch.set_facecolor("white")

        # ✅ Quadrat
        square = patches.Rectangle(
            (-1, -1), 2, 2,
            linewidth=6,
            edgecolor=fg_color,
            facecolor=bg_color
        )
        ax.add_patch(square)

        # NEU: gleiche Indexreihenfolge wie bei RoundClock
        # 0: oben, 1: oben-rechts, 2: rechts, 3: unten-rechts,
        # 4: unten, 5: unten-links, 6: links, 7: oben-links
        position_coords = [
            (0, 0.75),       # oben
            (0.75, 0.75),    # oben-rechts
            (0.75, 0),       # rechts
            (0.75, -0.75),   # unten-rechts
            (0, -0.75),      # unten
            (-0.75, -0.75),  # unten-links
            (-0.75, 0),      # links
            (-0.75, 0.75),   # oben-links
        ]

        tick_positions = [
            ((0, 0.85), (0, 1)),                # oben
            ((0.85, 0.85), (1.0, 1.0)),         # oben-rechts
            ((0.85, 0), (1.0, 0)),              # rechts
            ((0.85, -0.85), (1.0, -1.0)),       # unten-rechts
            ((0, -0.85), (0, -1.0)),            # unten
            ((-0.85, -0.85), (-1.0, -1.0)),     # unten-links
            ((-0.85, 0), (-1.0, 0)),            # links
            ((-0.78, 0.78), (-0.9, 0.9)),       # oben-links
        ]

        # ✅ Zahlen oder Ticks
        for i, num in enumerate(numbers):
            x, y = position_coords[i]

            if num in visible_numbers:
                ax.text(
                    x, y, str(num),
                    fontsize=35, fontweight='bold',
                    ha='center', va='center',
                    color=fg_color
                )
            else:
                start, end = tick_positions[i]
                ax.plot(
                    [start[0], end[0]],
                    [start[1], end[1]],
                    linewidth=6,
                    color=fg_color
                )

        # ✅ Zeiger – nutzt jetzt die gleiche Winkel-Logik wie RoundClock
        pointer_angle = self._get_pointer_angle(pointer_position)
        pointer_length = 0.4
        pointer_x = pointer_length * np.cos(pointer_angle)
        pointer_y = pointer_length * np.sin(pointer_angle)

        ax.plot([0, pointer_x], [0, pointer_y], linewidth=5, color=fg_color)
        ax.plot(0, 0, marker='o', markersize=15, color=fg_color)

        plt.tight_layout()
        plt.savefig(
            output_file,
            dpi=150,
            bbox_inches='tight',
            facecolor="white",
            edgecolor='none'
        )
        plt.close()



    def _get_pointer_angle(self, position):
        """
        Calculate the angle for the pointer based on position

        Position mapping (wie RoundClock):
        0=top, 1=top-right, 2=right, 3=bottom-right,
        4=bottom, 5=bottom-left, 6=left, 7=top-left
        """
        angles = [
            np.pi / 2,        # 0: oben
            np.pi / 4,        # 1: oben-rechts
            0,                # 2: rechts
            -np.pi / 4,       # 3: unten-rechts
            -np.pi / 2,       # 4: unten
            -3 * np.pi / 4,   # 5: unten-links
            np.pi,            # 6: links
            3 * np.pi / 4,    # 7: oben-links
        ]
        return angles[position]
"""
# Example usage
if __name__ == "__main__":
    clock = SquareClock()

    # Example 1: Clock starting at 8, showing only 8, 2, and 3
    print("Example 1: Starting at 8, showing numbers 8, 2, 3")
    clock.generate_clock(
        start_number=8,
        visible_numbers=[8, 2, 3],
        pointer_position=3,
        output_file='clock_example1.png',
        theme="dark"

    )

    # Example 2: Clock starting at 3
    print("\nExample 2: Starting at 3, showing numbers 3, 4, 5")
    clock.generate_clock(
        start_number=7,
        visible_numbers=[7, 8, 2],
        pointer_position=6,
        output_file='clock_example2.png',
        theme = "dark"
    )

    # Example 3: Clock starting at 1, showing all numbers
    print("\nExample 3: Starting at 1, showing all numbers")
    clock.generate_clock(
        start_number=1,
        visible_numbers=None,  # Show all numbers
        pointer_position=2,
        output_file='clock_example3.png',
        theme = "dark"
    )
    print("\nExample 4: Starting at 1, showing all numbers")
    clock.generate_clock(
        start_number=1,
        visible_numbers=[],  # Show all numbers
        pointer_position=2,
        output_file='clock_example4.png',
        theme="dark"
    )
"""