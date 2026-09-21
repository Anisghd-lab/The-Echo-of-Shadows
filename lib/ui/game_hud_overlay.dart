import 'package:flutter/material.dart';
import '../game/controls/touch_controller.dart';
import '../game/player/player_controller.dart';
import '../game/village_game.dart';

/// Flutter HUD overlay displayed over the Flame canvas.
class GameHUDOverlay extends StatefulWidget {
  final VillageGame game;
  final TouchInputController touchController;

  const GameHUDOverlay({
    Key? key,
    required this.game,
    required this.touchController,
  }) : super(key: key);

  @override
  State<GameHUDOverlay> createState() => _GameHUDOverlayState();
}

class _GameHUDOverlayState extends State<GameHUDOverlay> {
  bool _runLocked = false;
  String _lastSavedFeedback = '';

  @override
  Widget build(BuildContext context) {
    final pc = widget.game.villageWorld.playerController;

    return SafeArea(
      child: Stack(
        children: [
          // 1. Top Bar: Debug & Status Panel (Dark Thriller Theme)
          Positioned(
            top: 12,
            left: 12,
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              decoration: BoxDecoration(
                color: const Color(0xD90F172A),
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: const Color(0x3394A3B8)),
                boxShadow: const [
                  BoxShadow(color: Color(0x40000000), blurRadius: 6),
                ],
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Text(
                    "L'ÉCHO DES OMBRES",
                    style: TextStyle(
                      color: Color(0xFFE2E8F0),
                      fontSize: 13,
                      fontWeight: FontWeight.w700,
                      letterSpacing: 1.2,
                    ),
                  ),
                  const SizedBox(height: 4),
                  AnimatedBuilder(
                    animation: widget.touchController,
                    builder: (context, _) {
                      final stateName = pc.state == PlayerMovementState.idle
                          ? 'IDLE'
                          : (pc.state == PlayerMovementState.walk ? 'WALK' : 'RUN');
                      return Text(
                        "Alex: [${pc.worldX.toStringAsFixed(1)}, ${pc.worldY.toStringAsFixed(1)}] | $stateName (${pc.orientation})",
                        style: const TextStyle(
                          color: Color(0xFF94A3B8),
                          fontSize: 11,
                          fontFamily: 'monospace',
                        ),
                      );
                    },
                  ),
                  if (_lastSavedFeedback.isNotEmpty) ...[
                    const SizedBox(height: 4),
                    Text(
                      _lastSavedFeedback,
                      style: const TextStyle(
                        color: Color(0xFF10B981),
                        fontSize: 11,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ],
                ],
              ),
            ),
          ),

          // 2. Top-Right: Quick Actions (Save, Load, Zoom)
          Positioned(
            top: 12,
            right: 12,
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                // Zoom controls
                _buildIconButton(
                  icon: Icons.zoom_in,
                  onTap: () => widget.game.cameraController.zoomIn(),
                ),
                const SizedBox(width: 8),
                _buildIconButton(
                  icon: Icons.zoom_out,
                  onTap: () => widget.game.cameraController.zoomOut(),
                ),
                const SizedBox(width: 10),

                // Save button
                _buildActionButton(
                  label: "SAVE",
                  icon: Icons.save,
                  color: const Color(0xFF2563EB),
                  onTap: () async {
                    final success = await widget.game.saveCurrentGameState();
                    setState(() {
                      _lastSavedFeedback = success ? "✓ Position Sauvegardée" : "✗ Erreur";
                    });
                    Future.delayed(const Duration(seconds: 3), () {
                      if (mounted) setState(() => _lastSavedFeedback = '');
                    });
                  },
                ),
                const SizedBox(width: 8),

                // Load button
                _buildActionButton(
                  label: "LOAD",
                  icon: Icons.restore,
                  color: const Color(0xFF475569),
                  onTap: () async {
                    final success = await widget.game.loadSavedGameState();
                    setState(() {
                      _lastSavedFeedback = success ? "✓ Partie Chargée" : "Aucune sauvegarde";
                    });
                    Future.delayed(const Duration(seconds: 3), () {
                      if (mounted) setState(() => _lastSavedFeedback = '');
                    });
                  },
                ),
              ],
            ),
          ),

          // 3. Bottom-Left: Virtual Joystick for Android Touch Movement
          Positioned(
            bottom: 24,
            left: 24,
            child: VirtualJoystickWidget(
              controller: widget.touchController,
              radius: 60.0,
            ),
          ),

          // 4. Bottom-Right: Run Sprint Toggle (for mobile ease)
          Positioned(
            bottom: 30,
            right: 24,
            child: GestureDetector(
              onTap: () {
                setState(() {
                  _runLocked = !_runLocked;
                });
              },
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                decoration: BoxDecoration(
                  color: _runLocked ? const Color(0xFFDC2626) : const Color(0xD91E293B),
                  borderRadius: BorderRadius.circular(24),
                  border: Border.all(
                    color: _runLocked ? const Color(0xFFEF4444) : const Color(0x4494A3B8),
                  ),
                  boxShadow: const [
                    BoxShadow(color: Color(0x40000000), blurRadius: 8),
                  ],
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(
                      _runLocked ? Icons.directions_run : Icons.directions_walk,
                      color: Colors.white,
                      size: 20,
                    ),
                    const SizedBox(width: 6),
                    Text(
                      _runLocked ? "SPRINT ON" : "WALK",
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 12,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildIconButton({required IconData icon, required VoidCallback onTap}) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: 36,
        height: 36,
        decoration: BoxDecoration(
          color: const Color(0xD90F172A),
          shape: BoxShape.circle,
          border: Border.all(color: const Color(0x3394A3B8)),
        ),
        child: Icon(icon, color: Colors.white70, size: 18),
      ),
    );
  }

  Widget _buildActionButton({
    required String label,
    required IconData icon,
    required Color color,
    required VoidCallback onTap,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        decoration: BoxDecoration(
          color: color,
          borderRadius: BorderRadius.circular(8),
          boxShadow: const [
            BoxShadow(color: Color(0x33000000), blurRadius: 4),
          ],
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, color: Colors.white, size: 15),
            const SizedBox(width: 6),
            Text(
              label,
              style: const TextStyle(
                color: Colors.white,
                fontSize: 12,
                fontWeight: FontWeight.w700,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
