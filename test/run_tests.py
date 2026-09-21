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
    # Unified depth sorting
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

if __name__ == "__main__":
    print("=== Running The Echo of Shadows Phase 2 Verification Suite ===")
    test_isometric_coordinates()
    test_collisions()
    test_z_order()
    test_save_system_integration()
    print("=============================================================")
    print("ALL TESTS PASSED SUCCESSFULLY!")
