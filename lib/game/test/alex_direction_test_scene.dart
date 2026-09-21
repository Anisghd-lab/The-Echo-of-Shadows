import 'dart:ui';
import 'package:flame/components.dart';
import '../player/player_animation_controller.dart';
import '../player/player_controller.dart';
import '../player/player_orientation_controller.dart';

/// Scene displaying all 4 directions of Alex simultaneously in a cross pattern:
///          NW
///           ↑
///           |
/// SW ← CenterAlex → NE
///           |
///           ↓
///          SE
///
/// Features automatic 360° rotation cycle:
/// SE -> SW -> NW -> NE -> SE
/// and dynamic state toggling (Idle, Walk, Run, Interaction).
class AlexDirectionTestScene extends Component with HasGameRef {
  final PlayerAnimationController animationController;
  
  // Auto-rotating center character
  String _centerOrientation = PlayerOrientationController.southEast;
  PlayerMovementState _state = PlayerMovementState.idle;
  
  double _runningTime = 0.0;
  double _rotationTimer = 0.0;
  double rotationInterval = 1.5; // seconds per orientation
  bool autoRotate = true;

  // Calibrated size
  static final Vector2 characterSize = Vector2(36, 72);

  AlexDirectionTestScene({required this.animationController});

  PlayerMovementState get state => _state;
  set state(PlayerMovementState s) => _state = s;

  String get centerOrientation => _centerOrientation;

  void nextState() {
    switch (_state) {
      case PlayerMovementState.idle:
        _state = PlayerMovementState.walk;
        break;
      case PlayerMovementState.walk:
        _state = PlayerMovementState.run;
        break;
      case PlayerMovementState.run:
        _state = PlayerMovementState.interact;
        break;
      case PlayerMovementState.interact:
        _state = PlayerMovementState.idle;
        break;
    }
  }

  void rotateCW() {
    final idx = PlayerOrientationController.canonicalCycle.indexOf(_centerOrientation);
    _centerOrientation = PlayerOrientationController.canonicalCycle[(idx + 1) % PlayerOrientationController.canonicalCycle.length];
    _rotationTimer = 0.0;
  }

  void rotateCCW() {
    final idx = PlayerOrientationController.canonicalCycle.indexOf(_centerOrientation);
    _centerOrientation = PlayerOrientationController.canonicalCycle[(idx - 1 + PlayerOrientationController.canonicalCycle.length) % PlayerOrientationController.canonicalCycle.length];
    _rotationTimer = 0.0;
  }

  @override
  void update(double dt) {
    super.update(dt);
    _runningTime += dt;
    animationController.update(dt);

    if (autoRotate) {
      _rotationTimer += dt;
      if (_rotationTimer >= rotationInterval) {
        _rotationTimer = 0.0;
        rotateCW();
      }
    }
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);

    final center = Vector2(gameRef.size.x / 2, gameRef.size.y / 2);
    final distance = 140.0;

    // Background panel
    final bgPaint = Paint()..color = const Color(0xDD111827);
    canvas.drawRRect(
      RRect.fromRectAndRadius(
        Rect.fromCenter(center: Offset(center.x, center.y), width: 440, height: 440),
        const Radius.circular(16),
      ),
      bgPaint,
    );

    // Positions for compass display:
    // NW: Top
    // SE: Bottom
    // SW: Left
    // NE: Right
    final positions = {
      PlayerOrientationController.northWest: Offset(center.x, center.y - distance),
      PlayerOrientationController.southEast: Offset(center.x, center.y + distance),
      PlayerOrientationController.southWest: Offset(center.x - distance, center.y),
      PlayerOrientationController.northEast: Offset(center.x + distance, center.y),
    };

    // Draw connecting cross lines
    final linePaint = Paint()
      ..color = const Color(0x4438BDF8)
      ..strokeWidth = 2.0;
    canvas.drawLine(positions[PlayerOrientationController.southWest]!, positions[PlayerOrientationController.northEast]!, linePaint);
    canvas.drawLine(positions[PlayerOrientationController.northWest]!, positions[PlayerOrientationController.southEast]!, linePaint);

    // Render 4 static peripheral Alex instances
    for (final entry in positions.entries) {
      _renderAlexInstance(
        canvas: canvas,
        pos: entry.value,
        orientation: entry.key,
        label: entry.key,
        isCenter: false,
      );
    }

    // Render center auto-rotating Alex
    _renderAlexInstance(
      canvas: canvas,
      pos: Offset(center.x, center.y),
      orientation: _centerOrientation,
      label: '$_centerOrientation (Rotating)',
      isCenter: true,
    );
  }

  void _renderAlexInstance({
    required Canvas canvas,
    required Offset pos,
    required String orientation,
    required String label,
    required bool isCenter,
  }) {
    // 1. Ground contact shadow
    final shadowPaint = Paint()
      ..color = const Color(0x66000000)
      ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 4.0);
    canvas.drawOval(
      Rect.fromCenter(center: Offset(pos.dx, pos.dy), width: 32, height: 8),
      shadowPaint,
    );

    // Center highlight ring
    if (isCenter) {
      final ringPaint = Paint()
        ..color = const Color(0x88F59E0B)
        ..style = PaintingStyle.stroke
        ..strokeWidth = 2.0;
      canvas.drawCircle(Offset(pos.dx, pos.dy), 28, ringPaint);
    }

    // 2. Sprite rendering
    final renderInfo = animationController.getCurrentRenderInfo(
      state: _state,
      orientation: orientation,
      runningTime: _runningTime,
    );

    final sprite = renderInfo.sprite;
    if (sprite != null) {
      canvas.save();
      // Anchor at feet (bottomCenter)
      canvas.translate(pos.dx - characterSize.x / 2, pos.dy - characterSize.y);

      if (renderInfo.isFlipped) {
        canvas.translate(characterSize.x, 0);
        canvas.scale(-1.0, 1.0);
      }

      sprite.render(
        canvas,
        position: Vector2.zero(),
        size: characterSize,
      );
      canvas.restore();
    }
  }
}
