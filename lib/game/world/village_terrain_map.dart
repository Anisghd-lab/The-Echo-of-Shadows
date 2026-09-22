import 'dart:math' as math;

/// Represents the environmental terrain type of an isometric ground tile.
enum GroundType {
  snow,
  snowDeep,
  road,
  plaza,
  path,
  bridge,
  dock,
  ice,
  water,
  shore,
  yard,
  cliff,
}

/// Represents an individual cell in the village isometric tile map.
class TerrainTile {
  final int gridX;
  final int gridY;
  final GroundType type;
  final int variant;
  final bool isWalkable;
  final bool hasCollision;

  const TerrainTile({
    required this.gridX,
    required this.gridY,
    required this.type,
    this.variant = 0,
    required this.isWalkable,
    required this.hasCollision,
  });
}

/// Structured tile map data representing the authentic village terrain composition
/// reconstructed from the official blueprint (map du village.png).
class VillageTerrainMap {
  static const int minGridX = -14;
  static const int maxGridX = 14;
  static const int minGridY = -14;
  static const int maxGridY = 14;

  static final Map<int, Map<int, TerrainTile>> _cache = {};

  static void init() {
    _cache.clear();
    for (int y = minGridY; y <= maxGridY; y++) {
      _cache[y] = {};
      for (int x = minGridX; x <= maxGridX; x++) {
        _cache[y]![x] = _computeTile(x, y);
      }
    }
  }

  static TerrainTile getTile(int gx, int gy) {
    if (_cache.isEmpty) init();
    final row = _cache[gy];
    if (row != null) {
      final tile = row[gx];
      if (tile != null) return tile;
    }
    return _computeTile(gx, gy);
  }

  static TerrainTile _computeTile(int gx, int gy) {
    // Deterministic pseudo-random hash for natural variation
    final hVal = ((gx * 73856093) ^ (gy * 19349663)).abs() % 100;
    final sumXy = gx + gy;
    final diffXy = (gx - gy).abs();

    // 1. Wooden Bridge across River Gorge
    if (diffXy <= 1 && sumXy >= 8 && sumXy <= 15) {
      return TerrainTile(
        gridX: gx,
        gridY: gy,
        type: GroundType.bridge,
        variant: hVal % 2,
        isWalkable: true,
        hasCollision: false,
      );
    }

    // 2. River Docks
    final distLeftDock = math.hypot(gx - 2.0, gy - 8.0);
    final distRightDock = math.hypot(gx - 6.0, gy - 6.0);
    if (distLeftDock <= 1.5 || distRightDock <= 1.5) {
      return TerrainTile(
        gridX: gx,
        gridY: gy,
        type: GroundType.dock,
        variant: 0,
        isWalkable: true,
        hasCollision: false,
      );
    }

    // 3. Frozen River & Water Hazard (South Sector)
    if (sumXy >= 12) {
      return TerrainTile(
        gridX: gx,
        gridY: gy,
        type: GroundType.water,
        variant: hVal < 65 ? 0 : 1,
        isWalkable: false,
        hasCollision: true,
      );
    }
    if (sumXy >= 10) {
      return TerrainTile(
        gridX: gx,
        gridY: gy,
        type: GroundType.ice,
        variant: hVal < 70 ? 0 : 1,
        isWalkable: false,
        hasCollision: true,
      );
    }
    if (sumXy == 9) {
      return TerrainTile(
        gridX: gx,
        gridY: gy,
        type: GroundType.shore,
        variant: hVal < 60 ? 0 : 1,
        isWalkable: true,
        hasCollision: false,
      );
    }

    // 4. Central Circular Plaza
    final distCenter = math.hypot(gx.toDouble(), gy.toDouble());
    if (distCenter <= 2.8) {
      return TerrainTile(
        gridX: gx,
        gridY: gy,
        type: GroundType.plaza,
        variant: hVal < 70 ? 0 : 1,
        isWalkable: true,
        hasCollision: false,
      );
    }

    // 5. Main South Avenue
    if (diffXy <= 1 && sumXy >= 2 && sumXy <= 8) {
      return TerrainTile(
        gridX: gx,
        gridY: gy,
        type: GroundType.road,
        variant: hVal < 75 ? 0 : 1,
        isWalkable: true,
        hasCollision: false,
      );
    }

    // 6. Church Hill Ascent (Northeast Branch)
    if (gx >= 0 && gx <= 5 && gy <= 0 && gy >= -8) {
      final lineDist = (gy - (-1.6 * gx)).abs() / math.sqrt(1 + 1.6 * 1.6);
      if (lineDist <= 1.2) {
        return TerrainTile(
          gridX: gx,
          gridY: gy,
          type: GroundType.road,
          variant: hVal < 75 ? 0 : 1,
          isWalkable: true,
          hasCollision: false,
        );
      }
    }

    // 7. Marketplace & Sawmill (Southeast Branch)
    if (gx >= 0 && gx <= 9 && gy >= -2 && gy <= 2 && gy.abs() <= 1.2) {
      return TerrainTile(
        gridX: gx,
        gridY: gy,
        type: GroundType.path,
        variant: hVal < 65 ? 0 : 1,
        isWalkable: true,
        hasCollision: false,
      );
    }

    // 8. West Residential & Farm Trail (Northwest Branch)
    if (gx <= 0 && gx >= -8 && gy >= -4 && gy <= 2) {
      final lineDist = (gy - (-0.4 * gx)).abs() / math.sqrt(1 + 0.16);
      if (lineDist <= 1.2) {
        return TerrainTile(
          gridX: gx,
          gridY: gy,
          type: GroundType.path,
          variant: hVal < 65 ? 0 : 1,
          isWalkable: true,
          hasCollision: false,
        );
      }
    }

    // 9. Watermill Trail (Southwest Branch)
    if (gy >= 2 && gy <= 9 && gx >= -3 && gx <= 4 && (gx - (-1.0)).abs() <= 1.2) {
      return TerrainTile(
        gridX: gx,
        gridY: gy,
        type: GroundType.path,
        variant: hVal < 65 ? 0 : 1,
        isWalkable: true,
        hasCollision: false,
      );
    }

    // 10. Family House Court
    if (gx >= -3 && gx <= -1 && gy >= -6 && gy <= -4) {
      return TerrainTile(
        gridX: gx,
        gridY: gy,
        type: GroundType.yard,
        variant: 0,
        isWalkable: true,
        hasCollision: false,
      );
    }

    // 11. Mountain Cliffs / Perimeters
    if (gx <= -11 || gy <= -12 || (gx >= 11 && gy <= -3)) {
      return TerrainTile(
        gridX: gx,
        gridY: gy,
        type: GroundType.cliff,
        variant: 0,
        isWalkable: false,
        hasCollision: true,
      );
    }

    // 12. General Winter Snow Blanket (with 3 variants)
    return TerrainTile(
      gridX: gx,
      gridY: gy,
      type: hVal >= 90 ? GroundType.snowDeep : GroundType.snow,
      variant: hVal < 70 ? 0 : (hVal < 90 ? 1 : 2),
      isWalkable: true,
      hasCollision: false,
    );
  }
}
