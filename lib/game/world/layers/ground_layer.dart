import 'dart:math' as math;
import 'dart:ui';
import 'package:flame/components.dart';
import '../asset_registry.dart';
import '../isometric_coordinates.dart';

enum TerrainZone {
  frozenRiver,
  mainRoad,
  plaza,
  sidePath,
  buildingYard,
  deepSnow,
}

/// Layer 1: Multi-zone winter terrain avoiding repetitive tileset appearance.
class GroundLayer extends Component with HasGameRef {
  Sprite? _stoneTileSprite;
  Sprite? _stoneVarSprite;
  Sprite? _snowTileSprite;
  Sprite? _iceTileSprite;

  final int gridRadius;

  GroundLayer({this.gridRadius = 24});

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

  /// Classifies each grid coordinate into a distinct environmental zone.
  TerrainZone _getZone(int x, int y) {
    final scale = IsometricCoordinates.worldScale;
    // 1. Frozen River at entrance
    if (y <= -2.0 * scale) {
      return TerrainZone.frozenRiver;
    }

    // 2. Central Square / Plaza (around world Y: 5.5, X: 0.0)
    final dx = x.toDouble();
    final dy = (y - 5.5 * scale);
    final distToSquare = math.sqrt(dx * dx + dy * dy);
    if (distToSquare <= 2.8 * scale) {
      return TerrainZone.plaza;
    }

    // 3. Main North-South Village Street
    if (x.abs() <= 1.0 * scale && y >= -1.0 * scale && y <= 11.0 * scale) {
      return TerrainZone.mainRoad;
    }

    // 4. Church Path (East branch)
    if (x >= 1.0 * scale && x <= 7.0 * scale && y >= 4.0 * scale && y <= 6.0 * scale) {
      return TerrainZone.sidePath;
    }

    // 5. Cottage Path (West branch)
    if (x <= -1.0 * scale && x >= -6.0 * scale && y >= 4.0 * scale && y <= 9.0 * scale) {
      return TerrainZone.sidePath;
    }

    // 6. Yard around Family House & Church
    if ((x.abs() <= 3.0 * scale && y >= 9.0 * scale && y <= 12.0 * scale) ||
        (x >= 4.0 * scale && x <= 8.0 * scale && y >= 3.0 * scale && y <= 7.0 * scale)) {
      return TerrainZone.buildingYard;
    }

    // 7. General Snow-covered ground
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
