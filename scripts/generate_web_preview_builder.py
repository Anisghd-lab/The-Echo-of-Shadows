import os

code = r'''import os
import json
import base64

ROOT_DIR = "/root/the_echo_of_shadows"
ASSETS_DIR = os.path.join(ROOT_DIR, "new assets")
OUT_FILE = os.path.join(ROOT_DIR, "web_preview", "index.html")

def to_base64(rel_path, mirror=False):
    full_path = os.path.join(ASSETS_DIR, rel_path)
    if os.path.exists(full_path):
        if mirror:
            from PIL import Image
            import io
            im = Image.open(full_path).convert("RGBA")
            im_flipped = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            buf = io.BytesIO()
            im_flipped.save(buf, format="PNG")
            return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")
        else:
            with open(full_path, "rb") as f:
                return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    return ""

def build():
    print("Embedding Official New Assets into Web Preview...")
    
    # 1. Alex 360° & Cardinal Sprites (from official new assets library)
    alex_n = to_base64("characters/alex/Alex-—-Personnage-principal01.png")
    alex_ne = to_base64("characters/alex/Alex-—-Personnage-principal03.png")
    alex_e = to_base64("characters/alex/Alex-—-Personnage-principal05.png")
    alex_se = to_base64("characters/alex/Alex-—-Personnage-principal07.png")
    alex_s = to_base64("characters/alex/Alex-—-Personnage-principal09.png")
    alex_sw = to_base64("characters/alex/Alex-—-Personnage-principal11.png")
    alex_w = to_base64("characters/alex/Alex-—-Personnage-principal13.png")
    alex_nw = to_base64("characters/alex/Alex-—-Personnage-principal15.png")
    
    # 2. NPCs
    npc_emma = to_base64("characters/emma/Emma01.png")
    npc_ethan = to_base64("characters/ethan/Ethan-—-Frère-d’Alex01.png")
    npc_james = to_base64("characters/officer_james/Officer-James01.png")
    npc_michael = to_base64("characters/old_michael/Old-Michael01.png")

    # 3. Master Blueprint Map
    map_village_master = to_base64("environments/village/map du village.png")

    # 4. Village Buildings & Exterior
    family_house = to_base64("environments/family_house/MAISON-FAMILLIALE02.png")
    family_house_int = to_base64("environments/family_house/MAISON-FAMILLIALE03.png")
    alex_bedroom_int = to_base64("environments/family_house/MAISON-FAMILLIALE04.png")
    church = to_base64("environments/village/VILLAGE-ENVIRONMENT-104.png")
    watermill = to_base64("environments/village/VILLAGE-ENVIRONMENT-103.png")
    windmill = to_base64("environments/village/VILLAGE-ENVIRONMENT-102.png")
    cottage_west = to_base64("environments/village/VILLAGE-ENVIRONMENT-101.png")
    cottage_south = to_base64("environments/village/VILLAGE-ENVIRONMENT-106.png")
    east_workshop = to_base64("environments/village/VILLAGE-ENVIRONMENT-105.png")
    sawmill = to_base64("environments/village/VILLAGE-ENVIRONMENT-105.png")
    bridge_elem = to_base64("environments/village/VILLAGE-ENVIRONMENT-108.png")

    # 5. Props & Decor
    well = to_base64("environments/village/VILLAGE-ENVIRONMENT-111.png")
    statue = to_base64("environments/village/VILLAGE-ENVIRONMENT-106.png")
    lamp_post = to_base64("environments/village/VILLAGE-ENVIRONMENT-110.png")
    iron_gate = to_base64("environments/village/VILLAGE-ENVIRONMENT-113.png")
    market_stall_01 = to_base64("environments/village/VILLAGE-ENVIRONMENT-116.png")
    market_stall_02 = to_base64("environments/village/VILLAGE-ENVIRONMENT-121.png")
    sawmill_crane = to_base64("environments/village/VILLAGE-ENVIRONMENT-129.png")
    dock_crane = to_base64("environments/village/VILLAGE-ENVIRONMENT-137.png")
    stacked_logs = to_base64("environments/village/VILLAGE-ENVIRONMENT-142.png")
    boat = to_base64("environments/village/VILLAGE-ENVIRONMENT-152.png")
    bunker_ext = to_base64("environments/bunker/INTERIORS-BUNKER02.png")
    bunker_int = to_base64("environments/bunker/INTERIORS-BUNKER03.png")

    # 6. Interactive & Narrative Props
    prop_phone = to_base64("props/interactive/TELEPHONE-PRPOS01.png")
    prop_cassette = to_base64("props/narrative/NARRATIVE-PROPS-FURNITURE01.png")
    prop_recorder = to_base64("props/narrative/NARRATIVE-PROPS-FURNITURE03.png")
    prop_key = to_base64("props/narrative/NARRATIVE-PROPS-FURNITURE04.png")
    prop_notebook = to_base64("props/narrative/NARRATIVE-PROPS-FURNITURE05.png")
    prop_photos = to_base64("props/narrative/NARRATIVE-PROPS-FURNITURE06.png")
    prop_documents = to_base64("props/narrative/NARRATIVE-PROPS-FURNITURE07.png")
    prop_board = to_base64("props/narrative/NARRATIVE-PROPS-FURNITURE08.png")
    prop_countdown = to_base64("props/narrative/NARRATIVE-PROPS-FURNITURE09.png")

    # 7. Nature & Terrain Tiles
    pine_tree = to_base64("nature/NATURE-GAMEPLAY-STRUCTURES02.png")
    dead_tree = to_base64("nature/NATURE-GAMEPLAY-STRUCTURES06.png")
    stone_slab = to_base64("nature/NATURE-GAMEPLAY-STRUCTURES04.png")
    stone_slab_var = to_base64("nature/NATURE-GAMEPLAY-STRUCTURES07.png")
    snow_slab = to_base64("nature/NATURE-GAMEPLAY-STRUCTURES08.png")
    ice_slab = to_base64("nature/NATURE-GAMEPLAY-STRUCTURES10.png")
    cliff = to_base64("nature/NATURE-GAMEPLAY-STRUCTURES09.png")

    print(f"Generating standalone web preview at {OUT_FILE}...")

    # We will write the full HTML
    from generate_html_template import get_html_content
    html = get_html_content(
        alex_n=alex_n, alex_ne=alex_ne, alex_e=alex_e, alex_se=alex_se,
        alex_s=alex_s, alex_sw=alex_sw, alex_w=alex_w, alex_nw=alex_nw,
        npc_emma=npc_emma, npc_ethan=npc_ethan, npc_james=npc_james, npc_michael=npc_michael,
        map_village_master=map_village_master,
        family_house=family_house, family_house_int=family_house_int, alex_bedroom_int=alex_bedroom_int,
        church=church, watermill=watermill, windmill=windmill,
        cottage_west=cottage_west, cottage_south=cottage_south, east_workshop=east_workshop,
        sawmill=sawmill, bridge_elem=bridge_elem,
        well=well, statue=statue, lamp_post=lamp_post, iron_gate=iron_gate,
        market_stall_01=market_stall_01, market_stall_02=market_stall_02,
        sawmill_crane=sawmill_crane, dock_crane=dock_crane, stacked_logs=stacked_logs,
        boat=boat, bunker_ext=bunker_ext, bunker_int=bunker_int,
        prop_phone=prop_phone, prop_cassette=prop_cassette, prop_recorder=prop_recorder,
        prop_key=prop_key, prop_notebook=prop_notebook, prop_photos=prop_photos,
        prop_documents=prop_documents, prop_board=prop_board, prop_countdown=prop_countdown,
        pine_tree=pine_tree, dead_tree=dead_tree,
        stone_slab=stone_slab, stone_slab_var=stone_slab_var,
        snow_slab=snow_slab, ice_slab=ice_slab, cliff=cliff
    )

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Successfully generated {OUT_FILE} ({len(html)} bytes)")

if __name__ == "__main__":
    build()
'''

with open('/root/the_echo_of_shadows/web_preview/build_preview.py', 'w') as f:
    f.write(code)

print('Updated web_preview/build_preview.py wrapper.')
