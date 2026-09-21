import 'dart:ui';
import 'package:flame/components.dart';
import '../asset_registry.dart';
import '../collision_box.dart';
import '../isometric_coordinates.dart';
import '../point_of_interest.dart';

class PropItem {
  final String id;
  final String assetId;
  final double worldX;
  final double worldY;
  final double displayWidth;
  final double displayHeight;
  final double collisionWidth;
  final double collisionHeight;
  final bool hasCollision;

  const PropItem({
    required this.id,
    required this.assetId,
    required this.worldX,
    required this.worldY,
    required this.displayWidth,
    required this.displayHeight,
    this.collisionWidth = 0.5,
    this.collisionHeight = 0.5,
    this.hasCollision = true,
  });
}

class PropSpriteComponent extends PositionComponent with HasGameRef {
  final PropItem prop;
  Sprite? _sprite;

  PropSpriteComponent(this.prop) {
    anchor = Anchor.bottomCenter;
    size = Vector2(prop.displayWidth, prop.displayHeight);

    final screenPos = IsometricCoordinates.worldToScreen(prop.worldX, prop.worldY);
    position = Vector2(screenPos.x, screenPos.y);

    // Dynamic Z-Order based on base ground contact point
    priority = IsometricCoordinates.calculateZOrder(
      prop.worldX,
      prop.worldY,
      layerBase: IsometricCoordinates.zOrderProps,
    );
  }

  @override
  Future<void> onLoad() async {
    final registry = GameAssetRegistry();
    final path = registry.getPath(prop.assetId);
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
    }
  }
}

/// Layer 4: Environmental props composed for realistic spatial storytelling.
class PropLayer extends Component with HasGameRef {
  final CollisionManager collisionManager;

  final List<PropItem> props = const [
    // 1. Ancient Stone Well at the Village Square
    PropItem(
      id: 'old_well',
      assetId: GameAssetRegistry.villageWell,
      worldX: 0.0,
      worldY: 6.0,
      displayWidth: 100,
      displayHeight: 112,
      collisionWidth: 0.8,
      collisionHeight: 0.8,
      hasCollision: true,
    ),

    // 2. Iron Gate to Cemetery & Church Path
    PropItem(
      id: 'church_cemetery_gate',
      assetId: GameAssetRegistry.villageIronGate,
      worldX: 4.2,
      worldY: 5.0,
      displayWidth: 130,
      displayHeight: 84,
      collisionWidth: 0.8,
      collisionHeight: 0.3,
      hasCollision: true,
    ),

    // 3. Iron Gate to West Cottages
    PropItem(
      id: 'cottage_gate',
      assetId: GameAssetRegistry.villageIronGate,
      worldX: -3.6,
      worldY: 4.5,
      displayWidth: 130,
      displayHeight: 84,
      collisionWidth: 0.8,
      collisionHeight: 0.3,
      hasCollision: true,
    ),

    // 4. Street Lamps along the Main Road
    PropItem(
      id: 'street_lamp_01',
      assetId: GameAssetRegistry.villageStreetLamp,
      worldX: -1.2,
      worldY: 1.5,
      displayWidth: 38,
      displayHeight: 96,
      collisionWidth: 0.3,
      collisionHeight: 0.3,
      hasCollision: true,
    ),
    PropItem(
      id: 'street_lamp_02',
      assetId: GameAssetRegistry.villageStreetLamp,
      worldX: 1.2,
      worldY: 4.0,
      displayWidth: 38,
      displayHeight: 96,
      collisionWidth: 0.3,
      collisionHeight: 0.3,
      hasCollision: true,
    ),
    PropItem(
      id: 'street_lamp_03',
      assetId: GameAssetRegistry.villageStreetLamp,
      worldX: -1.2,
      worldY: 8.5,
      displayWidth: 38,
      displayHeight: 96,
      collisionWidth: 0.3,
      collisionHeight: 0.3,
      hasCollision: true,
    ),

    // 5. Pine Trees & Dead Trees (Environmental framing)
    PropItem(
      id: 'pine_church_01',
      assetId: GameAssetRegistry.villagePineTree,
      worldX: 8.5,
      worldY: 3.5,
      displayWidth: 90,
      displayHeight: 86,
      collisionWidth: 0.5,
      collisionHeight: 0.5,
      hasCollision: true,
    ),
    PropItem(
      id: 'pine_church_02',
      assetId: GameAssetRegistry.villagePineTree,
      worldX: 5.5,
      worldY: 3.0,
      displayWidth: 85,
      displayHeight: 80,
      collisionWidth: 0.5,
      collisionHeight: 0.5,
      hasCollision: true,
    ),
    PropItem(
      id: 'dead_tree_cemetery',
      assetId: GameAssetRegistry.villageDeadTree,
      worldX: 7.2,
      worldY: 6.8,
      displayWidth: 80,
      displayHeight: 132,
      collisionWidth: 0.4,
      collisionHeight: 0.4,
      hasCollision: true,
    ),
    PropItem(
      id: 'pine_west_01',
      assetId: GameAssetRegistry.villagePineTree,
      worldX: -7.0,
      worldY: 3.0,
      displayWidth: 95,
      displayHeight: 90,
      collisionWidth: 0.5,
      collisionHeight: 0.5,
      hasCollision: true,
    ),
    PropItem(
      id: 'pine_west_02',
      assetId: GameAssetRegistry.villagePineTree,
      worldX: -7.5,
      worldY: 7.0,
      displayWidth: 95,
      displayHeight: 90,
      collisionWidth: 0.5,
      collisionHeight: 0.5,
      hasCollision: true,
    ),
    PropItem(
      id: 'dead_tree_family_house',
      assetId: GameAssetRegistry.villageDeadTree,
      worldX: 2.2,
      worldY: 10.0,
      displayWidth: 80,
      displayHeight: 132,
      collisionWidth: 0.4,
      collisionHeight: 0.4,
      hasCollision: true,
    ),

    // 6. Natural Perimeter Cliffs (avoiding empty void)
    PropItem(
      id: 'north_cliff_01',
      assetId: GameAssetRegistry.villageCliff,
      worldX: -3.5,
      worldY: 12.5,
      displayWidth: 220,
      displayHeight: 260,
      collisionWidth: 1.8,
      collisionHeight: 1.0,
      hasCollision: true,
    ),
    PropItem(
      id: 'north_cliff_02',
      assetId: GameAssetRegistry.villageCliff,
      worldX: 4.0,
      worldY: 12.0,
      displayWidth: 220,
      displayHeight: 260,
      collisionWidth: 1.8,
      collisionHeight: 1.0,
      hasCollision: true,
    ),
  ];

  PropLayer({required this.collisionManager});

  @override
  Future<void> onLoad() async {
    for (final p in props) {
      add(PropSpriteComponent(p));

      if (p.hasCollision) {
        collisionManager.addObstacle(
          IsometricCollisionBox(
            id: 'col_${p.id}',
            worldX: p.worldX,
            worldY: p.worldY,
            halfWidth: p.collisionWidth / 2,
            halfHeight: p.collisionHeight / 2,
            label: p.id,
          ),
        );
      }
    }
  }
}
