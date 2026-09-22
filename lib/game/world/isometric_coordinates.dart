import 'dart:math' as math;

/// Centralized Isometric Coordinate Engine for L'Écho des Ombres.
///
/// Standard 2:1 Dimetric Isometric projection:
/// - tileWidth: 128 px
/// - tileHeight: 64 px
///
/// Coordinate conventions:
/// - World coordinates (worldX, worldY): continuous logical game world units.
/// - Screen coordinates (screenX, screenY): 2D pixel coordinates rendered on canvas.
/// - Grid coordinates (gridX, gridY): integer tile indices.
class IsometricCoordinates {
  // Canonical isometric tile dimensions (Phase 3.3 Fine Cobblestones & High Density Paving)
  // Default: 80x40 px (strict 2:1 dimetric ratio, 2.56x tile density)
  static double tileWidth = 80.0;
  static double tileHeight = 40.0;
  static double get halfTileWidth => tileWidth / 2.0;
  static double get halfTileHeight => tileHeight / 2.0;

  /// Ratio relative to baseline 128x64 grid.
  /// Preserves world physical layout and pixel alignment while scaling tile density.
  static double get worldScale => 128.0 / tileWidth;

  /// Sets tile dimensions while strictly maintaining dimetric 2:1 aspect ratio.
  static void setTileDimensions(double width, double height) {
    if (width / height != 2.0) {
      throw ArgumentError('Tile dimensions must strictly preserve 2:1 ratio (width / height == 2)');
    }
    tileWidth = width;
    tileHeight = height;
  }

  /// Resets to Phase 3.3 canonical default (80x40).
  static void resetToDefault() {
    tileWidth = 80.0;
    tileHeight = 40.0;
  }

  // Layer base offsets for Z-ordering
  static const int zOrderGround = 0;
  static const int zOrderRoad = 10000;
  static const int zOrderBuilding = 20000;
  static const int zOrderProps = 30000;
  static const int zOrderCharacters = 40000;
  static const int zOrderWeather = 90000;
  static const int zOrderUI = 100000;

  /// Converts continuous world coordinates (x, y) to 2D screen coordinates.
  /// Formula:
  /// screenX = (worldX - worldY) * halfTileWidth
  /// screenY = (worldX + worldY) * halfTileHeight
  static Point2D worldToScreen(double worldX, double worldY) {
    final screenX = (worldX - worldY) * halfTileWidth;
    final screenY = (worldX + worldY) * halfTileHeight;
    return Point2D(screenX, screenY);
  }

  /// Converts 2D screen coordinates back to continuous world coordinates.
  static Point2D screenToWorld(double screenX, double screenY) {
    final worldX = (screenX / halfTileWidth + screenY / halfTileHeight) / 2.0;
    final worldY = (screenY / halfTileHeight - screenX / halfTileWidth) / 2.0;
    return Point2D(worldX, worldY);
  }

  /// Converts integer grid coordinates (tileX, tileY) to the screen center of that tile.
  static Point2D gridToScreen(int gridX, int gridY) {
    return worldToScreen(gridX.toDouble(), gridY.toDouble());
  }

  /// Converts screen coordinates to the containing integer grid tile (gridX, gridY).
  static GridIndex screenToGrid(double screenX, double screenY) {
    final world = screenToWorld(screenX, screenY);
    return GridIndex(world.x.floor(), world.y.floor());
  }

  /// Calculates dynamic depth priority (Z-Order) for sorting sprites.
  /// Characters and dynamic props use their ground contact base (worldX, worldY).
  /// Objects with higher (worldX + worldY) are rendered in front.
  static int calculateZOrder(double worldX, double worldY, {int layerBase = zOrderCharacters}) {
    // Each world unit corresponds to 100 depth levels for fine sub-tile ordering
    final depth = ((worldX + worldY) * 100).round();
    return layerBase + depth;
  }

  /// Calculates direction vector to canonical 4-way isometric orientation:
  /// - 'SE': (+X, +Y screen direction, facing viewer-right / South-East)
  /// - 'SW': (-X, +Y screen direction, facing viewer-left / South-West)
  /// - 'NE': (+X, -Y screen direction, facing back-right / North-East)
  /// - 'NW': (-X, -Y screen direction, facing back-left / North-West)
  static String vectorToOrientation(double dx, double dy) {
    if (dx == 0 && dy == 0) return 'SE';

    final angle = math.atan2(dy, dx); // [-PI, PI]
    // Map angle to 4 isometric directions:
    // Angle in degrees: 0 is Right, 90 is Down, 180/-180 is Left, -90 is Up
    if (angle >= 0 && angle < math.pi / 2) {
      return 'SE'; // Down-Right
    } else if (angle >= math.pi / 2 && angle <= math.pi) {
      return 'SW'; // Down-Left
    } else if (angle >= -math.pi && angle < -math.pi / 2) {
      return 'NW'; // Up-Left
    } else {
      return 'NE'; // Up-Right
    }
  }

  /// Calculates direction vector to true 8-way orientation (Cardinal + Isometric):
  /// - 'E':  [-22.5°, 22.5°)
  /// - 'SE': [22.5°, 67.5°)
  /// - 'S':  [67.5°, 112.5°)
  /// - 'SW': [112.5°, 157.5°)
  /// - 'W':  >= 157.5° or < -157.5°
  /// - 'NW': [-157.5°, -112.5°)
  /// - 'N':  [-112.5°, -67.5°)
  /// - 'NE': [-67.5°, -22.5°)
  static String vectorToOrientation8Way(double dx, double dy) {
    if (dx == 0 && dy == 0) return 'SE';
    final angle = math.atan2(dy, dx);
    if (angle >= -math.pi / 8 && angle < math.pi / 8) {
      return 'E';
    } else if (angle >= math.pi / 8 && angle < 3 * math.pi / 8) {
      return 'SE';
    } else if (angle >= 3 * math.pi / 8 && angle < 5 * math.pi / 8) {
      return 'S';
    } else if (angle >= 5 * math.pi / 8 && angle < 7 * math.pi / 8) {
      return 'SW';
    } else if (angle >= -3 * math.pi / 8 && angle < -math.pi / 8) {
      return 'NE';
    } else if (angle >= -5 * math.pi / 8 && angle < -3 * math.pi / 8) {
      return 'N';
    } else if (angle >= -7 * math.pi / 8 && angle < -5 * math.pi / 8) {
      return 'NW';
    } else {
      return 'W';
    }
  }
}

class Point2D {
  final double x;
  final double y;
  const Point2D(this.x, this.y);

  @override
  String toString() => 'Point2D($x, $y)';
}

class GridIndex {
  final int x;
  final int y;
  const GridIndex(this.x, this.y);

  @override
  String toString() => 'GridIndex($x, $y)';
}
