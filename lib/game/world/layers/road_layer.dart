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

    // Draw main path connecting from spawn bridge into central village
    final pathPoints = [
      IsometricCoordinates.worldToScreen(0, 0),
      IsometricCoordinates.worldToScreen(0, 5),
      IsometricCoordinates.worldToScreen(3, 5),
      IsometricCoordinates.worldToScreen(3, 10),
      IsometricCoordinates.worldToScreen(-4, 5),
    ];

    for (final pt in pathPoints) {
      canvas.drawOval(
        Rect.fromCenter(
          center: Offset(pt.x, pt.y),
          width: IsometricCoordinates.tileWidth * 1.4,
          height: IsometricCoordinates.tileHeight * 1.4,
        ),
        roadPaint,
      );
    }
  }
}
