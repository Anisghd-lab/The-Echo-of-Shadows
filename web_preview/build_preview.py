import os
import json
import base64

ROOT_DIR = "/root/the_echo_of_shadows"
ASSETS_DIR = os.path.join(ROOT_DIR, "assets", "images")
OUT_FILE = os.path.join(ROOT_DIR, "web_preview", "index.html")

def to_base64(rel_path):
    full_path = os.path.join(ASSETS_DIR, rel_path)
    if os.path.exists(full_path):
        with open(full_path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    return ""

def build():
    print("Embedding Phase 3.1 Village World assets & 360° Alex animations...")
    
    # 1. Alex 4-Way Directional Sprites (Idle, Walk, Run, Interaction)
    alex_idle_se = to_base64("characters/alex/idle/Alex-—-Animation-Idle03.png")
    alex_idle_sw = to_base64("characters/alex/idle/Alex-—-Animation-Idle10.png")
    alex_idle_ne = to_base64("characters/alex/idle/Alex-—-Animation-Idle06.png")
    alex_idle_nw = to_base64("characters/alex/idle/Alex-—-Animation-Idle07.png")
    
    alex_walk_se = to_base64("characters/alex/walk/Alex-—-Marche36.png")
    alex_walk_sw = to_base64("characters/alex/walk/Alex-—-Marche42.png")
    alex_walk_ne = to_base64("characters/alex/walk/Alex-—-Marche18.png")
    alex_walk_nw = to_base64("characters/alex/walk/Alex-—-Marche10.png")
    
    alex_run_se = to_base64("characters/alex/run/Alex-—-Course11.png")
    alex_run_sw = to_base64("characters/alex/run/Alex-—-Course40.png")
    alex_run_ne = to_base64("characters/alex/run/Alex-—-Course10.png")
    alex_run_nw = to_base64("characters/alex/run/Alex-—-Course26.png")

    alex_interact_se = to_base64("characters/alex/interaction/Alex-—-Interaction01.png")
    alex_interact_sw = to_base64("characters/alex/interaction/Alex-—-Interaction14.png")
    alex_interact_ne = to_base64("characters/alex/interaction/Alex-—-Interaction28.png")
    alex_interact_nw = to_base64("characters/alex/interaction/Alex-—-Interaction64.png")
    
    # 2. Buildings & Environment
    family_house = to_base64("environments/family_house/exterior/Maison-familiale-extérieure01.png")
    church = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet05.png")
    cottage_01 = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet01.png")
    cottage_02 = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet02.png")
    iron_gate = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet15.png")
    stone_slab = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet25.png")
    snow_slab = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet31.png")
    ice_slab = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet32.png")
    well = to_base64("environments/village/decor/Village-abandonné-—-Route-&-décor-extérieur01.png")
    pine_tree = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet37.png")
    dead_tree = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet34.png")
    lamp_post = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet20.png")
    cliff = to_base64("environments/village/decor/Village-abandonné-—-Route-&-décor-extérieur52.png")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>L'Écho des Ombres — Phase 3.1 Village Continu & 360° Alex</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; user-select: none; -webkit-tap-highlight-color: transparent; }}
    html, body {{ width: 100%; height: 100%; overflow: hidden; background: #121B28; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #E2E8F0; }}
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
      background: rgba(15, 23, 42, 0.88);
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
      0%, 100% {{ border-color: rgba(56, 189, 248, 0.4); }}
      50% {{ border-color: rgba(56, 189, 248, 0.9); }}
    }}

    /* Debug Panel */
    #debug-panel {{
      position: absolute; top: 12px; left: 12px;
      background: rgba(15, 23, 42, 0.92);
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
        <span class="location-name" id="loc-title">L'ÉCHO DES OMBRES</span>
      </div>
      <div class="interaction-prompt" id="prompt-badge" style="display: none;">
        <span>🔍</span>
        <span id="prompt-text">Inspect</span>
      </div>
    </div>

    <!-- Debug HUD -->
    <div id="debug-panel">
      <div style="color: #EAB308; font-weight: bold; margin-bottom: 4px;">=== DIAGNOSTICS & SYSTEM ===</div>
      <div id="dbg-fps">FPS: 60</div>
      <div id="dbg-pos">Alex: [0.0, 0.0]</div>
      <div id="dbg-state">State: IDLE (SE)</div>
      <div id="dbg-poi">POI: NONE</div>
      <div id="dbg-cam">Cam: [0, 0] | Zoom: 1.15</div>
      <div id="dbg-bounds">Bounds: Continuous World (Zero Void)</div>
    </div>

    <!-- Debug Tools -->
    <div id="debug-tools">
      <button class="btn-dev" onclick="zoomCam(0.15)">🔍 +</button>
      <button class="btn-dev" onclick="zoomCam(-0.15)">🔍 -</button>
      <button class="btn-dev" style="background: #2563EB;" onclick="saveGame()">💾 SAVE</button>
      <button class="btn-dev" style="background: #10B981;" onclick="loadGame()">📂 LOAD</button>
    </div>

    <div id="debug-toggle" onclick="toggleDebug()">⚙️</div>

    <div id="touch-controls">
      <div id="touch-stick"></div>
    </div>

    <div id="action-controls">
      <div class="rotation-row">
        <button class="btn-rotate" title="Turn Left (Q)" onclick="rotateAlexCCW()">↺</button>
        <div class="orient-badge" id="hud-orient">SE</div>
        <button class="btn-rotate" title="Turn Right (E)" onclick="rotateAlexCW()">↻</button>
      </div>
      <button id="sprint-btn" onclick="toggleSprint()">
        <span>⚡</span> SPRINT
      </button>
    </div>

    <div id="notification"></div>
  </div>

  <script>
    // 1. Isometric Engine Constants
    const TILE_W = 128;
    const TILE_H = 64;
    const HALF_W = 64;
    const HALF_H = 32;

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
      familyHouse: new Image(),
      church: new Image(),
      cottage01: new Image(),
      cottage02: new Image(),
      ironGate: new Image(),
      slab: new Image(),
      snowSlab: new Image(),
      iceSlab: new Image(),
      well: new Image(),
      pineTree: new Image(),
      deadTree: new Image(),
      lampPost: new Image(),
      cliff: new Image()
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

    images.familyHouse.src = "{family_house}";
    images.church.src = "{church}";
    images.cottage01.src = "{cottage_01}";
    images.cottage02.src = "{cottage_02}";
    images.ironGate.src = "{iron_gate}";
    images.slab.src = "{stone_slab}";
    images.snowSlab.src = "{snow_slab}";
    images.iceSlab.src = "{ice_slab}";
    images.well.src = "{well}";
    images.pineTree.src = "{pine_tree}";
    images.deadTree.src = "{dead_tree}";
    images.lampPost.src = "{lamp_post}";
    images.cliff.src = "{cliff}";

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

    // 4. Player State (Calibrated Human Scale 28x56)
    const alex = {{
      wx: 0.0,
      wy: 0.0,
      w: 28,
      h: 56,
      radius: 0.28,
      orientation: 'SE',
      state: 'IDLE',
      isSprinting: false,
      frameTimer: 0
    }};

    // Canonical 360° cycle (Clockwise: SE -> SW -> NW -> NE -> SE)
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

    // 5. Canonical Points of Interest (POIs)
    const pois = [
      {{ id: 'VILLAGE_ENTRANCE', name: 'Village Entrance (Bridge)', wx: 0.0, wy: 0.0, r: 1.8, prompt: '[E] Inspect snowy bridge' }},
      {{ id: 'VILLAGE_SQUARE', name: 'Central Square', wx: 0.0, wy: 5.5, r: 2.2, prompt: '[E] Examine central plaza' }},
      {{ id: 'OLD_WELL', name: 'Ancient Stone Well', wx: 0.0, wy: 6.0, r: 1.5, prompt: '[E] Look into the frozen well' }},
      {{ id: 'ABANDONED_CHURCH', name: 'St. Jude Abandoned Church', wx: 6.5, wy: 5.0, r: 2.4, prompt: '[E] Examine church doors' }},
      {{ id: 'FAMILY_HOUSE', name: 'Alex Family House', wx: 0.0, wy: 10.5, r: 2.0, prompt: '[E] Enter family house' }},
      {{ id: 'ABANDONED_HOUSE_01', name: 'Dilapidated Cottage', wx: -5.5, wy: 4.5, r: 1.8, prompt: '[E] Inspect wooden porch' }},
      {{ id: 'ABANDONED_HOUSE_02', name: 'Forester Shack', wx: -5.5, wy: 8.5, r: 1.8, prompt: '[E] Examine shuttered window' }}
    ];

    // 6. Collision Obstacles
    const obstacles = [
      {{ id: 'well', wx: 0.0, wy: 6.0, hw: 0.7, hh: 0.7 }},
      {{ id: 'church', wx: 6.5, wy: 5.0, hw: 1.5, hh: 1.5 }},
      {{ id: 'cottage01', wx: -5.5, wy: 4.5, hw: 1.3, hh: 1.2 }},
      {{ id: 'cottage02', wx: -5.5, wy: 8.5, hw: 1.2, hh: 1.3 }},
      {{ id: 'house', wx: 0.0, wy: 10.8, hw: 1.6, hh: 1.4 }},
      {{ id: 'gate', wx: 4.2, wy: 5.0, hw: 0.3, hh: 0.8 }},
      {{ id: 'lamp1', wx: 1.2, wy: 2.5, hw: 0.25, hh: 0.25 }},
      {{ id: 'lamp2', wx: -1.2, wy: 5.5, hw: 0.25, hh: 0.25 }},
      {{ id: 'lamp3', wx: -1.2, wy: 8.5, hw: 0.25, hh: 0.25 }},
      {{ id: 'cliff1', wx: -3.5, wy: 12.5, hw: 1.2, hh: 1.2 }},
      {{ id: 'cliff2', wx: 4.0, wy: 12.0, hw: 1.2, hh: 1.2 }}
    ];

    function checkCollision(x, y, radius) {{
      for (const obs of obstacles) {{
        const cx = Math.max(obs.wx - obs.hw, Math.min(x, obs.wx + obs.hw));
        const cy = Math.max(obs.wy - obs.hh, Math.min(y, obs.wy + obs.hh));
        const dx = x - cx;
        const dy = y - cy;
        if (dx * dx + dy * dy < radius * radius) return true;
      }}
      return false;
    }}

    function resolveMovement(curX, curY, targetX, targetY, radius) {{
      if (!checkCollision(targetX, targetY, radius)) return {{ x: targetX, y: targetY }};
      if (!checkCollision(targetX, curY, radius)) return {{ x: targetX, y: curY }};
      if (!checkCollision(curX, targetY, radius)) return {{ x: curX, y: targetY }};
      return {{ x: curX, y: curY }};
    }}

    // 7. Camera Clamping (Calibrated to village geometry)
    const camera = {{
      x: 0,
      y: 0,
      minX: -1600,
      maxX: 1600,
      minY: -850,
      maxY: 1150,
      zoom: 1.15
    }};

    // 8. Input State
    const keys = {{}};
    let inputX = 0;
    let inputY = 0;
    let isDebug = false;

    window.addEventListener('keydown', (e) => {{
      const k = e.key.toLowerCase();
      keys[k] = true;
      if (k === 'q') rotateAlexCCW();
      if (k === 'e') rotateAlexCW();
    }});
    window.addEventListener('keyup', (e) => {{ keys[e.key.toLowerCase()] = false; }});

    // Touch Joystick Handling (With Turn-on-the-spot deadzone)
    const joystick = document.getElementById('touch-controls');
    const stick = document.getElementById('touch-stick');
    let touchId = null;

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
          stick.style.transform = 'translate(0px, 0px)';
          break;
        }}
      }}
    }}
    joystick.addEventListener('touchend', endJoystick);
    joystick.addEventListener('touchcancel', endJoystick);

    function updateJoystick(t) {{
      const rect = joystick.getBoundingClientRect();
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
      let dx = t.clientX - cx;
      let dy = t.clientY - cy;
      const dist = Math.hypot(dx, dy);
      const maxDist = rect.width / 2;

      if (dist > maxDist) {{
        dx = (dx / dist) * maxDist;
        dy = (dy / dist) * maxDist;
      }}
      stick.style.transform = `translate(${{dx}}px, ${{dy}}px)`;
      inputX = dx / maxDist;
      inputY = dy / maxDist;
    }}

    // 9. Winter Weather Particles
    const snowflakes = [];
    for (let i = 0; i < 90; i++) {{
      snowflakes.push({{
        x: (Math.random() - 0.5) * 1600,
        y: -400 + Math.random() * 1000,
        vy: 40 + Math.random() * 50,
        vx: -15 - Math.random() * 20,
        r: 1.0 + Math.random() * 1.8,
        alpha: 0.3 + Math.random() * 0.5
      }});
    }}

    // 10. Game Loop
    let lastTime = performance.now();

    function gameLoop(now) {{
      const dt = Math.min((now - lastTime) / 1000, 0.1);
      lastTime = now;

      // Movement Input
      let moveX = inputX;
      let moveY = inputY;

      if (keys['w'] || keys['arrowup']) moveY -= 1;
      if (keys['s'] || keys['arrowdown']) moveY += 1;
      if (keys['a'] || keys['arrowleft']) moveX -= 1;
      if (keys['d'] || keys['arrowright']) moveX += 1;

      const len = Math.hypot(moveX, moveY);
      
      // Threshold 1: Below 0.10 -> Deadzone / Idle
      if (len < 0.10) {{
        alex.state = 'IDLE';
      }} else {{
        const normX = moveX / len;
        const normY = moveY / len;

        // 4-Way Isometric Orientation from 360° input angle
        const angle = Math.atan2(normY, normX);
        if (angle >= 0 && angle < Math.PI / 2) alex.orientation = 'SE';
        else if (angle >= Math.PI / 2 && angle <= Math.PI) alex.orientation = 'SW';
        else if (angle >= -Math.PI && angle < -Math.PI / 2) alex.orientation = 'NW';
        else alex.orientation = 'NE';
        document.getElementById('hud-orient').textContent = alex.orientation;

        // Threshold 2: Between 0.10 and 0.30 -> Rotate on the spot (NO displacement)
        if (len < 0.30) {{
          alex.state = 'IDLE';
          // World X, Y remain strictly unchanged
        }} else {{
          // Threshold 3: Move (Walk or Run)
          const isRunning = alex.isSprinting || len > 0.72 || keys['shift'];
          alex.state = isRunning ? 'RUN' : 'WALK';
          const speed = isRunning ? 4.8 : 2.4;

          const worldDx = (normX + normY) * speed * dt * 0.707;
          const worldDy = (-normX + normY) * speed * dt * 0.707;

          const resolved = resolveMovement(alex.wx, alex.wy, alex.wx + worldDx, alex.wy + worldDy, alex.radius);
          alex.wx = resolved.x;
          alex.wy = resolved.y;
        }}
      }}

      // Camera Follow with dynamic viewport clamping preventing any void exposure
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
        if (f.y > 700) {{ f.y = -500; f.x = (Math.random() - 0.5) * 1600; }}
        if (f.x < -800) f.x = 800;
      }}

      // POI Check
      let activePOI = null;
      for (const poi of pois) {{
        const dx = alex.wx - poi.wx;
        const dy = alex.wy - poi.wy;
        if (dx * dx + dy * dy <= poi.r * poi.r) {{
          activePOI = poi;
          break;
        }}
      }}

      // Update HUD Elements
      const locTitle = document.getElementById('loc-title');
      const promptBadge = document.getElementById('prompt-badge');
      const promptText = document.getElementById('prompt-text');

      if (activePOI) {{
        locTitle.textContent = activePOI.name;
        promptBadge.style.display = 'inline-flex';
        promptText.textContent = activePOI.prompt;
      }} else {{
        locTitle.textContent = "L'ÉCHO DES OMBRES";
        promptBadge.style.display = 'none';
      }}

      if (isDebug) {{
        document.getElementById('dbg-pos').textContent = `Alex: [${{alex.wx.toFixed(2)}}, ${{alex.wy.toFixed(2)}}]`;
        document.getElementById('dbg-state').textContent = `State: ${{alex.state}} (${{alex.orientation}}) | Z: ${{calculateZ(alex.wx, alex.wy)}}`;
        document.getElementById('dbg-poi').textContent = `POI: ${{activePOI ? activePOI.id : 'NONE'}}`;
        document.getElementById('dbg-cam').textContent = `Cam: [${{camera.x.toFixed(0)}}, ${{camera.y.toFixed(0)}}] | Zoom: ${{camera.zoom.toFixed(2)}}`;
      }}

      render(now);
      requestAnimationFrame(gameLoop);
    }}

    function render(now) {{
      // Continuous background tone (deep winter night blue)
      ctx.fillStyle = '#121B28';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      ctx.save();
      ctx.translate(canvas.width / 2, canvas.height / 2);
      ctx.scale(camera.zoom * window.devicePixelRatio, camera.zoom * window.devicePixelRatio);
      ctx.translate(-camera.x, -camera.y);

      // 1. Multi-Zone Continuous Ground Layer (Expanded grid coverage without diamond cutoff)
      const gridR = 24;
      for (let x = -gridR; x <= gridR; x++) {{
        for (let y = -gridR; y <= gridR; y++) {{
          const pos = worldToScreen(x, y);

          // Zone selection
          let isRiver = y <= -2;
          let isPlaza = Math.hypot(x, y - 5.5) <= 2.8;
          let isMainRoad = Math.abs(x) <= 1 && y >= -1 && y <= 11;
          let isChurchPath = x >= 1 && x <= 7 && y >= 4 && y <= 6;
          let isCottagePath = x <= -1 && x >= -6 && y >= 4 && y <= 9;
          let isYard = (Math.abs(x) <= 3 && y >= 9 && y <= 12) || (x >= 4 && x <= 8 && y >= 3 && y <= 7);

          let tileImg = images.snowSlab;
          if (isRiver) {{
            tileImg = images.iceSlab || images.snowSlab;
          }} else if (isPlaza || isMainRoad || isChurchPath || isCottagePath) {{
            tileImg = images.slab;
          }} else if (isYard) {{
            tileImg = images.snowSlab;
          }} else {{
            tileImg = images.snowSlab;
          }}

          // Render with 1px overlap to eliminate subpixel cracks
          if (tileImg && tileImg.complete && tileImg.naturalWidth > 0) {{
            ctx.drawImage(tileImg, pos.x - HALF_W, pos.y - HALF_H, TILE_W + 1, TILE_H + 1);
          }} else {{
            ctx.beginPath();
            ctx.moveTo(pos.x, pos.y - HALF_H);
            ctx.lineTo(pos.x + HALF_W, pos.y);
            ctx.lineTo(pos.x, pos.y + HALF_H);
            ctx.lineTo(pos.x - HALF_W, pos.y);
            ctx.closePath();
            ctx.fillStyle = isRiver ? '#0F172A' : (isPlaza ? '#334155' : (isYard ? '#2A3441' : '#1A232E'));
            ctx.fill();
          }}
        }}
      }}

      // 2. Dynamic Z-Ordered Renderables (Hierarchical depth sorting)
      const renderables = [
        // Family House (North Destination)
        {{
          type: 'building', id: 'house', wx: 0.0, wy: 10.5,
          z: calculateZ(0.0, 10.5, 20000),
          img: images.familyHouse, w: 320, h: 298, pivotY: 0.88
        }},
        // St. Jude Church (East Hill)
        {{
          type: 'building', id: 'church', wx: 6.5, wy: 5.0,
          z: calculateZ(6.5, 5.0, 20000),
          img: images.church, w: 280, h: 370, pivotY: 0.90
        }},
        // Cottage 01 (West)
        {{
          type: 'building', id: 'cottage1', wx: -5.5, wy: 4.5,
          z: calculateZ(-5.5, 4.5, 20000),
          img: images.cottage01, w: 260, h: 244, pivotY: 0.88
        }},
        // Cottage 02 (West Shack)
        {{
          type: 'building', id: 'cottage2', wx: -5.5, wy: 8.5,
          z: calculateZ(-5.5, 8.5, 20000),
          img: images.cottage02, w: 240, h: 270, pivotY: 0.88
        }},
        // Cemetery Iron Gate
        {{
          type: 'prop', id: 'gate', wx: 4.2, wy: 5.0,
          z: calculateZ(4.2, 5.0, 30000),
          img: images.ironGate, w: 160, h: 100, pivotY: 0.90
        }},
        // Ancient Stone Well (Center Plaza)
        {{
          type: 'prop', id: 'well', wx: 0.0, wy: 6.0,
          z: calculateZ(0.0, 6.0, 30000),
          img: images.well, w: 100, h: 112, pivotY: 0.85
        }},
        // Victorian Street Lamps
        {{
          type: 'prop', id: 'lamp1', wx: 1.2, wy: 2.5,
          z: calculateZ(1.2, 2.5, 30000),
          img: images.lampPost, w: 38, h: 96, pivotY: 0.95
        }},
        {{
          type: 'prop', id: 'lamp2', wx: -1.2, wy: 5.5,
          z: calculateZ(-1.2, 5.5, 30000),
          img: images.lampPost, w: 38, h: 96, pivotY: 0.95
        }},
        {{
          type: 'prop', id: 'lamp3', wx: -1.2, wy: 8.5,
          z: calculateZ(-1.2, 8.5, 30000),
          img: images.lampPost, w: 38, h: 96, pivotY: 0.95
        }},
        // Pine Trees & Border Vegetation
        {{
          type: 'prop', id: 'pine1', wx: 8.5, wy: 3.5,
          z: calculateZ(8.5, 3.5, 30000),
          img: images.pineTree, w: 90, h: 86, pivotY: 0.90
        }},
        {{
          type: 'prop', id: 'pine2', wx: 5.5, wy: 3.0,
          z: calculateZ(5.5, 3.0, 30000),
          img: images.pineTree, w: 85, h: 80, pivotY: 0.90
        }},
        {{
          type: 'prop', id: 'pine3', wx: -7.0, wy: 3.0,
          z: calculateZ(-7.0, 3.0, 30000),
          img: images.pineTree, w: 95, h: 90, pivotY: 0.90
        }},
        {{
          type: 'prop', id: 'dead1', wx: 7.2, wy: 6.8,
          z: calculateZ(7.2, 6.8, 30000),
          img: images.deadTree, w: 80, h: 132, pivotY: 0.90
        }},
        {{
          type: 'prop', id: 'dead2', wx: 2.2, wy: 10.0,
          z: calculateZ(2.2, 10.0, 30000),
          img: images.deadTree, w: 80, h: 132, pivotY: 0.90
        }},
        // Perimeter Cliffs
        {{
          type: 'prop', id: 'cliff1', wx: -3.5, wy: 12.5,
          z: calculateZ(-3.5, 12.5, 20000),
          img: images.cliff, w: 220, h: 260, pivotY: 0.90
        }},
        {{
          type: 'prop', id: 'cliff2', wx: 4.0, wy: 12.0,
          z: calculateZ(4.0, 12.0, 20000),
          img: images.cliff, w: 220, h: 260, pivotY: 0.90
        }},
        // Alex Character (Ground contact Z-order)
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

          let charImg = images.idleSE;
          if (alex.state === 'IDLE') {{
            if (alex.orientation === 'SW') charImg = images.idleSW;
            else if (alex.orientation === 'NE') charImg = images.idleNE;
            else if (alex.orientation === 'NW') charImg = images.idleNW;
            else charImg = images.idleSE;
          }} else if (alex.state === 'WALK') {{
            if (alex.orientation === 'SW') charImg = images.walkSW;
            else if (alex.orientation === 'NE') charImg = images.walkNE;
            else if (alex.orientation === 'NW') charImg = images.walkNW;
            else charImg = images.walkSE;
          }} else if (alex.state === 'RUN') {{
            if (alex.orientation === 'SW') charImg = images.runSW;
            else if (alex.orientation === 'NE') charImg = images.runNE;
            else if (alex.orientation === 'NW') charImg = images.runNW;
            else charImg = images.runSE;
          }}

          if (charImg && charImg.complete && charImg.naturalWidth > 0) {{
            ctx.drawImage(charImg, dx, dy, alex.w, alex.h);
          }} else {{
            // Fallback silhouette
            ctx.fillStyle = '#38BDF8';
            ctx.fillRect(dx, dy, alex.w, alex.h);
          }}

          if (isDebug) {{
            // Debug Hitbox
            ctx.strokeStyle = '#38BDF8';
            ctx.lineWidth = 1.5;
            ctx.strokeRect(dx, dy, alex.w, alex.h);
          }}
        }} else if (r.img && r.img.complete && r.img.naturalWidth > 0) {{
          const dx = pt.x - r.w / 2;
          const dy = pt.y - r.h * r.pivotY;
          ctx.drawImage(r.img, dx, dy, r.w, r.h);

          if (isDebug) {{
            ctx.strokeStyle = r.type === 'building' ? 'rgba(239, 68, 68, 0.7)' : 'rgba(234, 179, 8, 0.7)';
            ctx.lineWidth = 1;
            ctx.strokeRect(dx, dy, r.w, r.h);
          }}
        }}
      }}

      // 3. Falling Snowflakes
      for (const f of snowflakes) {{
        ctx.beginPath();
        ctx.arc(f.x, f.y, f.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(241, 245, 249, ${{f.alpha}})`;
        ctx.fill();
      }}

      ctx.restore();
    }}

    // 11. Responsive Canvas Resize
    function resize() {{
      canvas.width = window.innerWidth * window.devicePixelRatio;
      canvas.height = window.innerHeight * window.devicePixelRatio;
    }}
    window.addEventListener('resize', resize);
    resize();

    // 12. Dev & Debug Actions
    function toggleDebug() {{
      isDebug = !isDebug;
      document.getElementById('debug-toggle').classList.toggle('active', isDebug);
      document.getElementById('debug-panel').style.display = isDebug ? 'block' : 'none';
      document.getElementById('debug-tools').style.display = isDebug ? 'flex' : 'none';
    }}

    function zoomCam(delta) {{
      camera.zoom = Math.max(0.85, Math.min(camera.zoom + delta, 1.6));
    }}

    function toggleSprint() {{
      alex.isSprinting = !alex.isSprinting;
      document.getElementById('sprint-btn').classList.toggle('active', alex.isSprinting);
    }}

    function showToast(msg) {{
      const t = document.getElementById('notification');
      t.textContent = msg;
      t.style.display = 'block';
      setTimeout(() => {{ t.style.display = 'none'; }}, 3000);
    }}

    function saveGame() {{
      const saveObj = {{
        save_id: 'slot_01_village',
        chapter: 1,
        map: 'VILLAGE_ABANDONED',
        alex: {{ wx: alex.wx, wy: alex.wy, orient: alex.orientation }},
        timestamp: Date.now()
      }};
      localStorage.setItem('echo_save_slot', JSON.stringify(saveObj));
      showToast('Game saved locally (100% Offline)');
    }}

    function loadGame() {{
      const raw = localStorage.getItem('echo_save_slot');
      if (raw) {{
        const saveObj = JSON.parse(raw);
        alex.wx = saveObj.alex.wx;
        alex.wy = saveObj.alex.wy;
        alex.orientation = saveObj.alex.orient;
        document.getElementById('hud-orient').textContent = alex.orientation;
        showToast('Game state restored');
      }} else {{
        showToast('No local save found');
      }}
    }}

    // Start engine loop
    requestAnimationFrame(gameLoop);
  </script>
</body>
</html>
"""

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"=== Successfully updated Phase 3.1 {OUT_FILE} ===")

if __name__ == "__main__":
    build()
