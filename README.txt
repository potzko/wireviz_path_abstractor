Wireviz Length Argument Abstraction Tool

This tool is designed to simplify the process of managing cable lengths in wireviz files by abstracting the length argument.
 Users can define connections, virtual points, and distances in a separate data file, which are then automatically integrated into wireviz files.

The file we will use has one of two options, but both share a main blueprint:
connections and virtual points are meant to represent a physical point in a braid, such as the connection to an aux chord or a point where you want to route your wires through.
Distances are the physical distances between two points.

For example, if I have a USB hub, I might say that I have the following connections:
  computer_usb, usb_hub_input, usb_hub_out_1, usb_hub_out_2, mouse, keyboard.
I like passing my cable behind my screen so I'd have a virtual point:
  screen.
The distances I can measure are as follows:
  computer_usb -> usb_hub_input = 20
  usb_hub_input -> usb_hub_out_1 = 0
  usb_hub_input -> usb_hub_out_2 = 0
  usb_hub_out_1 -> screen = 10
  usb_hub_out_2 -> screen = 10
  screen -> mouse = 20
  screen -> keyboard = 40

(Note: it is assumed that all connections are bidirectional.)

To represent this, you can choose one of two formats:
YML format:

connections:
  - computer_usb
  - usb_hub_input
  - usb_hub_out_1
  - usb_hub_out_2
  - mouse
  - keyboard
virtual_points:
  - screen
distances:
  - [computer_usb, usb_hub_input, 20]
  - [usb_hub_input, usb_hub_out_1, 0]
  - [usb_hub_input, usb_hub_out_2, 0]
  - [usb_hub_out_1, screen, 10]
  - [usb_hub_out_2, screen, 10]
  - [screen, mouse, 20]
  - [screen, keyboard, 40]


Any file ending in a format other than .yml will be assumed to be in the other format:
Connections {
  computer_usb, usb_hub_input, usb_hub_out_1, usb_hub_out_2
  mouse, keyboard
}
Virtual_points {
  screen
}
Distances {
  (computer_usb, usb_hub_input, 20), (usb_hub_input, usb_hub_out_1, 0), (usb_hub_input, usb_hub_out_2, 0), (usb_hub_out_1, screen, 10)
  (usb_hub_out_2, screen, 10), (screen, mouse, 20), (screen, keyboard, 40)
}

Now, let's take the wireviz first example:

connectors:
  X1:
    type: D-Sub
    subtype: female
    pinlabels: [DCD, RX, TX, DTR, GND, DSR, RTS, CTS, RI]
  X2:
    type: Molex KK 254
    subtype: female
    pinlabels: [GND, RX, TX]

cables:
  W1:
    gauge: 0.25 mm2
    length: 0.2
    #@length dist a d path v2 v1 dist h
    color_code: DIN
    wirecount: 3
    shield: true

connections:
  -
    - X1: [5,2,3]
    - W1: [1,2,3]
    - X2: [1,3,2]
  -
    - X1: 5
    - W1: s


In this case, I have to already know that the length of W1 is 0.2.
What if I don't know that yet? I'd like to state that the length of W1 is the length between X1 and X2 (to be determined).
So what I can do is define our data inside of our file:

Connections {
  X1, X2
}
Virtual_points {}
Connections {
  (X1, X2, 0.2)
}

And mark the path inside of the wireviz file:

...
Cables:
  W1:
    gauge: 0.25 mm2
    #@length X1 X2
    color_code: DIN
    wirecount: 3
    shield: true
...

Now, run main.py with the command line arguments <path to data file> <path to wireviz file> <path to output file>
and look at the generated file:

...
Cables:
  W1:
    gauge: 0.25 mm2
    length: 0.2 #path X1 -> X2
    color_code: DIN
    wirecount: 3
    shield: true
...

The tool took the data from the data file and transplanted it into the wireviz file.
Putting the correct length as well as marking the path as a comment


You can mark the mode you would like the tool to use from 3 options: path, dist, connection_count.

"Path" will follow the exact path provided. If a connection is missing, it will crash and display an error message about which connection is missing.
"Dist" will find the shortest path from A to B and will crash if a connection/virtual point B is not reachable from A.
"Connection_count" will find the path with the minimum amount of connections from A to B and will crash if a connection/virtual point B is not reachable from A.

To switch between modes, simply write down the mode you would like to use in your path. For example:
#@length dist X1 X2
or
#@length connection_count X1 X2

Would both work (although more useful in a more complex context).

When defining a path, you can also chain a path between points. For example:
Connections {
  A, B, D
}
Virtual_points {
  C
}
Connections {
  (A, C, 2), (B, C, 3), (D, C, 5)
}

If I wanted to mark a path from A to D,
#@length A D would crash as there is no connection (A, D, ...).
In that case I can do
#@length A C D
where the output file would have 
length: 7 #path A -> C -> D.

If I want, I can also let the tool work for me and find the best path by itself.
#@length dist A D
would return the same result
Another neat trick is that you can chain the paths as you like:
#@length dist A D B
would be the same as saying "find me the shortest path from A to D, and then add the shortest path from D to B"
and the tool will just continue to work as before:
length: 15 #path A -> C -> D -> C -> B

You can also change modes in the middle of the path:

#@length dist A D path C B
"shortest path from A to D, then add the length from connections (D, C) and then (C, B)"
length: 15 #path A -> C -> D -> C -> B