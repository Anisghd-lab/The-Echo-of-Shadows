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

  GroundLayer({this.gridRadius = 14});

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
    // 1. Frozen River at entrance
    if (y <= -2) {
      return TerrainZone.frozenRiver;
    }

    // 2. Central Square / Plaza (around world Y: 5.5, X: 0.0)
    final dx = x.toDouble();
    final dy = (y - 5.5);
    final distToSquare = math.sqrt(dx * dx + dy * dy);
    if (distToSquare <= 2.8) {
      return TerrainZone.plaza;
    }

    // 3. Main North-South Village Street
    if (x.abs() <= 1 && y >= -1 && y <= 11) {
      return TerrainZone.mainRoad;
    }

    // 4. Church Path (East branch)
    if (x >= 1 && x <= 7 && y >= 4 && y <= 6) {
      return TerrainZone.sidePath;
    }

    // 5. Cottage Path (West branch)
    if (x <= -1 && x >= -6 && y >= 4 && y <= 9) {
      return TerrainZone.sidePath;
    }

    // 6. Yard around Family House & Church
    if ((x.abs() <= 3 && y >= 9 && y <= 12) || (x >= 4 && x <= 8 && y >= 3 && y <= 7)) {
      return TerrainZone.buildingYard;
    }

    // 7. General Snow-covered ground
    return TerrainZone.deepSnow;
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);

    for (var x = -gridRadius; x <= gridRadius; x++) {
      for (var y = -gridRadius; y <= gridRadius; y++) {
        // Organic diamond bounds to blend with forest background
        if (x.abs() + y.abs() > gridRadius + 4) continue;

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

        if (activeSprite != null) {
          activeSprite.render(
            canvas,
            position: Vector2(
              screenPos.x - IsometricCoordinates.halfTileWidth,
              screenPos.y - IsometricCoordinates.halfTileHeight,
            ),
            size: Vector2(
              IsometricCoordinates.tileWidth,
              IsometricCoordinates.tileHeight,
            ),
          );
        } else {
          final path = Path()
            ..moveTo(screenPos.x, screenPos.y - IsometricCoordinates.halfTileHeight)
            ..lineTo(screenPos.x + IsometricCoordinates.halfTileWidth, screenPos.y)
            ..lineTo(screenPos.x, screenPos.y + IsometricCoordinates.halfTileHeight)
            ..lineTo(screenPos.x - IsometricCoordinates.halfTileWidth, screenPos.y)
            ..close();

          canvas.drawPath(path, Paint()..color = fallbackColor);
          canvas.drawPath(
            path,
            Paint()
              ..color = const Color(0x22FFFFFF)
              ..style = PaintingStyle.stroke
              ..strokeWidth = 0.5,
          );
        }
      }
    }
  }
}
