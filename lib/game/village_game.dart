import 'dart:math' as math;
import 'package:flame/components.dart';
import 'package:flame/events.dart';
import 'package:flame/game.dart';
import 'package:flutter/services.dart';
import '../save/save_manager.dart';
import 'camera/isometric_camera.dart';
import 'controls/touch_controller.dart';
import 'world/asset_registry.dart';
import 'world/isometric_coordinates.dart';
import 'world/village_world.dart';

/// Main Flame Game orchestrating the Village World, Alex, Camera, and SaveManager.
class VillageGame extends FlameGame with KeyboardEvents {
  final SaveManager saveManager;
  final TouchInputController touchController;

  late final VillageWorld villageWorld;
  late final IsometricCameraController cameraController;

  // Keyboard state tracking
  final Set<LogicalKeyboardKey> _pressedKeys = {};

  VillageGame({
    required this.saveManager,
    required this.touchController,
  });

  @override
  Future<void> onLoad() async {
    // 1. Initialize Asset Registry
    GameAssetRegistry().initDefaults();

    // 2. Load or initialize saved position
    double startX = 0.0;
    double startY = 0.0;
    String startOrientation = 'SE';

    final save = saveManager.currentSave;
    if (save != null) {
      startX = save.position.x;
      startY = save.position.y;
      startOrientation = save.position.orientation;
    }

    // 3. Instantiate Village World
    villageWorld = VillageWorld(
      initialPlayerX: startX,
      initialPlayerY: startY,
      initialOrientation: startOrientation,
    );
    await add(villageWorld);

    // 4. Setup Camera & Viewport limits
    // Calculate world bounding box in screen coordinates
    final screenMin = IsometricCoordinates.worldToScreen(
      villageWorld.minWorldX,
      villageWorld.minWorldY,
    );
    final screenMax = IsometricCoordinates.worldToScreen(
      villageWorld.maxWorldX,
      villageWorld.maxWorldY,
    );

    cameraController = IsometricCameraController(
      camera: camera,
      minBounds: Vector2(-1200, -900),
      maxBounds: Vector2(1200, 900),
      zoomLevel: 1.0,
    );
  }

  @override
  void update(double dt) {
    super.update(dt);

    // 1. Combine Touch Input + Keyboard Input
    double inputX = touchController.inputX;
    double inputY = touchController.inputY;

    // Keyboard overrides or supplements touch
    if (_pressedKeys.isNotEmpty) {
      double kx = 0;
      double ky = 0;
      if (_pressedKeys.contains(LogicalKeyboardKey.keyA) ||
          _pressedKeys.contains(LogicalKeyboardKey.arrowLeft)) {
        kx -= 1;
      }
      if (_pressedKeys.contains(LogicalKeyboardKey.keyD) ||
          _pressedKeys.contains(LogicalKeyboardKey.arrowRight)) {
        kx += 1;
      }
      if (_pressedKeys.contains(LogicalKeyboardKey.keyW) ||
          _pressedKeys.contains(LogicalKeyboardKey.arrowUp)) {
        ky -= 1;
      }
      if (_pressedKeys.contains(LogicalKeyboardKey.keyS) ||
          _pressedKeys.contains(LogicalKeyboardKey.arrowDown)) {
        ky += 1;
      }

      if (kx != 0 || ky != 0) {
        final isShift = _pressedKeys.contains(LogicalKeyboardKey.shiftLeft) ||
            _pressedKeys.contains(LogicalKeyboardKey.shiftRight);
        final mag = isShift ? 1.0 : 0.5; // Walk vs Run
        final len = math.sqrt(kx * kx + ky * ky);
        inputX = (kx / len) * mag;
        inputY = (ky / len) * mag;
      }
    }

    // 2. Update Alex movement & animation state
    villageWorld.playerController.update(
      inputX: inputX,
      inputY: inputY,
      dt: dt,
    );

    // 3. Update Camera following Alex
    cameraController.update(
      targetPosition: villageWorld.alex.position,
      viewportSize: size,
      dt: dt,
    );
  }

  @override
  KeyEventResult onKeyEvent(
    KeyEvent event,
    Set<LogicalKeyboardKey> keysPressed,
  ) {
    _pressedKeys.clear();
    _pressedKeys.addAll(keysPressed);
    return KeyEventResult.handled;
  }

  /// Persists current game state to local storage via SaveManager.
  Future<bool> saveCurrentGameState() async {
    final pc = villageWorld.playerController;
    saveManager.updatePosition(
      map: 'VILLAGE_ABANDONED',
      x: pc.worldX,
      y: pc.worldY,
      orientation: pc.orientation,
    );
    return await saveManager.saveGame();
  }

  /// Reloads saved game state and teleports Alex.
  Future<bool> loadSavedGameState() async {
    final save = await saveManager.loadGame();
    if (save != null) {
      villageWorld.playerController.teleport(
        save.position.x,
        save.position.y,
        newOrientation: save.position.orientation,
      );
      return true;
    }
    return false;
  }
}
