import 'package:flame/components.dart';
import '../asset_registry.dart';
import '../isometric_coordinates.dart';

/// Layer 1: Base ground tiles (cobblestone slabs, frozen earth, snow).
class GroundLayer extends Component with HasGameRef {
  Sprite? _groundTileSprite;
  final int gridRadius;

  GroundLayer({this.gridRadius = 14});

  @override
  Future<void> onLoad() async {
    final registry = GameAssetRegistry();
    final tilePath = registry.getPath(GameAssetRegistry.villageStoneSlab);
    if (tilePath.isNotEmpty) {
      try {
        final image = await gameRef.images.load(tilePath);
        _groundTileSprite = Sprite(image);
      } catch (_) {}
    }
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);

    // Renders isometric ground tiles in diamond grid
    for (var x = -gridRadius; x <= gridRadius; x++) {
      for (var y = -gridRadius; y <= gridRadius; y++) {
        // Skip extreme corners for natural organic perimeter
        if (x.abs() + y.abs() > gridRadius + 4) continue;

        final screenPos = IsometricCoordinates.gridToScreen(x, y);

        if (_groundTileSprite != null) {
          _groundTileSprite!.render(
            canvas,
            position: Vector2(
              screenPos.x - IsometricCoordinates.halfTileWidth,
              screenPos.y - IsometricCoordinates.halfTileHeight,
            ),
            size: Vector2(
              IsometricCoordinates.tileWidth,
              IsometricCoordinates.tileHeight,
            ),
          );
        } else {
          // Fallback tinted tile outline
          final path = Path()
            ..moveTo(screenPos.x, screenPos.y - IsometricCoordinates.halfTileHeight)
            ..lineTo(screenPos.x + IsometricCoordinates.halfTileWidth, screenPos.y)
            ..lineTo(screenPos.x, screenPos.y + IsometricCoordinates.halfTileHeight)
            ..lineTo(screenPos.x - IsometricCoordinates.halfTileWidth, screenPos.y)
            ..close();

          final fillPaint = Paint()..color = const Color(0xFF232B32);
          final strokePaint = Paint()
            ..color = const Color(0xFF1E242B)
            ..style = PaintingStyle.stroke
            ..strokeWidth = 1.0;

          canvas.drawPath(path, fillPaint);
          canvas.drawPath(path, strokePaint);
        }
      }
    }
  }
}
