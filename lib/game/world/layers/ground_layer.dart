import 'dart:math' as math;
import 'dart:ui';
import 'package:flame/components.dart';
import '../asset_registry.dart';
import '../isometric_coordinates.dart';

enum TerrainZone {
  frozenRiver,
  woodenBridge,
  plaza,
  mainRoad,
  sidePath,
  buildingYard,
  deepSnow,
}

/// Layer 1: Multi-zone winter terrain reconstructed from Map village .png.
class GroundLayer extends Component with HasGameRef {
  Sprite? _stoneTileSprite;
  Sprite? _stoneVarSprite;
  Sprite? _snowTileSprite;
  Sprite? _iceTileSprite;

  final int gridRadius;

  GroundLayer({this.gridRadius = 39});

  @override
  Future<void> onLoad() async {
    final registry = GameAssetRegistry();

    // Load terrain tile variants
    _stoneTileSprite = await _loadSprite(registry.getPath(GameAssetRegistry.villageStoneSlab));
    _stoneVarSprite = await _loadSprite(registry.getPath(GameAssetRegistry.villageStoneSlabVar));
    _snowTileSprite = await _loadSprite(registry.getPath(GameAssetRegistry.villageSnowSlab));
    _iceTileSprite = await _loadSprite(registry.getPath(GameAssetRegistry.villageIceSlab));
  }

  Future<Sprite?> _loadSprite(String path) async {
    if (path.isEmpty) return null;
    try {
      final img = await gameRef.images.load(path);
      return Sprite(img);
    } catch (_) {
      return null;
    }
  }

  /// Classifies each grid coordinate into a distinct environmental zone based on Map village .png.
  TerrainZone _getZone(int x, int y) {
    final scale = IsometricCoordinates.worldScale;

    // 1. Wooden Bridge across the river gorge
    final isBridge = (x - y).abs() <= (1.2 * scale) &&
        (x + y) >= (8.0 * scale) &&
        (x + y) <= (15.5 * scale);
    if (isBridge) {
      return TerrainZone.woodenBridge;
    }

    // 2. River Docks
    final isLeftDock = math.hypot(x - 2.0 * scale, y - 8.5 * scale) <= (1.8 * scale);
    final isRightDock = math.hypot(x - 6.0 * scale, y - 6.0 * scale) <= (1.8 * scale);
    if (isLeftDock || isRightDock) {
      return TerrainZone.woodenBridge;
    }

    // 3. Frozen River (South Sector)
    if ((x + y) >= 10.0 * scale) {
      return TerrainZone.frozenRiver;
    }

    // 4. Central Circular Plaza (around (0.0, 0.0))
    final distToCenter = math.hypot(x.toDouble(), y.toDouble());
    if (distToCenter <= 2.6 * scale) {
      return TerrainZone.plaza;
    }

    // 5. Main South Avenue (Connecting Bridge to Plaza)
    if ((x - y).abs() <= 1.2 * scale && (x + y) >= 0.0 && (x + y) <= 9.5 * scale) {
      return TerrainZone.mainRoad;
    }

    // 6. Church Hill Ascent (Northeast Branch)
    if (x >= 0.0 && x <= 5.5 * scale && y <= 0.0 && y >= -8.5 * scale) {
      final lineDist = ((y - (-1.8 * x)) / math.sqrt(1 + 1.8 * 1.8)).abs();
      if (lineDist <= 1.4 * scale) return TerrainZone.sidePath;
    }

    // 7. Marketplace & Sawmill Street (Southeast Branch)
    if (x >= 0.0 && x <= 9.5 * scale && y >= -2.5 * scale && y <= 1.8 * scale) {
      return TerrainZone.sidePath;
    }

    // 8. West Residential & Farm Road (Northwest Branch)
    if (x <= 0.0 && x >= -9.0 * scale && y >= -4.5 * scale && y <= 2.5 * scale) {
      return TerrainZone.sidePath;
    }

    // 9. Watermill Trail (Southwest Branch)
    if (y >= 2.0 * scale && y <= 9.5 * scale && x <= 4.5 * scale && x >= -3.5 * scale) {
      return TerrainZone.sidePath;
    }

    // 10. Yards & Enclosures (Farm field, Church yard, Cottage surrounds)
    if ((x <= -4.0 * scale && x >= -7.5 * scale && y <= -1.5 * scale && y >= -5.5 * scale) ||
        (x >= 1.0 * scale && x <= 5.5 * scale && y <= -6.0 * scale && y >= -9.5 * scale)) {
      return TerrainZone.buildingYard;
    }

    // 11. General Deep Winter Snow
    return TerrainZone.deepSnow;
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);

    // Continuous ground coverage: render all tiles in rectangular grid
    // without diamond cutoff to prevent any void exposure at screen corners
    for (var x = -gridRadius; x <= gridRadius; x++) {
      for (var y = -gridRadius; y <= gridRadius; y++) {
        final screenPos = IsometricCoordinates.gridToScreen(x, y);
        final zone = _getZone(x, y);

        Sprite? activeSprite;
        Color fallbackColor;

        switch (zone) {
          case TerrainZone.frozenRiver:
            activeSprite = _iceTileSprite ?? _snowTileSprite;
            fallbackColor = const Color(0xFF1E293B);
            break;
          case TerrainZone.woodenBridge:
            activeSprite = _stoneVarSprite ?? _stoneTileSprite;
            fallbackColor = const Color(0xFF78350F);
            break;
          case TerrainZone.plaza:
            activeSprite = ((x + y) % 2 == 0) ? _stoneTileSprite : _stoneVarSprite;
            fallbackColor = const Color(0xFF475569);
            break;
          case TerrainZone.mainRoad:
            activeSprite = ((x + y) % 3 == 0) ? _stoneVarSprite : _stoneTileSprite;
            fallbackColor = const Color(0xFF334155);
            break;
          case TerrainZone.sidePath:
            activeSprite = _stoneTileSprite ?? _snowTileSprite;
            fallbackColor = const Color(0xFF334155);
            break;
          case TerrainZone.buildingYard:
            activeSprite = ((x * y) % 2 == 0) ? _snowTileSprite : _stoneVarSprite;
            fallbackColor = const Color(0xFF2A3441);
            break;
          case TerrainZone.deepSnow:
            activeSprite = _snowTileSprite ?? _iceTileSprite;
            fallbackColor = const Color(0xFF1A232E);
            break;
        }

        // Add 1.0 px overlap to completely eliminate subpixel rasterization gaps/seams
        if (activeSprite != null) {
          activeSprite.render(
            canvas,
            position: Vector2(
              screenPos.x - IsometricCoordinates.halfTileWidth,
              screenPos.y - IsometricCoordinates.halfTileHeight,
            ),
            size: Vector2(
              IsometricCoordinates.tileWidth + 1.0,
              IsometricCoordinates.tileHeight + 1.0,
            ),
          );
        } else {
          final path = Path()
            ..moveTo(screenPos.x, screenPos.y - IsometricCoordinates.halfTileHeight - 0.5)
            ..lineTo(screenPos.x + IsometricCoordinates.halfTileWidth + 0.5, screenPos.y)
            ..lineTo(screenPos.x, screenPos.y + IsometricCoordinates.halfTileHeight + 0.5)
            ..lineTo(screenPos.x - IsometricCoordinates.halfTileWidth - 0.5, screenPos.y)
            ..close();

          canvas.drawPath(path, Paint()..color = fallbackColor);
        }
      }
    }
  }
}
