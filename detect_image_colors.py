#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from collections import Counter
from collections import namedtuple
from operator import itemgetter, mul, attrgetter
import colorsys
import webcolors
from PIL import Image as Im
from PIL import ImageChops
from colormath.color_objects import LabColor
from colormath.color_diff import delta_e_cie1976
import json
import random
from math import sqrt

Color = namedtuple('Color', ['value', 'prominence'])
Palette = namedtuple('Palette', 'colors bgcolor')
Point = namedtuple('Point', ('coords', 'n', 'ct'))
Cluster = namedtuple('Cluster', ('points', 'center', 'n'))

def closest_color(requested_color):
  min_colors = {}
  for (key, name) in webcolors.css3_hex_to_names.items():
    (r_c, g_c, b_c) = webcolors.hex_to_rgb(key)
    rd = (r_c - requested_color[0]) ** 2
    gd = (g_c - requested_color[1]) ** 2
    bd = (b_c - requested_color[2]) ** 2
    min_colors[rd + gd + bd] = name
  return min_colors[min(min_colors.keys())]

def distance(c1, c2):
  return delta_e_cie1976(LabColor(*c1), LabColor(*c2))

def rgb_to_hex(color):
  return '#%.02x%.02x%.02x' % color

def hex_to_rgb(color):
  return (int(color[1:3], 16), int(color[3:5], 16), int(color[5:7],
      16))

def norm_color(c):
  (r, g, b) = c
  return (r / 255.0, g / 255.0, b / 255.0)


def detect_background(im, colors, to_canonical):
  BACKGROUND_PROMINENCE = 0.4
  if colors[0].prominence >= BACKGROUND_PROMINENCE:
    return (colors[1:], colors[0])

  (w, h) = im.size
  points = [
    (0, 0),
    (0, h / 2),
    (0, h - 1),
    (w / 2, h - 1),
    (w - 1, h - 1),
    (w - 1, h / 2),
    (w - 1, 0),
    (w / 2, 0),
    ]
  edge_dist = Counter(im.getpixel(p) for p in points)

  ((majority_col, majority_count), ) = edge_dist.most_common(1)
  if majority_count >= 3:
    canonical_bg = to_canonical[majority_col]
    (bg_color, ) = [c for c in colors if c.value == canonical_bg]
    colors = [c for c in colors if c.value != canonical_bg]
  else:
    bg_color = None

  return (colors, bg_color)

def meets_min_saturation(c, threshold):
  return colorsys.rgb_to_hsv(*norm_color(c.value))[1] > threshold

def autocrop(im, bgcolor):
  if im.mode != 'RGB':
    im = im.convert('RGB')
  bg = Im.new('RGB', im.size, bgcolor)
  diff = ImageChops.difference(im, bg)
  bbox = diff.getbbox()
  if bbox:
    return im.crop(bbox)
  return im

rtoh = lambda rgb: '#%s' % ''.join('%02x' % p for p in rgb)

def extract_colors(filename, n):
  WHITE = (255, 255, 255)
  BLACK = (0, 0, 0)

  N_QUANTIZED = 100  # start with an adaptive palette of this size
  MIN_DISTANCE = 10.0  # min distance to consider two colors different
  MIN_PROMINENCE = 0.01  # ignore if less than this proportion of image
  MIN_SATURATION = 0.05  # ignore if not saturated enough
  BACKGROUND_PROMINENCE = 0.5  # level of prominence indicating a bg color
  MAX_COLORS = n

  im = Im.open(filename)

  if im.mode != 'RGB':
    im = im.convert('RGB')
  im = autocrop(im, WHITE)
  im = im.convert('P', palette=Im.ADAPTIVE,
          colors=N_QUANTIZED).convert('RGB')
  data = im.getdata()
  dist = Counter(data)
  n_pixels = mul(*im.size)

  to_canonical = {WHITE: WHITE, BLACK: BLACK}
  aggregated = Counter({WHITE: 0, BLACK: 0})
  sorted_cols = sorted(dist.iteritems(), key=itemgetter(1),
             reverse=True)
  for (c, n) in sorted_cols:
    if c in aggregated:
      aggregated[c] += n
    else:
      (d, nearest) = min((distance(c, alt), alt) for alt in
                 aggregated)
      if d < MIN_DISTANCE:
        aggregated[nearest] += n
        to_canonical[c] = nearest
      else:
        aggregated[c] = n
        to_canonical[c] = c

  colors = sorted((Color(c, n / float(n_pixels)) for (c, n) in
          aggregated.iteritems()), key=attrgetter('prominence'
          ), reverse=True)

  (colors, bg_color) = detect_background(im, colors, to_canonical)

  sat_colors = [c for c in colors if meets_min_saturation(c,
          MIN_SATURATION)]
  if bg_color and not meets_min_saturation(bg_color, MIN_SATURATION):
    bg_color = None
  if sat_colors:
    colors = sat_colors
  else:
    colors = colors[:1]

  colors = [c for c in colors if c.prominence >= colors[0].prominence
        * MIN_PROMINENCE][:MAX_COLORS]

  final_colors_hex = []
  for color in colors:
    final_colors_hex.append(rgb_to_hex(color[0]))

  return json.dumps(final_colors_hex, indent=4)

def palette(filename, n):
  return extract_colors(filename, n)

if __name__ == "__main__":
  print palette(filename=sys.argv[1], n=3)

