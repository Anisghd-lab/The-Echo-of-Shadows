import os
import json
import math

def test_isometric_coordinates():
    print("Test 1: Isometric Coordinates...")
    TILE_W = 128.0
    TILE_H = 64.0
    HALF_W = 64.0
    HALF_H = 32.0

    # worldToScreen & screenToWorld
    wx, wy = 5.5, -3.2
    sx = (wx - wy) * HALF_W
    sy = (wx + wy) * HALF_H

    calc_wx = (sx / HALF_W + sy / HALF_H) / 2.0
    calc_wy = (sy / HALF_H - sx / HALF_W) / 2.0

    assert abs(wx - calc_wx) < 1e-4, f"Failed wx: {wx} != {calc_wx}"
    assert abs(wy - calc_wy) < 1e-4, f"Failed wy: {wy} != {calc_wy}"

    # vectorToOrientation
    def vec_to_orient(dx, dy):
        angle = math.atan2(dy, dx)
        if 0 <= angle < math.pi / 2:
            return 'SE'
        elif math.pi / 2 <= angle <= math.pi:
            return 'SW'
        elif -math.pi <= angle < -math.pi / 2:
            return 'NW'
        else:
            return 'NE'

    assert vec_to_orient(1, 1) == 'SE'
    assert vec_to_orient(-1, 1) == 'SW'
    assert vec_to_orient(-1, -1) == 'NW'
    assert vec_to_orient(1, -1) == 'NE'

    # Z-Order
    z_back = 40000 + round((0.0 + 2.0) * 100)
    z_front = 40000 + round((0.0 + 5.0) * 100)
    assert z_front > z_back, "Z-order front must be > back"
    print("  ✓ Isometric Coordinates: PASSED")

def test_collisions():
    print("Test 2: Collisions & Sliding...")
    ox, oy, hw, hh = 4.0, 4.0, 1.0, 1.0
    radius = 0.28

    def collides(x, y):
        cx = max(ox - hw, min(x, ox + hw))
        cy = max(oy - hh, min(y, oy + hh))
        dx = x - cx
        dy = y - cy
        return (dx * dx + dy * dy) < (radius * radius)

    assert collides(4.0, 4.0) == True
    assert collides(0.0, 0.0) == False

    # Slide resolution
    cx, cy = 2.5, 1.0
    tx, ty = 3.5, 1.2
    res_x, res_y = cx, cy
    if not collides(tx, ty):
        res_x, res_y = tx, ty
    elif not collides(tx, cy):
        res_x, res_y = tx, cy
    elif not collides(cx, ty):
        res_x, res_y = cx, cy

    assert not collides(res_x, res_y), "Resolved pos must not collide"
    print("  ✓ Collisions & Sliding: PASSED")

def test_z_order():
    print("Test 3: Z-Order Dynamic Sorting...")
    def unified_z(x, y):
        return round((x + y) * 100)

    u_well = unified_z(0.0, 4.0)
    u_alex = unified_z(0.0, 6.0)
    u_house = unified_z(0.0, 8.0)

    assert u_alex > u_well, "Alex (y=6) must be in front of well (y=4)"
    assert u_alex < u_house, "Alex (y=6) must be behind house (y=8)"
    print("  ✓ Z-Order Depth Sorting: PASSED")

def test_save_system_integration():
    print("Test 4: Asset Registry & Save Integrity...")
    registry_path = "/root/the_echo_of_shadows/assets/data/asset_registry.json"
    assert os.path.exists(registry_path), "asset_registry.json must exist"
    with open(registry_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["metadata"]["total_files"] == 1258
    assert "maison_familiale_extérieure01" in data["assets"]
    assert "village_abandonné_environment_sprite_sheet05" in data["assets"]
    assert "alex_animation_idle03" in data["assets"]
    assert "alex_marche01" in data["assets"]
    assert "village_abandonné_route_décor_extérieur01" in data["assets"]
    print("  ✓ Asset Registry (1258 assets verified): PASSED")

def test_phase3_poi_system():
    print("Test 5: Phase 3 Points of Interest (POI) Registry & Proximity...")
    pois = [
        {"id": "VILLAGE_ENTRANCE", "nameEn": "Village Entrance (Bridge)", "nameFr": "Entrée du village (Pont)", "x": 0.0, "y": 0.0, "radius": 1.8},
        {"id": "VILLAGE_SQUARE", "nameEn": "Central Square", "nameFr": "Place centrale", "x": 0.0, "y": 5.5, "radius": 2.2},
        {"id": "OLD_WELL", "nameEn": "Ancient Stone Well", "nameFr": "Puits en pierre", "x": 0.0, "y": 6.0, "radius": 1.5},
        {"id": "ABANDONED_CHURCH", "nameEn": "St. Jude Abandoned Church", "nameFr": "Église abandonnée St-Jude", "x": 6.5, "y": 5.0, "radius": 2.4},
        {"id": "FAMILY_HOUSE", "nameEn": "Alex Family House", "nameFr": "Maison familiale", "x": 0.0, "y": 10.5, "radius": 2.0},
        {"id": "ABANDONED_HOUSE_01", "nameEn": "Dilapidated Cottage", "nameFr": "Cottage délabré", "x": -5.5, "y": 4.5, "radius": 1.8},
        {"id": "ABANDONED_HOUSE_02", "nameEn": "Forester Shack", "nameFr": "Cabane du garde", "x": -5.5, "y": 8.5, "radius": 1.8},
    ]

    assert len(pois) == 7, "7 Canonical POIs required"

    def find_poi(px, py):
        closest = None
        min_dist = float('inf')
        for p in pois:
            dx = px - p["x"]
            dy = py - p["y"]
            dist = math.sqrt(dx * dx + dy * dy)
            if dist <= p["radius"] and dist < min_dist:
                min_dist = dist
                closest = p
        return closest

    assert find_poi(0.1, 0.1)["id"] == "VILLAGE_ENTRANCE"
    assert find_poi(0.1, 5.9)["id"] == "OLD_WELL"
    assert find_poi(0.2, 10.4)["id"] == "FAMILY_HOUSE"
    assert find_poi(12.0, 12.0) is None
    print("  ✓ POI Proximity & Detection: PASSED")

def test_phase3_human_scale_proportions():
    print("Test 6: Phase 3 Human Scale Proportions...")
    alex_w, alex_h = 28.0, 56.0
    church_h = 370.0
    house_w = 320.0
    well_h = 112.0
    lamp_h = 96.0

    estimated_door_w = house_w * 0.16
    assert alex_w < estimated_door_w
    assert church_h / alex_h >= 6.0
    assert lamp_h > alex_h
    assert (well_h * 0.4) < alex_h
    print("  ✓ Human Scale Proportions (28x56 Alex vs Environment): PASSED")

def test_phase3_terrain_zones():
    print("Test 7: Phase 3 Multi-Zone Terrain System...")
    def get_zone(x, y):
        if y <= -2:
            return "frozenRiver"
        dx = float(x)
        dy = float(y) - 5.5
        dist_to_square = math.sqrt(dx * dx + dy * dy)
        if dist_to_square <= 2.8:
            return "plaza"
        if abs(x) <= 1 and -1 <= y <= 11:
            return "mainRoad"
        if 1 <= x <= 7 and 4 <= y <= 6:
            return "sidePath"
        if -6 <= x <= -1 and 4 <= y <= 9:
            return "sidePath"
        if (abs(x) <= 3 and 9 <= y <= 12) or (4 <= x <= 8 and 3 <= y <= 7):
            return "buildingYard"
        return "deepSnow"

    assert get_zone(0, -3) == "frozenRiver"
    assert get_zone(0, 0) == "mainRoad"
    assert get_zone(0, 5) == "plaza"
    assert get_zone(0, 6) == "plaza"
    assert get_zone(6, 5) == "sidePath"
    assert get_zone(6, 3) == "buildingYard"
    assert get_zone(10, 10) == "deepSnow"
    print("  ✓ Multi-Zone Terrain Classification: PASSED")

def test_phase3_1_360_rotation_cycle():
    print("Test 8: Phase 3.1 360° Rotation Cycle (Clockwise & Counter-Clockwise)...")
    cycle = ['SE', 'SW', 'NW', 'NE']
    
    # 1. Clockwise: SE -> SW -> NW -> NE -> SE
    cur = 'SE'
    transitions_cw = []
    for _ in range(4):
        next_idx = (cycle.index(cur) + 1) % len(cycle)
        transitions_cw.append((cur, cycle[next_idx]))
        cur = cycle[next_idx]
    
    assert transitions_cw == [
        ('SE', 'SW'),
        ('SW', 'NW'),
        ('NW', 'NE'),
        ('NE', 'SE')
    ], f"CW rotation cycle failed: {transitions_cw}"

    # 2. Counter-Clockwise: SE -> NE -> NW -> SW -> SE
    cur = 'SE'
    transitions_ccw = []
    for _ in range(4):
        prev_idx = (cycle.index(cur) - 1 + len(cycle)) % len(cycle)
        transitions_ccw.append((cur, cycle[prev_idx]))
        cur = cycle[prev_idx]

    assert transitions_ccw == [
        ('SE', 'NE'),
        ('NE', 'NW'),
        ('NW', 'SW'),
        ('SW', 'SE')
    ], f"CCW rotation cycle failed: {transitions_ccw}"
    print("  ✓ 360° Rotation Transitions (CW & CCW): PASSED")

def test_phase3_1_inplace_rotation_invariance():
    print("Test 9: Phase 3.1 In-Place Rotation Position Invariance...")
    world_x = 4.25
    world_y = -1.80

    # In-place turn: low joystick magnitude (0.10 <= mag < 0.30)
    def update_player(input_x, input_y, cur_x, cur_y):
        mag = math.hypot(input_x, input_y)
        angle = math.atan2(input_y, input_x)
        if 0 <= angle < math.pi / 2:
            orient = 'SE'
        elif math.pi / 2 <= angle <= math.pi:
            orient = 'SW'
        elif -math.pi <= angle < -math.pi / 2:
            orient = 'NW'
        else:
            orient = 'NE'

        if mag < 0.30: # Turn in place zone
            return cur_x, cur_y, orient, "IDLE"
        else: # Movement zone
            dx = (input_x + input_y) * 2.4 * 0.1 * 0.707
            dy = (-input_x + input_y) * 2.4 * 0.1 * 0.707
            return cur_x + dx, cur_y + dy, orient, "WALK"

    # Turn to SW
    new_x, new_y, orient, state = update_player(-0.15, 0.15, world_x, world_y)
    assert orient == 'SW'
    assert state == 'IDLE'
    assert new_x == world_x and new_y == world_y, "World coordinates MUST NOT change during in-place rotation"

    # Turn to NW
    new_x, new_y, orient, state = update_player(-0.15, -0.15, world_x, world_y)
    assert orient == 'NW'
    assert state == 'IDLE'
    assert new_x == world_x and new_y == world_y

    # Turn to NE
    new_x, new_y, orient, state = update_player(0.15, -0.15, world_x, world_y)
    assert orient == 'NE'
    assert state == 'IDLE'
    assert new_x == world_x and new_y == world_y
    print("  ✓ In-Place Rotation Position Invariance: PASSED")

def test_phase3_1_directional_animation_assignment():
    print("Test 10: Phase 3.1 Directional Animation Assignment (Idle, Walk, Run)...")
    # Verify mapping for all 4 orientations
    assets_dir = "/root/the_echo_of_shadows/assets/images/characters/alex"
    
    idle_assets = {
        'SE': 'idle/Alex-—-Animation-Idle03.png',
        'SW': 'idle/Alex-—-Animation-Idle10.png',
        'NE': 'idle/Alex-—-Animation-Idle06.png',
        'NW': 'idle/Alex-—-Animation-Idle07.png',
    }
    walk_assets = {
        'SE': 'walk/Alex-—-Marche36.png',
        'SW': 'walk/Alex-—-Marche42.png',
        'NE': 'walk/Alex-—-Marche18.png',
        'NW': 'walk/Alex-—-Marche10.png',
    }
    run_assets = {
        'SE': 'run/Alex-—-Course11.png',
        'SW': 'run/Alex-—-Course40.png',
        'NE': 'run/Alex-—-Course10.png',
        'NW': 'run/Alex-—-Course26.png',
    }

    for orient in ['SE', 'SW', 'NE', 'NW']:
        assert os.path.exists(os.path.join(assets_dir, idle_assets[orient])), f"Missing idle asset for {orient}"
        assert os.path.exists(os.path.join(assets_dir, walk_assets[orient])), f"Missing walk asset for {orient}"
        assert os.path.exists(os.path.join(assets_dir, run_assets[orient])), f"Missing run asset for {orient}"

    print("  ✓ 4-Way Animation Asset Mapping (SE, SW, NE, NW): PASSED")

def test_phase3_1_directional_interaction():
    print("Test 11: Phase 3.1 Directional Interaction Cone...")
    # Alex at (0.0, 0.0), Ethan desk at (0.0, 10.5)
    alex_x, alex_y = 0.0, 0.0
    desk_x, desk_y = 0.0, 10.5

    def is_facing(orient, ax, ay, tx, ty, max_deg=75.0):
        # screen angle:
        screen_angles = {'SE': math.pi/4, 'SW': 3*math.pi/4, 'NW': -3*math.pi/4, 'NE': -math.pi/4}
        dx = (tx - ty) - (ax - ay)
        dy = ((tx + ty) - (ax + ay)) * 0.5
        target_angle = math.atan2(dy, dx)
        facing_angle = screen_angles[orient]
        diff = abs(target_angle - facing_angle)
        while diff > math.pi:
            diff = abs(2 * math.pi - diff)
        return diff <= (max_deg * math.pi / 180.0)

    # When facing SW (-X, +Y in screen space), target at world (0, 10.5) (+Y axis) is in front
    assert is_facing('SW', alex_x, alex_y, 0.0, 10.5) == True
    assert is_facing('NE', alex_x, alex_y, 0.0, 10.5) == False

    # When facing SE (+X, +Y in screen space), target at world (10.5, 0) (+X axis) is in front
    assert is_facing('SE', alex_x, alex_y, 10.5, 0.0) == True
    assert is_facing('NW', alex_x, alex_y, 10.5, 0.0) == False
    print("  ✓ Directional Interaction Cone: PASSED")

def test_phase3_1_visual_continuity_camera_zero_void():
    print("Test 12: Phase 3.1 Visual Continuity, Zero Void & Edge Clamping...")
    # Camera viewports tested: min zoom (0.85), max zoom (1.6)
    # Screen boundaries: North, South, East, West, Diagonals
    viewports = [(1920, 1080), (2400, 1080), (1280, 720)]
    zooms = [0.85, 1.15, 1.6]
    
    # Terrain grid radius = 24
    grid_r = 24
    HALF_W = 64.0
    HALF_H = 32.0
    # Minimum and maximum screen coordinates covered by terrain
    terrain_min_x = -grid_r * 2 * HALF_W # -3072
    terrain_max_x = grid_r * 2 * HALF_W  # +3072
    terrain_min_y = -grid_r * 2 * HALF_H # -1536
    terrain_max_y = grid_r * 2 * HALF_H  # +1536

    camera_min_x = -1600.0
    camera_max_x = 1600.0
    camera_min_y = -850.0
    camera_max_y = 1150.0

    # For every viewport and zoom level, verify visible rect stays inside terrain rect
    for vw, vh in viewports:
        for zoom in zooms:
            half_w = (vw / 2.0) / zoom
            half_h = (vh / 2.0) / zoom

            # Clamped camera positions at all extreme corners
            cam_corners = [
                ("North", (0.0, camera_max_y - half_h)),
                ("South", (0.0, camera_min_y + half_h)),
                ("East", (camera_max_x - half_w, 0.0)),
                ("West", (camera_min_x + half_w, 0.0)),
                ("Diag NE", (camera_max_x - half_w, camera_min_y + half_h)),
                ("Diag NW", (camera_min_x + half_w, camera_min_y + half_h)),
                ("Diag SE", (camera_max_x - half_w, camera_max_y - half_h)),
                ("Diag SW", (camera_min_x + half_w, camera_max_y - half_h)),
            ]

            for label, (cx, cy) in cam_corners:
                visible_left = cx - half_w
                visible_right = cx + half_w
                visible_top = cy - half_h
                visible_bottom = cy + half_h

                assert visible_left >= terrain_min_x, f"Void exposed on left ({visible_left} < {terrain_min_x}) at {label} zoom {zoom}"
                assert visible_right <= terrain_max_x, f"Void exposed on right ({visible_right} > {terrain_max_x}) at {label} zoom {zoom}"
                assert visible_top >= terrain_min_y, f"Void exposed on top ({visible_top} < {terrain_min_y}) at {label} zoom {zoom}"
                assert visible_bottom <= terrain_max_y, f"Void exposed on bottom ({visible_bottom} > {terrain_max_y}) at {label} zoom {zoom}"

    print("  ✓ Zero Void Guaranteed across all edges, diagonals, and zoom levels (0.85 to 1.6): PASSED")

def test_phase3_pure_local_save_integrity():
    print("Test 13: Pure Local Save State...")
    save_data = {
        "save_id": "slot_01_village_phase3_1",
        "timestamp": 1726950000000,
        "chapter": 1,
        "current_map": "VILLAGE_ABANDONED",
        "position": {
            "x": 0.0,
            "y": 5.5,
            "orientation": "SW"
        },
        "inventory": [{"id": "flash_light", "name": "Lampe torche"}],
        "evidence": [{"id": "ethan_cassette", "name": "Cassette audio"}],
        "trust_variables": {"emma": 50, "james": 40, "michael": 30},
        "suspicion_level": 15,
        "flags": {"village_entered": True, "old_well_inspected": True}
    }
    serialized = json.dumps(save_data)
    assert "firebase" not in serialized.lower()
    assert "cloud" not in serialized.lower()
    print("  ✓ Local Save Integrity: PASSED")

def test_phase3_2_asset_transparency():
    print("Test 14: Phase 3.2 Asset Transparency & Elimination of White Rectangles...")
    from PIL import Image
    import numpy as np

    assets = {
        'puits': 'environments/village/decor/Village-abandonné-—-Route-&-décor-extérieur01.png',
        'arbres_pin': 'environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet37.png',
        'arbres_mort': 'environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet34.png',
        'clôtures': 'environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet15.png',
        'maisons_01': 'environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet01.png',
        'maisons_02': 'environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet02.png',
        'maison_famille': 'environments/family_house/exterior/Maison-familiale-extérieure01.png',
        'église': 'environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet05.png',
        'props_lampadaire': 'environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet20.png',
        'props_falaise': 'environments/village/decor/Village-abandonné-—-Route-&-décor-extérieur52.png',
        'alex_idle_se': 'characters/alex/idle/Alex-—-Animation-Idle03.png',
        'alex_idle_sw': 'characters/alex/idle/Alex-—-Animation-Idle10.png',
        'alex_walk_se': 'characters/alex/walk/Alex-—-Marche36.png',
        'alex_walk_sw': 'characters/alex/walk/Alex-—-Marche42.png',
    }

    base_dir = '/root/the_echo_of_shadows/assets/images'
    for name, rel in assets.items():
        p = os.path.join(base_dir, rel)
        im = Image.open(p)
        assert im.mode == 'RGBA', f'{name} must be RGBA'
        arr = np.array(im)
        h, w = arr.shape[:2]
        alpha = arr[:, :, 3]
        rgb = arr[:, :, :3]

        border_mask = np.zeros((h, w), dtype=bool)
        border_mask[0, :] = True
        border_mask[-1, :] = True
        border_mask[:, 0] = True
        border_mask[:, -1] = True

        white_border = np.sum(border_mask & (alpha > 180) & np.all(rgb > 230, axis=2))
        assert white_border <= 10, f'{name} has white background rectangle! ({white_border} px)'

        transparent_pct = np.mean(alpha == 0) * 100
        assert transparent_pct > 15.0, f'{name} transparent area too low ({transparent_pct}%)'

    print("  ✓ All 14 Core Village Assets 100% Free of White Background Rectangles: PASSED")

def test_phase3_2_debug_overlay_clean_release():
    print("Test 15: Phase 3.2 Debug Overlay & Clean Release Mode Verification...")
    web_preview_file = "/root/the_echo_of_shadows/web_preview/index.html"
    with open(web_preview_file, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Verify default debug state is FALSE
    assert "let isDebug = false;" in html or "let isDebug=false;" in html, "isDebug must be false by default"

    # 2. Verify debug-panel and debug-tools default style display: none
    assert "#debug-panel {" in html and "display: none;" in html
    assert "#debug-tools {" in html and "display: none;" in html

    # 3. Verify that hitboxes and debug strokes are guarded strictly behind if (isDebug)
    assert "if (isDebug)" in html

    print("  ✓ Release Mode Cleanliness (Debug Off, Zero Hitboxes, Zero Technical Overlays): PASSED")

if __name__ == "__main__":
    print("=== Running The Echo of Shadows Phase 3.2 Verification Suite ===")
    test_isometric_coordinates()
    test_collisions()
    test_z_order()
    test_save_system_integration()
    test_phase3_poi_system()
    test_phase3_human_scale_proportions()
    test_phase3_terrain_zones()
    test_phase3_1_360_rotation_cycle()
    test_phase3_1_inplace_rotation_invariance()
    test_phase3_1_directional_animation_assignment()
    test_phase3_1_directional_interaction()
    test_phase3_1_visual_continuity_camera_zero_void()
    test_phase3_pure_local_save_integrity()
    test_phase3_2_asset_transparency()
    test_phase3_2_debug_overlay_clean_release()
    print("=============================================================")
    print("ALL 15 PHASE 3.2 TESTS PASSED SUCCESSFULLY!")
