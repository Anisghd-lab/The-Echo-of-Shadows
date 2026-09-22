import os
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

def crop_strip_to_base64(rel_path, col, total_cols, mirror=False):
    full_path = os.path.join(ASSETS_DIR, rel_path)
    if os.path.exists(full_path):
        from PIL import Image
        import io
        im = Image.open(full_path).convert("RGBA")
        fw = im.width / total_cols
        fh = im.height
        box = (int(col * fw), 0, int((col + 1) * fw), fh)
        frame = im.crop(box)
        if mirror:
            frame = frame.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        buf = io.BytesIO()
        frame.save(buf, format="PNG")
        return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")
    return ""

def build():
    print("Embedding Official New Assets into Web Preview...")
    
    # 1. Alex 360° & Cardinal Sprites strictly from official new assets library
    alex_frames = {
        f"alex_{i:02d}": to_base64(f"characters/alex/Alex-—-Personnage-principal{i:02d}.png")
        for i in range(1, 17)
    }
    alex_n = alex_frames["alex_01"]
    alex_ne = alex_frames["alex_03"]
    alex_e = alex_frames["alex_05"]
    alex_se = alex_frames["alex_07"]
    alex_s = alex_frames["alex_09"]
    alex_sw = alex_frames["alex_11"]
    alex_w = alex_frames["alex_13"]
    alex_nw = alex_frames["alex_15"]
    
    # 2. Authentic Walk Animation Frames (Phases 4 & 5)
    walk_frames = {
        "walk_w1": crop_strip_to_base64("Alex walk/Alex-—-Marche01.png", 0, 4),
        "walk_w2": crop_strip_to_base64("Alex walk/Alex-—-Marche01.png", 1, 4),
        "walk_w3": crop_strip_to_base64("Alex walk/Alex-—-Marche01.png", 2, 4),
        "walk_w4": crop_strip_to_base64("Alex walk/Alex-—-Marche01.png", 3, 4),
        "walk_ne1": to_base64("Alex walk/Alex-—-Marche03.png"),
        "walk_ne2": to_base64("Alex walk/Alex-—-Marche04.png"),
        "walk_ne3": to_base64("Alex walk/Alex-—-Marche05.png"),
        "walk_ne4": to_base64("Alex walk/Alex-—-Marche06.png"),
        "walk_n1": to_base64("Alex walk/Alex-—-Marche17.png"),
        "walk_n2": to_base64("Alex walk/Alex-—-Marche38.png"),
        "walk_n3": to_base64("Alex walk/Alex-—-Marche20.png"),
        "walk_n4": to_base64("Alex walk/Alex-—-Marche39.png"),
        "walk_s1": to_base64("Alex walk/Alex-—-Marche54.png"),
        "walk_s2": to_base64("Alex walk/Alex-—-Marche55.png"),
        "walk_s3": to_base64("Alex walk/Alex-—-Marche56.png"),
        "walk_s4": to_base64("Alex walk/Alex-—-Marche57.png"),
        "walk_nw1": to_base64("Alex walk/Alex-—-Marche09.png"),
        "walk_nw2": to_base64("Alex walk/Alex-—-Marche11.png"),
        "walk_nw3": to_base64("Alex walk/Alex-—-Marche14.png"),
        "walk_nw4": to_base64("Alex walk/Alex-—-Marche18.png"),
    }

    # 3. Authentic Run Animation Frames (Phase 7)
    run_frames = {
        f"run_w{i+1}": crop_strip_to_base64("Alex run/Alex-—-Course02.png", i, 7)
        for i in range(7)
    }
    run_frames.update({
        "run_ne1": crop_strip_to_base64("Alex run/Alex-—-Course07.png", 0, 2),
        "run_ne2": crop_strip_to_base64("Alex run/Alex-—-Course07.png", 1, 2),
        "run_ne3": to_base64("Alex run/Alex-—-Course10.png"),
        "run_ne4": to_base64("Alex run/Alex-—-Course16.png"),
        "run_sw1": crop_strip_to_base64("Alex run/Alex-—-Course20.png", 0, 2),
        "run_sw2": crop_strip_to_base64("Alex run/Alex-—-Course20.png", 1, 2),
        "run_sw3": to_base64("Alex run/Alex-—-Course24.png"),
        "run_sw4": to_base64("Alex run/Alex-—-Course28.png"),
        "run_nw1": to_base64("Alex run/Alex-—-Course01.png"),
        "run_nw2": to_base64("Alex run/Alex-—-Course04.png"),
        "run_nw3": to_base64("Alex run/Alex-—-Course05.png"),
        "run_nw4": to_base64("Alex run/Alex-—-Course06.png"),
        "run_n1": crop_strip_to_base64("Alex run/Alex-—-Course12.png", 0, 2),
        "run_n2": crop_strip_to_base64("Alex run/Alex-—-Course12.png", 1, 2),
        "run_n3": to_base64("Alex run/Alex-—-Course13.png"),
        "run_n4": to_base64("Alex run/Alex-—-Course15.png"),
        "run_s1": to_base64("Alex run/Alex-—-Course34.png"),
        "run_s2": to_base64("Alex run/Alex-—-Course35.png"),
        "run_s3": to_base64("Alex run/Alex-—-Course36.png"),
        "run_s4": to_base64("Alex run/Alex-—-Course37.png"),
    })

    # 4. NPC 360° Frames (Emma, Ethan, James, Michael)
    npc_emma_frames = {
        f"emma_{i:02d}": to_base64(f"characters/emma/Emma{i:02d}.png")
        for i in range(1, 19)
    }
    npc_james_frames = {
        f"james_{i:02d}": to_base64(f"characters/officer_james/Officer-James{i:02d}.png")
        for i in range(1, 19)
    }
    npc_michael_frames = {
        f"michael_{i:02d}": to_base64(f"characters/old_michael/Old-Michael{i:02d}.png")
        for i in range(1, 19)
    }
    npc_ethan_frames = {
        f"ethan_{i:02d}": to_base64(f"characters/ethan/Ethan-frère-de-Alex{i:02d}.png")
        for i in range(1, 13)
    }
    npc_emma = npc_emma_frames["emma_07"]
    npc_ethan = npc_ethan_frames.get("ethan_11", npc_ethan_frames.get("ethan_01", ""))
    npc_james = npc_james_frames["james_11"]
    npc_michael = npc_michael_frames["michael_07"]

    # 5. Master Blueprint Map
    map_village_master = to_base64("map du village.png") if os.path.exists(os.path.join(ASSETS_DIR, "map du village.png")) else to_base64("environments/village/map du village.png")

    # 6. Village Buildings & Exterior
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

    # 7. Props & Decor
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

    # 8. Interactive & Narrative Props
    prop_phone = to_base64("props/interactive/TELEPHONE-PRPOS01.png")
    prop_cassette = to_base64("props/narrative/NARRATIVE-PROPS-FURNITURE01.png")
    prop_recorder = to_base64("props/narrative/NARRATIVE-PROPS-FURNITURE03.png")
    prop_key = to_base64("props/narrative/NARRATIVE-PROPS-FURNITURE04.png")
    prop_notebook = to_base64("props/narrative/NARRATIVE-PROPS-FURNITURE05.png")
    prop_photos = to_base64("props/narrative/NARRATIVE-PROPS-FURNITURE06.png")
    prop_documents = to_base64("props/narrative/NARRATIVE-PROPS-FURNITURE07.png")
    prop_board = to_base64("props/narrative/NARRATIVE-PROPS-FURNITURE08.png")
    prop_countdown = to_base64("props/narrative/NARRATIVE-PROPS-FURNITURE09.png")

    # 9. Authentic Diamond Ground Tiles & Foliage (Dimetric 2:1)
    snow_a = to_base64("nature/NATURE-GAMEPLAY-STRUCTURES54.png")
    snow_b = to_base64("nature/NATURE-GAMEPLAY-STRUCTURES61.png")
    snow_c = to_base64("nature/NATURE-GAMEPLAY-STRUCTURES187.png")
    road_a = to_base64("nature/NATURE-GAMEPLAY-STRUCTURES55.png")
    road_b = to_base64("nature/NATURE-GAMEPLAY-STRUCTURES69.png")
    plaza_a = to_base64("nature/NATURE-GAMEPLAY-STRUCTURES57.png")
    plaza_b = to_base64("nature/NATURE-GAMEPLAY-STRUCTURES2181.png")
    path_a = to_base64("nature/NATURE-GAMEPLAY-STRUCTURES58.png")
    path_b = to_base64("nature/NATURE-GAMEPLAY-STRUCTURES60.png")
    bridge_planks = to_base64("nature/NATURE-GAMEPLAY-STRUCTURES68.png")
    dock_planks = to_base64("nature/NATURE-GAMEPLAY-STRUCTURES100.png")
    ice_a = to_base64("nature/NATURE-GAMEPLAY-STRUCTURES62.png")
    ice_b = to_base64("nature/NATURE-GAMEPLAY-STRUCTURES67.png")
    water_a = to_base64("nature/NATURE-GAMEPLAY-STRUCTURES65.png")
    water_b = to_base64("nature/NATURE-GAMEPLAY-STRUCTURES66.png")
    shore_a = to_base64("nature/NATURE-GAMEPLAY-STRUCTURES56.png")
    shore_b = to_base64("nature/NATURE-GAMEPLAY-STRUCTURES63.png")
    cliff = to_base64("nature/NATURE-GAMEPLAY-STRUCTURES09.png")
    pine_tree = to_base64("nature/NATURE-GAMEPLAY-STRUCTURES02.png")
    dead_tree = to_base64("nature/NATURE-GAMEPLAY-STRUCTURES06.png")

    print(f"Generating standalone web preview at {OUT_FILE}...")

    from generate_html_template import get_html_content
    html = get_html_content(
        alex_n=alex_n, alex_ne=alex_ne, alex_e=alex_e, alex_se=alex_se,
        alex_s=alex_s, alex_sw=alex_sw, alex_w=alex_w, alex_nw=alex_nw,
        **alex_frames,
        **walk_frames,
        **run_frames,
        **npc_emma_frames,
        **npc_james_frames,
        **npc_michael_frames,
        **npc_ethan_frames,
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
        snow_a=snow_a, snow_b=snow_b, snow_c=snow_c,
        road_a=road_a, road_b=road_b,
        plaza_a=plaza_a, plaza_b=plaza_b,
        path_a=path_a, path_b=path_b,
        bridge_planks=bridge_planks, dock_planks=dock_planks,
        ice_a=ice_a, ice_b=ice_b,
        water_a=water_a, water_b=water_b,
        shore_a=shore_a, shore_b=shore_b,
        cliff=cliff
    )

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Successfully generated {OUT_FILE} ({len(html)} bytes)")

if __name__ == "__main__":
    build()
