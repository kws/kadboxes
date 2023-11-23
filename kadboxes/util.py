import jupyter_cadquery
import jupyter_cadquery.replay


def enable_viewer(tab_name="KADBoxes"):
    jupyter_cadquery.set_defaults(axes=True, timeit=False)
    jupyter_cadquery.open_viewer(tab_name, cad_width=640, height=480, glass=True)
    jupyter_cadquery.replay.enable_replay(False, False)
    jupyter_cadquery.replay.replay