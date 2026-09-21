import 'package:flame/components.dart';
import '../player/alex_component.dart';
import '../player/player_animation_controller.dart';
import '../player/player_controller.dart';
import 'collision_box.dart';
import 'layers/building_layer.dart';
import 'layers/characters_layer.dart';
import 'layers/ground_layer.dart';
import 'layers/prop_layer.dart';
import 'layers/road_layer.dart';
import 'layers/weather_effects_layer.dart';

/// The root Flame World component for the Abandoned Village scene.
class VillageWorld extends World with HasGameRef {
  final CollisionManager collisionManager = CollisionManager();
  late final PlayerController playerController;
  late final PlayerAnimationController playerAnimationController;
  late final AlexComponent alex;

  // World boundaries in continuous isometric units
  final double minWorldX = -12.0;
  final double maxWorldX = 12.0;
  final double minWorldY = -12.0;
  final double maxWorldY = 12.0;

  final double initialPlayerX;
  final double initialPlayerY;
  final String initialOrientation;

  VillageWorld({
    this.initialPlayerX = 0.0,
    this.initialPlayerY = 0.0,
    this.initialOrientation = 'SE',
  });

  @override
  Future<void> onLoad() async {
    // 1. Initialize Player Controllers
    playerController = PlayerController(
      worldX: initialPlayerX,
      worldY: initialPlayerY,
      orientation: initialOrientation,
      collisionManager: collisionManager,
    );

    playerAnimationController = PlayerAnimationController();
    await playerAnimationController.load(gameRef);

    alex = AlexComponent(
      controller: playerController,
      animationController: playerAnimationController,
    );

    // 2. Add Perimeter World Boundary Collisions
    _addPerimeterCollisions();

    // 3. Mount Layers in strict isometric order
    // Ground
    add(GroundLayer());

    // Roads & Pathways
    add(RoadLayer());

    // Buildings (with collision registration)
    add(BuildingLayer(collisionManager: collisionManager));

    // Props (with collision registration)
    add(PropLayer(collisionManager: collisionManager));

    // Characters (dynamically sorted)
    add(CharactersLayer(alex: alex));

    // Weather Effects
    add(WeatherEffectsLayer());
  }

  void _addPerimeterCollisions() {
    // Left boundary
    collisionManager.addObstacle(
      IsometricCollisionBox(
        id: 'boundary_left',
        worldX: minWorldX - 1.0,
        worldY: 0.0,
        halfWidth: 1.0,
        halfHeight: maxWorldY,
        label: 'boundary',
      ),
    );
    // Right boundary
    collisionManager.addObstacle(
      IsometricCollisionBox(
        id: 'boundary_right',
        worldX: maxWorldX + 1.0,
        worldY: 0.0,
        halfWidth: 1.0,
        halfHeight: maxWorldY,
        label: 'boundary',
      ),
    );
    // Top boundary
    collisionManager.addObstacle(
      IsometricCollisionBox(
        id: 'boundary_top',
        worldX: 0.0,
        worldY: minWorldY - 1.0,
        halfWidth: maxWorldX,
        halfHeight: 1.0,
        label: 'boundary',
      ),
    );
    // Bottom boundary
    collisionManager.addObstacle(
      IsometricCollisionBox(
        id: 'boundary_bottom',
        worldX: 0.0,
        worldY: maxWorldY + 1.0,
        halfWidth: maxWorldX,
        halfHeight: 1.0,
        label: 'boundary',
      ),
    );
  }
}
