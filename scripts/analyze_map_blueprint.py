from PIL import Image, ImageDraw, ImageFont

map_path = '/root/the_echo_of_shadows/new assets/map du village.png'
out_path = '/root/the_echo_of_shadows/web_preview/map_annotated.png'

im = Image.open(map_path).convert('RGB')
draw = ImageDraw.Draw(im)

# Key locations identified on the 1536x1024 canvas
features = [
    # River & Bridge
    ("FROZEN_RIVER", (100, 700, 1450, 1000), (0, 150, 255)),
    ("WATERMILL", (120, 570, 320, 750), (255, 200, 0)),
    ("MAIN_BRIDGE", (670, 620, 780, 770), (255, 100, 0)),
    ("LEFT_DOCK", (380, 730, 600, 860), (200, 150, 100)),
    ("RIGHT_DOCK", (780, 800, 980, 940), (200, 150, 100)),
    ("RIVERSIDE_COTTAGE", (1100, 620, 1240, 740), (255, 255, 0)),

    # Center Plaza
    ("CENTRAL_PLAZA", (680, 330, 880, 480), (0, 255, 255)),
    ("STATUE_MONUMENT", (750, 360, 800, 440), (255, 0, 255)),
    ("ANCIENT_WELL", (800, 480, 860, 550), (0, 255, 100)),
    ("PLAZA_SHRINE", (650, 320, 710, 380), (200, 200, 0)),

    # Church & Cemetery
    ("CHURCH_ST_JUDE", (990, 80, 1200, 340), (255, 50, 50)),
    ("CEMETERY", (810, 210, 980, 380), (180, 100, 220)),
    ("CEMETERY_STEPS", (930, 340, 980, 390), (255, 255, 255)),

    # Marketplace & Sawmill
    ("MARKETPLACE", (910, 410, 1100, 540), (255, 120, 180)),
    ("SAWMILL_LUMBER", (1260, 410, 1440, 560), (220, 160, 80)),
    ("EAST_COTTAGES", (1060, 400, 1240, 520), (255, 220, 100)),

    # Residential & Farm
    ("COTTAGE_SOUTH", (580, 440, 710, 570), (255, 220, 50)),
    ("COTTAGE_WEST", (480, 320, 610, 440), (255, 220, 50)),
    ("COTTAGE_NORTH", (600, 180, 760, 320), (255, 220, 50)),
    ("COTTAGE_FAR_WEST", (280, 420, 440, 540), (255, 220, 50)),
    ("FARM_FIELD", (250, 220, 480, 370), (100, 255, 100)),
    ("WINDMILL", (90, 240, 210, 410), (255, 180, 0)),
    ("MINE_ENTRANCE", (160, 80, 260, 170), (180, 180, 180)),
    ("NORTH_CLIFFS", (0, 0, 1536, 150), (100, 100, 150)),
]

for name, box, col in features:
    draw.rectangle(box, outline=col, width=3)
    draw.text((box[0] + 5, box[1] + 5), name, fill=col)

im.save(out_path)
print(f'Annotated blueprint saved: {out_path}')
