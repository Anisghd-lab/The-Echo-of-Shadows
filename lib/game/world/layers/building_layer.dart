import 'dart:ui';
import 'package:flame/components.dart';
import '../asset_registry.dart';
import '../collision_box.dart';
import '../isometric_coordinates.dart';

class BuildingItem {
  final String id;
  final String assetId;
  final double worldX;
  final double worldY;
  final double displayWidth;
  final double displayHeight;
  final double collisionWidth;
  final double collisionHeight;

  const BuildingItem({
    required this.id,
    required this.assetId,
    required this.worldX,
    required this.worldY,
    required this.displayWidth,
    required this.displayHeight,
    required this.collisionWidth,
    required this.collisionHeight,
  });
}

/// Single visual building component with independent ground Z-ordering.
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

    // Dynamic Z-Order based on base world contact point
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
      // Fallback debug building silhouette
      final paint = Paint()..color = const Color(0xFF64748B);
      canvas.drawRect(Rect.fromLTWH(0, 0, size.x, size.y), paint);
    }
  }
}

/// Layer 3: Main architectural structures of the abandoned village.
class BuildingLayer extends Component with HasGameRef {
  final CollisionManager collisionManager;

  // Canonical buildings in the Village World
  final List<BuildingItem> buildings = const [
    // 1. Abandoned Family House (Objective destination)
    BuildingItem(
      id: 'family_house',
      assetId: GameAssetRegistry.familyHouseExterior,
      worldX: 0.0,
      worldY: 8.0,
      displayWidth: 220,
      displayHeight: 205,
      collisionWidth: 1.2,
      collisionHeight: 1.2,
    ),

    // 2. Village Church (High on the hill)
    BuildingItem(
      id: 'village_church',
      assetId: GameAssetRegistry.villageChurch,
      worldX: 6.0,
      worldY: 5.0,
      displayWidth: 200,
      displayHeight: 260,
      collisionWidth: 1.4,
      collisionHeight: 1.4,
    ),

    // 3. Abandoned Cottage 01
    BuildingItem(
      id: 'village_cottage_01',
      assetId: GameAssetRegistry.villageHouse01,
      worldX: -5.0,
      worldY: 5.0,
      displayWidth: 200,
      displayHeight: 190,
      collisionWidth: 1.2,
      collisionHeight: 1.2,
    ),
  ];

  BuildingLayer({required this.collisionManager});

  @override
  Future<void> onLoad() async {
    for (final b in buildings) {
      // 1. Add visual component with Z-Order
      add(BuildingSpriteComponent(b));

      // 2. Register ground collision box
      collisionManager.addObstacle(
        IsometricCollisionBox(
          id: 'col_${b.id}',
          worldX: b.worldX,
          worldY: b.worldY,
          halfWidth: b.collisionWidth / 2,
          halfHeight: b.collisionHeight / 2,
          label: b.id,
        ),
      );
    }
  }
}
