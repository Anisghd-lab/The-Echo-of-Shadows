import 'package:flame/game.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'game/controls/touch_controller.dart';
import 'game/village_game.dart';
import 'save/save_manager.dart';
import 'ui/game_hud_overlay.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Lock orientation to Landscape for cinematic isometric view
  await SystemChrome.setPreferredOrientations([
    DeviceOrientation.landscapeLeft,
    DeviceOrientation.landscapeRight,
  ]);

  // Immersive full screen
  await SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);

  // Initialize pure local SaveManager
  final saveManager = SaveManager();
  final hasSave = await saveManager.initialize();
  if (!hasSave) {
    await saveManager.createNewGame();
  } else {
    await saveManager.loadGame();
  }

  // Initialize Touch controller
  final touchController = TouchInputController();

  // Instantiate Game
  final game = VillageGame(
    saveManager: saveManager,
    touchController: touchController,
  );

  runApp(
    MaterialApp(
      title: "L'Écho des Ombres",
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark(),
      home: Scaffold(
        backgroundColor: const Color(0xFF0F172A),
        body: Stack(
          children: [
            // Flame Canvas
            GameWidget(
              game: game,
              overlayBuilderMap: {
                'HUD': (BuildContext context, VillageGame g) {
                  return GameHUDOverlay(
                    game: g,
                    touchController: touchController,
                  );
                },
              },
              initialActiveOverlays: const ['HUD'],
            ),
          ],
        ),
      ),
    ),
  );
}
