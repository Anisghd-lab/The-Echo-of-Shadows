import 'package:flutter/material.dart';
import '../game/controls/touch_controller.dart';
import '../game/dialogue/dialogue_manager.dart';
import '../game/dialogue/dialogue_models.dart';
import '../game/player/player_controller.dart';
import '../game/village_game.dart';

/// HUD Overlay supporting clean immersive RELEASE mode and toggleable DEBUG mode.
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
  bool _isDebugMode = false; // RELEASE mode by default
  bool _runLocked = false;
  String _statusNotification = '';

  @override
  Widget build(BuildContext context) {
    final pc = widget.game.villageWorld.playerController;
    final activePOI = widget.game.villageWorld.activePOI;

    return SafeArea(
      child: Stack(
        children: [
          // ===================================================================
          // 1. RELEASE HUD: Cinematic Location & Objective Badge
          // ===================================================================
          if (!_isDebugMode) ...[
            Positioned(
              top: 16,
              left: 16,
              child: AnimatedOpacity(
                duration: const Duration(milliseconds: 300),
                opacity: 0.9,
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                  decoration: BoxDecoration(
                    color: const Color(0xB30F172A),
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: const Color(0x3394A3B8)),
                    boxShadow: const [
                      BoxShadow(color: Color(0x66000000), blurRadius: 10),
                    ],
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Container(
                        width: 8,
                        height: 8,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          color: activePOI != null
                              ? const Color(0xFF38BDF8)
                              : const Color(0xFF64748B),
                        ),
                      ),
                      const SizedBox(width: 8),
                      Text(
                        activePOI != null ? activePOI.nameEn : "L'ÉCHO DES OMBRES",
                        style: const TextStyle(
                          color: Color(0xFFF1F5F9),
                          fontSize: 12,
                          fontWeight: FontWeight.w600,
                          letterSpacing: 0.8,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),

            // Active POI Interaction Prompt if near an interactive structure
            if (activePOI?.defaultInteractionPrompt != null)
              Positioned(
                top: 70,
                left: 16,
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  decoration: BoxDecoration(
                    color: const Color(0xD91E293B),
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: const Color(0x4D38BDF8)),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Icon(Icons.touch_app, size: 14, color: Color(0xFF38BDF8)),
                      const SizedBox(width: 6),
                      Text(
                        activePOI!.defaultInteractionPrompt!,
                        style: const TextStyle(
                          color: Color(0xFFE2E8F0),
                          fontSize: 11,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
          ],

          // ===================================================================
          // 2. DEBUG MODE PANEL: Diagnostics & Dev Tools
          // ===================================================================
          if (_isDebugMode) ...[
            Positioned(
              top: 12,
              left: 12,
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                decoration: BoxDecoration(
                  color: const Color(0xE60F172A),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: const Color(0xFFEAB308)),
                  boxShadow: const [
                    BoxShadow(color: Color(0x80000000), blurRadius: 6),
                  ],
                ),
                child: AnimatedBuilder(
                  animation: widget.touchController,
                  builder: (context, _) {
                    final stateStr = pc.state == PlayerMovementState.idle
                        ? 'IDLE'
                        : (pc.state == PlayerMovementState.walk ? 'WALK' : 'RUN');
                    final zOrder = widget.game.villageWorld.alex.priority;
                    return Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        const Text(
                          "DEBUG MODE [ACTIVE]",
                          style: TextStyle(
                            color: Color(0xFFEAB308),
                            fontSize: 11,
                            fontWeight: FontWeight.w800,
                          ),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          "Alex Pos: [${pc.worldX.toStringAsFixed(2)}, ${pc.worldY.toStringAsFixed(2)}]",
                          style: const TextStyle(color: Color(0xFF94A3B8), fontSize: 10, fontFamily: 'monospace'),
                        ),
                        Text(
                          "State: $stateStr | Orient: ${pc.orientation} | Z: $zOrder",
                          style: const TextStyle(color: Color(0xFF94A3B8), fontSize: 10, fontFamily: 'monospace'),
                        ),
                        Text(
                          "POI: ${activePOI?.id ?? 'NONE'}",
                          style: const TextStyle(color: Color(0xFF38BDF8), fontSize: 10, fontFamily: 'monospace'),
                        ),
                      ],
                    );
                  },
                ),
              ),
            ),

            // Debug Tools Bar (Save, Load, Zoom)
            Positioned(
              top: 12,
              right: 56,
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  _buildDebugButton(
                    icon: Icons.zoom_in,
                    onTap: () => widget.game.cameraController.zoomIn(),
                  ),
                  const SizedBox(width: 4),
                  _buildDebugButton(
                    icon: Icons.zoom_out,
                    onTap: () => widget.game.cameraController.zoomOut(),
                  ),
                  const SizedBox(width: 6),
                  _buildDebugButton(
                    label: "SAVE",
                    icon: Icons.save,
                    onTap: () async {
                      final ok = await widget.game.saveCurrentGameState();
                      _showNotification(ok ? "✓ Position sauvegardée" : "✗ Erreur");
                    },
                  ),
                  const SizedBox(width: 4),
                  _buildDebugButton(
                    label: "LOAD",
                    icon: Icons.restore,
                    onTap: () async {
                      final ok = await widget.game.loadSavedGameState();
                      _showNotification(ok ? "✓ Position chargée" : "Aucune sauvegarde");
                    },
                  ),
                ],
              ),
            ),
          ],

          // ===================================================================
          // 3. Top-Right: Discreet Debug Mode Toggle Switch
          // ===================================================================
          Positioned(
            top: 12,
            right: 12,
            child: GestureDetector(
              onTap: () {
                setState(() {
                  _isDebugMode = !_isDebugMode;
                });
              },
              child: Container(
                width: 34,
                height: 34,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: _isDebugMode ? const Color(0xFFEAB308) : const Color(0x660F172A),
                  border: Border.all(
                    color: _isDebugMode ? const Color(0xFFCA8A04) : const Color(0x3394A3B8),
                  ),
                ),
                child: Icon(
                  Icons.tune,
                  size: 16,
                  color: _isDebugMode ? Colors.black : Colors.white70,
                ),
              ),
            ),
          ),

          // Notification Banner
          if (_statusNotification.isNotEmpty)
            Positioned(
              bottom: 100,
              left: 0,
              right: 0,
              child: Center(
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  decoration: BoxDecoration(
                    color: const Color(0xE60F172A),
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: const Color(0xFF10B981)),
                  ),
                  child: Text(
                    _statusNotification,
                    style: const TextStyle(
                      color: Color(0xFF10B981),
                      fontSize: 12,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
              ),
            ),

          // ===================================================================
          // 4. Touch Joystick (Subtle Dark Glass Design)
          // ===================================================================
          Positioned(
            bottom: 24,
            left: 24,
            child: Opacity(
              opacity: 0.75,
              child: VirtualJoystickWidget(
                controller: widget.touchController,
                radius: 55.0,
              ),
            ),
          ),

          // ===================================================================
          // 5. Mobile Sprint & 360° In-Place Rotation Controls
          // ===================================================================
          Positioned(
            bottom: 24,
            right: 24,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                // In-place 360° turn buttons
                Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    GestureDetector(
                      onTap: () {
                        setState(() {
                          widget.game.villageWorld.playerController.rotateCounterClockwise();
                        });
                      },
                      child: Container(
                        padding: const EdgeInsets.all(8),
                        decoration: BoxDecoration(
                          color: const Color(0x801E293B),
                          shape: BoxShape.circle,
                          border: Border.all(color: const Color(0x3394A3B8)),
                        ),
                        child: const Icon(Icons.rotate_left, color: Colors.white, size: 18),
                      ),
                    ),
                    const SizedBox(width: 8),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                      decoration: BoxDecoration(
                        color: const Color(0xB30F172A),
                        borderRadius: BorderRadius.circular(10),
                        border: Border.all(color: const Color(0x3338BDF8)),
                      ),
                      child: Text(
                        pc.orientation,
                        style: const TextStyle(
                          color: Color(0xFF38BDF8),
                          fontSize: 11,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                    const SizedBox(width: 8),
                    GestureDetector(
                      onTap: () {
                        setState(() {
                          widget.game.villageWorld.playerController.rotateClockwise();
                        });
                      },
                      child: Container(
                        padding: const EdgeInsets.all(8),
                        decoration: BoxDecoration(
                          color: const Color(0x801E293B),
                          shape: BoxShape.circle,
                          border: Border.all(color: const Color(0x3394A3B8)),
                        ),
                        child: const Icon(Icons.rotate_right, color: Colors.white, size: 18),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                // Sprint button
                GestureDetector(
                  onTap: () {
                    setState(() {
                      _runLocked = !_runLocked;
                    });
                  },
                  child: AnimatedContainer(
                    duration: const Duration(milliseconds: 200),
                    padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                    decoration: BoxDecoration(
                      color: _runLocked ? const Color(0xCCDC2626) : const Color(0x801E293B),
                      borderRadius: BorderRadius.circular(20),
                      border: Border.all(
                        color: _runLocked ? const Color(0xFFEF4444) : const Color(0x3394A3B8),
                      ),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(
                          _runLocked ? Icons.directions_run : Icons.directions_walk,
                          color: Colors.white,
                          size: 16,
                        ),
                        const SizedBox(width: 4),
                        Text(
                          _runLocked ? "SPRINT" : "WALK",
                          style: const TextStyle(
                            color: Colors.white,
                            fontSize: 11,
                            fontWeight: FontWeight.w700,
                            letterSpacing: 0.5,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),

          // ===================================================================
          // 4. NPC DIALOGUE & PROXIMITY INTERACTION OVERLAY (Phase 17 & 18)
          // ===================================================================
          ValueListenableBuilder<DialogueNode?>(
            valueListenable: DialogueManager.instance.activeDialogueNotifier,
            builder: (context, dialogueNode, _) {
              if (dialogueNode == null) {
                // If not in dialogue, check for nearby interactable NPC
                final nearbyNpc = widget.game.villageWorld.charactersLayer.getInteractableNpc();
                if (nearbyNpc != null) {
                  return Positioned(
                    bottom: 110,
                    left: 0,
                    right: 0,
                    child: Center(
                      child: GestureDetector(
                        onTap: () {
                          DialogueManager.instance.startDialogue(
                            npcId: nearbyNpc.id,
                            alex: widget.game.villageWorld.alex,
                            npc: nearbyNpc,
                          );
                        },
                        child: Container(
                          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                          decoration: BoxDecoration(
                            color: const Color(0xEE0F172A),
                            borderRadius: BorderRadius.circular(24),
                            border: Border.all(color: const Color(0xFF38BDF8), width: 1.5),
                            boxShadow: const [
                              BoxShadow(color: Color(0x99000000), blurRadius: 12),
                            ],
                          ),
                          child: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                decoration: BoxDecoration(
                                  color: const Color(0xFF38BDF8),
                                  borderRadius: BorderRadius.circular(4),
                                ),
                                child: const Text(
                                  'E',
                                  style: TextStyle(
                                    color: Color(0xFF0F172A),
                                    fontWeight: FontWeight.bold,
                                    fontSize: 12,
                                  ),
                                ),
                              ),
                              const SizedBox(width: 8),
                              Text(
                                "Parler à ${nearbyNpc.name}",
                                style: const TextStyle(
                                  color: Colors.white,
                                  fontWeight: FontWeight.w600,
                                  fontSize: 13,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  );
                }
                return const SizedBox.shrink();
              }

              // Active Dialogue Window (non-blocking, narrative choices)
              return Positioned(
                bottom: 24,
                left: 20,
                right: 20,
                child: Center(
                  child: Container(
                    constraints: const BoxConstraints(maxWidth: 650),
                    padding: const EdgeInsets.all(18),
                    decoration: BoxDecoration(
                      color: const Color(0xF50F172A),
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: const Color(0xFF38BDF8), width: 1.5),
                      boxShadow: const [
                        BoxShadow(color: Color(0xCC000000), blurRadius: 20),
                      ],
                    ),
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Header: Speaker Name & Role
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  dialogueNode.speakerName,
                                  style: const TextStyle(
                                    color: Color(0xFF38BDF8),
                                    fontSize: 16,
                                    fontWeight: FontWeight.w800,
                                    letterSpacing: 0.5,
                                  ),
                                ),
                                Text(
                                  dialogueNode.speakerRole,
                                  style: const TextStyle(
                                    color: Color(0xFF94A3B8),
                                    fontSize: 11,
                                    fontWeight: FontWeight.w500,
                                  ),
                                ),
                              ],
                            ),
                            IconButton(
                              icon: const Icon(Icons.close, color: Color(0xFF94A3B8), size: 18),
                              onPressed: () => DialogueManager.instance.closeDialogue(),
                              padding: EdgeInsets.zero,
                              constraints: const BoxConstraints(),
                            ),
                          ],
                        ),
                        const Divider(color: Color(0x3338BDF8), height: 18),
                        // Dialogue Text
                        Text(
                          dialogueNode.text,
                          style: const TextStyle(
                            color: Color(0xFFF1F5F9),
                            fontSize: 13.5,
                            height: 1.45,
                            fontWeight: FontWeight.w400,
                          ),
                        ),
                        const SizedBox(height: 14),
                        // Dialogue Choices
                        if (dialogueNode.choices.isNotEmpty)
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.stretch,
                            children: dialogueNode.choices.map((choice) {
                              return Padding(
                                padding: const EdgeInsets.only(bottom: 6.0),
                                child: OutlinedButton(
                                  style: OutlinedButton.styleFrom(
                                    foregroundColor: const Color(0xFFE2E8F0),
                                    backgroundColor: const Color(0x401E293B),
                                    side: const BorderSide(color: Color(0x5538BDF8)),
                                    padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                                    alignment: Alignment.centerLeft,
                                    shape: RoundedRectangleBorder(
                                      borderRadius: BorderRadius.circular(8),
                                    ),
                                  ),
                                  onPressed: () {
                                    DialogueManager.instance.selectChoice(choice);
                                  },
                                  child: Text(
                                    "▸ ${choice.text}",
                                    style: const TextStyle(fontSize: 12.5),
                                  ),
                                ),
                              );
                            }).toList(),
                          ),
                      ],
                    ),
                  ),
                ),
              );
            },
          ),
        ],
      ),
    );
  }

  void _showNotification(String msg) {
    setState(() => _statusNotification = msg);
    Future.delayed(const Duration(seconds: 3), () {
      if (mounted && _statusNotification == msg) {
        setState(() => _statusNotification = '');
      }
    });
  }

  Widget _buildDebugButton({String? label, required IconData icon, required VoidCallback onTap}) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
        decoration: BoxDecoration(
          color: const Color(0xCC1E293B),
          borderRadius: BorderRadius.circular(6),
          border: Border.all(color: const Color(0x4494A3B8)),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, color: Colors.white, size: 14),
            if (label != null) ...[
              const SizedBox(width: 4),
              Text(label, style: const TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold)),
            ],
          ],
        ),
      ),
    );
  }
}
