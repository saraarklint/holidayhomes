#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 09:19:46 2021

@author: sara
"""

import matplotlib.pyplot as plt
import seaborn as sns

def include_map(df, hue=None, style=None, size=None, alpha=None, s=35, palette=None, 
                title='Holiday homes in Rørvig', figsize=(16,16), Vaengerne=False):
    """
    For making a seaborn scatterplot of a Pandas DataFrame (incl. longitude/latitude)
    on a map of Rorvig (or a map of the area Vaengerne in Rorvig)
    Vaengerne = True to zoom for the area Vaengerne
    hue, style, size, alpha, s, palette, title: as for sns.scatterplot()
    """
    if Vaengerne:
        longmin = 11.7288
        longmax = 11.7489
        latmin = 55.9477
        latmax = 55.9607
        mapimage = plt.imread('mapVaengerne.png')
    else:
        longmin = 11.715354
        longmax = 11.790168
        latmin = 55.935818
        latmax = 55.97464
        mapimage = plt.imread('map4581.png')
    if ('latitude' not in df.columns) or ('longitude' not in df.columns):
        print('DataFrame misses latitude or longitude.')
    else:
        fig, ax = plt.subplots(figsize = figsize)
        ax = sns.scatterplot(x='longitude', y='latitude', data=df, hue=hue, style=style, size=None, alpha=alpha, s=s, palette=palette)
        ax.set_title(title)
        ax.set_xlim(longmin, longmax)
        ax.set_ylim(latmin, latmax)
        ax.imshow(mapimage, zorder=0, extent = [longmin, longmax, latmin, latmax]);