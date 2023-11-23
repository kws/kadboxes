import cadquery as cq

def mounting_box(l, w, h, wall_thickness=1, frac=2):
    """
    Creates a mounting "box"    
    """
    wall_thickness *= 2
    oshell = (
        cq.Workplane("XY")
        .workplane(offset=h/2)
        .box(l+wall_thickness, w+wall_thickness, h)
    )
    ishell = (
        cq.Workplane("XY")
        .workplane(offset=h/2)
        .box(l, w, h)
    )
    box = oshell.cut(ishell)

    if frac > 0:
        box = box.faces("<Y").workplane(centerOption="CenterOfMass").rect(l/frac, h).cutThruAll()
        box = box.faces("<X").workplane(centerOption="CenterOfMass").rect(w/frac, h).cutThruAll()
    
    return box

def pin_stands(l, w, outer, inner, base_height=2, pin_height=2):
    thick_pins = (
        cq.Workplane("XY")
        .rect(l, w, forConstruction=True)
        .vertices()
        .circle(outer)
        .extrude(base_height)
        .faces(">Z")
        .workplane()
        .rect(l, w, forConstruction=True)
        .vertices()
        .circle(inner)
        .extrude(pin_height)      
    )
    
    return thick_pins
    
    
def transistor_holder(diameter, height=2, padding=1):
    radius = diameter / 2
    holder = (
        cq.Workplane("XY")
        .circle(radius + padding)
        .extrude(height)
        .faces("<Z")
        .circle(radius)
        .cutThruAll()
        
    )
    return holder


def snap_join(l, w, radius=0.5):
    snap_join = (
        cq.Workplane("top")
        .circle(radius)
        .extrude(w)
        .copyWorkplane(
            cq.Workplane("left", origin=(0, 0, 0))
        )
        .circle(radius)
        .extrude(l)
        .copyWorkplane(
            cq.Workplane("left", origin=(0, w, 0))
        )
        .circle(radius)
        .extrude(l)
        .copyWorkplane(
            cq.Workplane("top", origin=(-l, 0, 0))
        )
        .circle(radius)
        .extrude(w)
    )
    return snap_join
        

def container(base_length, base_width, height, wall_thickness=1, with_snap=True):
    height = height + wall_thickness
    sides = wall_thickness * 2
    oshell = (
        cq.Workplane("XY")
        .workplane(height/2 - wall_thickness)
        .box(base_length+sides, base_width+sides, height)
        .edges("|Z").fillet(2)
    )

    ishell = (
        oshell.faces("<Z")
        .workplane(invert=True, offset=wall_thickness)
        .rect(base_length, base_width)
        .extrude(height, False)
    )
    
    container = oshell.cut(ishell)
        
    if with_snap:
        snap_pos = height - wall_thickness -2
        grove = (
            snap_join(base_length, base_width)
            .translate((base_length/2, -base_width/2, snap_pos))
        )
        container = container.cut(grove)
    
    

    return container

def lid(base_length, base_width, height, wall_thickness=2, with_snap=True):
    ct = (
        cq.Workplane("XY")
        .workplane(height/2 - height)
        .box(base_length+wall_thickness*2, base_width+wall_thickness*2, height)
        .edges("|Z").fillet(2)
    )
    fuzz = 0.75
    
    ct = (
        ct.faces(">Z")
        .rect(base_length-fuzz, base_width-fuzz)
        .extrude(3)
    )
    
    ct = (
        ct.faces(">Z")
        .rect(base_length-fuzz-wall_thickness, base_width-fuzz-wall_thickness)
        .cutBlind(-height-1)
    )
    
    if with_snap:
        snap_pos = 2
        grove = (
            snap_join(base_length-fuzz, base_width-fuzz)
            .translate(((base_length-fuzz)/2, -(base_width-fuzz)/2, snap_pos))
        )
        
        cut_out = (
            cq.Workplane("XY")
            .rect(base_length, base_width)
            .vertices()
            .box(base_length/2, base_width/2, 2)
            .translate((0, 0, snap_pos))
        )
        grove = grove.cut(cut_out)
        
        ct = ct.union(grove)

    ct = ct.rotate((0, 0, 0), (1, 0, 0), 180) #Flip 180 degrees
    return ct


def add_button_holder(box, x, y):
    # Fixed size 7x7mm with 3.8mm hole
    dim = 7
    dia = 3.8
    height = 5
    
    holder = mounting_box(dim, dim, height, frac=10)
    
    box = box.faces(">Z").center(x, y).hole(dia).center(-x, -y)
    box = box.union(holder.translate((x, y, 0)))
    
    return box

def add_lrd_holder(box, x, y):
    # Fixed size 5.25mm holder with 4mm hole
    holder = 5.25
    dia = 4
    
    holder = transistor_holder(holder, height=4)
    
    box = box.faces(">Z").center(x, y).hole(dia).center(-x, -y)
    box = box.union(holder.translate((x, y, 0)))
    
    return box
