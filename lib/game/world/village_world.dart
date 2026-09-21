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
import 'point_of_interest.dart';

/// The root Flame World component for the Abandoned Village scene.
class VillageWorld extends World with HasGameRef {
  final CollisionManager collisionManager = CollisionManager();
  late final PlayerController playerController;
  late final PlayerAnimationController playerAnimationController;
  late final AlexComponent alex;

  // Calibrated world boundaries enclosing the village composition
  final double minWorldX = -9.0;
  final double maxWorldX = 10.0;
  final double minWorldY = -2.5;
  final double maxWorldY = 13.5;

  final double initialPlayerX;
  final double initialPlayerY;
  final String initialOrientation;

  // Active Point of Interest
  PointOfInterest? activePOI;

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
    // Ground (Multi-zone: River, Cobblestones, Plaza, Snow, Yards)
    add(GroundLayer(gridRadius: 15));

    // Roads & Pathways
    add(RoadLayer());

    // Buildings (Church, Family House, Cottages)
    add(BuildingLayer(collisionManager: collisionManager));

    // Props (Well, Gates, Street Lamps, Pine & Dead Trees, Cliffs)
    add(PropLayer(collisionManager: collisionManager));

    // Characters (Alex with calibrated human scale and dynamic Z-ordering)
    add(CharactersLayer(alex: alex));

    // Atmospheric Weather (Wind-driven snow, freezing sleet, fog mist)
    add(WeatherEffectsLayer());
  }

  @override
  void update(double dt) {
    super.update(dt);
    // Check nearest Point of Interest
    activePOI = VillagePOIRegistry.findActivePOI(
      playerController.worldX,
      playerController.worldY,
    );
  }

  void _addPerimeterCollisions() {
    // West forest boundary
    collisionManager.addObstacle(
      IsometricCollisionBox(
        id: 'boundary_west',
        worldX: minWorldX - 0.5,
        worldY: (minWorldY + maxWorldY) / 2,
        halfWidth: 0.5,
        halfHeight: (maxWorldY - minWorldY) / 2,
        label: 'boundary',
      ),
    );
    // East cliff boundary
    collisionManager.addObstacle(
      IsometricCollisionBox(
        id: 'boundary_east',
        worldX: maxWorldX + 0.5,
        worldY: (minWorldY + maxWorldY) / 2,
        halfWidth: 0.5,
        halfHeight: (maxWorldY - minWorldY) / 2,
        label: 'boundary',
      ),
    );
    // South frozen river boundary
    collisionManager.addObstacle(
      IsometricCollisionBox(
        id: 'boundary_south',
        worldX: (minWorldX + maxWorldX) / 2,
        worldY: minWorldY - 0.5,
        halfWidth: (maxWorldX - minWorldX) / 2,
        halfHeight: 0.5,
        label: 'boundary',
      ),
    );
    // North mountain boundary
    collisionManager.addObstacle(
      IsometricCollisionBox(
        id: 'boundary_north',
        worldX: (minWorldX + maxWorldX) / 2,
        worldY: maxWorldY + 0.5,
        halfWidth: (maxWorldX - minWorldX) / 2,
        halfHeight: 0.5,
        label: 'boundary',
      ),
    );
  }
}
