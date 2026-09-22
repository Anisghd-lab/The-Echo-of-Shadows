import 'package:flame/components.dart';
import '../../characters/npc_component.dart';
import '../../player/alex_component.dart';
import '../../player/player_orientation_controller.dart';

/// Layer 5: Characters layer dynamically sorted by ground contact point.
/// Holds Alex and all authentic village NPCs (Emma, Ethan, James, Michael).
class CharactersLayer extends Component {
  final AlexComponent alex;
  final List<NpcComponent> npcs = [];

  CharactersLayer({required this.alex});

  @override
  Future<void> onLoad() async {
    await super.onLoad();

    // 1. Add Alex (Protagonist)
    add(alex);

    // 2. Add Emma (Village Friend) at (-1.0, -2.5)
    final emma = NpcComponent(
      id: 'NPC_EMMA',
      name: 'Emma',
      role: "Amie d'Alex",
      worldX: -1.0,
      worldY: -2.5,
      orientation: PlayerOrientationController.southEast,
      assetFolder: 'new assets/characters/emma',
      assetPrefix: 'Emma',
    );
    npcs.add(emma);
    add(emma);

    // 3. Add Officer James (Forester) at (7.0, -0.5)
    final james = NpcComponent(
      id: 'NPC_JAMES',
      name: 'Officier James',
      role: 'Surveillant forestier',
      worldX: 7.0,
      worldY: -0.5,
      orientation: PlayerOrientationController.southWest,
      assetFolder: 'new assets/characters/officer_james',
      assetPrefix: 'Officer-James',
    );
    npcs.add(james);
    add(james);

    // 4. Add Old Michael (Elder / Church Caretaker) at (2.5, -4.5)
    final michael = NpcComponent(
      id: 'NPC_MICHAEL',
      name: 'Vieux Michael',
      role: "Gardien de l'église",
      worldX: 2.5,
      worldY: -4.5,
      orientation: PlayerOrientationController.southEast,
      assetFolder: 'new assets/characters/old_michael',
      assetPrefix: 'Old-Michael',
    );
    npcs.add(michael);
    add(michael);

    // 5. Add Ethan Miller (Echo / Missing Brother) at (1.2, 2.4)
    final ethan = NpcComponent(
      id: 'NPC_ETHAN',
      name: 'Ethan Miller',
      role: 'Frère disparu',
      worldX: 1.2,
      worldY: 2.4,
      orientation: PlayerOrientationController.northWest,
      assetFolder: 'new assets/characters/ethan',
      assetPrefix: 'Ethan-frère-de-Alex',
      frameCount: 12,
    );
    npcs.add(ethan);
    add(ethan);
  }

  /// Returns the NPC closest to Alex if within interaction range and facing.
  NpcComponent? getInteractableNpc() {
    for (final npc in npcs) {
      if (npc.isPlayerInRange(alex)) {
        if (alex.controller.isFacingTarget(npc.worldX, npc.worldY, maxAngleDegrees: 85.0)) {
          return npc;
        }
      }
    }
    return null;
  }
}
