import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    print symbols
    for command in commands:
        print command
        args=command["args"]
        if command["op"] == 'push':
            stack.append( [x[:] for x in stack[-1]] )

        elif command["op"] == 'pop':
            stack.pop()

        elif command["op"] == 'sphere':
            #print 'SPHERE\t' + str(args)
            if "constants" in command and command["constants"] is not None:
                reflect=command["constants"]
            else:
                reflect=".white"
            add_sphere(coords,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step_3d)
            matrix_mult(stack[-1], coords)
            draw_polygons(coords, screen, zbuffer, view, ambient, light,symbols,reflect)
            coords = []

        elif command["op"] == 'torus':
            #print 'TORUS\t' + str(args)
            if "constants" in command and command["constants"] is not None:
                reflect=command["constants"]
            else:
                reflect=".white"
            print(coords)
            add_torus(coords,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), step_3d)
            matrix_mult(stack[-1], coords)
            draw_polygons(coords, screen, zbuffer, view, ambient, light, symbols,reflect)
            coords = []

        elif command["op"] == 'box':
            #print 'BOX\t' + str(args)
            if "constants" in command and command["constants"] is not None:
                reflect=command["constants"]
            else:
                reflect=".white"
            add_box(coords,
                    float(args[0]), float(args[1]), float(args[2]),
                    float(args[3]), float(args[4]), float(args[5]))
            matrix_mult(stack[-1], coords)
            draw_polygons(coords, screen, zbuffer, view, ambient, light, symbols,reflect)
            coords = []

            '''
            elif command["op"] == 'circle':
                #print 'CIRCLE\t' + str(args)
                add_circle(edges,
                           float(args[0]), float(args[1]), float(args[2]),
                           float(args[3]), step)
                matrix_mult(stack[-1], edges)
                draw_lines(edges, screen, zbuffer, color)
                edges = []

            elif command["op"] == 'hermite' or command["op"] == 'bezier':
                #print 'curve\t' + command["op"] + ": " + str(args)
                add_curve(edges,
                          float(args[0]), float(args[1]),
                          float(args[2]), float(args[3]),
                          float(args[4]), float(args[5]),
                          float(args[6]), float(args[7]),
                          step, command["op"])
                matrix_mult(stack[-1], edges)
                draw_lines(edges, screen, zbuffer, color)
                edges = []
            '''

        elif command["op"] == 'line':
            #print 'LINE\t' + str(args)
            add_edge( edges,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), float(args[5]) )
            matrix_mult(stack[-1], edges)
            draw_lines(edges, screen, zbuffer, color)
            edges = []

        elif command["op"] == 'scale':
            #print 'SCALE\t' + str(args)
            t = make_scale(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult(stack[-1], t)
            stack[-1] = [x[:] for x in t]


        elif command["op"] == 'move':
            #print 'MOVE\t' + str(args)
            t = make_translate(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult(stack[-1], t)
            stack[-1] = [x[:] for x in t]


        elif command["op"] == 'rotate':
            #print 'ROTATE\t' + str(args)
            theta = float(args[1]) * (math.pi / 180)

            if args[0] == 'x':
                t = make_rotX(theta)
            elif args[0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult(stack[-1], t)
            stack[-1] = [x[:] for x in t]

            '''
            elif command["op"] == 'ident':
                ident(transform)

            elif command["op"] == 'apply':
                matrix_mult( transform, edges )
                matrix_mult( transform, polygons )

            elif command["op"] == 'clear':
                clear_screen(screen)
                clear_zbuffer(zbuffer)
            '''
        elif command["op"] == 'display' or command["op"] == 'save':
            #clear_screen(screen)
            if command["op"] == 'display':
                display(screen)
            else:
                save_extension(screen, args[0])
