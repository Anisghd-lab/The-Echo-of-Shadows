import 'dart:ui';
import 'package:flame/components.dart';
import '../asset_registry.dart';
import '../collision_box.dart';
import '../isometric_coordinates.dart';
import '../village_map.dart';

class BuildingItem {
  final String id;
  final String poiId;
  final String assetId;
  final double worldX;
  final double worldY;
  final double displayWidth;
  final double displayHeight;
  final double collisionWidth;
  final double collisionHeight;
  final double collisionOffsetY;

  const BuildingItem({
    required this.id,
    required this.poiId,
    required this.assetId,
    required this.worldX,
    required this.worldY,
    required this.displayWidth,
    required this.displayHeight,
    required this.collisionWidth,
    required this.collisionHeight,
    this.collisionOffsetY = 0.0,
  });

  factory BuildingItem.fromMapBuilding(MapBuilding b) {
    return BuildingItem(
      id: b.id,
      poiId: b.poiId,
      assetId: b.assetId,
      worldX: b.worldX,
      worldY: b.worldY,
      displayWidth: b.displayWidth,
      displayHeight: b.displayHeight,
      collisionWidth: b.collisionHalfWidth * 2.0,
      collisionHeight: b.collisionHalfHeight * 2.0,
      collisionOffsetY: b.collisionOffsetY,
    );
  }
}

class BuildingSpriteComponent extends PositionComponent with HasGameRef {
  final BuildingItem building;
  Sprite? _sprite;

  BuildingSpriteComponent(this.building) {
    anchor = Anchor.bottomCenter;
    size = Vector2(building.displayWidth, building.displayHeight);

    final scale = IsometricCoordinates.worldScale;
    final wx = building.worldX * scale;
    final wy = building.worldY * scale;

    final screenPos = IsometricCoordinates.worldToScreen(wx, wy);
    position = Vector2(screenPos.x, screenPos.y);

    // Z-Order: dynamic priority anchored at the base of the foundation
    priority = IsometricCoordinates.calculateZOrder(
      wx,
      wy,
      layerBase: IsometricCoordinates.zOrderBuilding,
    );
  }

  @override
  Future<void> onLoad() async {
    final registry = GameAssetRegistry();
    final path = registry.getPath(building.assetId);
    if (path.isNotEmpty) {
      try {
        final image = await gameRef.images.load(path);
        _sprite = Sprite(image);
      } catch (_) {}
    }
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);
    if (_sprite != null) {
      _sprite!.render(canvas, position: Vector2.zero(), size: size);
    } else {
      final paint = Paint()..color = const Color(0xFF64748B);
      canvas.drawRect(Rect.fromLTWH(0, 0, size.x, size.y), paint);
    }
  }
}

/// Layer 3: Main buildings of the village reconstructed from Map village .png.
class BuildingLayer extends Component with HasGameRef {
  final CollisionManager collisionManager;
  final VillageMap? villageMap;

  BuildingLayer({
    required this.collisionManager,
    this.villageMap,
  });

  List<BuildingItem> get buildings {
    final vMap = villageMap ?? VillageMap.canonical();
    return vMap.buildings.map((b) => BuildingItem.fromMapBuilding(b)).toList();
  }

  @override
  Future<void> onLoad() async {
    final scale = IsometricCoordinates.worldScale;
    for (final b in buildings) {
      add(BuildingSpriteComponent(b));

      collisionManager.addObstacle(
        IsometricCollisionBox(
          id: 'col_${b.id}',
          worldX: b.worldX * scale,
          worldY: (b.worldY + b.collisionOffsetY) * scale,
          halfWidth: (b.collisionWidth / 2) * scale,
          halfHeight: (b.collisionHeight / 2) * scale,
          label: b.id,
        ),
      );
    }
  }
}
