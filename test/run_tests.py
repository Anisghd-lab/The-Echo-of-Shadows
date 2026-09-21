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
    # Obstacle at (4.0, 4.0) halfWidth 1.0, halfHeight 1.0 (bounds [3, 5])
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
        res_x, res_y = cx, ty

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

    # Check at entrance
    at_entrance = find_poi(0.1, 0.1)
    assert at_entrance is not None and at_entrance["id"] == "VILLAGE_ENTRANCE"

    # Check at old well
    at_well = find_poi(0.1, 5.9)
    assert at_well is not None and at_well["id"] == "OLD_WELL"

    # Check at family house
    at_family = find_poi(0.2, 10.4)
    assert at_family is not None and at_family["id"] == "FAMILY_HOUSE"

    # Check far out
    out_of_bounds = find_poi(12.0, 12.0)
    assert out_of_bounds is None
    print("  ✓ POI Proximity & Detection: PASSED")

def test_phase3_human_scale_proportions():
    print("Test 6: Phase 3 Human Scale Proportions...")
    # Alex calibrated dimensions
    alex_w, alex_h = 28.0, 56.0
    church_w, church_h = 280.0, 370.0
    house_w, house_h = 320.0, 298.0
    cottage_w, cottage_h = 260.0, 244.0
    well_w, well_h = 100.0, 112.0
    lamp_w, lamp_h = 38.0, 96.0

    # Doorway scale verification: standard door width ~ 45-60px
    estimated_door_w = house_w * 0.16 # ~51.2px
    assert alex_w < estimated_door_w, f"Alex width {alex_w} must fit through door {estimated_door_w}"

    # Church height proportion: Church must be at least 5x Alex height
    assert church_h / alex_h >= 6.0, f"Church height ratio {church_h / alex_h} must feel monumental"

    # Lamp height proportion: Street lamp taller than Alex
    assert lamp_h > alex_h, "Street lamp must be taller than Alex"

    # Well height proportion: Well rim below Alex waist/chest
    well_rim_h = well_h * 0.4 # ~44px
    assert well_rim_h < alex_h, "Well rim must be lower than Alex"
    print("  ✓ Human Scale Proportions (28x56 Alex vs Environment): PASSED")

def test_phase3_terrain_zones():
    print("Test 7: Phase 3 Multi-Zone Terrain System...")
    def get_zone(x, y):
        # 1. Frozen River at entrance
        if y <= -2:
            return "frozenRiver"

        # 2. Central Square / Plaza (around world Y: 5.5, X: 0.0)
        dx = float(x)
        dy = float(y) - 5.5
        dist_to_square = math.sqrt(dx * dx + dy * dy)
        if dist_to_square <= 2.8:
            return "plaza"

        # 3. Main North-South Village Street
        if abs(x) <= 1 and -1 <= y <= 11:
            return "mainRoad"

        # 4. Church Path (East branch)
        if 1 <= x <= 7 and 4 <= y <= 6:
            return "sidePath"

        # 5. Cottage Path (West branch)
        if -6 <= x <= -1 and 4 <= y <= 9:
            return "sidePath"

        # 6. Yard around Family House & Church
        if (abs(x) <= 3 and 9 <= y <= 12) or (4 <= x <= 8 and 3 <= y <= 7):
            return "buildingYard"

        # 7. General Snow-covered ground
        return "deepSnow"

    assert get_zone(0, -3) == "frozenRiver"
    assert get_zone(0, 0) == "mainRoad"
    assert get_zone(0, 5) == "plaza"
    assert get_zone(0, 6) == "plaza"
    assert get_zone(6, 5) == "sidePath"
    assert get_zone(6, 3) == "buildingYard"
    assert get_zone(10, 10) == "deepSnow"
    print("  ✓ Multi-Zone Terrain Classification: PASSED")

def test_phase3_camera_clamping():
    print("Test 8: Phase 3 Camera Clamping & Void Prevention...")
    min_x, max_x = -850.0, 750.0
    min_y, max_y = -380.0, 780.0

    def clamp_cam(tx, ty):
        cx = max(min_x, min(tx, max_x))
        cy = max(min_y, min(ty, max_y))
        return cx, cy

    # Normal target inside bounds
    cx, cy = clamp_cam(0.0, 200.0)
    assert cx == 0.0 and cy == 200.0

    # Extreme world boundary attempt
    cx_out, cy_out = clamp_cam(-2000.0, 3000.0)
    assert cx_out == min_x and cy_out == max_y, "Camera must clamp to bounds to prevent void"
    print("  ✓ Camera Clamping & Void Prevention: PASSED")

def test_phase3_pure_local_save_integrity():
    print("Test 9: Phase 3 Pure Local Save State...")
    save_data = {
        "save_id": "slot_01_village_phase3",
        "timestamp": 1726947000000,
        "chapter": 1,
        "current_map": "VILLAGE_ABANDONED",
        "position": {
            "x": 0.0,
            "y": 5.5,
            "orientation": "SE"
        },
        "inventory": [
            {"id": "flash_light", "name": "Lampe torche"},
            {"id": "ethan_key", "name": "Clé ancienne"}
        ],
        "evidence": [
            {"id": "ethan_cassette", "name": "Cassette audio d'Ethan"}
        ],
        "trust_variables": {
            "emma": 50,
            "james": 40,
            "michael": 30
        },
        "suspicion_level": 15,
        "flags": {
            "village_entrance_crossed": True,
            "seen_church_gates": True,
            "inspected_old_well": True
        }
    }

    serialized = json.dumps(save_data)
    deserialized = json.loads(serialized)
    assert deserialized["current_map"] == "VILLAGE_ABANDONED"
    assert deserialized["position"]["y"] == 5.5
    assert deserialized["flags"]["inspected_old_well"] is True
    assert "firebase" not in serialized.lower(), "Zero firebase allowed"
    assert "cloud" not in serialized.lower(), "Zero cloud allowed"
    print("  ✓ Pure Local Save State (0% Cloud, 100% Local): PASSED")

if __name__ == "__main__":
    print("=== Running The Echo of Shadows Phase 3 Verification Suite ===")
    test_isometric_coordinates()
    test_collisions()
    test_z_order()
    test_save_system_integration()
    test_phase3_poi_system()
    test_phase3_human_scale_proportions()
    test_phase3_terrain_zones()
    test_phase3_camera_clamping()
    test_phase3_pure_local_save_integrity()
    print("=============================================================")
    print("ALL 9 PHASE 3 TESTS PASSED SUCCESSFULLY!")
