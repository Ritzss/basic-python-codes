import random
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

class SpacePartition:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rectangles = []
        self.subregions = [(0, 0, width, height)]  # initial available space
    
    def place_rectangle(self, rect_width, rect_height, rotate=False):
        # Check all available subregions for a fit
        for i, (x, y, w, h) in enumerate(self.subregions):
            # Check if rectangle fits (with rotation if needed)
            if rotate and rect_height <= w - 1 and rect_width <= h - 1:
                rect_width, rect_height = rect_height, rect_width
            if rect_width <= w - 1 and rect_height <= h - 1:
                self.rectangles.append((x, y, rect_width, rect_height))
                self.split_space(i, x, y, rect_width, rect_height)
                return True
        return False
    
    def split_space(self, index, x, y, rw, rh):
        # Remove the used space and split the remaining space into subregions
        _, _, w, h = self.subregions.pop(index)
        # Two new regions: remaining width and remaining height after placing the rectangle
        if w - rw - 1 > 0:
            self.subregions.append((x + rw + 1, y, w - rw - 1, h))
        if h - rh - 1 > 0:
            self.subregions.append((x, y + rh + 1, w, h - rh - 1))

    def plot_rectangles(self):
        fig, ax = plt.subplots()
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.set_aspect('equal')

        # Plot each rectangle
        for (x, y, w, h) in self.rectangles:
            rect = Rectangle((x, y), w, h, edgecolor='blue', facecolor='orange', linewidth=2)
            ax.add_patch(rect)
            ax.text(x + w / 2, y + h / 2, f'{w}x{h}', va='center', ha='center', color='black')

        plt.show()

def generate_random_rectangles(num_rectangles, max_width, max_height):
    return [(random.randint(5, max_width), random.randint(5, max_height)) for _ in range(num_rectangles)]

def main():
    # Create the initial space of 100x100 units
    space = SpacePartition(100, 100)

    # Generate 5 random rectangles with widths and heights between 5 and 30 units
    rectangles = generate_random_rectangles(5, 30, 30)

    # Try to place each rectangle in the space
    for i, (rw, rh) in enumerate(rectangles):
        if not space.place_rectangle(rw, rh, rotate=bool(random.getrandbits(1))):
            raise ValueError(f"Placement not possible for rectangle {i} ({rw}x{rh})")

    # Plot the result
    space.plot_rectangles()

if __name__ == '__main__':
    main()
