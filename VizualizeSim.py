BigBadWolf
==========
#Visualize

import math
import time

from Tkinter import *

class FoodVisualization:
    def __init__(self, num_pred, num_prey, width, height, delay = 1):
        "Initializes a visualization with the specified parameters."
        # Number of seconds to pause after each frame
        self.delay = delay

        self.max_dim = max(width, height)
        self.width = width
        self.height = height
        self.num_pred = num_pred
        self.num_prey = num_prey

        # Initialize a drawing surface
        self.master = Tk()
        self.w = Canvas(self.master, width=500, height=500)
        self.w.pack()
        self.master.update()

        # Draw a backing and lines
        x1, y1 = self._map_coords(0, 0)
        x2, y2 = self._map_coords(width, height)
        self.w.create_rectangle(x1, y1, x2, y2, fill = "white")

        # Draw gray squares for dirty tiles
        self.tiles = {}
        for i in range(width):
            for j in range(height):
                x1, y1 = self._map_coords(i, j)
                x2, y2 = self._map_coords(i + 1, j + 1)
                self.tiles[(i, j)] = self.w.create_rectangle(x1, y1, x2, y2,
                                                             fill = "gray")

        # Draw gridlines
        for i in range(width + 1):
            x1, y1 = self._map_coords(i, 0)
            x2, y2 = self._map_coords(i, height)
            self.w.create_line(x1, y1, x2, y2)
        for i in range(height + 1):
            x1, y1 = self._map_coords(0, i)
            x2, y2 = self._map_coords(width, i)
            self.w.create_line(x1, y1, x2, y2)

        # Draw some status text
        self.preds = None
        self.preys = None
        self.text = self.w.create_text(25, 0, anchor=NW,
                                       text=self._status_string(0, 0, 0))
        self.time = 0
        self.master.update()

    def _status_string(self, time, num_pred, num_prey):
        "Returns an appropriate status string to print."
        return "Time: %04d; %d Predators %d Preys" % \
            (time, num_pred, num_prey)

    def _map_coords(self, x, y):
        "Maps grid positions to window positions (in pixels)."
        return (250 + 450 * ((x - self.width / 2.0) / self.max_dim),
                250 + 450 * ((self.height / 2.0 - y) / self.max_dim))

    def _draw_animal(self, position, animalType):
        "Returns a circle representing an animal."
        x, y = position.getX(), position.getY()
        x0, y0 = self._map_coords(x - 0.1 , y - 0.1)
        x1, y1 = self._map_coords(x + 0.1, y + 0.1 )
        if animalType == 'Predator':
            return self.w.create_oval([x0, y0, x1, y1], fill="red")
        else:
            return self.w.create_oval([x0, y0, x1, y1], fill="blue")


    def update(self, predList, preyList):
        "Redraws the visualization"
##        for i in range(self.width):
##            for j in range(self.height):
##                if room.isTileCleaned(i, j):
##                    self.w.delete(self.tiles[(i, j)])
        # Delete all existing animals.
        if self.preds:
            for pred in self.preds:
                self.w.delete(pred)
                self.master.update_idletasks()
        if self.preys:
            for prey in self.preys:
                self.w.delete(prey)
                self.master.update_idletasks()
        # Draw new animals
        self.preds = []
        for pred in predList:
            pos = pred.getAnimalPosition()
            x, y = pos.getX(), pos.getY()
            x1, y1 = self._map_coords(x - 0.08, y - 0.08)
            x2, y2 = self._map_coords(x + 0.08, y + 0.08)
            self.preds.append(self.w.create_oval(x1, y1, x2, y2,
                                                  fill = "black"))
            self.preds.append(self._draw_animal(pred.getAnimalPosition(), 'Predator'))
        self.preys = []
        for prey in preyList:
            pos = prey.getAnimalPosition()
            x, y = pos.getX(), pos.getY()
            x1, y1 = self._map_coords(x - 0.08, y - 0.08)
            x2, y2 = self._map_coords(x + 0.08, y + 0.08)
            self.preys.append(self.w.create_oval(x1, y1, x2, y2,
                                                  fill = "black"))
            self.preys.append(self._draw_animal(prey.getAnimalPosition(), 'Prey'))

        # Update text
        self.w.delete(self.text)
        self.time += 1
        self.text = self.w.create_text(
            25, 0, anchor=NW,
            text=self._status_string(self.time, len(predList), len(preyList)))
        self.master.update()
        time.sleep(self.delay)

    def done(self):
        "Indicate that the animation is done so that we allow the user to close the window."
        mainloop()

