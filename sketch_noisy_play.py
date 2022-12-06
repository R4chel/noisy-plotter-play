import vsketch
import vpype as vp
import numpy as np
import math
from shapely.geometry import Point, LineString, Polygon


class NoisyPlaySketch(vsketch.SketchClass):
    # Sketch parameters:
    y_delta= vsketch.Param(10)
    max_delta = vsketch.Param(0.1)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a6", landscape=False, center=False)
        scale = "px"
        vsk.scale(scale)
        factor = 1 / vp.convert_length(scale)
        width, height = factor * vsk.width, factor * vsk.height

        xs = range(0,round(width), math.ceil(width/1000))
        ys = [0 for _ in range(len(xs))]
        z = 0
        for y_offset in range(0, math.ceil(height), self.y_delta):
            pts = LineString([(xs[i],ys[i]) for i in range(len(xs))])
            vsk.geometry(pts)
            zs = [z for i in range(len(xs))]
            z += 1
            noise = vsk.noise(xs,ys,zs,grid_mode=False)
            ys = [ys[i] + vsk.map(noise[i],0,1,-self.max_delta, self.max_delta) +self.y_delta for i in range(len(ys))]

        # implement your sketch here
        # vsk.circle(0, 0, self.radius, mode="radius")

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":      # 
    NoisyPlaySketch.display()
