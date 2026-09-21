import 'dart:ui';
import 'package:flame/components.dart';
import '../asset_registry.dart';
import '../collision_box.dart';
import '../isometric_coordinates.dart';
import '../point_of_interest.dart';

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
}

class BuildingSpriteComponent extends PositionComponent with HasGameRef {
  final BuildingItem building;
  Sprite? _sprite;

  BuildingSpriteComponent(this.building) {
    anchor = Anchor.bottomCenter;
    size = Vector2(building.displayWidth, building.displayHeight);

    final screenPos = IsometricCoordinates.worldToScreen(
      building.worldX,
      building.worldY,
    );
    position = Vector2(screenPos.x, screenPos.y);

    // Z-Order: dynamic priority anchored at the base of the foundation
    priority = IsometricCoordinates.calculateZOrder(
      building.worldX,
      building.worldY,
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

/// Layer 3: Main buildings of the village with calibrated scales and ground collision footprints.
class BuildingLayer extends Component with HasGameRef {
  final CollisionManager collisionManager;

  final List<BuildingItem> buildings = const [
    // 1. Family House (Destination at north end of main street)
    BuildingItem(
      id: 'family_house',
      poiId: VillagePOIRegistry.familyHouse,
      assetId: GameAssetRegistry.familyHouseExterior,
      worldX: 0.0,
      worldY: 10.5,
      displayWidth: 320,
      displayHeight: 298,
      collisionWidth: 1.8,
      collisionHeight: 1.2,
      collisionOffsetY: -0.2,
    ),

    // 2. St. Jude Abandoned Church (East Hill)
    BuildingItem(
      id: 'village_church',
      poiId: VillagePOIRegistry.abandonedChurch,
      assetId: GameAssetRegistry.villageChurch,
      worldX: 6.5,
      worldY: 5.0,
      displayWidth: 280,
      displayHeight: 370,
      collisionWidth: 2.0,
      collisionHeight: 1.6,
      collisionOffsetY: -0.3,
    ),

    // 3. Abandoned Cottage 01 (West Path South)
    BuildingItem(
      id: 'abandoned_house_01',
      poiId: VillagePOIRegistry.abandonedHouse01,
      assetId: GameAssetRegistry.villageHouse01,
      worldX: -5.5,
      worldY: 4.5,
      displayWidth: 260,
      displayHeight: 244,
      collisionWidth: 1.6,
      collisionHeight: 1.2,
      collisionOffsetY: -0.2,
    ),

    // 4. Abandoned Cottage 02 (West Path North)
    BuildingItem(
      id: 'abandoned_house_02',
      poiId: VillagePOIRegistry.abandonedHouse02,
      assetId: GameAssetRegistry.villageHouse02,
      worldX: -5.5,
      worldY: 8.5,
      displayWidth: 240,
      displayHeight: 270,
      collisionWidth: 1.5,
      collisionHeight: 1.2,
      collisionOffsetY: -0.2,
    ),
  ];

  BuildingLayer({required this.collisionManager});

  @override
  Future<void> onLoad() async {
    for (final b in buildings) {
      add(BuildingSpriteComponent(b));

      collisionManager.addObstacle(
        IsometricCollisionBox(
          id: 'col_${b.id}',
          worldX: b.worldX,
          worldY: b.worldY + b.collisionOffsetY,
          halfWidth: b.collisionWidth / 2,
          halfHeight: b.collisionHeight / 2,
          label: b.id,
        ),
      );
    }
  }
}
