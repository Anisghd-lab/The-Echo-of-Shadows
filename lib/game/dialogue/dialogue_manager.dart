import 'package:flutter/foundation.dart';
import '../../save/save_manager.dart';
import '../../save/save_model.dart';
import '../characters/npc_component.dart';
import '../player/alex_component.dart';
import '../player/player_controller.dart';
import 'dialogue_models.dart';

/// Central dialogue engine governing non-blocking character interactions,
/// narrative dialogue trees, choice consequences, and trust persistence.
class DialogueManager {
  static final DialogueManager instance = DialogueManager._();
  DialogueManager._() {
    _initTrees();
  }

  final Map<String, DialogueTree> _trees = {};

  DialogueNode? _currentNode;
  DialogueNode? get currentNode => _currentNode;

  NpcComponent? _activeNpc;
  NpcComponent? get activeNpc => _activeNpc;

  AlexComponent? _activeAlex;

  final ValueNotifier<DialogueNode?> activeDialogueNotifier = ValueNotifier<DialogueNode?>(null);

  bool get isInDialogue => _currentNode != null;

  void _initTrees() {
    // 1. EMMA'S DIALOGUE TREE (Village Friend)
    _trees['NPC_EMMA'] = DialogueTree(
      npcId: 'NPC_EMMA',
      startNodeId: 'EMMA_START',
      nodes: {
        'EMMA_START': const DialogueNode(
          id: 'EMMA_START',
          speakerName: 'Emma',
          speakerRole: "Amie d'enfance & résidente",
          speakerPortrait: 'new assets/characters/emma/Emma09.png',
          text: "Alex ! Tu es vraiment revenu... Dix ans après cette nuit de 2014. Tu cherches toujours la vérité sur Ethan ?",
          choices: [
            DialogueChoice(
              text: "Emma, que s'est-il passé exactement cette nuit-là ?",
              nextNodeId: 'EMMA_NIGHT_2014',
              trustDelta: 5,
              trustNpcKey: 'emma',
              flagToSet: 'emma_asked_about_2014',
            ),
            DialogueChoice(
              text: "L'Officier James affirme que c'était une simple fugue...",
              nextNodeId: 'EMMA_JAMES_LIE',
              trustDelta: 10,
              trustNpcKey: 'emma',
              flagToSet: 'emma_warned_about_james',
            ),
            DialogueChoice(
              text: "Je n'ai pas le temps de parler, je dois fouiller le village.",
              nextNodeId: 'EMMA_DISMISSED',
              trustDelta: -5,
              trustNpcKey: 'emma',
            ),
          ],
        ),
        'EMMA_NIGHT_2014': const DialogueNode(
          id: 'EMMA_NIGHT_2014',
          speakerName: 'Emma',
          speakerRole: "Amie d'enfance & résidente",
          speakerPortrait: 'new assets/characters/emma/Emma09.png',
          text: "Il y avait des projecteurs près de la vieille scierie, et une sirène dans les bois. Ethan m'avait confié un carnet la veille. Regarde près du vieux puits, il y a caché une clé.",
          choices: [
            DialogueChoice(
              text: "Merci Emma. Je vais aller voir au puits.",
              nextNodeId: 'END',
              trustDelta: 5,
              trustNpcKey: 'emma',
              flagToSet: 'hint_well_key',
              evidenceId: 'EVIDENCE_EMMA_NOTE',
              evidenceTitle: "Témoignage d'Emma sur 2014",
              evidenceDescription: "Emma confirme des lumières anormales et une sirène près de la scierie avant la disparition.",
            ),
          ],
        ),
        'EMMA_JAMES_LIE': const DialogueNode(
          id: 'EMMA_JAMES_LIE',
          speakerName: 'Emma',
          speakerRole: "Amie d'enfance & résidente",
          speakerPortrait: 'new assets/characters/emma/Emma09.png',
          text: "James ment ! Il a scellé le périmètre forestier immédiatement. Fais attention à ce que tu dis devant lui.",
          choices: [
            DialogueChoice(
              text: "Je serai prudent. Merci de me prévenir.",
              nextNodeId: 'END',
              trustDelta: 5,
              trustNpcKey: 'emma',
              flagToSet: 'suspicious_of_officer_james',
            ),
          ],
        ),
        'EMMA_DISMISSED': const DialogueNode(
          id: 'EMMA_DISMISSED',
          speakerName: 'Emma',
          speakerRole: "Amie d'enfance & résidente",
          speakerPortrait: 'new assets/characters/emma/Emma09.png',
          text: "Très bien... Fais attention à toi dans la brume.",
          choices: [
            DialogueChoice(
              text: "[Fermer]",
              nextNodeId: 'END',
            ),
          ],
        ),
      },
    );

    // 2. OFFICER JAMES'S DIALOGUE TREE (Law Enforcement)
    _trees['NPC_JAMES'] = DialogueTree(
      npcId: 'NPC_JAMES',
      startNodeId: 'JAMES_START',
      nodes: {
        'JAMES_START': const DialogueNode(
          id: 'JAMES_START',
          speakerName: 'Officier James',
          speakerRole: 'Surveillant du secteur forestier',
          speakerPortrait: 'new assets/characters/officer_james/Officer-James09.png',
          text: "Halte-là, Alex. Le village est sous arrêté municipal de couvre-feu. La zone au nord de la scierie est strictement interdite d'accès.",
          choices: [
            DialogueChoice(
              text: "Je cherche juste les affaires de mon frère Ethan.",
              nextNodeId: 'JAMES_ETHAN',
              trustDelta: 5,
              trustNpcKey: 'james',
            ),
            DialogueChoice(
              text: "Pourquoi interdire la scierie ? Qu'avez-vous à cacher ?",
              nextNodeId: 'JAMES_ACCUSATION',
              trustDelta: -10,
              trustNpcKey: 'james',
              flagToSet: 'james_antagonized',
            ),
            DialogueChoice(
              text: "Bien reçu, officier. Je reste sur la route principale.",
              nextNodeId: 'END',
              trustDelta: 5,
              trustNpcKey: 'james',
            ),
          ],
        ),
        'JAMES_ETHAN': const DialogueNode(
          id: 'JAMES_ETHAN',
          speakerName: 'Officier James',
          speakerRole: 'Surveillant du secteur forestier',
          speakerPortrait: 'new assets/characters/officer_james/Officer-James09.png',
          text: "Le dossier d'Ethan est clos depuis longtemps. Ne remue pas le passé, Alex. Il y a des choses enfouies sous ce village qu'il vaut mieux laisser dormir.",
          choices: [
            DialogueChoice(
              text: "Je trouverai la vérité, quoi qu'il en coûte.",
              nextNodeId: 'END',
              flagToSet: 'alex_determined_against_james',
              evidenceId: 'EVIDENCE_JAMES_CONFIRMATION',
              evidenceTitle: "Avertissement de l'Officier James",
              evidenceDescription: "L'officier James admet à demi-mot que des secrets sont enfouis sous le village.",
            ),
          ],
        ),
        'JAMES_ACCUSATION': const DialogueNode(
          id: 'JAMES_ACCUSATION',
          speakerName: 'Officier James',
          speakerRole: 'Surveillant du secteur forestier',
          speakerPortrait: 'new assets/characters/officer_james/Officer-James09.png',
          text: "Surveille ton langage, petit. Je représente l'autorité ici. Circule avant que je ne confisque ton matériel.",
          choices: [
            DialogueChoice(
              text: "[S'éloigner]",
              nextNodeId: 'END',
            ),
          ],
        ),
      },
    );

    // 3. OLD MICHAEL'S DIALOGUE TREE (Church Elder)
    _trees['NPC_MICHAEL'] = DialogueTree(
      npcId: 'NPC_MICHAEL',
      startNodeId: 'MICHAEL_START',
      nodes: {
        'MICHAEL_START': const DialogueNode(
          id: 'MICHAEL_START',
          speakerName: 'Vieux Michael',
          speakerRole: "Doyen du village & gardien de l'église",
          speakerPortrait: 'new assets/characters/old_michael/Old-Michael09.png',
          text: "Que la paix soit sur toi, mon enfant. Les ombres s'épaississent sur notre village depuis que les fondations de l'ancien bunker ont été perturbées.",
          choices: [
            DialogueChoice(
              text: "Un bunker ? Où se trouve son entrée, Michael ?",
              nextNodeId: 'MICHAEL_BUNKER',
              trustDelta: 5,
              trustNpcKey: 'michael',
              flagToSet: 'learned_bunker_existence',
            ),
            DialogueChoice(
              text: "Avez-vous vu Ethan avant sa disparition ?",
              nextNodeId: 'MICHAEL_ETHAN',
              trustDelta: 5,
              trustNpcKey: 'michael',
            ),
            DialogueChoice(
              text: "Prenez soin de vous, Michael.",
              nextNodeId: 'END',
            ),
          ],
        ),
        'MICHAEL_BUNKER': const DialogueNode(
          id: 'MICHAEL_BUNKER',
          speakerName: 'Vieux Michael',
          speakerRole: "Doyen du village & gardien de l'église",
          speakerPortrait: 'new assets/characters/old_michael/Old-Michael09.png',
          text: "Derrière les ruines de l'église, sous les dalles de pierre. Mais l'accès est verrouillé par un dispositif électronique des années 80. Il te faudra trouver la carte magnétique.",
          choices: [
            DialogueChoice(
              text: "Je vais chercher cette carte. Merci Michael.",
              nextNodeId: 'END',
              evidenceId: 'EVIDENCE_BUNKER_LOCATION',
              evidenceTitle: "Entrée secrète du Bunker",
              evidenceDescription: "Le Vieux Michael révèle que l'entrée du bunker est dissimulée sous l'église.",
            ),
          ],
        ),
        'MICHAEL_ETHAN': const DialogueNode(
          id: 'MICHAEL_ETHAN',
          speakerName: 'Vieux Michael',
          speakerRole: "Doyen du village & gardien de l'église",
          speakerPortrait: 'new assets/characters/old_michael/Old-Michael09.png',
          text: "Il priait souvent ici. Il avait peur des bruits métalliques venus du sous-sol la nuit.",
          choices: [
            DialogueChoice(
              text: "[Fermer]",
              nextNodeId: 'END',
            ),
          ],
        ),
      },
    );

    // 4. ETHAN'S DIALOGUE TREE (Echo / Apparition)
    _trees['NPC_ETHAN'] = DialogueTree(
      npcId: 'NPC_ETHAN',
      startNodeId: 'ETHAN_START',
      nodes: {
        'ETHAN_START': const DialogueNode(
          id: 'ETHAN_START',
          speakerName: 'Ethan (Écho)',
          speakerRole: 'Frère disparu',
          speakerPortrait: 'new assets/characters/ethan/Ethan-frère-de-Alex01.png',
          text: "Alex... Tu as suivi le signal... Ne crois pas les rapports officiels. La cassette dans notre chambre contient la première clé...",
          choices: [
            DialogueChoice(
              text: "Ethan ! Où es-tu ? Comment puis-je te retrouver ?",
              nextNodeId: 'ETHAN_SIGNAL',
              trustDelta: 10,
              trustNpcKey: 'ethan',
              flagToSet: 'ethan_echo_contacted',
            ),
            DialogueChoice(
              text: "Est-ce une hallucination...",
              nextNodeId: 'END',
            ),
          ],
        ),
        'ETHAN_SIGNAL': const DialogueNode(
          id: 'ETHAN_SIGNAL',
          speakerName: 'Ethan (Écho)',
          speakerRole: 'Frère disparu',
          speakerPortrait: 'new assets/characters/ethan/Ethan-frère-de-Alex01.png',
          text: "Le bunker... sous les racines... Le temps nous est compté...",
          choices: [
            DialogueChoice(
              text: "J'arrive, Ethan.",
              nextNodeId: 'END',
              evidenceId: 'EVIDENCE_ETHAN_WHISPER',
              evidenceTitle: "Message spectral d'Ethan",
              evidenceDescription: "Ethan communique par interférences et ordonne de fouiller la maison familiale.",
            ),
          ],
        ),
      },
    );
  }

  /// Starts a dialogue interaction with an NPC.
  /// Automatically turns Alex and the NPC to face each other.
  void startDialogue({
    required String npcId,
    required AlexComponent alex,
    required NpcComponent npc,
  }) {
    final tree = _trees[npcId];
    if (tree == null) return;

    _activeAlex = alex;
    _activeNpc = npc;

    // 1. Put Alex in talk state (freezes movement)
    alex.controller.state = PlayerMovementState.talk;

    // 2. Dynamic Bidirectional Facing (Phase 16)
    alex.controller.faceTarget(npc.worldX, npc.worldY);
    npc.faceTarget(alex.worldX, alex.worldY);

    // 3. Set starting node
    _currentNode = tree.startNode;
    activeDialogueNotifier.value = _currentNode;
  }

  /// Selects a choice and executes consequences on trust, flags, and evidence.
  void selectChoice(DialogueChoice choice) {
    if (_activeNpc == null || _currentNode == null) return;

    // 1. Apply Trust Delta
    if (choice.trustDelta != 0 && choice.trustNpcKey != null) {
      _applyTrustDelta(choice.trustNpcKey!, choice.trustDelta);
    }

    // 2. Set Flag
    if (choice.flagToSet != null) {
      SaveManager.setFlag(choice.flagToSet!, true);
    }

    // 3. Add Evidence if present
    if (choice.evidenceId != null) {
      SaveManager.addEvidence(EvidenceItemModel(
        id: choice.evidenceId!,
        titleId: choice.evidenceTitle ?? choice.evidenceId!,
        descriptionId: choice.evidenceDescription ?? '',
        category: 'investigation',
        discoveredAt: DateTime.now().toIso8601String(),
      ));
    }

    // 4. Advance or End
    if (choice.nextNodeId == 'END') {
      closeDialogue();
    } else {
      final tree = _trees[_activeNpc!.id];
      _currentNode = tree?.getNode(choice.nextNodeId);
      activeDialogueNotifier.value = _currentNode;
    }
  }

  void closeDialogue() {
    _currentNode = null;
    activeDialogueNotifier.value = null;

    if (_activeAlex != null) {
      _activeAlex!.controller.state = PlayerMovementState.idle;
      _activeAlex = null;
    }
    _activeNpc = null;
  }

  void _applyTrustDelta(String npcKey, int delta) {
    final currentSave = SaveManager.currentSave;
    if (currentSave == null) return;

    int emma = currentSave.trustEmma;
    int james = currentSave.trustJames;
    int michael = currentSave.trustMichael;
    int ethan = currentSave.trustEthan;
    int david = currentSave.trustDavid;
    int sarah = currentSave.trustSarah;

    switch (npcKey.toLowerCase()) {
      case 'emma':
        emma = (emma + delta).clamp(0, 100);
        break;
      case 'james':
        james = (james + delta).clamp(0, 100);
        break;
      case 'michael':
        michael = (michael + delta).clamp(0, 100);
        break;
      case 'ethan':
        ethan = (ethan + delta).clamp(0, 100);
        break;
      case 'david':
        david = (david + delta).clamp(0, 100);
        break;
      case 'sarah':
        sarah = (sarah + delta).clamp(0, 100);
        break;
    }

    SaveManager.currentSave = currentSave.copyWith(
      trustEmma: emma,
      trustJames: james,
      trustMichael: michael,
      trustEthan: ethan,
      trustDavid: david,
      trustSarah: sarah,
    );
  }
}
