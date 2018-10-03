#!/usr/bin/env python

# Copyright (c) 2018, University of Stuttgart
# All rights reserved.
#
# Permission to use, copy, modify, and distribute this software for any purpose
# with or without   fee is hereby granted, provided   that the above  copyright
# notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS  SOFTWARE INCLUDING ALL  IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR  BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR  ANY DAMAGES WHATSOEVER RESULTING  FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION,   ARISING OUT OF OR IN    CONNECTION WITH THE USE   OR
# PERFORMANCE OF THIS SOFTWARE.
#
#                                        Jim Mainprice on Sunday June 13 2018

import demos_common_imports
import time
import numpy as np
from numpy.testing import assert_allclose
from itertools import izip

from pyrieef.geometry.workspace import EnvBox
from pyrieef.geometry.pixel_map import *
import pyrieef.rendering.workspace_renderer as render
import pyrieef.learning.demonstrations as demos
from pyrieef.learning.dataset import *

dataset = load_workspace_dataset('1k_small.hdf5')
rows = 1  # 3
cols = 1  # 4
t_sleep = 0.4
for workspaces in izip(*[iter(dataset)] * (rows * cols)):
    viewer = render.WorkspaceHeightmap(
        workspaces[0].workspace)
    for k, ws in enumerate(workspaces):
        # viewer.set_drawing_axis(k)
        viewer.set_workspace(ws.workspace)
        print ws.costmap.shape
        # viewer.draw_ws_background(
        #     RegressedPixelGridSpline(
        #         ws.costmap,
        #         ws.workspace.box.dim[0] / ws.costmap.shape[0],
        #         ws.workspace.box.extent()))
        viewer.draw_ws_background(demos.obsatcle_potential(ws.workspace))
        viewer.draw_ws_obstacles()
        if ws.demonstrations:
            for trajectory in ws.demonstrations:
                configurations = trajectory.list_configurations()
                viewer.draw_ws_line(configurations, color="r")
                viewer.draw_ws_point(configurations[0], color="k")

    viewer.show_once()
    time.sleep(t_sleep)
