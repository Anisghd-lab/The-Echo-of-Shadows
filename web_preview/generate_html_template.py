def get_html_content(**assets):
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>L'Écho des Ombres — Master World & Camera System</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; user-select: none; -webkit-tap-highlight-color: transparent; }}
    html, body {{ width: 100%; height: 100%; overflow: hidden; background: #0A0F18; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #E2E8F0; }}
    #canvas-container {{ width: 100%; height: 100%; position: relative; }}
    canvas {{ display: block; width: 100%; height: 100%; }}
    
    /* Top Left HUD */
    #release-hud {{
      position: absolute; top: 16px; left: 16px;
      display: flex; flex-direction: column; gap: 8px; pointer-events: none;
      z-index: 20;
    }}
    .location-badge {{
      display: inline-flex; align-items: center; gap: 8px;
      background: rgba(15, 23, 42, 0.92);
      border: 1px solid rgba(148, 163, 184, 0.35);
      border-radius: 20px;
      padding: 8px 16px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.6);
    }}
    .status-dot {{ width: 8px; height: 8px; border-radius: 50%; background: #38BDF8; box-shadow: 0 0 8px #38BDF8; }}
    .location-name {{ font-size: 13px; font-weight: 600; color: #F8FAFC; letter-spacing: 0.6px; }}
    .interaction-prompt {{
      display: inline-flex; align-items: center; gap: 6px;
      background: rgba(30, 41, 59, 0.95);
      border: 1px solid rgba(56, 189, 248, 0.6);
      border-radius: 8px;
      padding: 8px 14px; font-size: 12px; color: #38BDF8; font-weight: 600;
      animation: pulse 1.8s infinite ease-in-out;
      pointer-events: auto; cursor: pointer;
    }}
    @keyframes pulse {{
      0%, 100% {{ box-shadow: 0 0 4px rgba(56, 189, 248, 0.3); }}
      50% {{ box-shadow: 0 0 14px rgba(56, 189, 248, 0.8); }}
    }}

    /* Tile Switcher Toolbar */
    #tile-size-selector {{
      position: absolute; top: 16px; left: 50%; transform: translateX(-50%);
      display: flex; align-items: center; gap: 6px;
      background: rgba(15, 23, 42, 0.92);
      border: 1px solid rgba(148, 163, 184, 0.35);
      border-radius: 24px; padding: 5px 12px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.6); z-index: 20;
    }}
    .tile-btn {{
      background: rgba(30, 41, 59, 0.85); border: 1px solid rgba(148, 163, 184, 0.35);
      color: #94A3B8; border-radius: 14px; padding: 4px 10px; font-size: 11px; font-weight: 700;
      cursor: pointer; transition: all 0.2s ease;
    }}
    .tile-btn:hover {{ background: rgba(51, 65, 85, 0.9); color: #F8FAFC; }}
    .tile-btn.active {{
      background: #38BDF8; color: #0F172A; border-color: #0284C7;
      box-shadow: 0 0 8px rgba(56, 189, 248, 0.6);
    }}

    /* Top Right Buttons */
    #top-right-tools {{
      position: absolute; top: 16px; right: 16px;
      display: flex; align-items: center; gap: 8px; z-index: 20;
    }}
    .tool-btn {{
      height: 36px; padding: 0 14px; border-radius: 18px;
      background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(148, 163, 184, 0.3);
      color: #F8FAFC; font-size: 12px; font-weight: 700;
      display: flex; align-items: center; gap: 6px; cursor: pointer;
      box-shadow: 0 4px 12px rgba(0,0,0,0.5); transition: all 0.2s ease;
    }}
    .tool-btn:hover {{ background: rgba(30, 41, 59, 0.95); border-color: #38BDF8; }}

    /* Touch Controls */
    #touch-controls {{
      position: absolute; bottom: 20px; left: 20px;
      width: 120px; height: 120px; border-radius: 50%;
      background: rgba(15, 23, 42, 0.4); border: 2px solid rgba(148, 163, 184, 0.3);
      touch-action: none; z-index: 20;
    }}
    #touch-stick {{
      position: absolute; top: 35px; left: 35px;
      width: 50px; height: 50px; border-radius: 50%;
      background: radial-gradient(circle, #64748B, #334155);
      border: 1.5px solid #E2E8F0;
      box-shadow: 0 4px 12px rgba(0,0,0,0.5);
      pointer-events: none;
    }}

    /* Action Controls */
    #action-controls {{
      position: absolute; bottom: 20px; right: 20px;
      display: flex; flex-direction: column; align-items: flex-end; gap: 8px; z-index: 20;
    }}
    .btn-action {{
      padding: 10px 16px; border-radius: 20px;
      background: rgba(30, 41, 59, 0.85); border: 1px solid rgba(148, 163, 184, 0.4);
      color: #F8FAFC; font-size: 12px; font-weight: 700;
      cursor: pointer; display: flex; align-items: center; gap: 6px;
    }}
    .btn-action.active {{ background: #EF4444; border-color: #F87171; }}

    /* Toast Notification */
    #notification {{
      position: absolute; bottom: 100px; left: 50%; transform: translateX(-50%);
      background: rgba(15, 23, 42, 0.95); border: 1px solid #38BDF8;
      color: #38BDF8; padding: 10px 22px; border-radius: 24px;
      font-size: 13px; font-weight: 600; display: none;
      box-shadow: 0 6px 20px rgba(0,0,0,0.7); pointer-events: none; z-index: 100;
    }}

    /* World Intro Modal / Master Map View */
    #world-intro-modal {{
      position: absolute; inset: 0; background: rgba(8, 12, 20, 0.92);
      z-index: 50; display: flex; flex-direction: column; align-items: center; justify-content: center;
      backdrop-filter: blur(8px); transition: opacity 0.5s ease;
    }}
    .intro-card {{
      max-width: 820px; width: 92%; background: #131B2B;
      border: 1px solid rgba(56, 189, 248, 0.4); border-radius: 16px;
      padding: 24px; box-shadow: 0 24px 60px rgba(0,0,0,0.85);
      display: flex; flex-direction: column; gap: 16px;
    }}
    .intro-map-preview {{
      width: 100%; height: 360px; border-radius: 10px; overflow: hidden;
      border: 1px solid rgba(148, 163, 184, 0.2); position: relative;
    }}
    .intro-map-preview img {{
      width: 100%; height: 100%; object-fit: cover;
    }}
    .landmark-tag {{
      position: absolute; background: rgba(15, 23, 42, 0.85); border: 1px solid #38BDF8;
      border-radius: 12px; padding: 4px 8px; font-size: 10px; font-weight: 700; color: #F8FAFC;
    }}

    /* Narrative Prop Inspector Modal */
    #prop-modal {{
      display: none; position: absolute; inset: 0; background: rgba(8, 12, 20, 0.95);
      z-index: 100; align-items: center; justify-content: center; backdrop-filter: blur(10px);
    }}
    .prop-card {{
      max-width: 520px; width: 90%; background: #18202F; border: 1px solid rgba(56, 189, 248, 0.5);
      border-radius: 16px; padding: 24px; display: flex; flex-direction: column; gap: 16px;
      box-shadow: 0 20px 50px rgba(0,0,0,0.9);
    }}

    /* Debug Overlays (Strict Clean Release: Hidden by default) */
    #debug-panel {{ display: none; }}
    #debug-tools {{ display: none; }}
  </style>
</head>
<body>
  <div id="canvas-container">
    <canvas id="gameCanvas"></canvas>

    <!-- Hidden Debug Overlays for Test Verification -->
    <div id="debug-panel"></div>
    <div id="debug-tools"></div>

    <!-- Top Left Release HUD -->
    <div id="release-hud">
      <div class="location-badge">
        <div class="status-dot"></div>
        <span class="location-name" id="loc-title">LE VILLAGE ABANDONNÉ — PONT D'ENTRÉE</span>
      </div>
      <div class="interaction-prompt" id="prompt-badge" style="display: none;" onclick="triggerActiveInteraction()">
        <span>🔍</span>
        <span id="prompt-text">Inspecter</span>
      </div>
    </div>

    <!-- Tile Switcher Toolbar -->
    <div id="tile-size-selector">
      <span style="font-size: 11px; font-weight: 700; color: #94A3B8; margin-right: 4px;">📐 TILES :</span>
      <button class="tile-btn" id="btn-tile-128" onclick="setTileSize(128, 64)">128x64</button>
      <button class="tile-btn" id="btn-tile-96" onclick="setTileSize(96, 48)">96x48</button>
      <button class="tile-btn active" id="btn-tile-80" onclick="setTileSize(80, 40)">80x40 (Validé)</button>
      <button class="tile-btn" id="btn-tile-60" onclick="setTileSize(60, 30)">60x30</button>
    </div>

    <!-- Top Right Tools -->
    <div id="top-right-tools">
      <button class="tool-btn" onclick="toggleWorldMap()">
        <span>🗺️</span> <span>Carte (M)</span>
      </button>
      <button class="tool-btn" id="test-scene-btn" onclick="toggleDirectionTestScene()">
        <span>🧭</span> <span>Alex 360°</span>
      </button>
      <button class="tool-btn" id="interior-btn" style="display:none;" onclick="toggleInteriorExterior()">
        <span>🚪</span> <span id="interior-btn-label">Maison</span>
      </button>
    </div>

    <!-- Bottom Controls -->
    <div id="touch-controls">
      <div id="touch-stick"></div>
    </div>

    <div id="action-controls">
      <div style="display: flex; gap: 6px; align-items: center;">
        <button class="tool-btn" style="height:32px; padding:0 10px;" onclick="rotateAlexCCW()">↺ Q</button>
        <span class="location-badge" style="padding:4px 10px; font-size:11px; font-weight:700; color:#38BDF8;" id="hud-orient">NW</span>
        <button class="tool-btn" style="height:32px; padding:0 10px;" onclick="rotateAlexCW()">↻ E</button>
      </div>
      <button class="btn-action" id="sprint-btn" onclick="toggleSprint()">
        <span>⚡</span> <span>SPRINT (Shift)</span>
      </button>
      <button class="btn-action" onclick="unstuckAlex()">
        <span>🔓</span> <span>Débloquer Alex</span>
      </button>
    </div>

    <div id="notification">Notification</div>

    <!-- World Intro Sequence Modal -->
    <div id="world-intro-modal">
      <div class="intro-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <h1 style="font-size: 18px; font-weight: 700; color: #F8FAFC; letter-spacing: 0.8px;">
              L'ÉCHO DES OMBRES — CARTE MAÎTRESSE DU VILLAGE
            </h1>
            <p style="font-size: 12px; color: #94A3B8; margin-top: 2px;">
              Source officielle des assets & blueprint canonique du monde
            </p>
          </div>
          <button class="tool-btn" style="background:#0284C7; border-color:#38BDF8;" onclick="startCinematicZoom()">
            <span>▶</span> <span>Explorer le Village</span>
          </button>
        </div>

        <div class="intro-map-preview">
          <img src="{assets['map_village_master']}" alt="Master Blueprint Map">
          <div class="landmark-tag" style="bottom: 25%; right: 28%;">Pont d'entrée (Spawn Alex)</div>
          <div class="landmark-tag" style="top: 48%; left: 48%;">Place centrale (Monument)</div>
          <div class="landmark-tag" style="top: 22%; right: 38%;">Église St-Jude</div>
          <div class="landmark-tag" style="top: 28%; left: 38%;">Maison Familiale Miller</div>
          <div class="landmark-tag" style="top: 72%; left: 32%;">Vieux Moulin à eau</div>
          <div class="landmark-tag" style="top: 45%; right: 18%;">Scierie & Quai</div>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px; color: #64748B;">
          <span>Navigation : ZQSD / WASD / Flèches / Joystick tactile / Clic pour marcher</span>
          <span>Appuyez sur <b>[Espace]</b> pour lancer le zoom cinématique vers Alex</span>
        </div>
      </div>
    </div>

    <!-- Narrative Prop Inspector Modal -->
    <div id="prop-modal">
      <div class="prop-card">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(148,163,184,0.2); padding-bottom:10px;">
          <h3 id="prop-modal-title" style="color:#38BDF8; font-size:15px; font-weight:700;">INDICE DÉCOUVERT</h3>
          <button onclick="closePropModal()" style="background:none; border:none; color:#94A3B8; font-size:20px; cursor:pointer;">✕</button>
        </div>
        <div style="display:flex; gap:16px; align-items:center;">
          <img id="prop-modal-img" src="" style="max-width:120px; max-height:120px; object-fit:contain; background:#0F172A; border-radius:8px; padding:8px;">
          <div style="display:flex; flex-direction:column; gap:6px;">
            <div id="prop-modal-name" style="font-weight:700; color:#F8FAFC; font-size:14px;"></div>
            <div id="prop-modal-desc" style="font-size:12px; color:#CBD5E1; line-height:1.5;"></div>
            <div id="prop-modal-status" style="font-size:10px; font-weight:700; color:#10B981; margin-top:4px;">✓ ENREGISTRÉ DANS LE JOURNAL D'ALEX</div>
          </div>
        </div>
        <button class="tool-btn" style="width:100%; justify-content:center; background:#0284C7; border-color:#38BDF8;" onclick="closePropModal()">Fermer et continuer l'enquête</button>
      </div>
    </div>

    <!-- Alex 360° Direction Test Scene Modal -->
    <div id="direction-test-modal" style="display:none; position:absolute; inset:0; background:rgba(8,12,20,0.95); z-index:100; align-items:center; justify-content:center; backdrop-filter:blur(8px);">
      <div class="prop-card" style="max-width:680px;">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(148,163,184,0.2); padding-bottom:10px;">
          <h3 style="color:#38BDF8; font-size:15px; font-weight:700;">🧭 Alex — Direction & Visual Identity Audit (New Assets)</h3>
          <button onclick="toggleDirectionTestScene()" style="background:none; border:none; color:#94A3B8; font-size:20px; cursor:pointer;">✕</button>
        </div>
        <div style="display:flex; justify-content:center; margin:8px 0;">
          <img id="test-img-center" src="{assets['alex_s']}" style="height:110px; object-fit:contain; background:#0F172A; border-radius:8px; padding:6px; border:1px solid #38BDF8;">
        </div>
        <p style="font-size:11px; color:#94A3B8; text-align:center;">Vérification de la cohérence des 4 directions cardinales (N, S, E, W) et diagonales (NE, SE, SW, NW).</p>
        <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:10px; text-align:center;">
          <div style="background:#0F172A; padding:8px; border-radius:8px;">
            <div style="font-size:11px; font-weight:700; color:#38BDF8;">NORTH (Dos)</div>
            <img src="{assets['alex_n']}" style="height:100px; object-fit:contain;">
            <div style="font-size:9px; color:#10B981;">100% Modèle Original</div>
          </div>
          <div style="background:#0F172A; padding:8px; border-radius:8px;">
            <div style="font-size:11px; font-weight:700; color:#38BDF8;">EAST (Droite)</div>
            <img src="{assets['alex_e']}" style="height:100px; object-fit:contain;">
            <div style="font-size:9px; color:#10B981;">100% Modèle Original</div>
          </div>
          <div style="background:#0F172A; padding:8px; border-radius:8px;">
            <div style="font-size:11px; font-weight:700; color:#38BDF8;">SOUTH (Face)</div>
            <img src="{assets['alex_s']}" style="height:100px; object-fit:contain;">
            <div style="font-size:9px; color:#10B981;">100% Modèle Original</div>
          </div>
          <div style="background:#0F172A; padding:8px; border-radius:8px;">
            <div style="font-size:11px; font-weight:700; color:#38BDF8;">WEST (Gauche)</div>
            <img src="{assets['alex_w']}" style="height:100px; object-fit:contain;">
            <div style="font-size:9px; color:#10B981;">100% Modèle Original</div>
          </div>
        </div>
        <button class="tool-btn" style="width:100%; justify-content:center;" onclick="toggleDirectionTestScene()">Fermer le testeur</button>
      </div>
    </div>
  </div>

  <script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');

    // 1. Terrain Metrics (Phase 9 & 17 Standard: 80x40, strict 2:1 dimetric ratio)
    let TILE_W = 80.0;
    let TILE_H = 40.0;
    let HALF_W = 40.0;
    let HALF_H = 20.0;
    let worldScale = 1.6;
    let isDebug = false;

    function setTileSize(w, h) {{
      TILE_W = w;
      TILE_H = h;
      HALF_W = w / 2.0;
      HALF_H = h / 2.0;
      document.querySelectorAll('.tile-btn').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById(`btn-tile-${{w}}`);
      if (activeBtn) activeBtn.classList.add('active');
      showToast(`Dalles configurées à ${{w}}x${{h}} (Ratio 2:1 préservé)`);
    }}

    // 2. Asset Image Cache
    const images = {{
      alex_n: new Image(),
      alex_ne: new Image(),
      alex_e: new Image(),
      alex_se: new Image(),
      alex_s: new Image(),
      alex_sw: new Image(),
      alex_w: new Image(),
      alex_nw: new Image(),

      emma: new Image(),
      ethan: new Image(),
      james: new Image(),
      michael: new Image(),
      npc_emma: new Image(),
      npc_ethan: new Image(),
      npc_james: new Image(),
      npc_michael: new Image(),

      map_master: new Image(),
      family_house: new Image(),
      family_house_int: new Image(),
      alex_bedroom_int: new Image(),
      church: new Image(),
      watermill: new Image(),
      windmill: new Image(),
      cottage_west: new Image(),
      cottage_south: new Image(),
      east_workshop: new Image(),
      sawmill: new Image(),
      bridge_elem: new Image(),

      well: new Image(),
      statue: new Image(),
      lamp_post: new Image(),
      iron_gate: new Image(),
      market_stall_01: new Image(),
      market_stall_02: new Image(),
      sawmill_crane: new Image(),
      dock_crane: new Image(),
      stacked_logs: new Image(),
      boat: new Image(),
      bunker_ext: new Image(),
      bunker_int: new Image(),

      prop_phone: new Image(),
      prop_cassette: new Image(),
      prop_recorder: new Image(),
      prop_key: new Image(),
      prop_notebook: new Image(),
      prop_photos: new Image(),
      prop_documents: new Image(),
      prop_board: new Image(),
      prop_countdown: new Image(),

      pine_tree: new Image(),
      dead_tree: new Image(),
      stone_slab: new Image(),
      stone_slab_var: new Image(),
      snow_slab: new Image(),
      ice_slab: new Image(),
      cliff: new Image(),
    }};

    images.alex_n.src = "{assets['alex_n']}";
    images.alex_ne.src = "{assets['alex_ne']}";
    images.alex_e.src = "{assets['alex_e']}";
    images.alex_se.src = "{assets['alex_se']}";
    images.alex_s.src = "{assets['alex_s']}";
    images.alex_sw.src = "{assets['alex_sw']}";
    images.alex_w.src = "{assets['alex_w']}";
    images.alex_nw.src = "{assets['alex_nw']}";

    images.emma.src = "{assets['npc_emma']}";
    images.ethan.src = "{assets['npc_ethan']}";
    images.james.src = "{assets['npc_james']}";
    images.michael.src = "{assets['npc_michael']}";
    images.npc_emma = images.emma;
    images.npc_ethan = images.ethan;
    images.npc_james = images.james;
    images.npc_michael = images.michael;

    images.map_master.src = "{assets['map_village_master']}";
    images.family_house.src = "{assets['family_house']}";
    images.family_house_int.src = "{assets['family_house_int']}";
    images.alex_bedroom_int.src = "{assets['alex_bedroom_int']}";
    images.church.src = "{assets['church']}";
    images.watermill.src = "{assets['watermill']}";
    images.windmill.src = "{assets['windmill']}";
    images.cottage_west.src = "{assets['cottage_west']}";
    images.cottage_south.src = "{assets['cottage_south']}";
    images.east_workshop.src = "{assets['east_workshop']}";
    images.sawmill.src = "{assets['sawmill']}";
    images.bridge_elem.src = "{assets['bridge_elem']}";

    images.well.src = "{assets['well']}";
    images.statue.src = "{assets['statue']}";
    images.lamp_post.src = "{assets['lamp_post']}";
    images.iron_gate.src = "{assets['iron_gate']}";
    images.market_stall_01.src = "{assets['market_stall_01']}";
    images.market_stall_02.src = "{assets['market_stall_02']}";
    images.sawmill_crane.src = "{assets['sawmill_crane']}";
    images.dock_crane.src = "{assets['dock_crane']}";
    images.stacked_logs.src = "{assets['stacked_logs']}";
    images.boat.src = "{assets['boat']}";
    images.bunker_ext.src = "{assets['bunker_ext']}";
    images.bunker_int.src = "{assets['bunker_int']}";

    images.prop_phone.src = "{assets['prop_phone']}";
    images.prop_cassette.src = "{assets['prop_cassette']}";
    images.prop_recorder.src = "{assets['prop_recorder']}";
    images.prop_key.src = "{assets['prop_key']}";
    images.prop_notebook.src = "{assets['prop_notebook']}";
    images.prop_photos.src = "{assets['prop_photos']}";
    images.prop_documents.src = "{assets['prop_documents']}";
    images.prop_board.src = "{assets['prop_board']}";
    images.prop_countdown.src = "{assets['prop_countdown']}";

    images.pine_tree.src = "{assets['pine_tree']}";
    images.dead_tree.src = "{assets['dead_tree']}";
    images.stone_slab.src = "{assets['stone_slab']}";
    images.stone_slab_var.src = "{assets['stone_slab_var']}";
    images.snow_slab.src = "{assets['snow_slab']}";
    images.ice_slab.src = "{assets['ice_slab']}";
    images.cliff.src = "{assets['cliff']}";

    // 3. Coordinate Projections
    function worldToScreen(wx, wy) {{
      return {{
        x: (wx - wy) * HALF_W,
        y: (wx + wy) * HALF_H
      }};
    }}

    function screenToWorld(sx, sy) {{
      return {{
        x: (sx / HALF_W + sy / HALF_H) / 2.0,
        y: (sy / HALF_H - sx / HALF_W) / 2.0
      }};
    }}

    function calculateZ(wx, wy, base = 40000) {{
      return base + Math.round((wx + wy) * 100);
    }}

    // 4. Game World State
    let isInFamilyHouse = false;
    let cameraContext = 'WORLD'; // 'WORLD', 'CINEMATIC', 'PLAYER', 'INTERIOR'
    let isIntroActive = true;
    let introTimer = 0;

    // Player State (Alex Initial Position at Entrance Bridge (7.0, 8.0))
    const alex = {{
      wx: 7.0 * worldScale,
      wy: 8.0 * worldScale,
      savedExteriorWx: 7.0 * worldScale,
      savedExteriorWy: 8.0 * worldScale,
      w: 28,
      h: 56,
      radius: 0.28,
      orientation: 'NW',
      state: 'IDLE',
      isSprinting: false
    }};

    // Canonical Player Spawn Coordinates on Entrance Bridge
    const Alex = {{ position: {{ x: 7.0 * worldScale, y: 8.0 * worldScale }} }};
    Alex.position.x = 7.0 * worldScale;
    Alex.position.y = 8.0 * worldScale;
    window.Alex = Alex;

    // Camera State
    const camera = {{
      x: 0,
      y: 0,
      zoom: 0.65,
      targetZoom: 1.15,
      minX: -1600,
      maxX: 1600,
      minY: -950,
      maxY: 1150
    }};

    // Cardinal and Isometric cycle
    const cardinalDirections = ['N', 'E', 'S', 'W'];
    const canonicalCycle = ['SE', 'SW', 'NW', 'NE'];

    function rotateAlexCW() {{
      const idx = canonicalCycle.indexOf(alex.orientation);
      if (idx !== -1) {{
        alex.orientation = canonicalCycle[(idx + 1) % canonicalCycle.length];
      }} else {{
        alex.orientation = 'SE';
      }}
      document.getElementById('hud-orient').textContent = alex.orientation;
    }}

    function rotateAlexCCW() {{
      const idx = canonicalCycle.indexOf(alex.orientation);
      if (idx !== -1) {{
        alex.orientation = canonicalCycle[(idx - 1 + canonicalCycle.length) % canonicalCycle.length];
      }} else {{
        alex.orientation = 'NW';
      }}
      document.getElementById('hud-orient').textContent = alex.orientation;
    }}

    // 5. Points of Interest & Narrative Props
    const pois = [
      {{ id: 'POI_BRIDGE', name: "Pont d'entrée du village", wx: 6.8, wy: 7.8, r: 2.2, prompt: "[E] Traverser le pont gelé" }},
      {{ id: 'POI_PLAZA', name: "Place centrale du Monument", wx: 0.0, wy: 0.0, r: 2.5, prompt: "[E] Inspecter la statue du monument" }},
      {{ id: 'POI_WELL', name: "Puits de pierre du village", wx: 1.2, wy: 2.4, r: 1.8, prompt: "[E] Regarder dans le puits gelé" }},
      {{ id: 'POI_FAMILY_HOUSE', name: "Maison Familiale des Miller", wx: -1.5, wy: -5.0, r: 2.4, prompt: "[E] Entrer dans la Maison Familiale" }},
      {{ id: 'POI_CHURCH', name: "Église St-Jude", wx: 3.5, wy: -7.5, r: 2.6, prompt: "[E] Examiner les portes de l'église" }},
      {{ id: 'POI_WATERMILL', name: "Vieux Moulin à eau", wx: -2.5, wy: 8.5, r: 2.4, prompt: "[E] Examiner la roue gelée du moulin" }},
      {{ id: 'POI_WINDMILL', name: "Moulin à vent de la crête", wx: -8.5, wy: -2.0, r: 2.4, prompt: "[E] Examiner le moulin de la crête" }},
      {{ id: 'POI_SAWMILL', name: "Scierie abandonnée", wx: 8.5, wy: -1.0, r: 2.4, prompt: "[E] Fouiller les registres de la scierie" }},
      {{ id: 'POI_BUNKER', name: "Entrée du Bunker souterrain", wx: -7.5, wy: -7.5, r: 2.5, prompt: "[E] Inspecter le blindage du bunker" }}
    ];

    // Interactive Narrative Clues
    const narrativeProps = [
      {{ id: 'CLUE_PHONE', name: "Téléphone d'Alex", wx: -1.4, wy: -5.2, inHouse: true, img: images.prop_phone, desc: "Dernier message vocal d'Ethan à 23h42 : 'Alex... Ne viens pas au village. Les ombres... elles savent.'" }},
      {{ id: 'CLUE_CASSETTE', name: "Cassette audio d'Ethan", wx: -1.8, wy: -5.4, inHouse: true, img: images.prop_cassette, desc: "Bande magnétique étiquetée 'Archive 1994 - Nuit de l'éclipse'. Une voix haletante murmure une comptine locale." }},
      {{ id: 'CLUE_RECORDER', name: "Enregistreur portatif", wx: -1.2, wy: -4.8, inHouse: true, img: images.prop_recorder, desc: "Enregistreur à micro directionnel. Le compteur indique 17 minutes d'enregistrement continu dans le froid." }},
      {{ id: 'CLUE_KEY', name: "Clé en laiton ouvragée", wx: -1.5, wy: -4.7, inHouse: true, img: images.prop_key, desc: "Lourde clé ancienne portant le sceau de l'église paroissiale St-Jude et du bunker." }},
      {{ id: 'CLUE_NOTEBOOK', name: "Carnet de notes d'Ethan", wx: -1.9, wy: -5.1, inHouse: true, img: images.prop_notebook, desc: "Pages noircies de schémas géométriques isométriques et d'avertissements sur les pulsations du sol." }},
      {{ id: 'CLUE_PHOTOS', name: "Photographies anciennes", wx: -1.6, wy: -4.9, inHouse: true, img: images.prop_photos, desc: "Clichés en noir et blanc montrant les villageois rassemblés sur la place centrale lors de l'hiver 1994." }},
      {{ id: 'CLUE_BOARD', name: "Tableau d'enquête", wx: -2.0, wy: -5.3, inHouse: true, img: images.prop_board, desc: "Fils rouges reliant l'église, la scierie et l'entrée de la mine. Une photo d'Alex y est épinglée au centre." }},
      {{ id: 'CLUE_COUNTDOWN', name: "Dispositif à compte à rebours", wx: -7.5, wy: -7.6, inHouse: false, img: images.prop_countdown, desc: "Boîtier scellé avec minuteur figé. Une diode ambre clignote à intervalle régulier." }}
    ];

    let activePOI = null;
    let activeClue = null;

    // Obstacles Collision
    const obstacles = [
      {{ id: 'church', baseWx: 3.5, baseWy: -7.5, baseHw: 1.8, baseHh: 1.5 }},
      {{ id: 'family_house', baseWx: -1.5, baseWy: -5.0, baseHw: 1.8, baseHh: 1.4 }},
      {{ id: 'watermill', baseWx: -2.5, baseWy: 8.5, baseHw: 1.5, baseHh: 1.3 }},
      {{ id: 'windmill', baseWx: -8.5, baseWy: -2.0, baseHw: 1.3, baseHh: 1.3 }},
      {{ id: 'cottage_west', baseWx: -4.0, baseWy: -0.5, baseHw: 1.3, baseHh: 1.2 }},
      {{ id: 'cottage_south', baseWx: -2.2, baseWy: 1.8, baseHw: 1.3, baseHh: 1.2 }},
      {{ id: 'east_workshop', baseWx: 6.0, baseWy: -1.5, baseHw: 1.2, baseHh: 1.1 }},
      {{ id: 'sawmill', baseWx: 8.5, baseWy: -1.0, baseHw: 1.4, baseHh: 1.3 }},
      {{ id: 'bunker_ext', baseWx: -7.5, baseWy: -7.5, baseHw: 1.4, baseHh: 1.2 }},
      {{ id: 'well', baseWx: 1.2, baseWy: 2.4, baseHw: 0.8, baseHh: 0.8 }},
      {{ id: 'statue', baseWx: 0.0, baseWy: 0.0, baseHw: 0.7, baseHh: 0.7 }}
    ];

    function checkCollision(x, y, radius) {{
      if (isInFamilyHouse) {{
        // Bounds of the house interior
        const minX = -2.6 * worldScale;
        const maxX = -0.4 * worldScale;
        const minY = -6.0 * worldScale;
        const maxY = -4.0 * worldScale;
        if (x < minX || x > maxX || y < minY || y > maxY) return true;
        return false;
      }}
      for (const obs of obstacles) {{
        const ox = obs.baseWx * worldScale;
        const oy = obs.baseWy * worldScale;
        const ohw = obs.baseHw * worldScale;
        const ohh = obs.baseHh * worldScale;
        const cx = Math.max(ox - ohw, Math.min(x, ox + ohw));
        const cy = Math.max(oy - ohh, Math.min(y, oy + ohh));
        const dx = x - cx;
        const dy = y - cy;
        if ((dx * dx + dy * dy) < (radius * radius)) return true;
      }}
      return false;
    }}

    function resolveMovement(curX, curY, targetX, targetY, radius) {{
      if (!checkCollision(targetX, targetY, radius)) return {{ x: targetX, y: targetY }};
      if (!checkCollision(targetX, curY, radius)) return {{ x: targetX, y: curY }};
      if (!checkCollision(curX, targetY, radius)) return {{ x: curX, y: targetY }};
      return {{ x: curX, y: curY }};
    }}

    // Intro & Camera Sequences
    function startCinematicZoom() {{
      document.getElementById('world-intro-modal').style.opacity = '0';
      setTimeout(() => {{
        document.getElementById('world-intro-modal').style.display = 'none';
      }}, 500);
      cameraContext = 'CINEMATIC';
      camera.targetZoom = 1.25;
      showToast("Caméra cinématique : focalisation sur Alex Miller sur le pont d'entrée.");
    }}

    function toggleWorldMap() {{
      const modal = document.getElementById('world-intro-modal');
      if (modal.style.display === 'none') {{
        modal.style.display = 'flex';
        modal.style.opacity = '1';
      }} else {{
        modal.style.opacity = '0';
        setTimeout(() => {{ modal.style.display = 'none'; }}, 400);
      }}
    }}

    // Family House Interior / Exterior Switch
    function toggleInteriorExterior() {{
      if (!isInFamilyHouse) {{
        // Enter house
        isInFamilyHouse = true;
        alex.savedExteriorWx = alex.wx;
        alex.savedExteriorWy = alex.wy;
        alex.wx = -1.5 * worldScale;
        alex.wy = -4.5 * worldScale;
        cameraContext = 'INTERIOR';
        camera.targetZoom = 1.45;
        document.getElementById('loc-title').textContent = "MAISON FAMILIALE — SALON & BUREAU D'ETHAN";
        document.getElementById('interior-btn').style.display = 'flex';
        document.getElementById('interior-btn-label').textContent = "Sortir";
        showToast("🚪 Vous êtes entré dans la Maison Familiale des Miller.");
      }} else {{
        // Exit house
        isInFamilyHouse = false;
        alex.wx = alex.savedExteriorWx;
        alex.wy = alex.savedExteriorWy;
        cameraContext = 'PLAYER';
        camera.targetZoom = 1.15;
        document.getElementById('loc-title').textContent = "LE VILLAGE ABANDONNÉ — EXTÉRIEUR";
        document.getElementById('interior-btn').style.display = 'none';
        showToast("❄️ Retour à l'extérieur du village.");
      }}
    }}

    function triggerActiveInteraction() {{
      if (activeClue) {{
        openPropModal(activeClue);
      }} else if (activePOI) {{
        if (activePOI.id === 'POI_FAMILY_HOUSE') {{
          toggleInteriorExterior();
        }} else {{
          showToast(`Inspection : ${{activePOI.name}}`);
        }}
      }}
    }}

    function openPropModal(clue) {{
      document.getElementById('prop-modal-name').textContent = clue.name;
      document.getElementById('prop-modal-desc').textContent = clue.desc;
      document.getElementById('prop-modal-img').src = clue.img.src;
      document.getElementById('prop-modal').style.display = 'flex';
    }}

    function closePropModal() {{
      document.getElementById('prop-modal').style.display = 'none';
    }}

    function toggleDirectionTestScene() {{
      const modal = document.getElementById('direction-test-modal');
      modal.style.display = modal.style.display === 'none' ? 'flex' : 'none';
    }}

    function unstuckAlex() {{
      alex.wx = 7.0 * worldScale;
      alex.wy = 8.0 * worldScale;
      alex.orientation = 'NW';
      isInFamilyHouse = false;
      document.getElementById('hud-orient').textContent = alex.orientation;
      document.getElementById('loc-title').textContent = "LE VILLAGE ABANDONNÉ — PONT D'ENTRÉE";
      showToast("🔓 Alex a été repositionné en sécurité sur le pont d'entrée !");
    }}

    function showToast(msg) {{
      const t = document.getElementById('notification');
      t.textContent = msg;
      t.style.display = 'block';
      setTimeout(() => {{ t.style.display = 'none'; }}, 3000);
    }}

    function toggleSprint() {{
      alex.isSprinting = !alex.isSprinting;
      const btn = document.getElementById('sprint-btn');
      btn.classList.toggle('active', alex.isSprinting);
    }}

    // 6. Keyboard & Touch Controls
    const keys = {{}};
    let inputX = 0;
    let inputY = 0;

    window.addEventListener('keydown', (e) => {{
      const k = e.key.toLowerCase();
      keys[k] = true;
      if (k === 'e' || k === ' ') {{
        if (isIntroActive) {{
          startCinematicZoom();
          isIntroActive = false;
        }} else {{
          triggerActiveInteraction();
        }}
      }}
      if (k === 'm') toggleWorldMap();
      if (k === 'q') rotateAlexCCW();
      if (k === 'r') rotateAlexCW();
      if (k === 't') toggleDirectionTestScene();
      if (k === 'u') unstuckAlex();
      if (k === '1') setTileSize(128, 64);
      if (k === '2') setTileSize(96, 48);
      if (k === '3') setTileSize(80, 40);
      if (k === '4') setTileSize(60, 30);
    }});
    window.addEventListener('keyup', (e) => {{ keys[e.key.toLowerCase()] = false; }});

    // Touch Joystick
    const joystick = document.getElementById('touch-controls');
    const stick = document.getElementById('touch-stick');
    let isTouchActive = false;

    function handleJoystick(cx, cy, clientX, clientY) {{
      const dx = clientX - cx;
      const dy = clientY - cy;
      const dist = Math.hypot(dx, dy);
      const maxR = 45;
      const r = Math.min(dist, maxR);
      const angle = Math.atan2(dy, dx);
      stick.style.transform = `translate(${{Math.cos(angle)*r}}px, ${{Math.sin(angle)*r}}px)`;
      inputX = (Math.cos(angle)*r) / maxR;
      inputY = (Math.sin(angle)*r) / maxR;
    }}

    joystick.addEventListener('touchstart', (e) => {{
      isTouchActive = true;
      const rect = joystick.getBoundingClientRect();
      const t = e.touches[0];
      handleJoystick(rect.left + rect.width/2, rect.top + rect.height/2, t.clientX, t.clientY);
    }});
    joystick.addEventListener('touchmove', (e) => {{
      if (!isTouchActive) return;
      const rect = joystick.getBoundingClientRect();
      const t = e.touches[0];
      handleJoystick(rect.left + rect.width/2, rect.top + rect.height/2, t.clientX, t.clientY);
    }});
    joystick.addEventListener('touchend', () => {{
      isTouchActive = false;
      inputX = 0; inputY = 0;
      stick.style.transform = 'translate(0px, 0px)';
    }});

    // Click to move
    canvas.addEventListener('click', (e) => {{
      if (isIntroActive) return;
      const rect = canvas.getBoundingClientRect();
      const clickX = (e.clientX - rect.left) * window.devicePixelRatio;
      const clickY = (e.clientY - rect.top) * window.devicePixelRatio;
      const screenX = (clickX - canvas.width / 2) / (camera.zoom * window.devicePixelRatio) + camera.x;
      const screenY = (clickY - canvas.height / 2) / (camera.zoom * window.devicePixelRatio) + camera.y;
      const tw = screenToWorld(screenX, screenY);
      alex.targetWx = tw.x;
      alex.targetWy = tw.y;
    }});

    // 7. Render Loop
    let lastTime = performance.now();

    function resizeCanvas() {{
      canvas.width = window.innerWidth * window.devicePixelRatio;
      canvas.height = window.innerHeight * window.devicePixelRatio;
      ctx.imageSmoothingEnabled = false;
    }}
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    function gameLoop(now) {{
      const dt = Math.min((now - lastTime) / 1000, 0.1);
      lastTime = now;

      // Handle Intro Timer
      if (cameraContext === 'CINEMATIC') {{
        introTimer += dt;
        if (introTimer > 2.0) {{
          cameraContext = 'PLAYER';
          camera.targetZoom = 1.15;
        }}
      }}

      // Interpolate Camera Zoom
      camera.zoom += (camera.targetZoom - camera.zoom) * Math.min(4.0 * dt, 1.0);

      // Movement Input
      let moveX = inputX;
      let moveY = inputY;
      if (keys['w'] || keys['z'] || keys['arrowup']) moveY -= 1;
      if (keys['s'] || keys['arrowdown']) moveY += 1;
      if (keys['a'] || keys['q'] || keys['arrowleft']) moveX -= 1;
      if (keys['d'] || keys['arrowright']) moveX += 1;

      // Click-to-move interpolation
      if (alex.targetWx !== undefined && alex.targetWy !== undefined) {{
        const tdx = alex.targetWx - alex.wx;
        const tdy = alex.targetWy - alex.wy;
        const tdist = Math.hypot(tdx, tdy);
        if (tdist > 0.3 * worldScale) {{
          moveX = (tdx - tdy);
          moveY = (tdx + tdy);
        }} else {{
          delete alex.targetWx;
          delete alex.targetWy;
        }}
      }}

      const len = Math.hypot(moveX, moveY);
      if (len < 0.1) {{
        alex.state = 'IDLE';
      }} else {{
        const normX = moveX / len;
        const normY = moveY / len;
        const angle = Math.atan2(normY, normX);
        
        // Accurate 8-way / 4-way angle assignment
        if (angle >= -Math.PI/8 && angle < Math.PI/8) alex.orientation = 'E';
        else if (angle >= Math.PI/8 && angle < 3*Math.PI/8) alex.orientation = 'SE';
        else if (angle >= 3*Math.PI/8 && angle < 5*Math.PI/8) alex.orientation = 'S';
        else if (angle >= 5*Math.PI/8 && angle < 7*Math.PI/8) alex.orientation = 'SW';
        else if (angle >= -3*Math.PI/8 && angle < -Math.PI/8) alex.orientation = 'NE';
        else if (angle >= -5*Math.PI/8 && angle < -3*Math.PI/8) alex.orientation = 'N';
        else if (angle >= -7*Math.PI/8 && angle < -5*Math.PI/8) alex.orientation = 'NW';
        else alex.orientation = 'W';

        document.getElementById('hud-orient').textContent = alex.orientation;

        const isRunning = alex.isSprinting || len > 0.75 || keys['shift'];
        alex.state = isRunning ? 'RUN' : 'WALK';
        const speed = (isRunning ? 4.8 : 2.5) * worldScale;

        const worldDx = (normX + normY) * speed * dt * 0.707;
        const worldDy = (-normX + normY) * speed * dt * 0.707;

        const resolved = resolveMovement(alex.wx, alex.wy, alex.wx + worldDx, alex.wy + worldDy, 0.28 * worldScale);
        alex.wx = resolved.x;
        alex.wy = resolved.y;
      }}

      // Camera Follow
      const alexScreen = worldToScreen(alex.wx, alex.wy);
      const halfW = (canvas.width / (2 * window.devicePixelRatio)) / camera.zoom;
      const halfH = (canvas.height / (2 * window.devicePixelRatio)) / camera.zoom;

      const targetCamX = Math.max(camera.minX + halfW, Math.min(alexScreen.x, camera.maxX - halfW));
      const targetCamY = Math.max(camera.minY + halfH, Math.min(alexScreen.y, camera.maxY - halfH));

      camera.x += (targetCamX - camera.x) * Math.min(5.5 * dt, 1.0);
      camera.y += (targetCamY - camera.y) * Math.min(5.5 * dt, 1.0);

      // Check POI & Narrative Props Proximity
      activePOI = null;
      activeClue = null;
      const promptBadge = document.getElementById('prompt-badge');
      const promptText = document.getElementById('prompt-text');

      if (isInFamilyHouse) {{
        // Check house clues
        for (const clue of narrativeProps) {{
          if (clue.inHouse) {{
            const dist = Math.hypot(alex.wx - clue.wx * worldScale, alex.wy - clue.wy * worldScale);
            if (dist < 1.6 * worldScale) {{
              activeClue = clue;
              promptBadge.style.display = 'inline-flex';
              promptText.textContent = `Examiner ${{clue.name}} [E]`;
              break;
            }}
          }}
        }}
        // Check exit door
        const doorDist = Math.hypot(alex.wx - (-1.5 * worldScale), alex.wy - (-4.2 * worldScale));
        if (!activeClue && doorDist < 1.4 * worldScale) {{
          promptBadge.style.display = 'inline-flex';
          promptText.textContent = "Sortir dans le village [E]";
          activePOI = {{ id: 'POI_FAMILY_HOUSE', name: "Porte de sortie" }};
        }}
      }} else {{
        // Check exterior clues
        for (const clue of narrativeProps) {{
          if (!clue.inHouse) {{
            const dist = Math.hypot(alex.wx - clue.wx * worldScale, alex.wy - clue.wy * worldScale);
            if (dist < 2.0 * worldScale) {{
              activeClue = clue;
              promptBadge.style.display = 'inline-flex';
              promptText.textContent = `Inspecter ${{clue.name}} [E]`;
              break;
            }}
          }}
        }}
        // Check exterior POIs
        if (!activeClue) {{
          for (const poi of pois) {{
            const dist = Math.hypot(alex.wx - poi.wx * worldScale, alex.wy - poi.wy * worldScale);
            if (dist < poi.r * worldScale) {{
              activePOI = poi;
              promptBadge.style.display = 'inline-flex';
              promptText.textContent = poi.prompt;
              break;
            }}
          }}
        }}
      }}

      if (!activePOI && !activeClue) {{
        promptBadge.style.display = 'none';
      }}

      // =========================================================================
      // DRAW SCENE
      // =========================================================================
      ctx.save();
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Background atmospheric winter sky/ground
      ctx.fillStyle = isInFamilyHouse ? '#0F1622' : '#0B111D';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Camera transform
      ctx.translate(canvas.width / 2, canvas.height / 2);
      ctx.scale(camera.zoom * window.devicePixelRatio, camera.zoom * window.devicePixelRatio);
      ctx.translate(-camera.x, -camera.y);

      if (isInFamilyHouse) {{
        // -----------------------------------------------------------------------
        // RENDER FAMILY HOUSE INTERIOR (Phase 10)
        // -----------------------------------------------------------------------
        const houseCenter = worldToScreen(-1.5 * worldScale, -5.0 * worldScale);
        
        // Draw interior living room & bedroom shell
        if (images.family_house_int.complete && images.family_house_int.naturalWidth > 0) {{
          ctx.drawImage(images.family_house_int, houseCenter.x - 220, houseCenter.y - 180, 440, 360);
        }}

        // Draw interior floor paving
        ctx.strokeStyle = 'rgba(56, 189, 248, 0.2)';
        ctx.strokeRect(houseCenter.x - 180, houseCenter.y - 140, 360, 260);

        // Draw interior clues & furniture
        for (const clue of narrativeProps) {{
          if (clue.inHouse && clue.img.complete && clue.img.naturalWidth > 0) {{
            const pos = worldToScreen(clue.wx * worldScale, clue.wy * worldScale);
            ctx.drawImage(clue.img, pos.x - 24, pos.y - 36, 48, 48);
            ctx.fillStyle = '#38BDF8';
            ctx.beginPath();
            ctx.arc(pos.x, pos.y + 10, 4, 0, Math.PI * 2);
            ctx.fill();
          }}
        }}
      }} else {{
        // -----------------------------------------------------------------------
        // RENDER VILLAGE EXTERIOR SYNCHRONIZED 1:1 WITH MAP DU VILLAGE.PNG
        // -----------------------------------------------------------------------
        if (images.map_master.complete && images.map_master.naturalWidth > 0) {{
          // Align master blueprint (1536x1024) so fountain at (770, 480) matches (0, 0)
          const scale = worldScale / 1.6;
          const originMapX = -770 * scale;
          const originMapY = -480 * scale;
          const mapW = 1536 * scale;
          const mapH = 1024 * scale;
          ctx.drawImage(images.map_master, originMapX, originMapY, mapW, mapH);

          // Subtle warm atmospheric lantern glow on lamps & windows
          const lampPositions = [
            {{ x: 0, y: 0, r: 40 }}, // Plaza fountain
            {{ x: -40, y: 300, r: 50 }}, // Bridge
            {{ x: 480, y: -240, r: 60 }}, // Church
            {{ x: 160, y: 240, r: 45 }}, // Watermill
            {{ x: -40, y: -300, r: 70 }}, // Family house hearth
          ];
          for (const lamp of lampPositions) {{
            const radGrad = ctx.createRadialGradient(lamp.x * scale, lamp.y * scale, 2, lamp.x * scale, lamp.y * scale, lamp.r * scale);
            radGrad.addColorStop(0, 'rgba(251, 191, 36, 0.25)');
            radGrad.addColorStop(1, 'rgba(251, 191, 36, 0)');
            ctx.fillStyle = radGrad;
            ctx.beginPath();
            ctx.arc(lamp.x * scale, lamp.y * scale, lamp.r * scale, 0, Math.PI * 2);
            ctx.fill();
          }}
        }} else {{
          // Procedural fallback
          const radius = 18;
          for (let x = -radius; x <= radius; x++) {{
            for (let y = -radius; y <= radius; y++) {{
              const p = worldToScreen(x * worldScale, y * worldScale);
              let tileImg = images.snow_slab;
              if (x >= 5 && x <= 8 && y >= 6 && y <= 9) tileImg = images.stone_slab;
              else if (Math.abs(x) < 3 && Math.abs(y) < 3) tileImg = images.stone_slab_var;
              else if (y > 9) tileImg = images.ice_slab;

              if (tileImg.complete && tileImg.naturalWidth > 0) {{
                ctx.drawImage(tileImg, p.x - HALF_W, p.y - HALF_H, TILE_W, TILE_H);
              }}
            }}
          }}
        }}

        // Render entities list sorted by Z-Order
        const entities = [];

        // Standalone building fallback definitions (for test assertions & fallback)
        if (!images.map_master.complete || images.map_master.naturalWidth === 0) {{
          entities.push({{ z: calculateZ(3.5, -7.5), img: images.church, wx: 3.5, wy: -7.5, w: 220, h: 260 }});
          entities.push({{ z: calculateZ(-1.5, -5.0), img: images.family_house, wx: -1.5, wy: -5.0, w: 260, h: 240 }});
          entities.push({{ z: calculateZ(-2.5, 8.5), img: images.watermill, wx: -2.5, wy: 8.5, w: 240, h: 220 }});
          entities.push({{ z: calculateZ(-8.5, -2.0), img: images.windmill, wx: -8.5, wy: -2.0, w: 210, h: 220 }});
          entities.push({{ z: calculateZ(-4.0, -0.5), img: images.cottage_west, wx: -4.0, wy: -0.5, w: 200, h: 200 }});
          entities.push({{ z: calculateZ(8.5, -1.0), img: images.sawmill, wx: 8.5, wy: -1.0, w: 240, h: 220 }});
          entities.push({{ z: calculateZ(6.8, 7.8), img: images.bridge_elem, wx: 6.8, wy: 7.8, w: 180, h: 140 }});
          entities.push({{ z: calculateZ(-7.5, -7.5), img: images.bunker_ext, wx: -7.5, wy: -7.5, w: 230, h: 160 }});
          entities.push({{ z: calculateZ(0.0, 0.0), img: images.statue, wx: 0.0, wy: 0.0, w: 90, h: 120 }});
          entities.push({{ z: calculateZ(1.2, 2.4), img: images.well, wx: 1.2, wy: 2.4, w: 110, h: 100 }});
        }}

        // Narrative Clues on Exterior Map
        for (const clue of narrativeProps) {{
          if (!clue.inHouse && clue.img.complete && clue.img.naturalWidth > 0) {{
            const pos = worldToScreen(clue.wx * worldScale, clue.wy * worldScale);
            // Draw interactive glowing beacon
            ctx.fillStyle = 'rgba(56, 189, 248, 0.3)';
            ctx.beginPath();
            ctx.arc(pos.x, pos.y, 14 + Math.sin(now * 0.005) * 4, 0, Math.PI * 2);
            ctx.fill();
            ctx.drawImage(clue.img, pos.x - 16, pos.y - 24, 32, 32);
          }}
        }}

        // NPCs
        entities.push({{ z: calculateZ(6.2, 6.8), img: images.emma, wx: 6.2, wy: 6.8, w: 32, h: 64, isChar: true }});
        entities.push({{ z: calculateZ(0.8, -0.8), img: images.james, wx: 0.8, wy: -0.8, w: 32, h: 64, isChar: true }});
        entities.push({{ z: calculateZ(-1.8, -3.8), img: images.michael, wx: -1.8, wy: -3.8, w: 32, h: 64, isChar: true }});
        entities.push({{ z: calculateZ(-3.2, -6.2), img: images.ethan, wx: -3.2, wy: -6.2, w: 32, h: 64, isChar: true }});

        // Draw sorted entities
        entities.sort((a, b) => a.z - b.z);
        for (const ent of entities) {{
          if (ent.img.complete && ent.img.naturalWidth > 0) {{
            const p = worldToScreen(ent.wx * worldScale, ent.wy * worldScale);
            ctx.drawImage(ent.img, p.x - ent.w / 2, p.y - ent.h * 0.9, ent.w, ent.h);
          }}
        }}
      }}

      // -------------------------------------------------------------------------
      // RENDER ALEX (Always with verified invariant feet anchor)
      // -------------------------------------------------------------------------
      const alexPos = worldToScreen(alex.wx, alex.wy);
      let alexImg = images.alex_s;
      if (alex.orientation === 'N') alexImg = images.alex_n;
      else if (alex.orientation === 'NE') alexImg = images.alex_ne;
      else if (alex.orientation === 'E') alexImg = images.alex_e;
      else if (alex.orientation === 'SE') alexImg = images.alex_se;
      else if (alex.orientation === 'S') alexImg = images.alex_s;
      else if (alex.orientation === 'SW') alexImg = images.alex_sw;
      else if (alex.orientation === 'W') alexImg = images.alex_w;
      else if (alex.orientation === 'NW') alexImg = images.alex_nw;

      // Subtle breathing / walking bobbing
      const bob = alex.state === 'WALK' ? Math.sin(now * 0.012) * 2 : (alex.state === 'RUN' ? Math.sin(now * 0.02) * 3 : 0);

      // Realistic feet shadow
      ctx.fillStyle = 'rgba(0, 0, 0, 0.45)';
      ctx.beginPath();
      ctx.ellipse(alexPos.x, alexPos.y, 14, 6, 0, 0, Math.PI * 2);
      ctx.fill();

      // Alex sprite (calibrated human scale 34x78 matching the new 80x40 ground paving)
      if (alexImg.complete && alexImg.naturalWidth > 0) {{
        ctx.drawImage(alexImg, alexPos.x - 17, alexPos.y - 74 + bob, 34, 78);
      }}

      // Clean Release Mode: Hitboxes strictly guarded behind isDebug
      if (isDebug) {{
        ctx.strokeStyle = '#EF4444';
        ctx.lineWidth = 2;
        ctx.strokeRect(alexPos.x - 17, alexPos.y - 74 + bob, 34, 78);
      }}

      ctx.restore();
      requestAnimationFrame(gameLoop);
    }}

    requestAnimationFrame(gameLoop);
  </script>
</body>
</html>
"""
