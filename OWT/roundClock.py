import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


class RoundClock:
    def __init__(self, size=400):
        """
        Initialize the round clock generator.

        Parameters:
        size: aktuell nur fürs Verhältnis relevant, nicht für die Pixelzahl
        """
        self.size = size
        self.positions = 8  # 8 positions around the circle

    def generate_clock(self, start_number=1, visible_numbers=None,
                       pointer_position=2, output_file='round_clock.png',
                       theme="light"):
        """
        Generate a round clock image.

        theme:
        - "light" = weisser Kreis, alles schwarz
        - "dark"  = schwarzer Kreis, alles weiss
        """

        # ✅ Theme-Farben
        if theme == "dark":
            circle_bg = "black"
            fg_color = "white"
        else:
            circle_bg = "white"
            fg_color = "black"

        # Zahlenfolge erzeugen
        numbers = [(start_number + i - 1) % 8 + 1 for i in range(8)]

        # Sichtbare Zahlen
        if visible_numbers is None:
            visible_numbers = numbers[:]

        # Figur – gleiche Grundfläche wie bei SquareClock
        fig, ax = plt.subplots(1, 1, figsize=(6, 6))
        ax.set_aspect('equal')
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.axis('off')

        # ✅ Weisser Hintergrund ausserhalb des Kreises bleibt immer weiss
        fig.patch.set_facecolor("white")

        # ✅ Kreis (Zifferblatt)
        circle = patches.Circle(
            (0, 0), 1.0,
            linewidth=6,
            edgecolor=fg_color,
            facecolor=circle_bg
        )
        ax.add_patch(circle)

        # 8 Winkel (im Uhrzeigersinn, Start: oben)
        angles = [
            np.pi / 2,          # 0: oben
            np.pi / 4,          # 1: oben-rechts
            0.0,                # 2: rechts
            -np.pi / 4,         # 3: unten-rechts
            -np.pi / 2,         # 4: unten
            -3 * np.pi / 4,     # 5: unten-links
            np.pi,              # 6: links
            3 * np.pi / 4       # 7: oben-links
        ]

        # Radien für Text und Striche
        r_text = 0.7
        r_tick_inner = 0.9
        r_tick_outer = 1.02

        # ✅ Zahlen oder Striche setzen
        for i, num in enumerate(numbers):
            angle = angles[i]

            if num in visible_numbers:
                x = r_text * np.cos(angle)
                y = r_text * np.sin(angle)
                ax.text(
                    x, y, str(num),
                    fontsize=35, fontweight='bold',
                    ha='center', va='center',
                    color=fg_color
                )
            else:
                x1 = r_tick_inner * np.cos(angle)
                y1 = r_tick_inner * np.sin(angle)
                x2 = r_tick_outer * np.cos(angle)
                y2 = r_tick_outer * np.sin(angle)
                ax.plot(
                    [x1, x2], [y1, y2],
                    linewidth=4,
                    color=fg_color
                )

        # ✅ Zeiger
        pointer_angle = angles[pointer_position]
        pointer_length = 0.5
        px = pointer_length * np.cos(pointer_angle)
        py = pointer_length * np.sin(pointer_angle)

        ax.plot([0, px], [0, py], linewidth=6, color=fg_color)
        ax.plot(0, 0, marker='o', markersize=15, color=fg_color)

        plt.tight_layout()
        plt.savefig(
            output_file,
            dpi=150,
            bbox_inches='tight',
            facecolor="white",   # Aussen immer weiss
            edgecolor='none'
        )
        plt.close()


"""
if __name__ == "__main__":
    clock = RoundClock()
clock.generate_clock(
        start_number=1,
        visible_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
        pointer_position=2,
        output_file="round_dark.png",
        theme="dark"
    )
    """
