import 'dart:math' as math;
import 'collision_box.dart';
import 'isometric_coordinates.dart';
import 'village_map.dart';
import 'village_terrain_map.dart';

/// Navigation Grid and spatial zone locator for the reconstructed village.
class NavigationGrid {
  final VillageMap map;
  final CollisionManager collisionManager;

  NavigationGrid({
    required this.map,
    required this.collisionManager,
  });

  /// Determines whether continuous world coordinates (wx, wy) can be traversed by characters.
  bool isWalkable(double wx, double wy, {double characterRadius = 0.28}) {
    final scale = IsometricCoordinates.worldScale;

    // 1. World Bounds Check
    if (wx < map.bounds.minWorldX * scale ||
        wx > map.bounds.maxWorldX * scale ||
        wy < map.bounds.minWorldY * scale ||
        wy > map.bounds.maxWorldY * scale) {
      return false;
    }

    // 2. Collision Obstacles Check
    if (collisionManager.checkCollision(wx, wy, characterRadius * scale)) {
      return false;
    }

    // 3. Terrain Tile Walkability Check
    final tile = VillageTerrainMap.getTile((wx / scale).round(), (wy / scale).round());
    if (!tile.isWalkable) {
      if (!isOnBridge(wx, wy) && !isOnDock(wx, wy)) {
        return false;
      }
    }

    // 4. Water Hazard Check (River gorge at south, except when on bridge or docks)
    if (isRiverWater(wx, wy)) {
      if (!isOnBridge(wx, wy) && !isOnDock(wx, wy)) {
        return false;
      }
    }

    return true;
  }

  /// Checks if location is within the frozen river gorge.
  bool isRiverWater(double wx, double wy) {
    final scale = IsometricCoordinates.worldScale;
    // River flows across the south sector: wx + wy >= 10.0 * scale
    return (wx + wy) >= (10.0 * scale);
  }

  /// Checks if location is on the main wooden entrance bridge.
  bool isOnBridge(double wx, double wy) {
    final scale = IsometricCoordinates.worldScale;
    // Bridge spans from (4.5, 4.5) to (7.5, 7.5) with width ~1.2
    final diff = (wx - wy).abs();
    final sum = wx + wy;
    return diff <= (1.2 * scale) && sum >= (8.0 * scale) && sum <= (15.5 * scale);
  }

  /// Checks if location is on one of the wooden docks.
  bool isOnDock(double wx, double wy) {
    final scale = IsometricCoordinates.worldScale;
    // Left dock: wx ~ 2.0, wy ~ 8.5
    final dLeft = math.hypot(wx - 2.0 * scale, wy - 8.5 * scale);
    if (dLeft <= 1.8 * scale) return true;

    // Right cargo dock: wx ~ 6.0, wy ~ 6.0 (lower bank)
    final dRight = math.hypot(wx - 6.0 * scale, wy - 6.0 * scale);
    if (dRight <= 1.8 * scale) return true;

    return false;
  }

  /// Checks if location is on the paved central circular plaza.
  bool isOnPlaza(double wx, double wy) {
    final scale = IsometricCoordinates.worldScale;
    final dist = math.hypot(wx, wy);
    return dist <= (2.6 * scale);
  }

  /// Checks if location is on any recognized paved or cleared road.
  bool isOnRoad(double wx, double wy) {
    final scale = IsometricCoordinates.worldScale;

    // 1. Central Plaza
    if (isOnPlaza(wx, wy)) return true;

    // 2. Main South Avenue (Bridge to Plaza)
    if ((wx - wy).abs() <= (1.2 * scale) && (wx + wy) >= (0.0 * scale) && (wx + wy) <= (9.5 * scale)) {
      return true;
    }

    // 3. Church Hill Ascent (Northeast branch)
    // Runs towards (3.5, -7.5)
    if (wx >= (0.0 * scale) && wx <= (5.0 * scale) && wy <= (0.0 * scale) && wy >= (-8.5 * scale)) {
      final lineDist = ((wy - (-1.8 * wx)) / math.sqrt(1 + 1.8 * 1.8)).abs();
      if (lineDist <= 1.2 * scale) return true;
    }

    // 4. Marketplace & Sawmill Street (Southeast branch)
    // Runs towards (8.5, -1.0)
    if (wx >= (0.0 * scale) && wx <= (9.0 * scale) && wy >= (-2.5 * scale) && wy <= (1.5 * scale)) {
      return true;
    }

    // 5. West Residential & Farm Road (Northwest branch)
    // Runs towards (-5.5, -3.5)
    if (wx <= (0.0 * scale) && wx >= (-8.5 * scale) && wy >= (-4.5 * scale) && wy <= (2.5 * scale)) {
      return true;
    }

    // 6. Watermill Trail (Southwest branch)
    // Runs from bridge junction towards (-2.5, 8.5)
    if (wy >= (2.0 * scale) && wy <= (9.5 * scale) && wx <= (4.5 * scale) && wx >= (-3.5 * scale)) {
      return true;
    }

    return false;
  }

  /// Returns environmental zone identifier at the given coordinate.
  String getZoneAt(double wx, double wy) {
    if (isRiverWater(wx, wy)) {
      if (isOnBridge(wx, wy)) return 'ZONE_BRIDGE_APPROACH';
      if (isOnDock(wx, wy)) return 'ZONE_RIVER_DOCKS';
      return 'ZONE_FROZEN_RIVER';
    }
    if (isOnPlaza(wx, wy)) return 'ZONE_CENTRAL_PLAZA';
    if (isOnRoad(wx, wy)) return 'ZONE_MAIN_AVENUE';

    final scale = IsometricCoordinates.worldScale;
    if (wx >= (1.0 * scale) && wy <= (-3.0 * scale)) {
      if (wx <= (2.5 * scale) && wy >= (-6.0 * scale)) return 'ZONE_CEMETERY';
      return 'ZONE_CHURCH_HILL';
    }
    if (wx >= (3.5 * scale) && wy >= (-2.0 * scale) && wy <= (2.0 * scale)) {
      return 'ZONE_MARKETPLACE';
    }
    if (wx >= (7.0 * scale)) {
      return 'ZONE_LUMBER_YARD';
    }
    if (wx <= (-4.0 * scale) && wy <= (-1.5 * scale)) {
      if (wx <= (-7.0 * scale)) return 'ZONE_WINDMILL_RIDGE';
      return 'ZONE_FARM_FIELD';
    }
    if (wx <= (-1.0 * scale) && wy <= (-6.0 * scale)) {
      return 'ZONE_MINE_PASS';
    }

    return 'ZONE_RESIDENTIAL_WEST';
  }
}
