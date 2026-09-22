/// Represents a choice option the player can select in a dialogue node.
class DialogueChoice {
  final String text;
  final String nextNodeId;
  final int trustDelta;
  final String? trustNpcKey; // 'emma', 'james', 'michael', 'ethan', 'david', 'sarah'
  final String? flagToSet;
  final String? evidenceId;
  final String? evidenceTitle;
  final String? evidenceDescription;

  const DialogueChoice({
    required this.text,
    required this.nextNodeId,
    this.trustDelta = 0,
    this.trustNpcKey,
    this.flagToSet,
    this.evidenceId,
    this.evidenceTitle,
    this.evidenceDescription,
  });
}

/// Represents an individual dialogue speech bubble / turn in a conversation.
class DialogueNode {
  final String id;
  final String speakerName;
  final String speakerRole;
  final String? speakerPortrait;
  final String text;
  final List<DialogueChoice> choices;

  const DialogueNode({
    required this.id,
    required this.speakerName,
    required this.speakerRole,
    this.speakerPortrait,
    required this.text,
    this.choices = const [],
  });
}

/// Complete dialogue tree for a character.
class DialogueTree {
  final String npcId;
  final String startNodeId;
  final Map<String, DialogueNode> nodes;

  const DialogueTree({
    required this.npcId,
    required this.startNodeId,
    required this.nodes,
  });

  DialogueNode? get startNode => nodes[startNodeId];
  DialogueNode? getNode(String id) => nodes[id];
}
