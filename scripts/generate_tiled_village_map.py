import os
import json
import math
import subprocess

ROOT_DIR = "/root/the_echo_of_shadows"
ASSETS_DIR = os.path.join(ROOT_DIR, "new assets")
MAPS_DIR = os.path.join(ASSETS_DIR, "data", "maps")
os.makedirs(MAPS_DIR, exist_ok=True)

TSX_FILE = os.path.join(MAPS_DIR, "village_tileset.tsx")
TMX_FILE = os.path.join(MAPS_DIR, "village_map.tmx")
TMJ_FILE = os.path.join(MAPS_DIR, "village_map.tmj")

MAP_W = 32
MAP_H = 32
TILE_W = 128
TILE_H = 64
OFFSET_X = 16
OFFSET_Y = 16

# 1. Tile definitions
# ID 0..17: Ground tiles
# ID 18..27: Buildings
# ID 28..37: Props
# ID 38..39: Nature
tiles_data = [
    # (id, name, rel_path, width, height, type)
    (0, "snow_a", "NATURE GAMEPLAY STRUCTURES/NATURE-GAMEPLAY-STRUCTURES54.png", 105, 69, "ground"),
    (1, "snow_b", "NATURE GAMEPLAY STRUCTURES/NATURE-GAMEPLAY-STRUCTURES61.png", 103, 70, "ground"),
    (2, "snow_c", "NATURE GAMEPLAY STRUCTURES/NATURE-GAMEPLAY-STRUCTURES187.png", 93, 81, "ground"),
    (3, "road_a", "NATURE GAMEPLAY STRUCTURES/NATURE-GAMEPLAY-STRUCTURES55.png", 106, 70, "ground"),
    (4, "road_b", "NATURE GAMEPLAY STRUCTURES/NATURE-GAMEPLAY-STRUCTURES69.png", 105, 66, "ground"),
    (5, "plaza_a", "NATURE GAMEPLAY STRUCTURES/NATURE-GAMEPLAY-STRUCTURES57.png", 103, 70, "ground"),
    (6, "plaza_b", "NATURE GAMEPLAY STRUCTURES/NATURE-GAMEPLAY-STRUCTURES2181.png", 94, 87, "ground"),
    (7, "path_a", "NATURE GAMEPLAY STRUCTURES/NATURE-GAMEPLAY-STRUCTURES58.png", 99, 67, "ground"),
    (8, "path_b", "NATURE GAMEPLAY STRUCTURES/NATURE-GAMEPLAY-STRUCTURES60.png", 105, 70, "ground"),
    (9, "bridge_planks", "NATURE GAMEPLAY STRUCTURES/NATURE-GAMEPLAY-STRUCTURES68.png", 110, 77, "ground"),
    (10, "dock_planks", "NATURE GAMEPLAY STRUCTURES/NATURE-GAMEPLAY-STRUCTURES100.png", 108, 70, "ground"),
    (11, "ice_a", "NATURE GAMEPLAY STRUCTURES/NATURE-GAMEPLAY-STRUCTURES62.png", 103, 73, "ground"),
    (12, "ice_b", "NATURE GAMEPLAY STRUCTURES/NATURE-GAMEPLAY-STRUCTURES67.png", 101, 72, "ground"),
    (13, "water_a", "NATURE GAMEPLAY STRUCTURES/NATURE-GAMEPLAY-STRUCTURES65.png", 102, 73, "ground"),
    (14, "water_b", "NATURE GAMEPLAY STRUCTURES/NATURE-GAMEPLAY-STRUCTURES66.png", 99, 71, "ground"),
    (15, "shore_a", "NATURE GAMEPLAY STRUCTURES/NATURE-GAMEPLAY-STRUCTURES56.png", 102, 70, "ground"),
    (16, "shore_b", "NATURE GAMEPLAY STRUCTURES/NATURE-GAMEPLAY-STRUCTURES63.png", 103, 71, "ground"),
    (17, "cliff", "NATURE GAMEPLAY STRUCTURES/NATURE-GAMEPLAY-STRUCTURES09.png", 80, 141, "cliff"),

    # Buildings (IDs 18 to 27, GIDs 19 to 28)
    (18, "church", "VILLAGE ENVIRONMENT/VILLAGE-ENVIRONMENT-104.png", 265, 319, "building"),
    (19, "family_house", "MAISON FAMILLIALE/MAISON-FAMILLIALE02.png", 359, 337, "building"),
    (20, "watermill", "VILLAGE ENVIRONMENT/VILLAGE-ENVIRONMENT-103.png", 348, 298, "building"),
    (21, "windmill", "VILLAGE ENVIRONMENT/VILLAGE-ENVIRONMENT-102.png", 289, 299, "building"),
    (22, "cottage_west", "VILLAGE ENVIRONMENT/VILLAGE-ENVIRONMENT-101.png", 275, 289, "building"),
    (23, "cottage_south", "VILLAGE ENVIRONMENT/VILLAGE-ENVIRONMENT-106.png", 160, 184, "building"),
    (24, "east_workshop", "VILLAGE ENVIRONMENT/VILLAGE-ENVIRONMENT-105.png", 345, 304, "building"),
    (25, "sawmill", "VILLAGE ENVIRONMENT/VILLAGE-ENVIRONMENT-105.png", 345, 304, "building"),
    (26, "bunker_ext", "INTERIORS BUNKER/INTERIORS-BUNKER02.png", 351, 224, "building"),
    (27, "bridge_arch", "VILLAGE ENVIRONMENT/VILLAGE-ENVIRONMENT-108.png", 208, 149, "building"),

    # Props (IDs 28 to 37, GIDs 29 to 38)
    (28, "statue", "VILLAGE ENVIRONMENT/VILLAGE-ENVIRONMENT-106.png", 160, 184, "prop"),
    (29, "well", "VILLAGE ENVIRONMENT/VILLAGE-ENVIRONMENT-111.png", 227, 186, "prop"),
    (30, "market_stall_01", "VILLAGE ENVIRONMENT/VILLAGE-ENVIRONMENT-116.png", 209, 179, "prop"),
    (31, "market_stall_02", "VILLAGE ENVIRONMENT/VILLAGE-ENVIRONMENT-121.png", 268, 181, "prop"),
    (32, "sawmill_crane", "VILLAGE ENVIRONMENT/VILLAGE-ENVIRONMENT-129.png", 329, 197, "prop"),
    (33, "stacked_logs", "VILLAGE ENVIRONMENT/VILLAGE-ENVIRONMENT-142.png", 125, 196, "prop"),
    (34, "iron_gate", "VILLAGE ENVIRONMENT/VILLAGE-ENVIRONMENT-113.png", 88, 136, "prop"),
    (35, "boat", "VILLAGE ENVIRONMENT/VILLAGE-ENVIRONMENT-152.png", 179, 109, "prop"),
    (36, "dock_crane", "VILLAGE ENVIRONMENT/VILLAGE-ENVIRONMENT-137.png", 338, 252, "prop"),
    (37, "lamp_post", "VILLAGE ENVIRONMENT/VILLAGE-ENVIRONMENT-110.png", 89, 113, "prop"),

    # Nature (IDs 38 to 39, GIDs 40 to 41)
    (38, "pine_tree", "NATURE GAMEPLAY STRUCTURES/NATURE-GAMEPLAY-STRUCTURES02.png", 106, 180, "nature"),
    (39, "dead_tree", "NATURE GAMEPLAY STRUCTURES/NATURE-GAMEPLAY-STRUCTURES06.png", 96, 176, "nature")
]

# Generate village_tileset.tsx
tsx_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    f'<tileset version="1.10" tiledversion="1.11.0" name="village_tileset" tilewidth="359" tileheight="337" tilecount="{len(tiles_data)}" columns="0">',
    ' <grid orientation="isometric" width="128" height="64"/>'
]
for tid, tname, rel_p, w, h, ttype in tiles_data:
    source_p = f"../../{rel_p}"
    tsx_lines.append(f' <tile id="{tid}">')
    tsx_lines.append(f'  <properties>')
    tsx_lines.append(f'   <property name="name" value="{tname}"/>')
    tsx_lines.append(f'   <property name="type" value="{ttype}"/>')
    tsx_lines.append(f'  </properties>')
    tsx_lines.append(f'  <image width="{w}" height="{h}" source="{source_p}"/>')
    tsx_lines.append(f' </tile>')
tsx_lines.append('</tileset>')

with open(TSX_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(tsx_lines))
print(f"Generated TSX: {TSX_FILE}")

# 2. Generate Ground Terrain Tile Grid (32x32)
def compute_tile_gid(gx, gy):
    hVal = abs((gx * 73856093) ^ (gy * 19349663)) % 100
    sumXy = gx + gy
    diffXy = abs(gx - gy)

    # Bridge
    if diffXy <= 1 and sumXy >= 8 and sumXy <= 15:
        return 10  # bridge_planks (id 9 -> GID 10)
    
    # Docks
    dLeft = math.hypot(gx - 2.0, gy - 8.0)
    dRight = math.hypot(gx - 6.0, gy - 6.0)
    if dLeft <= 1.5 or dRight <= 1.5:
        return 11  # dock_planks (id 10 -> GID 11)

    # Water & Ice
    if sumXy >= 12:
        return 14 if hVal < 65 else 15  # water_a (14) or water_b (15)
    if sumXy >= 10:
        return 12 if hVal < 70 else 13  # ice_a (12) or ice_b (13)
    if sumXy == 9:
        return 16 if hVal < 60 else 17  # shore_a (16) or shore_b (17)

    # Plaza
    distCenter = math.hypot(gx, gy)
    if distCenter <= 2.8:
        return 6 if hVal < 70 else 7   # plaza_a (6) or plaza_b (7)

    # Main Avenue
    if diffXy <= 1 and sumXy >= 2 and sumXy <= 8:
        return 4 if hVal < 75 else 5   # road_a (4) or road_b (5)

    # Church Hill Road
    if gx >= 0 and gx <= 5 and gy <= 0 and gy >= -8:
        lineDist = abs(gy - (-1.6 * gx)) / math.sqrt(1 + 1.6 * 1.6)
        if lineDist <= 1.2:
            return 4 if hVal < 75 else 5

    # Marketplace & Sawmill
    if gx >= 0 and gx <= 9 and gy >= -2 and gy <= 2 and abs(gy) <= 1.2:
        return 8 if hVal < 65 else 9   # path_a (8) or path_b (9)

    # West Residential Trail
    if gx <= 0 and gx >= -8 and gy >= -4 and gy <= 2:
        lineDist = abs(gy - (-0.4 * gx)) / math.sqrt(1 + 0.16)
        if lineDist <= 1.2:
            return 8 if hVal < 65 else 9

    # Watermill Trail
    if gy >= 2 and gy <= 9 and gx >= -3 and gx <= 4 and abs(gx - (-1.0)) <= 1.2:
        return 8 if hVal < 65 else 9

    # Family House Court
    if gx >= -3 and gx <= -1 and gy >= -6 and gy <= -4:
        return 16  # shore_a (16)

    # Cliffs / Perimeters
    if gx <= -11 or gy <= -12 or (gx >= 11 and gy <= -3):
        return 18  # cliff (18)

    # General Snow Blanket
    if hVal >= 90:
        return 3   # snow_c (3)
    return 1 if hVal < 60 else 2       # snow_a (1) or snow_b (2)

grid_csv = []
for ty in range(MAP_H):
    row = []
    gy = ty - OFFSET_Y
    for tx in range(MAP_W):
        gx = tx - OFFSET_X
        gid = compute_tile_gid(gx, gy)
        row.append(str(gid))
    grid_csv.append(",".join(row))
ground_csv_str = ",\n".join(grid_csv)

# 3. Define Objects
def grid_to_tiled_pos(gx, gy):
    tx = gx + OFFSET_X
    ty = gy + OFFSET_Y
    # Tiled isometric object coordinates: x = tx * 64, y = ty * 64
    return tx * 64, ty * 64

# All 11 Buildings
buildings = [
    {"id": 101, "name": "BUILDING_CHURCH", "gid": 19, "wx": 3.5, "wy": -7.5, "w": 280, "h": 370, "feature": "CHURCH_ST_JUDE", "act": 2},
    {"id": 102, "name": "BUILDING_FAMILY_HOUSE", "gid": 20, "wx": -1.5, "wy": -5.0, "w": 320, "h": 298, "feature": "COTTAGE_NORTH", "act": 1},
    {"id": 103, "name": "BUILDING_WATERMILL", "gid": 21, "wx": -2.5, "wy": 8.5, "w": 260, "h": 244, "feature": "WATERMILL", "act": 2},
    {"id": 104, "name": "BUILDING_WINDMILL", "gid": 22, "wx": -8.5, "wy": -2.0, "w": 240, "h": 270, "feature": "WINDMILL", "act": 3},
    {"id": 105, "name": "BUILDING_COTTAGE_WEST", "gid": 23, "wx": -4.0, "wy": -0.5, "w": 220, "h": 205, "feature": "COTTAGE_WEST", "act": 1},
    {"id": 106, "name": "BUILDING_COTTAGE_SOUTH", "gid": 24, "wx": -2.2, "wy": 1.8, "w": 230, "h": 180, "feature": "COTTAGE_SOUTH", "act": 1},
    {"id": 107, "name": "BUILDING_COTTAGE_FAR_WEST", "gid": 23, "wx": -5.5, "wy": 2.0, "w": 210, "h": 188, "feature": "COTTAGE_FAR_WEST", "act": 2},
    {"id": 108, "name": "BUILDING_RIVERSIDE_COTTAGE", "gid": 23, "wx": 5.5, "wy": 3.0, "w": 215, "h": 190, "feature": "RIVERSIDE_COTTAGE", "act": 2},
    {"id": 109, "name": "BUILDING_EAST_WORKSHOP", "gid": 25, "wx": 6.0, "wy": -1.5, "w": 200, "h": 180, "feature": "EAST_COTTAGES", "act": 2},
    {"id": 110, "name": "BUILDING_SAWMILL", "gid": 26, "wx": 8.5, "wy": -1.0, "w": 210, "h": 195, "feature": "SAWMILL_LUMBER", "act": 2},
    {"id": 111, "name": "BUILDING_BUNKER", "gid": 27, "wx": -7.5, "wy": -7.5, "w": 230, "h": 160, "feature": "NORTH_BUNKER", "act": 3},
    {"id": 112, "name": "BUILDING_MAIN_BRIDGE", "gid": 28, "wx": 6.8, "wy": 7.8, "w": 208, "h": 149, "feature": "MAIN_BRIDGE", "act": 1},
]

# Props
props = [
    {"id": 201, "name": "PROP_STATUE", "gid": 29, "wx": 0.0, "wy": 0.0, "w": 90, "h": 140},
    {"id": 202, "name": "PROP_WELL", "gid": 30, "wx": 1.2, "wy": 2.4, "w": 100, "h": 112},
    {"id": 203, "name": "PROP_MARKET_STALL_1", "gid": 31, "wx": 4.5, "wy": -0.5, "w": 130, "h": 115},
    {"id": 204, "name": "PROP_MARKET_STALL_2", "gid": 32, "wx": 5.2, "wy": 0.4, "w": 115, "h": 105},
    {"id": 205, "name": "PROP_SAWMILL_CRANE", "gid": 33, "wx": 9.5, "wy": -1.8, "w": 88, "h": 139},
    {"id": 206, "name": "PROP_STACKED_LOGS", "gid": 34, "wx": 8.0, "wy": 0.2, "w": 103, "h": 93},
    {"id": 207, "name": "PROP_IRON_GATE", "gid": 35, "wx": 1.8, "wy": -3.2, "w": 130, "h": 85},
    {"id": 208, "name": "PROP_BOAT", "gid": 36, "wx": 2.0, "wy": 8.5, "w": 90, "h": 60},
    {"id": 209, "name": "PROP_DOCK_CRANE", "gid": 37, "wx": 6.0, "wy": 6.0, "w": 80, "h": 135},
]

# Street Lamps
street_lamps = [
    [4.2, 4.8], [4.8, 4.2], [7.2, 7.8], [7.8, 7.2],
    [-1.5, -0.8], [0.8, -1.5], [-0.8, 1.5], [1.5, 0.8],
    [1.8, 2.2], [2.5, -4.2], [3.8, -0.4], [-1.8, 0.6],
    [5.0, 2.6], [-4.2, -2.2]
]

# Trees
pine_trees = [
    [4.8, -8.5], [2.2, -8.2], [4.5, -6.5], [1.5, -8.5], [5.2, -7.0],
    [-7.0, -1.0], [-9.5, -3.5], [-8.0, 0.5], [-6.5, 3.5], [-10.0, -0.5], [-10.5, 2.0],
    [-5.0, -8.0], [-8.5, -6.5], [-6.0, -6.0], [-4.0, -7.0],
    [-4.0, 7.0], [-1.0, 9.5], [3.5, 7.5], [8.5, 5.0], [9.0, 6.5],
    [10.0, -2.5], [9.5, 1.5], [10.5, 0.0],
    [-3.0, -3.5], [-0.5, -2.5], [-3.5, 3.0]
]
dead_trees = [
    [0.8, -5.2], [1.5, -6.0], [2.2, -5.5], [2.8, -6.8],
    [-7.2, -5.2], [-9.0, -5.5], [7.5, -3.5]
]

# Build TMX XML
tmx_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    f'<map version="1.10" tiledversion="1.11.0" orientation="isometric" renderorder="right-down" width="{MAP_W}" height="{MAP_H}" tilewidth="{TILE_W}" tileheight="{TILE_H}" infinite="0" nextlayerid="10" nextobjectid="500">',
    ' <tileset firstgid="1" source="village_tileset.tsx"/>',
    
    # Layer 1: Blueprint Reference Image Layer
    ' <imagelayer id="1" name="Blueprint Reference (map du village.png)" opacity="0.4">',
    '  <image source="../../map du village.png" width="1536" height="1024"/>',
    ' </imagelayer>',
    
    # Layer 2: Ground Terrain
    f' <layer id="2" name="Ground Terrain (Sol Isométrique)" width="{MAP_W}" height="{MAP_H}">',
    '  <data encoding="csv">',
    ground_csv_str,
    '  </data>',
    ' </layer>',
    
    # Layer 3: Buildings
    ' <objectgroup id="3" name="Buildings (Bâtiments)">'
]

for b in buildings:
    ox, oy = grid_to_tiled_pos(b["wx"], b["wy"])
    tmx_lines.append(f'  <object id="{b["id"]}" name="{b["name"]}" type="building" gid="{b["gid"]}" x="{ox}" y="{oy}" width="{b["w"]}" height="{b["h"]}">' )
    tmx_lines.append('   <properties>')
    tmx_lines.append(f'    <property name="blueprint_feature" value="{b["feature"]}"/>')
    tmx_lines.append(f'    <property name="narrative_act" type="int" value="{b["act"]}"/>')
    tmx_lines.append('   </properties>')
    tmx_lines.append('  </object>')
tmx_lines.append(' </objectgroup>')

# Layer 4: Props
tmx_lines.append(' <objectgroup id="4" name="Props (Installations &amp; Mobilier)">')
for p in props:
    ox, oy = grid_to_tiled_pos(p["wx"], p["wy"])
    tmx_lines.append(f'  <object id="{p["id"]}" name="{p["name"]}" type="prop" gid="{p["gid"]}" x="{ox}" y="{oy}" width="{p["w"]}" height="{p["h"]}"/>')
tmx_lines.append(' </objectgroup>')

# Layer 5: Street Lamps
tmx_lines.append(' <objectgroup id="5" name="Street Lighting (Éclairage)">')
lamp_id = 250
for lx, ly in street_lamps:
    ox, oy = grid_to_tiled_pos(lx, ly)
    lamp_id += 1
    tmx_lines.append(f'  <object id="{lamp_id}" name="STREET_LAMP" type="light" gid="38" x="{ox}" y="{oy}" width="36" height="88">')
    tmx_lines.append('   <properties>')
    tmx_lines.append('    <property name="color" type="color" value="#fffbbf24"/>')
    tmx_lines.append('    <property name="radius" type="float" value="50.0"/>')
    tmx_lines.append('   </properties>')
    tmx_lines.append('  </object>')
tmx_lines.append(' </objectgroup>')

# Layer 6: Nature (Trees)
tmx_lines.append(' <objectgroup id="6" name="Nature (Végétation &amp; Forêt)">')
tree_id = 300
for tx, ty in pine_trees:
    ox, oy = grid_to_tiled_pos(tx, ty)
    tree_id += 1
    tmx_lines.append(f'  <object id="{tree_id}" name="PINE_TREE" type="nature" gid="39" x="{ox}" y="{oy}" width="88" height="146"/>')
for dx, dy in dead_trees:
    ox, oy = grid_to_tiled_pos(dx, dy)
    tree_id += 1
    tmx_lines.append(f'  <object id="{tree_id}" name="DEAD_TREE" type="nature" gid="40" x="{ox}" y="{oy}" width="78" height="128"/>')
tmx_lines.append(' </objectgroup>')

# Layer 7: Collisions
tmx_lines.append(' <objectgroup id="7" name="Collisions (Physique &amp; Limites)">')
col_id = 400
# Building collisions
for b in buildings:
    ox, oy = grid_to_tiled_pos(b["wx"], b["wy"])
    col_id += 1
    cw = b["w"] * 0.7
    ch = b["h"] * 0.4
    tmx_lines.append(f'  <object id="{col_id}" name="COL_{b["name"]}" type="collision" x="{ox - cw/2}" y="{oy - ch}" width="{cw}" height="{ch}"/>')

# River gorge water hazard
col_id += 1
ox_riv, oy_riv = grid_to_tiled_pos(0, 10)
tmx_lines.append(f'  <object id="{col_id}" name="COL_RIVER_WATER_HAZARD" type="hazard_water" x="{ox_riv - 300}" y="{oy_riv}" width="800" height="200"/>')
tmx_lines.append(' </objectgroup>')

# Layer 8: Gameplay Triggers & Spawns
tmx_lines.append(' <objectgroup id="8" name="Gameplay (Spawns, NPCs &amp; Indices)">')
sp_x, sp_y = grid_to_tiled_pos(7.0, 8.0)
tmx_lines.append(f'  <object id="490" name="PLAYER_SPAWN" type="spawn" x="{sp_x}" y="{sp_y}">')
tmx_lines.append('   <properties>')
tmx_lines.append('    <property name="character" value="Alex Miller"/>')
tmx_lines.append('    <property name="orientation" value="NW"/>')
tmx_lines.append('   </properties>')
tmx_lines.append('   <point/>')
tmx_lines.append('  </object>')

# NPCs
npcs = [
    (491, "NPC_EMMA", 6.2, 6.8, "Emma"),
    (492, "NPC_JAMES", 0.8, -0.8, "Officer James"),
    (493, "NPC_MICHAEL", -1.8, -3.8, "Old Michael"),
    (494, "NPC_ETHAN", -3.2, -6.2, "Ethan Miller")
]
for nid, nname, nx, ny, cname in npcs:
    nox, noy = grid_to_tiled_pos(nx, ny)
    tmx_lines.append(f'  <object id="{nid}" name="{nname}" type="npc" x="{nox}" y="{noy}">')
    tmx_lines.append(f'   <properties><property name="npc_name" value="{cname}"/></properties>')
    tmx_lines.append('   <point/>')
    tmx_lines.append('  </object>')
tmx_lines.append(' </objectgroup>')

tmx_lines.append('</map>')

with open(TMX_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(tmx_lines))
print(f"Generated TMX: {TMX_FILE}")

# 4. Export to TMJ (JSON) using official Tiled CLI
cmd = ["tiled", "--export-map", "json", TMX_FILE, TMJ_FILE]
env = os.environ.copy()
env["QT_QPA_PLATFORM"] = "offscreen"
res = subprocess.run(cmd, env=env, capture_output=True, text=True)
if res.returncode == 0:
    print(f"Successfully validated & exported TMJ via Tiled CLI: {TMJ_FILE}")
else:
    print(f"Tiled export notice: {res.stderr}")

print("Tiled Village Map generation completed successfully!")
