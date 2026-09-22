import os
import json
import base64

ROOT_DIR = "/root/the_echo_of_shadows"
ASSETS_DIR = os.path.join(ROOT_DIR, "assets", "images")
OUT_FILE = os.path.join(ROOT_DIR, "web_preview", "index.html")

def to_base64(rel_path, mirror=False):
    full_path = os.path.join(ASSETS_DIR, rel_path)
    if os.path.exists(full_path):
        if mirror:
            from PIL import Image
            import io
            im = Image.open(full_path).convert("RGBA")
            im_flipped = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            buf = io.BytesIO()
            im_flipped.save(buf, format="PNG")
            return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")
        else:
            with open(full_path, "rb") as f:
                return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    return ""

def build():
    print("Embedding Reconstructed Canonical Village assets from Map village .png...")
    
    # 1. Alex 4-Way Directional Sprites (Phase 3.3 Verified Canonical Set)
    alex_idle_se = to_base64("characters/alex/idle/Alex-—-Animation-Idle03.png")
    alex_idle_sw = to_base64("characters/alex/idle/Alex-—-Animation-Idle03.png", mirror=True)
    alex_idle_ne = to_base64("characters/alex/idle/Alex-—-Animation-Idle22.png")
    alex_idle_nw = to_base64("characters/alex/idle/Alex-—-Animation-Idle22.png", mirror=True)
    
    alex_walk_se = to_base64("characters/alex/walk/Alex-—-Marche36.png")
    alex_walk_sw = to_base64("characters/alex/walk/Alex-—-Marche36.png", mirror=True)
    alex_walk_ne = to_base64("characters/alex/walk/Alex-—-Marche18.png")
    alex_walk_nw = to_base64("characters/alex/walk/Alex-—-Marche10.png")
    
    alex_run_se = to_base64("characters/alex/run/Alex-—-Course11.png")
    alex_run_sw = to_base64("characters/alex/run/Alex-—-Course11.png", mirror=True)
    alex_run_ne = to_base64("characters/alex/run/Alex-—-Course10.png")
    alex_run_nw = to_base64("characters/alex/run/Alex-—-Course10.png", mirror=True)

    alex_interact_se = to_base64("characters/alex/interaction/Alex-—-Interaction01.png")
    alex_interact_sw = to_base64("characters/alex/interaction/Alex-—-Interaction01.png", mirror=True)
    alex_interact_ne = to_base64("characters/alex/interaction/Alex-—-Interaction28.png")
    alex_interact_nw = to_base64("characters/alex/interaction/Alex-—-Interaction28.png", mirror=True)
    
    # 2. NPCs
    npc_emma = to_base64("characters/emma/Emma-—-Personnage-principal01.png")
    npc_ethan = to_base64("characters/ethan/Ethan-—-Frère-d’Alex01.png")
    npc_james = to_base64("characters/james/Officer-James01.png")
    npc_michael = to_base64("characters/michael/Old-Michael01.png")

    # 3. Canonical Village Buildings from Map village .png
    family_house = to_base64("environments/family_house/exterior/Maison-familiale-extérieure01.png")
    church = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet05.png")
    watermill = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet01.png")
    windmill = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet02.png")
    cottage_west = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet03.png")
    cottage_south = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet04.png")
    cottage_far_west = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet06.png")
    riverside_cottage = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet07.png")
    east_workshop = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet08.png")
    sawmill = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet09.png")
    mine_archway = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet10.png")

    # 4. Props & Decor
    market_stall_01 = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet11.png")
    market_stall_02 = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet12.png")
    plaza_shrine = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet14.png")
    iron_gate = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet15.png")
    sawmill_crane = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet18.png")
    dock_crane = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet19.png")
    lamp_post = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet20.png")
    stacked_logs = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet24.png")
    pine_tree = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet37.png")
    dead_tree = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet34.png")
    well = to_base64("environments/village/decor/Village-abandonné-—-Route-&-décor-extérieur01.png")
    statue = to_base64("environments/village/decor/Village-abandonné-—-Route-&-décor-extérieur07.png")
    boat = to_base64("environments/village/decor/Village-abandonné-—-Route-&-décor-extérieur18.png")
    cliff = to_base64("environments/village/decor/Village-abandonné-—-Route-&-décor-extérieur52.png")

    # 5. Terrain Tiles
    stone_slab = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet25.png")
    stone_slab_var = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet26.png")
    snow_slab = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet31.png")
    ice_slab = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet32.png")

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>L'Écho des Ombres — Le Village Abandonné (Reconstruction Map)</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; user-select: none; -webkit-tap-highlight-color: transparent; }}
    html, body {{ width: 100%; height: 100%; overflow: hidden; background: #0E1626; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #E2E8F0; }}
    #canvas-container {{ width: 100%; height: 100%; position: relative; }}
    canvas {{ display: block; width: 100%; height: 100%; }}
    
    /* Release Mode Cinematic HUD */
    #release-hud {{
      position: absolute; top: 16px; left: 16px;
      display: flex; flex-direction: column; gap: 8px; pointer-events: none;
      transition: opacity 0.3s ease;
    }}
    .location-badge {{
      display: inline-flex; align-items: center; gap: 8px;
      background: rgba(15, 23, 42, 0.90);
      border: 1px solid rgba(148, 163, 184, 0.35);
      border-radius: 20px;
      padding: 8px 16px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.6);
    }}
    .status-dot {{ width: 8px; height: 8px; border-radius: 50%; background: #38BDF8; box-shadow: 0 0 8px #38BDF8; }}
    .location-name {{ font-size: 13px; font-weight: 600; color: #F8FAFC; letter-spacing: 0.6px; }}
    .interaction-prompt {{
      display: inline-flex; align-items: center; gap: 6px;
      background: rgba(30, 41, 59, 0.92);
      border: 1px solid rgba(56, 189, 248, 0.5);
      border-radius: 8px;
      padding: 6px 12px; font-size: 12px; color: #E2E8F0;
      animation: pulse 2s infinite ease-in-out;
    }}
    @keyframes pulse {{
      0%, 100% {{ box-shadow: 0 0 4px rgba(56, 189, 248, 0.3); }}
      50% {{ box-shadow: 0 0 12px rgba(56, 189, 248, 0.7); }}
    }}

    /* Debug HUD */
    #debug-panel {{
      position: absolute; top: 80px; left: 16px;
      background: rgba(15, 23, 42, 0.88);
      border: 1px solid #EAB308;
      border-radius: 8px;
      padding: 10px 14px; font-size: 11px; font-family: monospace;
      color: #94A3B8; display: none; line-height: 1.5; pointer-events: none;
    }}
    #debug-tools {{
      position: absolute; top: 12px; right: 54px;
      display: none; gap: 6px; align-items: center;
    }}
    
    /* Top Right Debug Toggle */
    #debug-toggle {{
      position: absolute; top: 16px; right: 16px;
      width: 36px; height: 36px; border-radius: 50%;
      background: rgba(15, 23, 42, 0.65);
      border: 1px solid rgba(148, 163, 184, 0.3);
      color: #94A3B8; font-size: 16px; display: flex;
      align-items: center; justify-content: center;
      cursor: pointer; transition: all 0.2s ease;
    }}
    #debug-toggle.active {{ background: #EAB308; color: #000; border-color: #CA8A04; }}

    .btn-dev {{
      background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(148, 163, 184, 0.4);
      color: #F8FAFC; border-radius: 6px; padding: 6px 10px; font-size: 11px;
      font-weight: 600; cursor: pointer; transition: background 0.15s;
    }}
    .btn-dev:hover {{ background: rgba(51, 65, 85, 0.9); }}

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

    /* Touch Controls */
    #touch-controls {{
      position: absolute; bottom: 20px; left: 20px;
      width: 120px; height: 120px; border-radius: 50%;
      background: rgba(15, 23, 42, 0.4);
      border: 2px solid rgba(148, 163, 184, 0.3);
      touch-action: none;
    }}
    #touch-stick {{
      position: absolute; top: 35px; left: 35px;
      width: 50px; height: 50px; border-radius: 50%;
      background: radial-gradient(circle, #64748B, #334155);
      border: 1.5px solid #E2E8F0;
      box-shadow: 0 4px 12px rgba(0,0,0,0.5);
      pointer-events: none;
    }}

    /* Action & Rotation Controls */
    #action-controls {{
      position: absolute; bottom: 20px; right: 20px;
      display: flex; flex-direction: column; align-items: flex-end; gap: 8px;
    }}
    .rotation-row {{
      display: flex; align-items: center; gap: 6px;
    }}
    .btn-rotate {{
      width: 38px; height: 38px; border-radius: 50%;
      background: rgba(30, 41, 59, 0.75); border: 1px solid rgba(148, 163, 184, 0.35);
      color: #F8FAFC; font-size: 15px; display: flex; align-items: center; justify-content: center;
      cursor: pointer; transition: transform 0.1s;
    }}
    .btn-rotate:active {{ transform: scale(0.92); background: rgba(56, 189, 248, 0.4); }}
    .orient-badge {{
      padding: 4px 8px; border-radius: 12px; background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(56, 189, 248, 0.4); font-size: 11px; font-weight: 700; color: #38BDF8;
    }}
    #sprint-btn {{
      padding: 10px 16px; border-radius: 20px;
      background: rgba(30, 41, 59, 0.65); border: 1px solid rgba(148, 163, 184, 0.3);
      color: #F8FAFC; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;
      cursor: pointer; display: flex; align-items: center; gap: 6px;
    }}
    #sprint-btn.active {{ background: rgba(220, 38, 38, 0.85); border-color: #EF4444; }}

    #notification {{
      position: absolute; bottom: 100px; left: 50%; transform: translateX(-50%);
      background: rgba(15, 23, 42, 0.95); border: 1px solid #10B981;
      color: #10B981; padding: 8px 18px; border-radius: 20px;
      font-size: 12px; font-weight: 600; display: none;
      box-shadow: 0 4px 16px rgba(0,0,0,0.6); pointer-events: none;
    }}
  </style>
</head>
<body>
  <div id="canvas-container">
    <canvas id="gameCanvas"></canvas>
    
    <!-- Release HUD -->
    <div id="release-hud">
      <div class="location-badge">
        <div class="status-dot"></div>
        <span class="location-name" id="loc-title">L'ÉCHO DES OMBRES — LE VILLAGE</span>
      </div>
      <div class="interaction-prompt" id="prompt-badge" style="display: none;">
        <span>🔍</span>
        <span id="prompt-text">Inspect</span>
      </div>
    </div>

    <!-- Tile Size Switcher Toolbar -->
    <div id="tile-size-selector" style="position: absolute; top: 16px; left: 50%; transform: translateX(-50%); display: flex; align-items: center; gap: 6px; background: rgba(15, 23, 42, 0.92); border: 1px solid rgba(148, 163, 184, 0.35); border-radius: 24px; padding: 5px 12px; box-shadow: 0 4px 16px rgba(0,0,0,0.6); z-index: 10;">
      <span style="font-size: 11px; font-weight: 700; color: #94A3B8; margin-right: 4px; display: flex; align-items: center; gap: 4px;"><span>📐</span> TILES :</span>
      <button class="tile-btn" id="btn-tile-128" onclick="setTileSize(128, 64)" title="Grandes dalles (128x64)">128x64</button>
      <button class="tile-btn" id="btn-tile-96" onclick="setTileSize(96, 48)" title="Premier test (+78% pavés)">96x48</button>
      <button class="tile-btn active" id="btn-tile-80" onclick="setTileSize(80, 40)" title="Choix validé (80x40, +156% pavés, ratio 2:1)">80x40 (Validé)</button>
      <button class="tile-btn" id="btn-tile-60" onclick="setTileSize(60, 30)" title="Dalles fines (60x30)">60x30</button>
    </div>

    <!-- Debug HUD -->
    <div id="debug-panel">
      <div style="color: #EAB308; font-weight: bold; margin-bottom: 4px;">=== DIAGNOSTICS & SYSTEM ===</div>
      <div id="dbg-fps">FPS: 60</div>
      <div id="dbg-pos">Alex: [6.50, 6.50]</div>
      <div id="dbg-state">State: IDLE (NW)</div>
      <div id="dbg-poi">POI: NONE</div>
      <div id="dbg-cam">Cam: [0, 0] | Zoom: 1.15</div>
      <div id="dbg-bounds">Bounds: Blueprint Map Reconstruction</div>
    </div>

    <!-- Debug Tools -->
    <div id="debug-tools">
      <button class="btn-dev" onclick="zoomCam(0.15)">🔍 +</button>
      <button class="btn-dev" onclick="zoomCam(-0.15)">🔍 -</button>
      <button class="btn-dev" style="background: #2563EB;" onclick="saveGame()">💾 SAVE</button>
      <button class="btn-dev" style="background: #10B981;" onclick="loadGame()">📂 LOAD</button>
    </div>

    <!-- Direction Test Scene Button -->
    <div id="test-scene-btn" onclick="toggleDirectionTestScene()" title="Alex Direction & Identity Test Scene (360°)" style="position: absolute; top: 16px; right: 60px; height: 36px; padding: 0 14px; border-radius: 18px; background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(56, 189, 248, 0.4); color: #38BDF8; font-size: 12px; font-weight: 700; display: flex; align-items: center; gap: 6px; cursor: pointer; transition: all 0.2s ease; box-shadow: 0 4px 12px rgba(0,0,0,0.5);">
      <span>🧭</span>
      <span>Alex 360° Test</span>
    </div>

    <!-- Top Right Debug Toggle -->
    <div id="debug-toggle" onclick="toggleDebug()" title="Toggle Debug Overlay">⚙</div>

    <!-- AlexDirectionTestScene Modal Overlay -->
    <div id="direction-test-modal" style="display: none; position: absolute; inset: 0; background: rgba(10, 14, 23, 0.95); z-index: 1000; align-items: center; justify-content: center; backdrop-filter: blur(10px);">
      <div style="background: #18202F; border: 1px solid rgba(56, 189, 248, 0.4); border-radius: 16px; padding: 24px; max-width: 720px; width: 94%; box-shadow: 0 20px 50px rgba(0,0,0,0.85); display: flex; flex-direction: column; gap: 16px;">
        
        <!-- Modal Header -->
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(148, 163, 184, 0.2); padding-bottom: 12px;">
          <div>
            <h2 style="font-size: 16px; font-weight: 700; color: #F8FAFC; display: flex; align-items: center; gap: 8px;">
              <span>🧭</span> AlexDirectionTestScene — Audit 360°
            </h2>
            <p style="font-size: 11px; color: #94A3B8; margin-top: 2px;">
              Vérification stricte de l'identité visuelle d'Alex dans les 4 orientations (SE, SW, NE, NW)
            </p>
          </div>
          <button onclick="toggleDirectionTestScene()" style="background: transparent; border: none; color: #94A3B8; font-size: 20px; cursor: pointer; padding: 4px 8px;">✕</button>
        </div>

        <!-- State Selector Tabs -->
        <div style="display: flex; gap: 8px; justify-content: center;">
          <button class="test-state-btn active" id="ts-idle" onclick="setTestSceneState('IDLE')">IDLE</button>
          <button class="test-state-btn" id="ts-walk" onclick="setTestSceneState('WALK')">WALK</button>
          <button class="test-state-btn" id="ts-run" onclick="setTestSceneState('RUN')">RUN</button>
          <button class="test-state-btn" id="ts-interact" onclick="setTestSceneState('INTERACTION')">INTERACTION</button>
        </div>

        <!-- Compass Display Area -->
        <div style="position: relative; width: 100%; height: 320px; background: #0F172A; border-radius: 12px; border: 1px solid rgba(148, 163, 184, 0.15); display: flex; align-items: center; justify-content: center;">
          
          <!-- Cross Lines -->
          <div style="position: absolute; width: 240px; height: 1px; background: rgba(56, 189, 248, 0.25);"></div>
          <div style="position: absolute; height: 240px; width: 1px; background: rgba(56, 189, 248, 0.25);"></div>

          <!-- Top: NW -->
          <div style="position: absolute; top: 12px; left: 50%; transform: translateX(-50%); display: flex; flex-direction: column; align-items: center;">
            <div style="font-size: 10px; font-weight: 700; color: #C084FC; margin-bottom: 2px;">NW (Back-Left)</div>
            <div style="position: relative; width: 42px; height: 84px; display: flex; align-items: flex-end; justify-content: center;">
              <div style="position: absolute; bottom: 0; width: 26px; height: 6px; border-radius: 50%; background: rgba(0,0,0,0.5);"></div>
              <img id="test-img-nw" src="" style="width: 38px; height: 76px; object-fit: contain; z-index: 1;">
            </div>
            <div style="font-size: 9px; color: #A855F7; margin-top: 2px;">FALLBACK (88%)</div>
          </div>

          <!-- Bottom: SE -->
          <div style="position: absolute; bottom: 12px; left: 50%; transform: translateX(-50%); display: flex; flex-direction: column; align-items: center;">
            <div style="position: relative; width: 42px; height: 84px; display: flex; align-items: flex-end; justify-content: center;">
              <div style="position: absolute; bottom: 0; width: 26px; height: 6px; border-radius: 50%; background: rgba(0,0,0,0.5);"></div>
              <img id="test-img-se" src="" style="width: 38px; height: 76px; object-fit: contain; z-index: 1;">
            </div>
            <div style="font-size: 10px; font-weight: 700; color: #F59E0B; margin-top: 2px;">SE (Front-Right)</div>
            <div style="font-size: 9px; color: #10B981;">CANONICAL (100%)</div>
          </div>

          <!-- Left: SW -->
          <div style="position: absolute; left: 24px; top: 50%; transform: translateY(-50%); display: flex; flex-direction: column; align-items: center;">
            <div style="font-size: 10px; font-weight: 700; color: #38BDF8; margin-bottom: 2px;">SW (Front-Left)</div>
            <div style="position: relative; width: 42px; height: 84px; display: flex; align-items: flex-end; justify-content: center;">
              <div style="position: absolute; bottom: 0; width: 26px; height: 6px; border-radius: 50%; background: rgba(0,0,0,0.5);"></div>
              <img id="test-img-sw" src="" style="width: 38px; height: 76px; object-fit: contain; z-index: 1;">
            </div>
            <div style="font-size: 9px; color: #38BDF8; margin-top: 2px;">FALLBACK (100%)</div>
          </div>

          <!-- Right: NE -->
          <div style="position: absolute; right: 24px; top: 50%; transform: translateY(-50%); display: flex; flex-direction: column; align-items: center;">
            <div style="font-size: 10px; font-weight: 700; color: #10B981; margin-bottom: 2px;">NE (Back-Right)</div>
            <div style="position: relative; width: 42px; height: 84px; display: flex; align-items: flex-end; justify-content: center;">
              <div style="position: absolute; bottom: 0; width: 26px; height: 6px; border-radius: 50%; background: rgba(0,0,0,0.5);"></div>
              <img id="test-img-ne" src="" style="width: 38px; height: 76px; object-fit: contain; z-index: 1;">
            </div>
            <div style="font-size: 9px; color: #10B981; margin-top: 2px;">GENUINE (88%)</div>
          </div>

          <!-- Center: Rotating Alex -->
          <div style="display: flex; flex-direction: column; align-items: center; z-index: 2;">
            <div style="font-size: 10px; font-weight: 700; color: #F59E0B; margin-bottom: 4px;" id="center-orient-label">SE (Rotation Active)</div>
            <div style="position: relative; width: 56px; height: 100px; display: flex; align-items: flex-end; justify-content: center; border-radius: 50%; box-shadow: 0 0 16px rgba(245, 158, 11, 0.35);">
              <div style="position: absolute; bottom: 2px; width: 34px; height: 8px; border-radius: 50%; background: rgba(0,0,0,0.65);"></div>
              <img id="test-img-center" src="" style="width: 46px; height: 92px; object-fit: contain; z-index: 3;">
            </div>
          </div>

        </div>

        <!-- Test Controls Footer -->
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div style="display: flex; gap: 8px; align-items: center;">
            <button class="btn-dev" onclick="stepTestRotationCCW()">↺ Tourner Q</button>
            <button class="btn-dev" id="btn-toggle-autorotate" style="background: #10B981;" onclick="toggleTestAutoRotate()">Auto-Rotation: ACTIF</button>
            <button class="btn-dev" onclick="stepTestRotationCW()">↻ Tourner E</button>
          </div>
          <div style="font-size: 11px; color: #10B981; font-weight: 600;">
            ✓ Même personnage garanti à 100% dans toutes les poses
          </div>
        </div>

      </div>
    </div>

    <!-- Action & Rotation Controls -->
    <div id="action-controls">
      <div class="rotation-row">
        <button class="btn-rotate" onclick="rotateAlexCCW()" title="Tourner à gauche (R / ↺)">↺</button>
        <span class="orient-badge" id="hud-orient">NW</span>
        <button class="btn-rotate" onclick="rotateAlexCW()" title="Tourner à droite (E / ↻)">↻</button>
      </div>
      <button id="unstuck-btn" onclick="unstuckAlex()" style="padding: 8px 14px; border-radius: 18px; background: rgba(220, 38, 38, 0.85); border: 1px solid #EF4444; color: #FFF; font-size: 11px; font-weight: 700; cursor: pointer; display: flex; align-items: center; gap: 6px; box-shadow: 0 4px 12px rgba(220, 38, 38, 0.4);" title="Débloquer Alex immédiatement">
        <span>🔓</span>
        <span>DÉBLOQUER ALEX</span>
      </button>
      <button id="sprint-btn" onclick="toggleSprint()">
        <span>⚡</span>
        <span id="sprint-text">SPRINT</span>
      </button>
    </div>

    <!-- On-screen D-Pad Controls for instant touch & mouse movement -->
    <div id="dpad-controls" style="position: absolute; bottom: 155px; left: 24px; display: grid; grid-template-columns: repeat(3, 40px); grid-template-rows: repeat(3, 40px); gap: 4px; z-index: 25;">
      <div></div>
      <button class="dpad-btn" id="dpad-up" onmousedown="setDpad(0, -1)" onmouseup="clearDpad()" ontouchstart="setDpad(0, -1)" ontouchend="clearDpad()" style="background: rgba(30, 41, 59, 0.85); border: 1px solid rgba(148, 163, 184, 0.4); border-radius: 8px; color: #FFF; font-size: 16px; cursor: pointer; display: flex; align-items: center; justify-content: center;" title="Haut (Z / W / ↑)">▲</button>
      <div></div>
      <button class="dpad-btn" id="dpad-left" onmousedown="setDpad(-1, 0)" onmouseup="clearDpad()" ontouchstart="setDpad(-1, 0)" ontouchend="clearDpad()" style="background: rgba(30, 41, 59, 0.85); border: 1px solid rgba(148, 163, 184, 0.4); border-radius: 8px; color: #FFF; font-size: 16px; cursor: pointer; display: flex; align-items: center; justify-content: center;" title="Gauche (Q / A / ←)">◀</button>
      <button class="dpad-btn" id="dpad-center" onclick="unstuckAlex()" style="background: rgba(15, 23, 42, 0.95); border: 1px solid #38BDF8; border-radius: 8px; color: #38BDF8; font-size: 12px; cursor: pointer; display: flex; align-items: center; justify-content: center;" title="Débloquer / Recentrer Alex sur le pont">🔓</button>
      <button class="dpad-btn" id="dpad-right" onmousedown="setDpad(1, 0)" onmouseup="clearDpad()" ontouchstart="setDpad(1, 0)" ontouchend="clearDpad()" style="background: rgba(30, 41, 59, 0.85); border: 1px solid rgba(148, 163, 184, 0.4); border-radius: 8px; color: #FFF; font-size: 16px; cursor: pointer; display: flex; align-items: center; justify-content: center;" title="Droite (D / →)">▶</button>
      <div></div>
      <button class="dpad-btn" id="dpad-down" onmousedown="setDpad(0, 1)" onmouseup="clearDpad()" ontouchstart="setDpad(0, 1)" ontouchend="clearDpad()" style="background: rgba(30, 41, 59, 0.85); border: 1px solid rgba(148, 163, 184, 0.4); border-radius: 8px; color: #FFF; font-size: 16px; cursor: pointer; display: flex; align-items: center; justify-content: center;" title="Bas (S / ↓)">▼</button>
      <div></div>
    </div>

    <!-- Touch / Mouse Virtual Joystick -->
    <div id="touch-controls">
      <div id="touch-stick"></div>
    </div>

    <!-- Notification Toast -->
    <div id="notification"></div>
  </div>

  <script>
    // 1. Isometric Engine Constants & Dynamic Dimetric Tile Sizing (Phase 3.3)
    let TILE_W = 80;
    let TILE_H = 40;
    let HALF_W = 40;
    let HALF_H = 20;
    let worldScale = 128.0 / 80.0;

    function setTileSize(w, h) {{
      if (w / h !== 2) return;
      const oldScale = worldScale;
      TILE_W = w;
      TILE_H = h;
      HALF_W = w / 2;
      HALF_H = h / 2;
      worldScale = 128.0 / w;

      alex.wx = alex.wx * (worldScale / oldScale);
      alex.wy = alex.wy * (worldScale / oldScale);

      document.querySelectorAll('.tile-btn').forEach(btn => btn.classList.remove('active'));
      const activeBtn = document.getElementById('btn-tile-' + w);
      if (activeBtn) activeBtn.classList.add('active');

      const mult = ((128 * 64) / (w * h)).toFixed(2);
      const prop = ((28 / w) * 100).toFixed(1);
      showToast(`Dalles: ${{w}}x${{h}} px (2:1) | Densité: ${{mult}}x | Alex: ${{prop}}% de dalle`);
    }}

    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');

    // 2. Asset Image Cache
    const images = {{
      idleSE: new Image(),
      idleSW: new Image(),
      idleNE: new Image(),
      idleNW: new Image(),
      walkSE: new Image(),
      walkSW: new Image(),
      walkNE: new Image(),
      walkNW: new Image(),
      runSE: new Image(),
      runSW: new Image(),
      runNE: new Image(),
      runNW: new Image(),
      interactSE: new Image(),
      interactSW: new Image(),
      interactNE: new Image(),
      interactNW: new Image(),
      emma: new Image(),
      ethan: new Image(),
      james: new Image(),
      michael: new Image(),
      familyHouse: new Image(),
      church: new Image(),
      watermill: new Image(),
      windmill: new Image(),
      cottageWest: new Image(),
      cottageSouth: new Image(),
      cottageFarWest: new Image(),
      riversideCottage: new Image(),
      eastWorkshop: new Image(),
      sawmill: new Image(),
      mineArchway: new Image(),
      marketStall01: new Image(),
      marketStall02: new Image(),
      plazaShrine: new Image(),
      ironGate: new Image(),
      sawmillCrane: new Image(),
      dockCrane: new Image(),
      lampPost: new Image(),
      stackedLogs: new Image(),
      pineTree: new Image(),
      deadTree: new Image(),
      well: new Image(),
      statue: new Image(),
      boat: new Image(),
      cliff: new Image(),
      slab: new Image(),
      slabVar: new Image(),
      snowSlab: new Image(),
      iceSlab: new Image()
    }};

    images.idleSE.src = "{alex_idle_se}";
    images.idleSW.src = "{alex_idle_sw}";
    images.idleNE.src = "{alex_idle_ne}";
    images.idleNW.src = "{alex_idle_nw}";
    images.walkSE.src = "{alex_walk_se}";
    images.walkSW.src = "{alex_walk_sw}";
    images.walkNE.src = "{alex_walk_ne}";
    images.walkNW.src = "{alex_walk_nw}";
    images.runSE.src = "{alex_run_se}";
    images.runSW.src = "{alex_run_sw}";
    images.runNE.src = "{alex_run_ne}";
    images.runNW.src = "{alex_run_nw}";
    images.interactSE.src = "{alex_interact_se}";
    images.interactSW.src = "{alex_interact_sw}";
    images.interactNE.src = "{alex_interact_ne}";
    images.interactNW.src = "{alex_interact_nw}";

    images.emma.src = "{npc_emma}";
    images.ethan.src = "{npc_ethan}";
    images.james.src = "{npc_james}";
    images.michael.src = "{npc_michael}";

    images.familyHouse.src = "{family_house}";
    images.church.src = "{church}";
    images.watermill.src = "{watermill}";
    images.windmill.src = "{windmill}";
    images.cottageWest.src = "{cottage_west}";
    images.cottageSouth.src = "{cottage_south}";
    images.cottageFarWest.src = "{cottage_far_west}";
    images.riversideCottage.src = "{riverside_cottage}";
    images.eastWorkshop.src = "{east_workshop}";
    images.sawmill.src = "{sawmill}";
    images.mineArchway.src = "{mine_archway}";

    images.marketStall01.src = "{market_stall_01}";
    images.marketStall02.src = "{market_stall_02}";
    images.plazaShrine.src = "{plaza_shrine}";
    images.ironGate.src = "{iron_gate}";
    images.sawmillCrane.src = "{sawmill_crane}";
    images.dockCrane.src = "{dock_crane}";
    images.lampPost.src = "{lamp_post}";
    images.stackedLogs.src = "{stacked_logs}";
    images.pineTree.src = "{pine_tree}";
    images.deadTree.src = "{dead_tree}";
    images.well.src = "{well}";
    images.statue.src = "{statue}";
    images.boat.src = "{boat}";
    images.cliff.src = "{cliff}";

    images.slab.src = "{stone_slab}";
    images.slabVar.src = "{stone_slab_var}";
    images.snowSlab.src = "{snow_slab}";
    images.iceSlab.src = "{ice_slab}";

    // 3. Coordinate Projection
    function worldToScreen(wx, wy) {{
      return {{
        x: (wx - wy) * HALF_W,
        y: (wx + wy) * HALF_H
      }};
    }}

    function calculateZ(wx, wy, base = 40000) {{
      return base + Math.round((wx + wy) * 100);
    }}

    // 4. Player State — Initial Spawn on Entrance Bridge facing NW into village (Alex.position.x = 7.0; Alex.position.y = 8.0;)
    const alex = {{
      wx: 7.0 * worldScale,
      wy: 8.0 * worldScale,
      w: 28,
      h: 56,
      radius: 0.28,
      orientation: 'NW',
      state: 'IDLE',
      isSprinting: false,
      frameTimer: 0
    }};

    // Direct global Alex.position accessor
    window.Alex = {{
      position: {{
        get x() {{ return alex.wx / worldScale; }},
        set x(val) {{ alex.wx = val * worldScale; }},
        get y() {{ return alex.wy / worldScale; }},
        set y(val) {{ alex.wy = val * worldScale; }}
      }}
    }};

    const canonicalCycle = ['SE', 'SW', 'NW', 'NE'];

    function rotateAlexCW() {{
      const idx = canonicalCycle.indexOf(alex.orientation);
      alex.orientation = canonicalCycle[(idx + 1) % canonicalCycle.length];
      document.getElementById('hud-orient').textContent = alex.orientation;
    }}

    function rotateAlexCCW() {{
      const idx = canonicalCycle.indexOf(alex.orientation);
      alex.orientation = canonicalCycle[(idx - 1 + canonicalCycle.length) % canonicalCycle.length];
      document.getElementById('hud-orient').textContent = alex.orientation;
    }}

    // 5. Canonical Points of Interest (POIs) reconstructed from Map village .png
    const pois = [
      {{ id: 'POI_BRIDGE', name: 'Pont de bois (Entrée)', baseWx: 6.5, baseWy: 6.5, baseR: 2.0, prompt: '[E] Traverser le pont de la rivière gelée' }},
      {{ id: 'POI_PLAZA_MONUMENT', name: 'Place centrale (Monument)', baseWx: 0.0, baseWy: 0.0, baseR: 2.2, prompt: '[E] Examiner la statue de pierre gravée' }},
      {{ id: 'POI_ANCIENT_WELL', name: 'Puits en pierre gelé', baseWx: 1.2, baseWy: 2.4, baseR: 1.6, prompt: '[E] Regarder dans le puits gelé et obscur' }},
      {{ id: 'POI_PLAZA_SHRINE', name: 'Oratoire en bois de la place', baseWx: -1.2, baseWy: -1.8, baseR: 1.5, prompt: '[E] Inspecter la plaque votive en bois' }},
      {{ id: 'POI_FAMILY_HOUSE', name: 'Maison familiale des Miller', baseWx: -1.5, baseWy: -5.0, baseR: 2.2, prompt: '[E] Essayer la porte d\\'entrée de la maison' }},
      {{ id: 'POI_CHURCH', name: 'Église abandonnée St-Jude', baseWx: 3.5, baseWy: -7.5, baseR: 2.5, prompt: '[E] Examiner les lourdes portes de chêne' }},
      {{ id: 'POI_CEMETERY', name: 'Cimetière paroissial & Sépultures', baseWx: 1.2, baseWy: -4.5, baseR: 2.0, prompt: '[E] Fouiller les tombes sous la neige' }},
      {{ id: 'POI_MARKETPLACE', name: 'Place du marché abandonnée', baseWx: 4.5, baseWy: -0.5, baseR: 2.0, prompt: '[E] Fouiller les étals abandonnés' }},
      {{ id: 'POI_CRAFTSMAN_HOUSE', name: 'Atelier d\\'artisan', baseWx: 6.0, baseWy: -1.5, baseR: 2.0, prompt: '[E] Frapper au volet de l\\'atelier' }},
      {{ id: 'POI_SAWMILL', name: 'Scierie et grue de levage', baseWx: 8.5, baseWy: -1.0, baseR: 2.2, prompt: '[E] Examiner les grumes et le registre de coupe' }},
      {{ id: 'POI_WATERMILL', name: 'Vieux Moulin à eau de la falaise', baseWx: -2.5, baseWy: 8.5, baseR: 2.2, prompt: '[E] Inspecter la roue gelée et la trappe' }},
      {{ id: 'POI_WINDMILL', name: 'Moulin à vent de la crête ouest', baseWx: -8.5, baseWy: -2.0, baseR: 2.2, prompt: '[E] Examiner le mécanisme et le point de vue' }},
      {{ id: 'POI_FARM', name: 'Champs gelés de la ferme', baseWx: -5.5, baseWy: -3.5, baseR: 2.0, prompt: '[E] Inspecter la remise à outils enneigée' }},
      {{ id: 'POI_MINE_ENTRANCE', name: 'Porche de l\\'ancienne mine', baseWx: -7.5, baseWy: -7.5, baseR: 2.4, prompt: '[E] Inspecter l\\'entrée du tunnel obscur' }},
      {{ id: 'POI_BOAT_DOCK', name: 'Embarcadère et barque amarrée', baseWx: 2.0, baseWy: 8.5, baseR: 1.8, prompt: '[E] Examiner la barque prise dans les glaces' }},
      {{ id: 'POI_CARGO_DOCK', name: 'Quai de déchargement', baseWx: 6.0, baseWy: 6.0, baseR: 1.8, prompt: '[E] Fouiller les caisses de ravitaillement' }},
      {{ id: 'POI_RIVERSIDE_COTTAGE', name: 'Poste de garde de la rivière', baseWx: 5.5, baseWy: 3.0, baseR: 2.0, prompt: '[E] Regarder à travers la fenêtre éclairée' }},
      {{ id: 'POI_COTTAGE_WEST', name: 'Maison du forgeron', baseWx: -4.0, baseWy: -0.5, baseR: 2.0, prompt: '[E] Vérifier l\\'entrée de la forge éteinte' }},
      {{ id: 'POI_COTTAGE_SOUTH', name: 'Maisonnette du pêcheur', baseWx: -2.2, baseWy: 1.8, baseR: 2.0, prompt: '[E] Examiner les filets suspendus au porche' }},
      {{ id: 'POI_COTTAGE_FAR_WEST', name: 'Chalet forestier de l\\'ouest', baseWx: -5.5, baseWy: 2.0, baseR: 2.0, prompt: '[E] Inspecter les gravures sur la porte' }}
    ];

    // 6. Collision Obstacles reconstructed from Map village .png
    const obstacles = [
      // Buildings
      {{ id: 'church', baseWx: 3.5, baseWy: -7.5, baseHw: 1.6, baseHh: 1.4 }},
      {{ id: 'family_house', baseWx: -1.5, baseWy: -5.0, baseHw: 1.6, baseHh: 1.2 }},
      {{ id: 'watermill', baseWx: -2.5, baseWy: 8.5, baseHw: 1.4, baseHh: 1.2 }},
      {{ id: 'windmill', baseWx: -8.5, baseWy: -2.0, baseHw: 1.2, baseHh: 1.2 }},
      {{ id: 'cottage_west', baseWx: -4.0, baseWy: -0.5, baseHw: 1.2, baseHh: 1.1 }},
      {{ id: 'cottage_south', baseWx: -2.2, baseWy: 1.8, baseHw: 1.2, baseHh: 1.1 }},
      {{ id: 'cottage_far_west', baseWx: -5.5, baseWy: 2.0, baseHw: 1.1, baseHh: 1.0 }},
      {{ id: 'riverside_cottage', baseWx: 5.5, baseWy: 3.0, baseHw: 1.2, baseHh: 1.1 }},
      {{ id: 'east_workshop', baseWx: 6.0, baseWy: -1.5, baseHw: 1.1, baseHh: 1.0 }},
      {{ id: 'sawmill', baseWx: 8.5, baseWy: -1.0, baseHw: 1.3, baseHh: 1.2 }},
      {{ id: 'mine_archway', baseWx: -7.5, baseWy: -7.5, baseHw: 1.2, baseHh: 1.0 }},

      // Props & Monument
      {{ id: 'statue', baseWx: 0.0, baseWy: 0.0, baseHw: 0.6, baseHh: 0.6 }},
      {{ id: 'well', baseWx: 1.2, baseWy: 2.4, baseHw: 0.7, baseHh: 0.7 }},
      {{ id: 'shrine', baseWx: -1.2, baseWy: -1.8, baseHw: 0.5, baseHh: 0.5 }},
      {{ id: 'market_stall1', baseWx: 4.5, baseWy: -0.5, baseHw: 0.9, baseHh: 0.6 }},
      {{ id: 'market_stall2', baseWx: 5.2, baseWy: 0.4, baseHw: 0.8, baseHh: 0.5 }},
      {{ id: 'sawmill_crane', baseWx: 9.5, baseWy: -1.8, baseHw: 0.6, baseHh: 0.6 }},
      {{ id: 'logs', baseWx: 8.0, baseWy: 0.2, baseHw: 0.8, baseHh: 0.5 }},
      {{ id: 'cemetery_gate', baseWx: 1.8, baseWy: -3.2, baseHw: 0.3, baseHh: 0.8 }},
      {{ id: 'farm_fence', baseWx: -5.5, baseWy: -3.5, baseHw: 1.8, baseHh: 0.3 }},
      {{ id: 'boat', baseWx: 2.0, baseWy: 8.5, baseHw: 0.6, baseHh: 0.4 }},
      {{ id: 'dock_crane', baseWx: 6.0, baseWy: 6.0, baseHw: 0.5, baseHh: 0.5 }}
    ];

    function checkCollision(x, y, radius) {{
      for (const obs of obstacles) {{
        const ox = obs.baseWx * worldScale;
        const oy = obs.baseWy * worldScale;
        const ohw = obs.baseHw * worldScale;
        const ohh = obs.baseHh * worldScale;
        const cx = Math.max(ox - ohw, Math.min(x, ox + ohw));
        const cy = Math.max(oy - ohh, Math.min(y, oy + ohh));
        const dx = x - cx;
        const dy = y - cy;
        if (dx * dx + dy * dy < radius * radius) return true;
      }}
      return false;
    }}

    function getMinObstacleDist(x, y, radius) {{
      let minClearance = Infinity;
      for (const obs of obstacles) {{
        const ox = obs.baseWx * worldScale;
        const oy = obs.baseWy * worldScale;
        const ohw = obs.baseHw * worldScale;
        const ohh = obs.baseHh * worldScale;
        const dx = Math.abs(x - ox) - ohw;
        const dy = Math.abs(y - oy) - ohh;
        let clearance;
        if (dx <= 0 && dy <= 0) {{
          clearance = Math.max(dx, dy) - radius;
        }} else {{
          const cx = Math.max(ox - ohw, Math.min(x, ox + ohw));
          const cy = Math.max(oy - ohh, Math.min(y, oy + ohh));
          clearance = Math.hypot(x - cx, y - cy) - radius;
        }}
        if (clearance < minClearance) minClearance = clearance;
      }}
      return minClearance;
    }}

    function resolveMovement(curX, curY, targetX, targetY, radius) {{
      // 1. Direct target is clear
      if (!checkCollision(targetX, targetY, radius)) return {{ x: targetX, y: targetY }};

      // 2. Sliding along X
      if (!checkCollision(targetX, curY, radius)) return {{ x: targetX, y: curY }};

      // 3. Sliding along Y
      if (!checkCollision(curX, targetY, radius)) return {{ x: curX, y: targetY }};

      // 4. Anti-stuck escape: If current position is in collision, allow any movement that increases clearance
      const curClearance = getMinObstacleDist(curX, curY, radius);
      if (curClearance < 0) {{
        const targetClearance = getMinObstacleDist(targetX, targetY, radius);
        if (targetClearance > curClearance) return {{ x: targetX, y: targetY }};
        const slideXClearance = getMinObstacleDist(targetX, curY, radius);
        if (slideXClearance > curClearance) return {{ x: targetX, y: curY }};
        const slideYClearance = getMinObstacleDist(curX, targetY, radius);
        if (slideYClearance > curClearance) return {{ x: curX, y: targetY }};
      }}

      return {{ x: curX, y: curY }};
    }}

    // 7. Camera Clamping (Encompassing complete village bounds)
    const camera = {{
      x: 0,
      y: 200,
      minX: -1600,
      maxX: 1600,
      minY: -950,
      maxY: 1100,
      zoom: 1.10
    }};

    // 8. Input State (Supporting QWERTY, AZERTY, Arrows, Touch, Mouse Joystick, D-Pad, Click-to-Move)
    const keys = {{}};
    let inputX = 0;
    let inputY = 0;
    let dpadX = 0;
    let dpadY = 0;
    let moveTarget = null;
    let isDebug = false;

    window.addEventListener('keydown', (e) => {{
      const k = e.key.toLowerCase();
      keys[k] = true;
      if (k === 'r') rotateAlexCW();
      if (k === 'f') rotateAlexCCW();
      if (k === 't') toggleDirectionTestScene();
      if (k === 'u') unstuckAlex();
      if (k === '1') setTileSize(128, 64);
      if (k === '2') setTileSize(96, 48);
      if (k === '3') setTileSize(80, 40);
      if (k === '4') setTileSize(60, 30);
    }});
    window.addEventListener('keyup', (e) => {{ keys[e.key.toLowerCase()] = false; }});

    // Touch & Mouse Joystick Handling
    const joystick = document.getElementById('touch-controls');
    const stick = document.getElementById('touch-stick');
    let touchId = null;
    let isMouseDragging = false;

    joystick.addEventListener('touchstart', (e) => {{
      const t = e.changedTouches[0];
      touchId = t.identifier;
      updateJoystick(t);
    }});
    joystick.addEventListener('touchmove', (e) => {{
      for (let i = 0; i < e.changedTouches.length; i++) {{
        if (e.changedTouches[i].identifier === touchId) {{
          updateJoystick(e.changedTouches[i]);
          break;
        }}
      }}
    }});
    function endJoystick(e) {{
      for (let i = 0; i < e.changedTouches.length; i++) {{
        if (e.changedTouches[i].identifier === touchId) {{
          touchId = null;
          inputX = 0;
          inputY = 0;
          stick.style.transform = `translate(0px, 0px)`;
          break;
        }}
      }}
    }}
    joystick.addEventListener('touchend', endJoystick);
    joystick.addEventListener('touchcancel', endJoystick);

    // Mouse dragging for virtual joystick (desktop & laptop support)
    joystick.addEventListener('mousedown', (e) => {{
      isMouseDragging = true;
      updateJoystick(e);
    }});
    window.addEventListener('mousemove', (e) => {{
      if (isMouseDragging) updateJoystick(e);
    }});
    window.addEventListener('mouseup', () => {{
      if (isMouseDragging) {{
        isMouseDragging = false;
        inputX = 0;
        inputY = 0;
        stick.style.transform = 'translate(0px, 0px)';
      }}
    }});

    function updateJoystick(t) {{
      const rect = joystick.getBoundingClientRect();
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
      let dx = t.clientX - cx;
      let dy = t.clientY - cy;
      const dist = Math.hypot(dx, dy);
      const maxR = rect.width / 2 - 25;
      if (dist > maxR) {{
        dx = (dx / dist) * maxR;
        dy = (dy / dist) * maxR;
      }}
      stick.style.transform = `translate(${{dx}}px, ${{dy}}px)`;
      inputX = dx / maxR;
      inputY = dy / maxR;
    }}

    // D-Pad Helper Handlers
    function setDpad(dx, dy) {{
      dpadX = dx;
      dpadY = dy;
      moveTarget = null;
    }}
    function clearDpad() {{
      dpadX = 0;
      dpadY = 0;
    }}

    // Click-to-Move / Tap-to-Move on canvas
    canvas.addEventListener('click', (e) => {{
      const rect = canvas.getBoundingClientRect();
      const clickX = (e.clientX - rect.left) * window.devicePixelRatio;
      const clickY = (e.clientY - rect.top) * window.devicePixelRatio;

      // Inverse camera transform
      const screenX = (clickX - canvas.width / 2) / (camera.zoom * window.devicePixelRatio) + camera.x;
      const screenY = (clickY - canvas.height / 2) / (camera.zoom * window.devicePixelRatio) + camera.y;

      const tw = screenToWorld(screenX, screenY);
      moveTarget = tw;
      showToast(`Alex marche vers [${{(tw.x / worldScale).toFixed(1)}}, ${{(tw.y / worldScale).toFixed(1)}}]`);
    }});

    // Unstuck / Reset Alex Function
    function unstuckAlex() {{
      alex.wx = 7.0 * worldScale;
      alex.wy = 8.0 * worldScale;
      alex.orientation = 'NW';
      moveTarget = null;
      inputX = 0;
      inputY = 0;
      dpadX = 0;
      dpadY = 0;
      isMouseDragging = false;
      stick.style.transform = 'translate(0px, 0px)';
      for (const k in keys) keys[k] = false;
      document.getElementById('hud-orient').textContent = alex.orientation;
      showToast('🔓 Alex a été débloqué et repositionné en sécurité sur le pont !');
    }}

    function toggleSprint() {{
      alex.isSprinting = !alex.isSprinting;
      const btn = document.getElementById('sprint-btn');
      btn.classList.toggle('active', alex.isSprinting);
    }}

    function toggleDebug() {{
      isDebug = !isDebug;
      document.getElementById('debug-toggle').classList.toggle('active', isDebug);
      document.getElementById('debug-panel').style.display = isDebug ? 'block' : 'none';
      document.getElementById('debug-tools').style.display = isDebug ? 'flex' : 'none';
    }}

    function zoomCam(delta) {{
      camera.zoom = Math.max(0.85, Math.min(1.6, camera.zoom + delta));
    }}

    function showToast(msg) {{
      const t = document.getElementById('notification');
      t.textContent = msg;
      t.style.display = 'block';
      setTimeout(() => {{ t.style.display = 'none'; }}, 2800);
    }}

    function saveGame() {{
      const saveState = {{
        wx: alex.wx / worldScale,
        wy: alex.wy / worldScale,
        orient: alex.orientation,
        timestamp: Date.now()
      }};
      localStorage.setItem('echo_save_village', JSON.stringify(saveState));
      showToast('Progression sauvegardée dans le repository local !');
    }}

    function loadGame() {{
      const raw = localStorage.getItem('echo_save_village');
      if (raw) {{
        const saveState = JSON.parse(raw);
        alex.wx = saveState.wx * worldScale;
        alex.wy = saveState.wy * worldScale;
        alex.orientation = saveState.orient || 'NW';
        document.getElementById('hud-orient').textContent = alex.orientation;
        showToast('Partie chargée avec succès !');
      }} else {{
        showToast('Aucune sauvegarde locale trouvée.');
      }}
    }}

    // 8b. AlexDirectionTestScene Logic
    let testSceneOpen = false;
    let testSceneState = 'IDLE';
    let testSceneOrient = 'SE';
    let testAutoRotate = true;
    let testRotateTimer = 0;

    function toggleDirectionTestScene() {{
      testSceneOpen = !testSceneOpen;
      const modal = document.getElementById('direction-test-modal');
      modal.style.display = testSceneOpen ? 'flex' : 'none';
      if (testSceneOpen) {{
        updateTestSceneDisplay();
      }}
    }}

    function setTestSceneState(st) {{
      testSceneState = st;
      document.querySelectorAll('.test-state-btn').forEach(b => b.classList.remove('active'));
      if (st === 'IDLE') document.getElementById('ts-idle').classList.add('active');
      else if (st === 'WALK') document.getElementById('ts-walk').classList.add('active');
      else if (st === 'RUN') document.getElementById('ts-run').classList.add('active');
      else if (st === 'INTERACTION') document.getElementById('ts-interact').classList.add('active');
      updateTestSceneDisplay();
    }}

    function getSpriteForStateAndOrient(st, orient) {{
      if (st === 'IDLE') {{
        if (orient === 'SW') return images.idleSW.src;
        if (orient === 'NE') return images.idleNE.src;
        if (orient === 'NW') return images.idleNW.src;
        return images.idleSE.src;
      }} else if (st === 'WALK') {{
        if (orient === 'SW') return images.walkSW.src;
        if (orient === 'NE') return images.walkNE.src;
        if (orient === 'NW') return images.walkNW.src;
        return images.walkSE.src;
      }} else if (st === 'RUN') {{
        if (orient === 'SW') return images.runSW.src;
        if (orient === 'NE') return images.runNE.src;
        if (orient === 'NW') return images.runNW.src;
        return images.runSE.src;
      }} else if (st === 'INTERACTION') {{
        if (orient === 'SW') return images.interactSW.src;
        if (orient === 'NE') return images.interactNE.src;
        if (orient === 'NW') return images.interactNW.src;
        return images.interactSE.src;
      }}
      return images.idleSE.src;
    }}

    function updateTestSceneDisplay() {{
      document.getElementById('test-img-se').src = getSpriteForStateAndOrient(testSceneState, 'SE');
      document.getElementById('test-img-sw').src = getSpriteForStateAndOrient(testSceneState, 'SW');
      document.getElementById('test-img-ne').src = getSpriteForStateAndOrient(testSceneState, 'NE');
      document.getElementById('test-img-nw').src = getSpriteForStateAndOrient(testSceneState, 'NW');
      
      document.getElementById('test-img-center').src = getSpriteForStateAndOrient(testSceneState, testSceneOrient);
      document.getElementById('center-orient-label').textContent = testSceneOrient + ' (Rotation Active)';
    }}

    function stepTestRotationCW() {{
      const idx = canonicalCycle.indexOf(testSceneOrient);
      testSceneOrient = canonicalCycle[(idx + 1) % canonicalCycle.length];
      updateTestSceneDisplay();
    }}

    function stepTestRotationCCW() {{
      const idx = canonicalCycle.indexOf(testSceneOrient);
      testSceneOrient = canonicalCycle[(idx - 1 + canonicalCycle.length) % canonicalCycle.length];
      updateTestSceneDisplay();
    }}

    function toggleTestAutoRotate() {{
      testAutoRotate = !testAutoRotate;
      const btn = document.getElementById('btn-toggle-autorotate');
      btn.textContent = 'Auto-Rotation: ' + (testAutoRotate ? 'ACTIF' : 'PAUSE');
      btn.style.background = testAutoRotate ? '#10B981' : '#64748B';
    }}

    // 9. Weather Snow Particles
    const snowflakes = [];
    for (let i = 0; i < 80; i++) {{
      snowflakes.push({{
        x: (Math.random() - 0.5) * 1600,
        y: (Math.random() - 0.5) * 1200,
        vx: -30 - Math.random() * 40,
        vy: 40 + Math.random() * 50,
        size: 1.0 + Math.random() * 2.0,
        alpha: 0.3 + Math.random() * 0.5
      }});
    }}

    // 10. Main Game Loop
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

      // Movement Input (combining keyboard WASD + ZQSD + Arrows, joystick, D-Pad, and Click-to-Move)
      let moveX = inputX + dpadX;
      let moveY = inputY + dpadY;

      // Support both QWERTY (WASD) and AZERTY (ZQSD) + Arrows
      if (keys['w'] || keys['z'] || keys['arrowup']) moveY -= 1;
      if (keys['s'] || keys['arrowdown']) moveY += 1;
      if (keys['a'] || keys['q'] || keys['arrowleft']) moveX -= 1;
      if (keys['d'] || keys['arrowright']) moveX += 1;

      // Click-to-Move navigation support
      if (Math.hypot(moveX, moveY) > 0.1) {{
        moveTarget = null;
      }} else if (moveTarget) {{
        const toTargetX = moveTarget.x - alex.wx;
        const toTargetY = moveTarget.y - alex.wy;
        const dist = Math.hypot(toTargetX, toTargetY);
        if (dist > 0.25 * worldScale) {{
          // Convert world displacement to screen input direction
          const screenDx = (toTargetX - toTargetY);
          const screenDy = (toTargetX + toTargetY);
          const sLen = Math.hypot(screenDx, screenDy);
          if (sLen > 0.001) {{
            moveX = screenDx / sLen;
            moveY = screenDy / sLen;
          }}
        }} else {{
          moveTarget = null;
        }}
      }}

      const len = Math.hypot(moveX, moveY);
      
      if (len < 0.10) {{
        alex.state = 'IDLE';
      }} else {{
        const normX = moveX / len;
        const normY = moveY / len;

        const angle = Math.atan2(normY, normX);
        if (angle >= 0 && angle < Math.PI / 2) alex.orientation = 'SE';
        else if (angle >= Math.PI / 2 && angle <= Math.PI) alex.orientation = 'SW';
        else if (angle >= -Math.PI && angle < -Math.PI / 2) alex.orientation = 'NW';
        else alex.orientation = 'NE';
        document.getElementById('hud-orient').textContent = alex.orientation;

        if (len < 0.30) {{
          alex.state = 'IDLE';
        }} else {{
          const isRunning = alex.isSprinting || len > 0.72 || keys['shift'];
          alex.state = isRunning ? 'RUN' : 'WALK';
          const speed = (isRunning ? 4.8 : 2.4) * worldScale;

          const worldDx = (normX + normY) * speed * dt * 0.707;
          const worldDy = (-normX + normY) * speed * dt * 0.707;

          const resolved = resolveMovement(alex.wx, alex.wy, alex.wx + worldDx, alex.wy + worldDy, 0.28 * worldScale);
          alex.wx = resolved.x;
          alex.wy = resolved.y;
        }}
      }}

      // Camera Follow with dynamic viewport clamping
      const alexScreen = worldToScreen(alex.wx, alex.wy);
      const halfW = (canvas.width / (2 * window.devicePixelRatio)) / camera.zoom;
      const halfH = (canvas.height / (2 * window.devicePixelRatio)) / camera.zoom;

      const minAllowedX = camera.minX + halfW;
      const maxAllowedX = camera.maxX - halfW;
      const targetCamX = minAllowedX < maxAllowedX ? Math.max(minAllowedX, Math.min(alexScreen.x, maxAllowedX)) : 0;

      const minAllowedY = camera.minY + halfH;
      const maxAllowedY = camera.maxY - halfH;
      const targetCamY = minAllowedY < maxAllowedY ? Math.max(minAllowedY, Math.min(alexScreen.y, maxAllowedY)) : 100;

      camera.x += (targetCamX - camera.x) * Math.min(5.5 * dt, 1.0);
      camera.y += (targetCamY - camera.y) * Math.min(5.5 * dt, 1.0);

      // Weather update
      for (const f of snowflakes) {{
        f.y += f.vy * dt;
        f.x += f.vx * dt;
        if (f.y > 800) {{ f.y = -600; f.x = (Math.random() - 0.5) * 1600; }}
        if (f.x < -800) f.x = 800;
      }}

      // POI Check
      let activePOI = null;
      for (const poi of pois) {{
        const px = poi.baseWx * worldScale;
        const py = poi.baseWy * worldScale;
        const pr = poi.baseR * worldScale;
        const dx = alex.wx - px;
        const dy = alex.wy - py;
        if (dx * dx + dy * dy <= pr * pr) {{
          activePOI = poi;
          break;
        }}
      }}

      const locTitle = document.getElementById('loc-title');
      const promptBadge = document.getElementById('prompt-badge');
      const promptText = document.getElementById('prompt-text');

      if (activePOI) {{
        locTitle.textContent = activePOI.name;
        promptBadge.style.display = 'inline-flex';
        promptText.textContent = activePOI.prompt;
      }} else {{
        locTitle.textContent = "LE VILLAGE ABANDONNÉ";
        promptBadge.style.display = 'none';
      }}

      if (isDebug) {{
        document.getElementById('dbg-pos').textContent = `Alex: [${{(alex.wx / worldScale).toFixed(2)}}, ${{(alex.wy / worldScale).toFixed(2)}}]`;
        document.getElementById('dbg-state').textContent = `State: ${{alex.state}} (${{alex.orientation}}) | Z: ${{calculateZ(alex.wx, alex.wy)}}`;
        document.getElementById('dbg-poi').textContent = `POI: ${{activePOI ? activePOI.id : 'NONE'}}`;
        document.getElementById('dbg-cam').textContent = `Cam: [${{camera.x.toFixed(0)}}, ${{camera.y.toFixed(0)}}] | Zoom: ${{camera.zoom.toFixed(2)}}`;
      }}

      render(now);
      requestAnimationFrame(gameLoop);
    }}

    function render(now) {{
      // Deep winter night tone
      ctx.fillStyle = '#0E1626';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      ctx.save();
      ctx.translate(canvas.width / 2, canvas.height / 2);
      ctx.scale(camera.zoom * window.devicePixelRatio, camera.zoom * window.devicePixelRatio);
      ctx.translate(-camera.x, -camera.y);

      // 1. Multi-Zone Ground Layer (Reconstructed matching Map village .png)
      const gridR = Math.ceil(26 * worldScale);
      for (let x = -gridR; x <= gridR; x++) {{
        for (let y = -gridR; y <= gridR; y++) {{
          const pos = worldToScreen(x, y);

          // Topologic zone classification
          const isBridge = (Math.abs(x - y) <= 1.2 * worldScale) && ((x + y) >= 8.0 * worldScale) && ((x + y) <= 15.5 * worldScale);
          const isLeftDock = Math.hypot(x - 2.0 * worldScale, y - 8.5 * worldScale) <= (1.8 * worldScale);
          const isRightDock = Math.hypot(x - 6.0 * worldScale, y - 6.0 * worldScale) <= (1.8 * worldScale);
          const isRiver = ((x + y) >= 10.0 * worldScale) && !isBridge && !isLeftDock && !isRightDock;
          const isPlaza = Math.hypot(x, y) <= (2.6 * worldScale);
          const isMainRoad = (Math.abs(x - y) <= 1.2 * worldScale) && ((x + y) >= 0.0) && ((x + y) <= 9.5 * worldScale);
          const isChurchPath = (x >= 0.0 && x <= 5.5 * worldScale && y <= 0.0 && y >= -8.5 * worldScale) &&
                               (Math.abs(y - (-1.8 * x)) / 2.06 <= 1.4 * worldScale);
          const isMarketStreet = (x >= 0.0 && x <= 9.5 * worldScale && y >= -2.5 * worldScale && y <= 1.8 * worldScale);
          const isFarmRoad = (x <= 0.0 && x >= -9.0 * worldScale && y >= -4.5 * worldScale && y <= 2.5 * worldScale);
          const isWatermillTrail = (y >= 2.0 * worldScale && y <= 9.5 * worldScale && x <= 4.5 * worldScale && x >= -3.5 * worldScale);
          const isFarmField = (x <= -4.0 * worldScale && x >= -7.5 * worldScale && y <= -1.5 * worldScale && y >= -5.5 * worldScale);

          let tileImg = images.snowSlab;
          if (isRiver) {{
            tileImg = images.iceSlab;
          }} else if (isBridge || isLeftDock || isRightDock) {{
            tileImg = images.slabVar;
          }} else if (isPlaza || isMainRoad || isChurchPath || isMarketStreet || isFarmRoad || isWatermillTrail) {{
            tileImg = ((x + y) % 2 === 0) ? images.slab : images.slabVar;
          }} else if (isFarmField) {{
            tileImg = images.snowSlab;
          }}

          if (tileImg && tileImg.complete && tileImg.naturalWidth > 0) {{
            ctx.drawImage(tileImg, pos.x - HALF_W, pos.y - HALF_H, TILE_W + 1, TILE_H + 1);
          }} else {{
            ctx.beginPath();
            ctx.moveTo(pos.x, pos.y - HALF_H);
            ctx.lineTo(pos.x + HALF_W, pos.y);
            ctx.lineTo(pos.x, pos.y + HALF_H);
            ctx.lineTo(pos.x - HALF_W, pos.y);
            ctx.closePath();
            ctx.fillStyle = isRiver ? '#0F172A' : (isPlaza ? '#334155' : (isBridge ? '#78350F' : '#1A232E'));
            ctx.fill();
          }}
        }}
      }}

      // 2. Dynamic Z-Ordered Renderables (Reconstructed Buildings, Props, NPCs, and Alex)
      const renderables = [
        // --- BUILDINGS ---
        // St. Jude Church (NE Hill)
        {{ type: 'building', id: 'church', wx: 3.5 * worldScale, wy: -7.5 * worldScale, z: calculateZ(3.5 * worldScale, -7.5 * worldScale, 20000), img: images.church, w: 280, h: 370, pivotY: 0.90 }},
        // Miller Family House (North Cottage)
        {{ type: 'building', id: 'house', wx: -1.5 * worldScale, wy: -5.0 * worldScale, z: calculateZ(-1.5 * worldScale, -5.0 * worldScale, 20000), img: images.familyHouse, w: 320, h: 298, pivotY: 0.88 }},
        // Watermill on cliff (SW)
        {{ type: 'building', id: 'watermill', wx: -2.5 * worldScale, wy: 8.5 * worldScale, z: calculateZ(-2.5 * worldScale, 8.5 * worldScale, 20000), img: images.watermill, w: 260, h: 244, pivotY: 0.88 }},
        // Windmill on west ridge
        {{ type: 'building', id: 'windmill', wx: -8.5 * worldScale, wy: -2.0 * worldScale, z: calculateZ(-8.5 * worldScale, -2.0 * worldScale, 20000), img: images.windmill, w: 240, h: 270, pivotY: 0.88 }},
        // West Cottage (Blacksmith)
        {{ type: 'building', id: 'cottage_west', wx: -4.0 * worldScale, wy: -0.5 * worldScale, z: calculateZ(-4.0 * worldScale, -0.5 * worldScale, 20000), img: images.cottageWest, w: 220, h: 205, pivotY: 0.88 }},
        // South Cottage (Fisherman)
        {{ type: 'building', id: 'cottage_south', wx: -2.2 * worldScale, wy: 1.8 * worldScale, z: calculateZ(-2.2 * worldScale, 1.8 * worldScale, 20000), img: images.cottageSouth, w: 230, h: 180, pivotY: 0.88 }},
        // Far West Cottage (Forester)
        {{ type: 'building', id: 'cottage_far_west', wx: -5.5 * worldScale, wy: 2.0 * worldScale, z: calculateZ(-5.5 * worldScale, 2.0 * worldScale, 20000), img: images.cottageFarWest, w: 210, h: 188, pivotY: 0.88 }},
        // Riverside Cottage (Guardhouse)
        {{ type: 'building', id: 'riverside_cottage', wx: 5.5 * worldScale, wy: 3.0 * worldScale, z: calculateZ(5.5 * worldScale, 3.0 * worldScale, 20000), img: images.riversideCottage, w: 215, h: 190, pivotY: 0.88 }},
        // East Workshop
        {{ type: 'building', id: 'east_workshop', wx: 6.0 * worldScale, wy: -1.5 * worldScale, z: calculateZ(6.0 * worldScale, -1.5 * worldScale, 20000), img: images.eastWorkshop, w: 200, h: 180, pivotY: 0.88 }},
        // Sawmill
        {{ type: 'building', id: 'sawmill', wx: 8.5 * worldScale, wy: -1.0 * worldScale, z: calculateZ(8.5 * worldScale, -1.0 * worldScale, 20000), img: images.sawmill, w: 210, h: 195, pivotY: 0.88 }},
        // Mine Archway
        {{ type: 'building', id: 'mine_archway', wx: -7.5 * worldScale, wy: -7.5 * worldScale, z: calculateZ(-7.5 * worldScale, -7.5 * worldScale, 20000), img: images.mineArchway, w: 170, h: 190, pivotY: 0.88 }},

        // --- PROPS ---
        // Founder Statue (Center Plaza)
        {{ type: 'prop', id: 'statue', wx: 0.0 * worldScale, wy: 0.0 * worldScale, z: calculateZ(0.0 * worldScale, 0.0 * worldScale, 30000), img: images.statue, w: 90, h: 140, pivotY: 0.90 }},
        // Stone Well (South of Plaza)
        {{ type: 'prop', id: 'well', wx: 1.2 * worldScale, wy: 2.4 * worldScale, z: calculateZ(1.2 * worldScale, 2.4 * worldScale, 30000), img: images.well, w: 100, h: 112, pivotY: 0.85 }},
        // Wooden Shrine (NW of Plaza)
        {{ type: 'prop', id: 'shrine', wx: -1.2 * worldScale, wy: -1.8 * worldScale, z: calculateZ(-1.2 * worldScale, -1.8 * worldScale, 30000), img: images.plazaShrine, w: 80, h: 95, pivotY: 0.88 }},
        // Market Stalls
        {{ type: 'prop', id: 'stall1', wx: 4.5 * worldScale, wy: -0.5 * worldScale, z: calculateZ(4.5 * worldScale, -0.5 * worldScale, 30000), img: images.marketStall01, w: 130, h: 115, pivotY: 0.88 }},
        {{ type: 'prop', id: 'stall2', wx: 5.2 * worldScale, wy: 0.4 * worldScale, z: calculateZ(5.2 * worldScale, 0.4 * worldScale, 30000), img: images.marketStall02, w: 115, h: 105, pivotY: 0.88 }},
        // Sawmill Crane & Logs
        {{ type: 'prop', id: 'crane', wx: 9.5 * worldScale, wy: -1.8 * worldScale, z: calculateZ(9.5 * worldScale, -1.8 * worldScale, 30000), img: images.sawmillCrane, w: 88, h: 139, pivotY: 0.92 }},
        {{ type: 'prop', id: 'logs', wx: 8.0 * worldScale, wy: 0.2 * worldScale, z: calculateZ(8.0 * worldScale, 0.2 * worldScale, 30000), img: images.stackedLogs, w: 103, h: 93, pivotY: 0.85 }},
        // Cemetery Iron Gate
        {{ type: 'prop', id: 'gate', wx: 1.8 * worldScale, wy: -3.2 * worldScale, z: calculateZ(1.8 * worldScale, -3.2 * worldScale, 30000), img: images.ironGate, w: 130, h: 85, pivotY: 0.90 }},
        // Moored Rowboat on River Pier
        {{ type: 'prop', id: 'boat', wx: 2.0 * worldScale, wy: 8.5 * worldScale, z: calculateZ(2.0 * worldScale, 8.5 * worldScale, 30000), img: images.boat, w: 90, h: 60, pivotY: 0.80 }},
        // Dock Hoist
        {{ type: 'prop', id: 'dock_crane', wx: 6.0 * worldScale, wy: 6.0 * worldScale, z: calculateZ(6.0 * worldScale, 6.0 * worldScale, 30000), img: images.dockCrane, w: 80, h: 135, pivotY: 0.90 }},

        // --- STREET LAMPS (Warm Lantern Posts) ---
        {{ type: 'prop', id: 'lamp_br1', wx: 4.2 * worldScale, wy: 4.8 * worldScale, z: calculateZ(4.2 * worldScale, 4.8 * worldScale, 30000), img: images.lampPost, w: 38, h: 96, pivotY: 0.95 }},
        {{ type: 'prop', id: 'lamp_br2', wx: 4.8 * worldScale, wy: 4.2 * worldScale, z: calculateZ(4.8 * worldScale, 4.2 * worldScale, 30000), img: images.lampPost, w: 38, h: 96, pivotY: 0.95 }},
        {{ type: 'prop', id: 'lamp_plz1', wx: -1.5 * worldScale, wy: -0.8 * worldScale, z: calculateZ(-1.5 * worldScale, -0.8 * worldScale, 30000), img: images.lampPost, w: 38, h: 96, pivotY: 0.95 }},
        {{ type: 'prop', id: 'lamp_plz2', wx: 0.8 * worldScale, wy: -1.5 * worldScale, z: calculateZ(0.8 * worldScale, -1.5 * worldScale, 30000), img: images.lampPost, w: 38, h: 96, pivotY: 0.95 }},
        {{ type: 'prop', id: 'lamp_plz3', wx: -0.8 * worldScale, wy: 1.5 * worldScale, z: calculateZ(-0.8 * worldScale, 1.5 * worldScale, 30000), img: images.lampPost, w: 38, h: 96, pivotY: 0.95 }},
        {{ type: 'prop', id: 'lamp_plz4', wx: 1.5 * worldScale, wy: 0.8 * worldScale, z: calculateZ(1.5 * worldScale, 0.8 * worldScale, 30000), img: images.lampPost, w: 38, h: 96, pivotY: 0.95 }},
        {{ type: 'prop', id: 'lamp_well', wx: 1.8 * worldScale, wy: 2.2 * worldScale, z: calculateZ(1.8 * worldScale, 2.2 * worldScale, 30000), img: images.lampPost, w: 38, h: 96, pivotY: 0.95 }},
        {{ type: 'prop', id: 'lamp_ch', wx: 2.5 * worldScale, wy: -4.2 * worldScale, z: calculateZ(2.5 * worldScale, -4.2 * worldScale, 30000), img: images.lampPost, w: 38, h: 96, pivotY: 0.95 }},
        {{ type: 'prop', id: 'lamp_mkt', wx: 3.8 * worldScale, wy: -0.4 * worldScale, z: calculateZ(3.8 * worldScale, -0.4 * worldScale, 30000), img: images.lampPost, w: 38, h: 96, pivotY: 0.95 }},
        {{ type: 'prop', id: 'lamp_wst', wx: -1.8 * worldScale, wy: 0.6 * worldScale, z: calculateZ(-1.8 * worldScale, 0.6 * worldScale, 30000), img: images.lampPost, w: 38, h: 96, pivotY: 0.95 }},

        // --- TREES ---
        {{ type: 'prop', id: 'pine_ch1', wx: 5.0 * worldScale, wy: -8.5 * worldScale, z: calculateZ(5.0 * worldScale, -8.5 * worldScale, 30000), img: images.pineTree, w: 85, h: 145, pivotY: 0.90 }},
        {{ type: 'prop', id: 'pine_ch2', wx: 2.0 * worldScale, wy: -9.0 * worldScale, z: calculateZ(2.0 * worldScale, -9.0 * worldScale, 30000), img: images.pineTree, w: 95, h: 160, pivotY: 0.90 }},
        {{ type: 'prop', id: 'dead_plz', wx: 0.8 * worldScale, wy: 3.5 * worldScale, z: calculateZ(0.8 * worldScale, 3.5 * worldScale, 30000), img: images.deadTree, w: 80, h: 135, pivotY: 0.90 }},
        {{ type: 'prop', id: 'pine_farm', wx: -7.0 * worldScale, wy: -4.5 * worldScale, z: calculateZ(-7.0 * worldScale, -4.5 * worldScale, 30000), img: images.pineTree, w: 90, h: 150, pivotY: 0.90 }},
        {{ type: 'prop', id: 'pine_mill', wx: -3.5 * worldScale, wy: 7.0 * worldScale, z: calculateZ(-3.5 * worldScale, 7.0 * worldScale, 30000), img: images.pineTree, w: 85, h: 140, pivotY: 0.90 }},
        {{ type: 'prop', id: 'pine_saw', wx: 10.0 * worldScale, wy: 0.5 * worldScale, z: calculateZ(10.0 * worldScale, 0.5 * worldScale, 30000), img: images.pineTree, w: 85, h: 140, pivotY: 0.90 }},

        // --- NPCS ---
        // Emma near Family House
        {{ type: 'npc', id: 'npc_emma', name: 'Emma', wx: -1.0 * worldScale, wy: -2.5 * worldScale, z: calculateZ(-1.0 * worldScale, -2.5 * worldScale, 40000), img: images.emma, w: 26, h: 54, pivotY: 0.95 }},
        // James near Sawmill
        {{ type: 'npc', id: 'npc_james', name: 'James', wx: 7.0 * worldScale, wy: -0.5 * worldScale, z: calculateZ(7.0 * worldScale, -0.5 * worldScale, 40000), img: images.james, w: 28, h: 56, pivotY: 0.95 }},
        // Michael near Church Steps
        {{ type: 'npc', id: 'npc_michael', name: 'Michael', wx: 2.5 * worldScale, wy: -4.5 * worldScale, z: calculateZ(2.5 * worldScale, -4.5 * worldScale, 40000), img: images.michael, w: 28, h: 56, pivotY: 0.95 }},
        // Ethan (Echo apparition near the well)
        {{ type: 'npc', id: 'npc_ethan', name: 'Ethan (Écho)', wx: 1.2 * worldScale, wy: 2.4 * worldScale, z: calculateZ(1.2 * worldScale, 2.4 * worldScale, 40000), img: images.ethan, w: 28, h: 55, pivotY: 0.95, isEcho: true }},

        // --- ALEX CHARACTER ---
        {{
          type: 'alex', id: 'alex', wx: alex.wx, wy: alex.wy,
          z: calculateZ(alex.wx, alex.wy, 40000)
        }}
      ];

      // Sort by Z-Order strictly
      renderables.sort((a, b) => a.z - b.z);

      for (const r of renderables) {{
        const pt = worldToScreen(r.wx, r.wy);

        if (r.type === 'alex') {{
          // Ground contact shadow
          ctx.beginPath();
          ctx.ellipse(pt.x, pt.y - 1, 10, 3.5, 0, 0, Math.PI * 2);
          ctx.fillStyle = 'rgba(0, 0, 0, 0.45)';
          ctx.fill();

          // Render Alex with genuine 4-way direction sprite
          const dx = pt.x - alex.w / 2;
          const dy = pt.y - alex.h;

          let spr = images.idleSE;
          if (alex.state === 'RUN') {{
            if (alex.orientation === 'SE') spr = images.runSE;
            else if (alex.orientation === 'SW') spr = images.runSW;
            else if (alex.orientation === 'NW') spr = images.runNW;
            else if (alex.orientation === 'NE') spr = images.runNE;
          }} else if (alex.state === 'WALK') {{
            if (alex.orientation === 'SE') spr = images.walkSE;
            else if (alex.orientation === 'SW') spr = images.walkSW;
            else if (alex.orientation === 'NW') spr = images.walkNW;
            else if (alex.orientation === 'NE') spr = images.walkNE;
          }} else {{
            if (alex.orientation === 'SE') spr = images.idleSE;
            else if (alex.orientation === 'SW') spr = images.idleSW;
            else if (alex.orientation === 'NW') spr = images.idleNW;
            else if (alex.orientation === 'NE') spr = images.idleNE;
          }}

          if (spr && spr.complete && spr.naturalWidth > 0) {{
            ctx.drawImage(spr, dx, dy, alex.w, alex.h);
          }}

          if (isDebug) {{
            ctx.strokeStyle = '#38BDF8';
            ctx.lineWidth = 1.5;
            ctx.strokeRect(dx, dy, alex.w, alex.h);
          }}
        }} else if (r.type === 'npc') {{
          // NPC Ground shadow
          ctx.beginPath();
          ctx.ellipse(pt.x, pt.y - 1, 9, 3.2, 0, 0, Math.PI * 2);
          ctx.fillStyle = r.isEcho ? 'rgba(56, 189, 248, 0.3)' : 'rgba(0, 0, 0, 0.4)';
          ctx.fill();

          const dx = pt.x - r.w / 2;
          const dy = pt.y - r.h;

          if (r.isEcho) ctx.globalAlpha = 0.75;
          if (r.img && r.img.complete && r.img.naturalWidth > 0) {{
            ctx.drawImage(r.img, dx, dy, r.w, r.h);
          }}
          if (r.isEcho) ctx.globalAlpha = 1.0;

          // Name badge above NPC
          ctx.fillStyle = r.isEcho ? '#38BDF8' : '#F8FAFC';
          ctx.font = 'bold 9px sans-serif';
          ctx.textAlign = 'center';
          ctx.fillText(r.name, pt.x, dy - 4);
        }} else {{
          // Building or Prop
          const pivotY = r.pivotY || 0.88;
          const dx = pt.x - r.w / 2;
          const dy = pt.y - r.h * pivotY;

          if (r.img && r.img.complete && r.img.naturalWidth > 0) {{
            ctx.drawImage(r.img, dx, dy, r.w, r.h);
          }}

          if (isDebug) {{
            ctx.strokeStyle = r.type === 'building' ? 'rgba(234, 179, 8, 0.6)' : 'rgba(16, 185, 129, 0.6)';
            ctx.lineWidth = 1;
            ctx.strokeRect(dx, dy, r.w, r.h);
          }}
        }}
      }}

      // 3. Ambient Lantern Glows
      for (const obs of obstacles) {{
        if (obs.id && obs.id.includes('lamp')) {{
          const lpt = worldToScreen(obs.baseWx * worldScale, obs.baseWy * worldScale);
          const grad = ctx.createRadialGradient(lpt.x, lpt.y - 45, 2, lpt.x, lpt.y - 45, 60);
          grad.addColorStop(0, 'rgba(253, 224, 71, 0.45)');
          grad.addColorStop(0.5, 'rgba(245, 158, 11, 0.15)');
          grad.addColorStop(1, 'rgba(0, 0, 0, 0)');
          ctx.fillStyle = grad;
          ctx.beginPath();
          ctx.arc(lpt.x, lpt.y - 45, 60, 0, Math.PI * 2);
          ctx.fill();
        }}
      }}

      // 4. Foreground Falling Snowflakes
      ctx.fillStyle = 'rgba(241, 245, 249, 0.75)';
      for (const f of snowflakes) {{
        ctx.beginPath();
        ctx.arc(f.x, f.y, f.size, 0, Math.PI * 2);
        ctx.fill();
      }}

      ctx.restore();
    }}

    requestAnimationFrame(gameLoop);
  </script>
</body>
</html>
"""

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"=== Successfully updated Reconstructed Village HTML at {OUT_FILE} ===")

if __name__ == "__main__":
    build()
