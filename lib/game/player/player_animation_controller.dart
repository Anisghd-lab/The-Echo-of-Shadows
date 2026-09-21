import 'package:flame/components.dart';
import 'package:flame/extensions.dart';
import '../world/asset_registry.dart';
import 'player_controller.dart';

/// Manages Alex's animations and directional sprites across Idle, Walk, and Run states.
class PlayerAnimationController {
  final Map<String, Sprite> _idleSprites = {};
  final Map<String, SpriteAnimation> _walkAnimations = {};
  final Map<String, SpriteAnimation> _runAnimations = {};

  bool _loaded = false;
  bool get isLoaded => _loaded;

  /// Loads real assets from Flame cache or root bundle.
  Future<void> load(dynamic gameRef) async {
    final registry = GameAssetRegistry();

    // 1. Load Idle Sprites for 4 orientations
    final idlePaths = {
      'SE': registry.getPath(GameAssetRegistry.alexIdleSE),
      'SW': registry.getPath(GameAssetRegistry.alexIdleSW),
      'NE': registry.getPath(GameAssetRegistry.alexIdleNE),
      'NW': registry.getPath(GameAssetRegistry.alexIdleNW),
    };

    for (final entry in idlePaths.entries) {
      try {
        final image = await gameRef.images.load(entry.value);
        _idleSprites[entry.key] = Sprite(image);
      } catch (_) {}
    }

    // 2. Load Walk Cycle (4-frame strip from Alex — Marche01: 392x182)
    try {
      final walkPath = registry.getPath(GameAssetRegistry.alexWalkStrip);
      final walkImage = await gameRef.images.load(walkPath);
      final frameWidth = (walkImage.width / 4).floorToDouble();
      final frameHeight = walkImage.height.toDouble();

      final walkFrames = <SpriteAnimationFrame>[];
      for (var i = 0; i < 4; i++) {
        final sprite = Sprite(
          walkImage,
          srcPosition: Vector2(i * frameWidth, 0),
          srcSize: Vector2(frameWidth, frameHeight),
        );
        walkFrames.add(SpriteAnimationFrame(sprite, 0.16));
      }
      final baseWalkAnim = SpriteAnimation(walkFrames);
      _walkAnimations['SE'] = baseWalkAnim;
      _walkAnimations['SW'] = baseWalkAnim;
      _walkAnimations['NE'] = baseWalkAnim;
      _walkAnimations['NW'] = baseWalkAnim;
    } catch (_) {}

    // 3. Load Run Cycle
    try {
      final runPath = registry.getPath(GameAssetRegistry.alexRunStrip);
      final runImage = await gameRef.images.load(runPath);
      final frameWidth = runImage.width.toDouble();
      final frameHeight = runImage.height.toDouble();
      final runSprite = Sprite(runImage, srcSize: Vector2(frameWidth, frameHeight));
      final runAnim = SpriteAnimation([SpriteAnimationFrame(runSprite, 0.12)]);
      _runAnimations['SE'] = runAnim;
      _runAnimations['SW'] = runAnim;
      _runAnimations['NE'] = runAnim;
      _runAnimations['NW'] = runAnim;
    } catch (_) {}

    _loaded = true;
  }

  /// Returns current sprite or animation frame to render.
  Sprite? getCurrentSprite({
    required PlayerMovementState state,
    required String orientation,
    required double runningTime,
  }) {
    if (state == PlayerMovementState.idle) {
      return _idleSprites[orientation] ?? _idleSprites['SE'];
    } else if (state == PlayerMovementState.walk) {
      final anim = _walkAnimations[orientation] ?? _walkAnimations['SE'];
      if (anim != null) {
        return anim.getSprite();
      }
      return _idleSprites[orientation];
    } else {
      final anim = _runAnimations[orientation] ?? _runAnimations['SE'];
      if (anim != null) {
        return anim.getSprite();
      }
      return _idleSprites[orientation];
    }
  }

  void update(double dt) {
    for (final anim in _walkAnimations.values) {
      anim.update(dt);
    }
    for (final anim in _runAnimations.values) {
      anim.update(dt);
    }
  }
}
