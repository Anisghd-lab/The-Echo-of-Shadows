import 'package:flame/components.dart';
import 'package:flame/extensions.dart';
import '../world/asset_registry.dart';
import 'player_controller.dart';
import 'player_orientation_controller.dart';

/// Manages Alex's genuine 4-way animations across Idle, Walk, Run, and Interaction states.
/// Covers full 360° rotation using dedicated directional sprite sequences.
class PlayerAnimationController {
  final Map<String, Sprite> _idleSprites = {};
  final Map<String, SpriteAnimation> _walkAnimations = {};
  final Map<String, SpriteAnimation> _runAnimations = {};
  final Map<String, Sprite> _interactSprites = {};

  bool _loaded = false;
  bool get isLoaded => _loaded;

  /// Loads real assets from Flame cache or root bundle.
  Future<void> load(dynamic gameRef) async {
    // 1. Load Idle Sprites for all 4 orientations (360°)
    final idleFiles = {
      PlayerOrientationController.southEast: 'assets/images/characters/alex/idle/Alex-—-Animation-Idle03.png',
      PlayerOrientationController.southWest: 'assets/images/characters/alex/idle/Alex-—-Animation-Idle10.png',
      PlayerOrientationController.northEast: 'assets/images/characters/alex/idle/Alex-—-Animation-Idle06.png',
      PlayerOrientationController.northWest: 'assets/images/characters/alex/idle/Alex-—-Animation-Idle07.png',
    };

    for (final entry in idleFiles.entries) {
      try {
        final image = await gameRef.images.load(entry.value);
        _idleSprites[entry.key] = Sprite(image);
      } catch (_) {}
    }

    // 2. Load Walk Cycles (Genuine multi-frame sequences per orientation)
    final walkFileMap = {
      PlayerOrientationController.southEast: [
        'assets/images/characters/alex/walk/Alex-—-Marche36.png',
        'assets/images/characters/alex/walk/Alex-—-Marche37.png',
        'assets/images/characters/alex/walk/Alex-—-Marche38.png',
        'assets/images/characters/alex/walk/Alex-—-Marche39.png',
        'assets/images/characters/alex/walk/Alex-—-Marche40.png',
        'assets/images/characters/alex/walk/Alex-—-Marche41.png',
      ],
      PlayerOrientationController.southWest: [
        'assets/images/characters/alex/walk/Alex-—-Marche42.png',
        'assets/images/characters/alex/walk/Alex-—-Marche43.png',
        'assets/images/characters/alex/walk/Alex-—-Marche44.png',
        'assets/images/characters/alex/walk/Alex-—-Marche45.png',
        'assets/images/characters/alex/walk/Alex-—-Marche46.png',
      ],
      PlayerOrientationController.northEast: [
        'assets/images/characters/alex/walk/Alex-—-Marche18.png',
        'assets/images/characters/alex/walk/Alex-—-Marche21.png',
        'assets/images/characters/alex/walk/Alex-—-Marche24.png',
        'assets/images/characters/alex/walk/Alex-—-Marche27.png',
        'assets/images/characters/alex/walk/Alex-—-Marche30.png',
      ],
      PlayerOrientationController.northWest: [
        'assets/images/characters/alex/walk/Alex-—-Marche10.png',
        'assets/images/characters/alex/walk/Alex-—-Marche12.png',
        'assets/images/characters/alex/walk/Alex-—-Marche15.png',
        'assets/images/characters/alex/walk/Alex-—-Marche32.png',
        'assets/images/characters/alex/walk/Alex-—-Marche35.png',
      ],
    };

    for (final entry in walkFileMap.entries) {
      final anim = await _loadFrameSequence(gameRef, entry.value, 0.14);
      if (anim != null) {
        _walkAnimations[entry.key] = anim;
      }
    }

    // Fallback: 4-frame strip for SE if sequence failed
    if (!_walkAnimations.containsKey(PlayerOrientationController.southEast)) {
      try {
        final stripImg = await gameRef.images.load('assets/images/characters/alex/walk/Alex-—-Marche01.png');
        final fw = (stripImg.width / 4).floorToDouble();
        final fh = stripImg.height.toDouble();
        final frames = <SpriteAnimationFrame>[];
        for (var i = 0; i < 4; i++) {
          final s = Sprite(stripImg, srcPosition: Vector2(i * fw, 0), srcSize: Vector2(fw, fh));
          frames.add(SpriteAnimationFrame(s, 0.16));
        }
        _walkAnimations[PlayerOrientationController.southEast] = SpriteAnimation(frames);
      } catch (_) {}
    }

    // 3. Load Run Cycles (Genuine multi-frame sequences per orientation)
    final runFileMap = {
      PlayerOrientationController.southEast: [
        'assets/images/characters/alex/run/Alex-—-Course11.png',
        'assets/images/characters/alex/run/Alex-—-Course14.png',
        'assets/images/characters/alex/run/Alex-—-Course16.png',
        'assets/images/characters/alex/run/Alex-—-Course19.png',
        'assets/images/characters/alex/run/Alex-—-Course22.png',
      ],
      PlayerOrientationController.southWest: [
        'assets/images/characters/alex/run/Alex-—-Course34.png',
        'assets/images/characters/alex/run/Alex-—-Course36.png',
        'assets/images/characters/alex/run/Alex-—-Course38.png',
        'assets/images/characters/alex/run/Alex-—-Course40.png',
      ],
      PlayerOrientationController.northEast: [
        'assets/images/characters/alex/run/Alex-—-Course05.png',
        'assets/images/characters/alex/run/Alex-—-Course08.png',
        'assets/images/characters/alex/run/Alex-—-Course10.png',
        'assets/images/characters/alex/run/Alex-—-Course13.png',
        'assets/images/characters/alex/run/Alex-—-Course15.png',
      ],
      PlayerOrientationController.northWest: [
        'assets/images/characters/alex/run/Alex-—-Course25.png',
        'assets/images/characters/alex/run/Alex-—-Course26.png',
        'assets/images/characters/alex/run/Alex-—-Course27.png',
        'assets/images/characters/alex/run/Alex-—-Course28.png',
        'assets/images/characters/alex/run/Alex-—-Course29.png',
      ],
    };

    for (final entry in runFileMap.entries) {
      final anim = await _loadFrameSequence(gameRef, entry.value, 0.10);
      if (anim != null) {
        _runAnimations[entry.key] = anim;
      }
    }

    // 4. Load Interaction Sprites for 4 orientations
    final interactFiles = {
      PlayerOrientationController.southEast: 'assets/images/characters/alex/interaction/Alex-—-Interaction01.png',
      PlayerOrientationController.southWest: 'assets/images/characters/alex/interaction/Alex-—-Interaction14.png',
      PlayerOrientationController.northEast: 'assets/images/characters/alex/interaction/Alex-—-Interaction28.png',
      PlayerOrientationController.northWest: 'assets/images/characters/alex/interaction/Alex-—-Interaction64.png',
    };

    for (final entry in interactFiles.entries) {
      try {
        final image = await gameRef.images.load(entry.value);
        _interactSprites[entry.key] = Sprite(image);
      } catch (_) {}
    }

    _loaded = true;
  }

  Future<SpriteAnimation?> _loadFrameSequence(
    dynamic gameRef,
    List<String> paths,
    double frameDuration,
  ) async {
    final frames = <SpriteAnimationFrame>[];
    for (final path in paths) {
      try {
        final img = await gameRef.images.load(path);
        frames.add(SpriteAnimationFrame(Sprite(img), frameDuration));
      } catch (_) {}
    }
    if (frames.isEmpty) return null;
    return SpriteAnimation(frames);
  }

  /// Returns current sprite or animation frame to render based on movement state and 4-way orientation.
  Sprite? getCurrentSprite({
    required PlayerMovementState state,
    required String orientation,
    required double runningTime,
  }) {
    final cleanOrient = PlayerOrientationController.canonicalCycle.contains(orientation)
        ? orientation
        : PlayerOrientationController.southEast;

    if (state == PlayerMovementState.idle) {
      return _idleSprites[cleanOrient] ?? _idleSprites[PlayerOrientationController.southEast];
    } else if (state == PlayerMovementState.walk) {
      final anim = _walkAnimations[cleanOrient] ?? _walkAnimations[PlayerOrientationController.southEast];
      if (anim != null) {
        return anim.getSprite();
      }
      return _idleSprites[cleanOrient];
    } else if (state == PlayerMovementState.run) {
      final anim = _runAnimations[cleanOrient] ?? _runAnimations[PlayerOrientationController.southEast];
      if (anim != null) {
        return anim.getSprite();
      }
      return _walkAnimations[cleanOrient]?.getSprite() ?? _idleSprites[cleanOrient];
    } else if (state == PlayerMovementState.interact) {
      return _interactSprites[cleanOrient] ?? _idleSprites[cleanOrient];
    }
    return _idleSprites[cleanOrient];
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
