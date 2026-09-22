import 'dart:ui';
import 'package:flame/components.dart';
import '../asset_registry.dart';
import '../isometric_coordinates.dart';
import '../village_terrain_map.dart';

/// Layer 1: Multi-zone winter terrain reconstructed from Map village .png.
/// Uses authentic dimetric diamond ground tiles (snow, road, plaza, bridge, water, ice)
/// without artificial tile repetition.
class GroundLayer extends Component with HasGameRef {
  // Authentic diamond tiles
  Sprite? _snowSpriteA;
  Sprite? _snowSpriteB;
  Sprite? _snowSpriteC;
  Sprite? _roadSpriteA;
  Sprite? _roadSpriteB;
  Sprite? _plazaSpriteA;
  Sprite? _plazaSpriteB;
  Sprite? _pathSpriteA;
  Sprite? _pathSpriteB;
  Sprite? _bridgeSprite;
  Sprite? _dockSprite;
  Sprite? _iceSpriteA;
  Sprite? _iceSpriteB;
  Sprite? _waterSpriteA;
  Sprite? _waterSpriteB;
  Sprite? _shoreSpriteA;
  Sprite? _shoreSpriteB;
  Sprite? _yardSprite;
  Sprite? _cliffSprite;

  final int gridRadius;

  GroundLayer({this.gridRadius = 18});

  @override
  Future<void> onLoad() async {
    VillageTerrainMap.init();
    final registry = GameAssetRegistry();

    _snowSpriteA = await _loadSprite(registry.getPath(GameAssetRegistry.villageSnowSlab));
    _snowSpriteB = await _loadSprite(registry.getPath(GameAssetRegistry.villageSnowVar));
    _snowSpriteC = await _loadSprite(registry.getPath(GameAssetRegistry.villageDeepSnow));

    _roadSpriteA = await _loadSprite(registry.getPath(GameAssetRegistry.villageStoneSlab));
    _roadSpriteB = await _loadSprite(registry.getPath(GameAssetRegistry.villageStoneSlabVar));

    _plazaSpriteA = await _loadSprite(registry.getPath(GameAssetRegistry.villagePlazaTile));
    _plazaSpriteB = await _loadSprite(registry.getPath(GameAssetRegistry.villagePlazaTileVar));

    _pathSpriteA = await _loadSprite(registry.getPath(GameAssetRegistry.villageDirtTrail));
    _pathSpriteB = await _loadSprite(registry.getPath(GameAssetRegistry.villageDirtTrailVar));

    _bridgeSprite = await _loadSprite(registry.getPath(GameAssetRegistry.villageBridgePlank));
    _dockSprite = await _loadSprite(registry.getPath(GameAssetRegistry.villageDockPlank));

    _iceSpriteA = await _loadSprite(registry.getPath(GameAssetRegistry.villageIceSlab));
    _iceSpriteB = await _loadSprite(registry.getPath(GameAssetRegistry.villageIceSlush));

    _waterSpriteA = await _loadSprite(registry.getPath(GameAssetRegistry.villageRiverWater));
    _waterSpriteB = await _loadSprite(registry.getPath(GameAssetRegistry.villageRiverWaterDeep));

    _shoreSpriteA = await _loadSprite(registry.getPath(GameAssetRegistry.villageRiverBank));
    _shoreSpriteB = await _loadSprite(registry.getPath(GameAssetRegistry.villageFrostedShore));

    _yardSprite = await _loadSprite(registry.getPath(GameAssetRegistry.villageFrostedShore));
    _cliffSprite = await _loadSprite(registry.getPath(GameAssetRegistry.villageCliff));
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

  Sprite? _resolveTileSprite(TerrainTile tile) {
    switch (tile.type) {
      case GroundType.snow:
        return tile.variant == 0 ? _snowSpriteA : _snowSpriteB;
      case GroundType.snowDeep:
        return _snowSpriteC ?? _snowSpriteB ?? _snowSpriteA;
      case GroundType.road:
        return tile.variant == 0 ? _roadSpriteA : _roadSpriteB;
      case GroundType.plaza:
        return tile.variant == 0 ? _plazaSpriteA : _plazaSpriteB;
      case GroundType.path:
        return tile.variant == 0 ? _pathSpriteA : _pathSpriteB;
      case GroundType.bridge:
        return _bridgeSprite ?? _roadSpriteA;
      case GroundType.dock:
        return _dockSprite ?? _bridgeSprite;
      case GroundType.ice:
        return tile.variant == 0 ? _iceSpriteA : _iceSpriteB;
      case GroundType.water:
        return tile.variant == 0 ? _waterSpriteA : _waterSpriteB;
      case GroundType.shore:
        return tile.variant == 0 ? _shoreSpriteA : _shoreSpriteB;
      case GroundType.yard:
        return _yardSprite ?? _shoreSpriteB;
      case GroundType.cliff:
        return _cliffSprite;
    }
  }

  Color _resolveFallbackColor(GroundType type) {
    switch (type) {
      case GroundType.snow:
      case GroundType.snowDeep:
        return const Color(0xFFCAD5E2);
      case GroundType.road:
      case GroundType.plaza:
        return const Color(0xFF64748B);
      case GroundType.path:
      case GroundType.yard:
        return const Color(0xFF78716C);
      case GroundType.bridge:
      case GroundType.dock:
        return const Color(0xFF92400E);
      case GroundType.ice:
        return const Color(0xFF7DD3FC);
      case GroundType.water:
        return const Color(0xFF1E3A8A);
      case GroundType.shore:
        return const Color(0xFF475569);
      case GroundType.cliff:
        return const Color(0xFF1E293B);
    }
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);

    final tw = IsometricCoordinates.tileWidth;
    final th = IsometricCoordinates.tileHeight;
    final hw = IsometricCoordinates.halfTileWidth;
    final hh = IsometricCoordinates.halfTileHeight;

    // Continuous multi-zone diamond ground rendering
    for (var x = -gridRadius; x <= gridRadius; x++) {
      for (var y = -gridRadius; y <= gridRadius; y++) {
        final screenPos = IsometricCoordinates.gridToScreen(x, y);
        final tile = VillageTerrainMap.getTile(x, y);

        final sprite = _resolveTileSprite(tile);

        if (sprite != null) {
          // Render with 1.0 px overlap to ensure clean rasterization without seams
          sprite.render(
            canvas,
            position: Vector2(screenPos.x - hw, screenPos.y - hh),
            size: Vector2(tw + 1.0, th + 1.0),
          );
        } else {
          final fallbackColor = _resolveFallbackColor(tile.type);
          final path = Path()
            ..moveTo(screenPos.x, screenPos.y - hh - 0.5)
            ..lineTo(screenPos.x + hw + 0.5, screenPos.y)
            ..lineTo(screenPos.x, screenPos.y + hh + 0.5)
            ..lineTo(screenPos.x - hw - 0.5, screenPos.y)
            ..close();

          canvas.drawPath(path, Paint()..color = fallbackColor);
        }
      }
    }
  }
}

