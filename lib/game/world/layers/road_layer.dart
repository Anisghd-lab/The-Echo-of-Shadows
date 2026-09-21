import 'dart:ui';
import 'package:flame/components.dart';
import '../isometric_coordinates.dart';

/// Layer 2: Roads, pathways, and bridge entering the village.
class RoadLayer extends Component with HasGameRef {
  RoadLayer() {
    priority = IsometricCoordinates.zOrderRoad;
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);

    final roadPaint = Paint()
      ..color = const Color(0x33475569)
      ..style = PaintingStyle.fill;

    final scale = IsometricCoordinates.worldScale;
    // Draw main path connecting from spawn bridge into central village
    final pathPoints = [
      IsometricCoordinates.worldToScreen(0, 0),
      IsometricCoordinates.worldToScreen(0, 5.0 * scale),
      IsometricCoordinates.worldToScreen(3.0 * scale, 5.0 * scale),
      IsometricCoordinates.worldToScreen(3.0 * scale, 10.0 * scale),
      IsometricCoordinates.worldToScreen(-4.0 * scale, 5.0 * scale),
    ];

    for (final pt in pathPoints) {
      canvas.drawOval(
        Rect.fromCenter(
          center: Offset(pt.x, pt.y),
          width: IsometricCoordinates.tileWidth * 1.4 * scale,
          height: IsometricCoordinates.tileHeight * 1.4 * scale,
        ),
        roadPaint,
      );
    }
  }
}
