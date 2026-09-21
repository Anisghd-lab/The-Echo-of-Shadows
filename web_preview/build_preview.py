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
    print("Embedding Phase 3 Village World assets for standalone web preview...")
    
    # 1. Alex Sprites
    alex_idle_se = to_base64("characters/alex/idle/Alex-—-Animation-Idle03.png")
    alex_idle_sw = to_base64("characters/alex/idle/Alex-—-Animation-Idle04.png")
    alex_idle_ne = to_base64("characters/alex/idle/Alex-—-Animation-Idle06.png")
    alex_idle_nw = to_base64("characters/alex/idle/Alex-—-Animation-Idle07.png")
    alex_walk = to_base64("characters/alex/walk/Alex-—-Marche01.png")
    
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
  <title>L'Écho des Ombres — Phase 3 Village Jouable</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; user-select: none; -webkit-tap-highlight-color: transparent; }}
    html, body {{ width: 100%; height: 100%; overflow: hidden; background: #070B12; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #E2E8F0; }}
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
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(148, 163, 184, 0.3);
      border-radius: 20px;
      padding: 8px 16px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.6);
    }}
    .status-dot {{ width: 8px; height: 8px; border-radius: 50%; background: #38BDF8; box-shadow: 0 0 8px #38BDF8; }}
    .location-name {{ font-size: 13px; font-weight: 600; color: #F8FAFC; letter-spacing: 0.6px; }}
    .interaction-prompt {{
      display: inline-flex; align-items: center; gap: 6px;
      background: rgba(30, 41, 59, 0.9);
      border: 1px solid rgba(56, 189, 248, 0.4);
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
      color: #94A3B8; display: flex; align-items: center; justify-content: center;
      cursor: pointer; font-size: 16px;
    }}
    #debug-toggle.active {{ background: #EAB308; color: #000; border-color: #CA8A04; }}

    .btn-dev {{
      background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(148, 163, 184, 0.4);
      color: #FFF; padding: 6px 10px; border-radius: 6px; font-size: 11px; font-weight: 600;
      cursor: pointer;
    }}
    .btn-dev:active {{ transform: scale(0.96); }}

    /* Touch Controls */
    #joystick-zone {{
      position: absolute; bottom: 24px; left: 24px;
      width: 110px; height: 110px; border-radius: 50%;
      background: rgba(15, 23, 42, 0.4);
      border: 2px solid rgba(148, 163, 184, 0.3);
      touch-action: none; display: flex; align-items: center; justify-content: center;
    }}
    #joystick-knob {{
      width: 44px; height: 44px; border-radius: 50%;
      background: radial-gradient(circle, #64748B, #334155);
      border: 2px solid #E2E8F0;
      box-shadow: 0 3px 8px rgba(0,0,0,0.6);
      pointer-events: none; transform: translate(0px, 0px);
    }}
    #sprint-btn {{
      position: absolute; bottom: 28px; right: 24px;
      background: rgba(30, 41, 59, 0.65);
      border: 1px solid rgba(148, 163, 184, 0.3);
      color: #FFF; padding: 10px 16px; border-radius: 20px;
      font-size: 12px; font-weight: 700; cursor: pointer;
    }}
    #sprint-btn.active {{ background: rgba(220, 38, 38, 0.85); border-color: #EF4444; }}

    /* Notification banner */
    #notification {{
      position: absolute; bottom: 85px; left: 50%; transform: translateX(-50%);
      background: rgba(15, 23, 42, 0.95); border: 1px solid #10B981;
      color: #10B981; padding: 8px 18px; border-radius: 20px;
      font-size: 12px; font-weight: 600; display: none;
    }}
  </style>
</head>
<body>
  <div id="canvas-container">
    <canvas id="gameCanvas"></canvas>
    
    <!-- Cinematic Release HUD (Default) -->
    <div id="release-hud">
      <div class="location-badge">
        <div class="status-dot"></div>
        <div class="location-name" id="loc-title">L'ÉCHO DES OMBRES</div>
      </div>
      <div class="interaction-prompt" id="prompt-badge" style="display: none;">
        <span>🔍</span> <span id="prompt-text">Inspect</span>
      </div>
    </div>

    <!-- Diagnostic Debug Panel (Toggleable) -->
    <div id="debug-panel">
      <div style="color: #EAB308; font-weight: bold; margin-bottom: 4px;">DEBUG MODE [ACTIVE]</div>
      <div id="dbg-pos">Alex: [0.0, 0.0]</div>
      <div id="dbg-state">State: IDLE (SE) | Z: 40000</div>
      <div id="dbg-poi">POI: NONE</div>
    </div>
    
    <!-- Debug Tools -->
    <div id="debug-tools">
      <button class="btn-dev" onclick="zoomIn()">Zoom +</button>
      <button class="btn-dev" onclick="zoomOut()">Zoom -</button>
      <button class="btn-dev" style="background: #2563EB;" onclick="saveGame()">💾 SAVE</button>
      <button class="btn-dev" onclick="loadGame()">↺ LOAD</button>
    </div>

    <!-- Debug Toggle Button -->
    <div id="debug-toggle" onclick="toggleDebug()">⚙</div>
    
    <!-- Mobile Joystick & Controls -->
    <div id="joystick-zone">
      <div id="joystick-knob"></div>
    </div>
    <div id="sprint-btn" onclick="toggleSprint()">SPRINT</div>

    <!-- Feedback Banner -->
    <div id="notification"></div>
  </div>

  <script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');

    function resize() {{
      canvas.width = window.innerWidth * window.devicePixelRatio;
      canvas.height = window.innerHeight * window.devicePixelRatio;
      ctx.imageSmoothingEnabled = true;
    }}
    window.addEventListener('resize', resize);
    resize();

    // 1. Centralized Isometric Constants (128x64)
    const TILE_W = 128;
    const TILE_H = 64;
    const HALF_W = 64;
    const HALF_H = 32;

    function worldToScreen(wx, wy) {{
      return {{
        x: (wx - wy) * HALF_W,
        y: (wx + wy) * HALF_H
      }};
    }}

    function calculateZ(wx, wy, base = 40000) {{
      return base + Math.round((wx + wy) * 100);
    }}

    // 2. Asset Loader
    const images = {{}};
    function loadImg(key, src) {{
      const img = new Image();
      img.src = src;
      images[key] = img;
    }}

    loadImg('idleSE', '{alex_idle_se}');
    loadImg('idleSW', '{alex_idle_sw}');
    loadImg('idleNE', '{alex_idle_ne}');
    loadImg('idleNW', '{alex_idle_nw}');
    loadImg('walkStrip', '{alex_walk}');
    loadImg('familyHouse', '{family_house}');
    loadImg('church', '{church}');
    loadImg('cottage01', '{cottage_01}');
    loadImg('cottage02', '{cottage_02}');
    loadImg('gate', '{iron_gate}');
    loadImg('slab', '{stone_slab}');
    loadImg('snowSlab', '{snow_slab}');
    loadImg('iceSlab', '{ice_slab}');
    loadImg('well', '{well}');
    loadImg('pineTree', '{pine_tree}');
    loadImg('deadTree', '{dead_tree}');
    loadImg('lampPost', '{lamp_post}');
    loadImg('cliff', '{cliff}');

    // 3. Points of Interest (POIs)
    const pois = [
      {{ id: 'VILLAGE_ENTRANCE', name: 'Village Entrance (Bridge)', wx: 0.0, wy: 0.0, r: 1.8, prompt: 'Inspect the snowy bridge' }},
      {{ id: 'VILLAGE_SQUARE', name: 'Central Square', wx: 0.0, wy: 5.5, r: 2.2, prompt: 'Examine central square' }},
      {{ id: 'OLD_WELL', name: 'Ancient Stone Well', wx: 0.0, wy: 6.0, r: 1.5, prompt: 'Look into the frozen well' }},
      {{ id: 'ABANDONED_CHURCH', name: 'St. Jude Church', wx: 6.5, wy: 5.0, r: 2.4, prompt: 'Examine gothic church entrance' }},
      {{ id: 'FAMILY_HOUSE', name: 'Alex Family House', wx: 0.0, wy: 10.5, r: 2.0, prompt: 'Approach family house door' }},
      {{ id: 'ABANDONED_HOUSE_01', name: 'Dilapidated Cottage', wx: -5.5, wy: 4.5, r: 1.8, prompt: 'Inspect wooden porch' }},
      {{ id: 'ABANDONED_HOUSE_02', name: 'Forester Shack', wx: -5.5, wy: 8.5, r: 1.8, prompt: 'Examine shuttered window' }},
    ];

    // 4. Collision Manager
    const obstacles = [
      // Family House Foundation
      {{ id: 'house', wx: 0.0, wy: 10.5, hw: 0.9, hh: 0.6 }},
      // Church Foundation
      {{ id: 'church', wx: 6.5, wy: 5.0, hw: 1.0, hh: 0.8 }},
      // Cottages
      {{ id: 'cottage01', wx: -5.5, wy: 4.5, hw: 0.8, hh: 0.6 }},
      {{ id: 'cottage02', wx: -5.5, wy: 8.5, hw: 0.75, hh: 0.6 }},
      // Well
      {{ id: 'well', wx: 0.0, wy: 6.0, hw: 0.4, hh: 0.4 }},
      // Gates
      {{ id: 'gate_church', wx: 4.2, wy: 5.0, hw: 0.4, hh: 0.2 }},
      {{ id: 'gate_cottage', wx: -3.6, wy: 4.5, hw: 0.4, hh: 0.2 }},
      // Street Lamps
      {{ id: 'lamp1', wx: -1.2, wy: 1.5, hw: 0.15, hh: 0.15 }},
      {{ id: 'lamp2', wx: 1.2, wy: 4.0, hw: 0.15, hh: 0.15 }},
      {{ id: 'lamp3', wx: -1.2, wy: 8.5, hw: 0.15, hh: 0.15 }},
      // Perimeter Cliffs
      {{ id: 'cliff1', wx: -3.5, wy: 12.5, hw: 0.9, hh: 0.5 }},
      {{ id: 'cliff2', wx: 4.0, wy: 12.0, hw: 0.9, hh: 0.5 }},
    ];

    function checkCollision(x, y, r = 0.2) {{
      for (const o of obstacles) {{
        const cx = Math.max(o.wx - o.hw, Math.min(x, o.wx + o.hw));
        const cy = Math.max(o.wy - o.hh, Math.min(y, o.wy + o.hh));
        const dx = x - cx;
        const dy = y - cy;
        if (dx * dx + dy * dy < r * r) return true;
      }}
      // Strict playable boundaries (prevent camera from showing void)
      if (x < -8.5 || x > 9.5 || y < -2.0 || y > 13.0) return true;
      return false;
    }}

    function resolveMovement(cx, cy, tx, ty, r = 0.2) {{
      if (!checkCollision(tx, ty, r)) return {{ x: tx, y: ty }};
      if (!checkCollision(tx, cy, r)) return {{ x: tx, y: cy }};
      if (!checkCollision(cx, ty, r)) return {{ x: cx, y: ty }};
      return {{ x: cx, y: cy }};
    }}

    // 5. Alex Player State (Calibrated Scale 28x56)
    const alex = {{
      wx: 0.0,
      wy: 0.0,
      orientation: 'SE',
      state: 'IDLE',
      walkFrame: 0,
      frameTimer: 0,
      radius: 0.2,
      isSprinting: false,
      w: 28,
      h: 56
    }};

    // 6. Camera Controller with Bounds Clamping
    const camera = {{
      x: 0,
      y: 0,
      zoom: 1.2,
      minX: -850,
      maxX: 750,
      minY: -380,
      maxY: 780
    }};

    function zoomIn() {{ camera.zoom = Math.min(camera.zoom + 0.15, 1.6); }}
    function zoomOut() {{ camera.zoom = Math.max(camera.zoom - 0.15, 0.85); }}

    // 7. Input Management
    let inputX = 0;
    let inputY = 0;
    const keys = {{}};

    window.addEventListener('keydown', e => {{
      keys[e.key.toLowerCase()] = true;
      if (e.key === 'Shift') alex.isSprinting = true;
      if (e.key.toLowerCase() === 'd' && !e.repeat && (keys['control'] || keys['alt'])) toggleDebug();
    }});
    window.addEventListener('keyup', e => {{
      keys[e.key.toLowerCase()] = false;
      if (e.key === 'Shift') alex.isSprinting = false;
    }});

    function toggleSprint() {{
      alex.isSprinting = !alex.isSprinting;
      const btn = document.getElementById('sprint-btn');
      if (alex.isSprinting) {{
        btn.classList.add('active');
        btn.textContent = 'RUNNING';
      }} else {{
        btn.classList.remove('active');
        btn.textContent = 'SPRINT';
      }}
    }}

    let isDebug = false;
    function toggleDebug() {{
      isDebug = !isDebug;
      document.getElementById('debug-toggle').classList.toggle('active', isDebug);
      document.getElementById('debug-panel').style.display = isDebug ? 'block' : 'none';
      document.getElementById('debug-tools').style.display = isDebug ? 'flex' : 'none';
    }}

    // Joystick Touch
    const jZone = document.getElementById('joystick-zone');
    const jKnob = document.getElementById('joystick-knob');
    let jActive = false;

    function handleJoystick(touch) {{
      const rect = jZone.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;
      const dx = touch.clientX - centerX;
      const dy = touch.clientY - centerY;
      const dist = Math.hypot(dx, dy);
      const maxR = rect.width / 2;

      let clampedX = dx;
      let clampedY = dy;
      if (dist > maxR) {{
        clampedX = (dx / dist) * maxR;
        clampedY = (dy / dist) * maxR;
      }}
      jKnob.style.transform = `translate(${{clampedX}}px, ${{clampedY}}px)`;
      inputX = clampedX / maxR;
      inputY = clampedY / maxR;
    }}

    function resetJoystick() {{
      jActive = false;
      jKnob.style.transform = 'translate(0px, 0px)';
      inputX = 0;
      inputY = 0;
    }}

    jZone.addEventListener('touchstart', e => {{ jActive = true; handleJoystick(e.touches[0]); }});
    jZone.addEventListener('touchmove', e => {{ if (jActive) handleJoystick(e.touches[0]); }});
    jZone.addEventListener('touchend', resetJoystick);
    jZone.addEventListener('touchcancel', resetJoystick);

    // 8. Save & Load System (100% Local Storage)
    function saveGame() {{
      const saveState = {{
        currentMap: 'VILLAGE_ABANDONED',
        position: {{ x: alex.wx, y: alex.wy, orientation: alex.orientation }},
        chapter: 'ACT_I_THE_RETURN',
        timestamp: new Date().toISOString()
      }};
      localStorage.setItem('echo_save_default', JSON.stringify(saveState));
      notify('✓ Position sauvegardée localement');
    }}

    function loadGame() {{
      const raw = localStorage.getItem('echo_save_default');
      if (raw) {{
        const state = JSON.parse(raw);
        alex.wx = state.position.x;
        alex.wy = state.position.y;
        alex.orientation = state.position.orientation || 'SE';
        notify('✓ Sauvegarde restaurée');
      }} else {{
        notify('Aucune sauvegarde');
      }}
    }}

    function notify(msg) {{
      const el = document.getElementById('notification');
      el.textContent = msg;
      el.style.display = 'block';
      setTimeout(() => {{ el.style.display = 'none'; }}, 3000);
    }}

    loadGame();

    // 9. Procedural Atmospheric Winter Weather (Snow, Fog, Sleet)
    const snowflakes = [];
    for (let i = 0; i < 95; i++) {{
      snowflakes.push({{
        x: (Math.random() - 0.5) * 1600,
        y: (Math.random() - 0.5) * 1200,
        vy: 30 + Math.random() * 35,
        vx: -18 - Math.random() * 18,
        r: 1.2 + Math.random() * 2.0,
        alpha: 0.3 + Math.random() * 0.45
      }});
    }}

    const fogBands = [];
    for (let i = 0; i < 4; i++) {{
      fogBands.push({{
        x: (Math.random() - 0.5) * 1200,
        y: -300 + i * 200,
        w: 550 + Math.random() * 250,
        h: 160 + Math.random() * 90,
        vx: -10 - Math.random() * 12,
        phase: Math.random() * Math.PI * 2
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
      if (len > 0.08) {{
        const normX = moveX / (len > 1 ? len : 1);
        const normY = moveY / (len > 1 ? len : 1);

        const isRunning = alex.isSprinting || len > 0.75;
        alex.state = isRunning ? 'RUN' : 'WALK';
        const speed = isRunning ? 4.6 : 2.3;

        // 4-Way Isometric Orientation
        const angle = Math.atan2(normY, normX);
        if (angle >= 0 && angle < Math.PI / 2) alex.orientation = 'SE';
        else if (angle >= Math.PI / 2 && angle <= Math.PI) alex.orientation = 'SW';
        else if (angle >= -Math.PI && angle < -Math.PI / 2) alex.orientation = 'NW';
        else alex.orientation = 'NE';

        // Displacement
        const worldDx = (normX + normY) * speed * dt * 0.707;
        const worldDy = (-normX + normY) * speed * dt * 0.707;

        const resolved = resolveMovement(alex.wx, alex.wy, alex.wx + worldDx, alex.wy + worldDy, alex.radius);
        alex.wx = resolved.x;
        alex.wy = resolved.y;

        alex.frameTimer += dt;
        if (alex.frameTimer > 0.14) {{
          alex.frameTimer = 0;
          alex.walkFrame = (alex.walkFrame + 1) % 4;
        }}
      }} else {{
        alex.state = 'IDLE';
        alex.walkFrame = 0;
      }}

      // Camera Smooth Follow + Strict Clamping
      const alexScreen = worldToScreen(alex.wx, alex.wy);
      const targetCamX = Math.max(camera.minX, Math.min(alexScreen.x, camera.maxX));
      const targetCamY = Math.max(camera.minY, Math.min(alexScreen.y, camera.maxY));
      camera.x += (targetCamX - camera.x) * Math.min(5.5 * dt, 1.0);
      camera.y += (targetCamY - camera.y) * Math.min(5.5 * dt, 1.0);

      // Weather update
      for (const f of snowflakes) {{
        f.y += f.vy * dt;
        f.x += f.vx * dt;
        if (f.y > 600) {{ f.y = -600; f.x = (Math.random() - 0.5) * 1600; }}
        if (f.x < -800) f.x = 800;
      }}
      for (const fog of fogBands) {{
        fog.x += fog.vx * dt;
        if (fog.x < -1000) fog.x = 1000;
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
      }}

      render(now);
      requestAnimationFrame(gameLoop);
    }}

    function render(now) {{
      ctx.fillStyle = '#070B12';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      ctx.save();
      ctx.translate(canvas.width / 2, canvas.height / 2);
      ctx.scale(camera.zoom * window.devicePixelRatio, camera.zoom * window.devicePixelRatio);
      ctx.translate(-camera.x, -camera.y);

      // 1. Multi-Zone Ground Layer (Zoning prevents tileset repetition)
      const gridR = 15;
      for (let x = -gridR; x <= gridR; x++) {{
        for (let y = -gridR; y <= gridR; y++) {{
          if (Math.abs(x) + Math.abs(y) > gridR + 4) continue;
          const pos = worldToScreen(x, y);

          // Zone selection
          let tileImg = images.snowSlab;
          let isPlaza = Math.hypot(x, y - 5.5) <= 2.8;
          let isMainRoad = Math.abs(x) <= 1 && y >= -1 && y <= 11;
          let isChurchPath = x >= 1 && x <= 7 && y >= 4 && y <= 6;
          let isCottagePath = x <= -1 && x >= -6 && y >= 4 && y <= 8;
          let isRiver = y <= -2;

          if (isRiver) {{
            tileImg = images.iceSlab || images.snowSlab;
          }} else if (isPlaza || isMainRoad || isChurchPath || isCottagePath) {{
            tileImg = images.slab;
          }} else {{
            tileImg = images.snowSlab || images.slab;
          }}

          if (tileImg && tileImg.complete && tileImg.naturalWidth > 0) {{
            ctx.drawImage(tileImg, pos.x - HALF_W, pos.y - HALF_H, TILE_W, TILE_H);
          }} else {{
            ctx.beginPath();
            ctx.moveTo(pos.x, pos.y - HALF_H);
            ctx.lineTo(pos.x + HALF_W, pos.y);
            ctx.lineTo(pos.x, pos.y + HALF_H);
            ctx.lineTo(pos.x - HALF_W, pos.y);
            ctx.closePath();
            ctx.fillStyle = isRiver ? '#0F172A' : (isPlaza ? '#334155' : '#1E293B');
            ctx.fill();
            ctx.strokeStyle = 'rgba(255,255,255,0.03)';
            ctx.stroke();
          }}
        }}
      }}

      // 2. Road Overlay (Smooth cobblestone connection)
      ctx.fillStyle = 'rgba(30, 41, 59, 0.45)';
      const roadNodes = [
        worldToScreen(0, -1), worldToScreen(0, 1), worldToScreen(0, 3),
        worldToScreen(0, 5), worldToScreen(0, 7), worldToScreen(0, 9),
        worldToScreen(2, 5), worldToScreen(4, 5), worldToScreen(-2, 5), worldToScreen(-4, 5)
      ];
      for (const pt of roadNodes) {{
        ctx.beginPath();
        ctx.ellipse(pt.x, pt.y, HALF_W * 1.4, HALF_H * 1.4, 0, 0, Math.PI * 2);
        ctx.fill();
      }}

      // 3. Dynamic Z-Ordered Renderables (Hierarchical depth sorting)
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
          type: 'building', id: 'cottage01', wx: -5.5, wy: 4.5,
          z: calculateZ(-5.5, 4.5, 20000),
          img: images.cottage01, w: 260, h: 244, pivotY: 0.88
        }},
        // Cottage 02 (West North)
        {{
          type: 'building', id: 'cottage02', wx: -5.5, wy: 8.5,
          z: calculateZ(-5.5, 8.5, 20000),
          img: images.cottage02, w: 240, h: 270, pivotY: 0.88
        }},
        // Ancient Stone Well (Square Center)
        {{
          type: 'prop', id: 'well', wx: 0.0, wy: 6.0,
          z: calculateZ(0.0, 6.0, 30000),
          img: images.well, w: 100, h: 112, pivotY: 0.85
        }},
        // Church Cemetery Gate
        {{
          type: 'prop', id: 'gate_church', wx: 4.2, wy: 5.0,
          z: calculateZ(4.2, 5.0, 30000),
          img: images.gate, w: 130, h: 84, pivotY: 0.85
        }},
        // West Cottage Gate
        {{
          type: 'prop', id: 'gate_cottage', wx: -3.6, wy: 4.5,
          z: calculateZ(-3.6, 4.5, 30000),
          img: images.gate, w: 130, h: 84, pivotY: 0.85
        }},
        // Street Lamps
        {{
          type: 'prop', id: 'lamp1', wx: -1.2, wy: 1.5,
          z: calculateZ(-1.2, 1.5, 30000),
          img: images.lampPost, w: 38, h: 96, pivotY: 0.95
        }},
        {{
          type: 'prop', id: 'lamp2', wx: 1.2, wy: 4.0,
          z: calculateZ(1.2, 4.0, 30000),
          img: images.lampPost, w: 38, h: 96, pivotY: 0.95
        }},
        {{
          type: 'prop', id: 'lamp3', wx: -1.2, wy: 8.5,
          z: calculateZ(-1.2, 8.5, 30000),
          img: images.lampPost, w: 38, h: 96, pivotY: 0.95
        }},
        // Pine Trees
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

          // Render Alex (Scale 28x56)
          const dx = pt.x - alex.w / 2;
          const dy = pt.y - alex.h;

          if (alex.state === 'IDLE') {{
            let img = images.idleSE;
            if (alex.orientation === 'SW') img = images.idleSW;
            else if (alex.orientation === 'NE') img = images.idleNE;
            else if (alex.orientation === 'NW') img = images.idleNW;

            if (img && img.complete) {{
              ctx.drawImage(img, dx, dy, alex.w, alex.h);
            }}
          }} else {{
            const strip = images.walkStrip;
            if (strip && strip.complete && strip.naturalWidth > 0) {{
              const frameW = strip.naturalWidth / 4;
              const frameH = strip.naturalHeight;
              const sx = alex.walkFrame * frameW;
              ctx.drawImage(strip, sx, 0, frameW, frameH, dx, dy, alex.w, alex.h);
            }} else {{
              ctx.drawImage(images.idleSE, dx, dy, alex.w, alex.h);
            }}
          }}
        }} else {{
          if (r.img && r.img.complete && r.img.naturalWidth > 0) {{
            const dx = pt.x - r.w / 2;
            const dy = pt.y - r.h * r.pivotY;
            ctx.drawImage(r.img, dx, dy, r.w, r.h);
          }}
        }}
      }}

      // 4. Procedural Atmospheric Fog & Snow
      for (const fog of fogBands) {{
        const alpha = 0.08 + 0.04 * Math.sin(now * 0.001 + fog.phase);
        ctx.fillStyle = `rgba(203, 213, 225, ${{alpha}})`;
        ctx.beginPath();
        ctx.ellipse(fog.x, fog.y, fog.w, fog.h, 0, 0, Math.PI * 2);
        ctx.fill();
      }}

      for (const f of snowflakes) {{
        ctx.fillStyle = `rgba(241, 245, 249, ${{f.alpha}})`;
        ctx.beginPath();
        ctx.arc(f.x, f.y, f.r, 0, Math.PI * 2);
        ctx.fill();
      }}

      ctx.restore();

      // 5. Cinematic Vignette (Cold Blue Thriller Rim)
      const grad = ctx.createRadialGradient(
        canvas.width / 2, canvas.height / 2, canvas.height * 0.4,
        canvas.width / 2, canvas.height / 2, canvas.width * 0.75
      );
      grad.addColorStop(0, 'rgba(7, 11, 18, 0)');
      grad.addColorStop(1, 'rgba(7, 11, 18, 0.75)');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
    }}

    requestAnimationFrame(gameLoop);
  </script>
</body>
</html>
"""

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"=== Successfully updated Phase 3 {OUT_FILE} ===")

if __name__ == "__main__":
    build()
