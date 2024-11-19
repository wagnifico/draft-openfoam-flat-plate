"""

Generating animation using pyvista

"""

import os
import shutil
import glob
import subprocess

# need to import vtk explicitly to use latex render
# https://github.com/pyvista/pyvista/discussions/2928
import vtk
import pyvista as pv
pv.start_xvfb()


run_folder = './runs/test'
output_folder = './runs/_tmp'

if os.path.exists(output_folder): shutil.rmtree(output_folder)
os.makedirs(output_folder)

filename = glob.glob(f'{run_folder}/*.OpenFOAM')[0]
reader = pv.POpenFOAMReader(filename)
reader.skip_zero_time = True # to avoid errors with replacement quantities
time = reader.time_values

plotter = pv.Plotter(
    border=False,
    notebook=False,
    off_screen=True,
    polygon_smoothing=True,
)
plotter.view_xy()
plotter.enable_parallel_projection()

plotter.add_text(
    r'$\mathrm{Re} = 200,~\alpha = 15~\mathrm{deg}$',
    font_size=16,font='times',
)

start_frame = 24
end_frame = 48

for i, t in enumerate(time[start_frame:end_frame]):
    print(f' - {i:05d}/{end_frame-start_frame:05d}')
    reader.set_active_time_value(t)
    mesh = reader.read()
    surface = mesh['boundary']['frontAndBack']

    # calculate the vorticity
    surface = surface.compute_derivative(
        scalars='U',gradient=False,vorticity=True)
    
    plotter.add_mesh(
        surface,
        show_edges=False,
        scalar_bar_args=dict(
            title=r'$\omega_z L / U_\mathrm{in} $',
            height=0.10,width=0.30,
            vertical=False,
            position_x=0.5-0.3/2,position_y=0.05,
            n_labels=3,
            italic=False,
            fmt='%.1f',
            title_font_size=32,label_font_size=32,
            font_family='times',
        ),
        show_scalar_bar=True,
        scalars='vorticity',component=2,
        cmap='bwr',n_colors=17,
        clim=[-100.,+100.],
        )
    if i == 0:
        plotter.camera.tight()
        plotter.camera.zoom(2.5)
    
    plotter.screenshot(
        f'{output_folder}/frame_t{i:04d}.png',
        transparent_background=True
        )

# generate gif with ffmpeg
framerate = 8
images_fmt = f'{output_folder}/frame_' + r't%04d.png'
gif_props = "[0]split[a][b]; [a]palettegen[palette]; [b][palette]paletteuse"
args=[
    'ffmpeg','-y','-hide_banner',
    '-framerate',str(framerate),
    '-filter_complex',gif_props,
    '-i',images_fmt,
    f'{run_folder}/animation.gif'
    ]
subprocess.run(args)

shutil.rmtree(output_folder)