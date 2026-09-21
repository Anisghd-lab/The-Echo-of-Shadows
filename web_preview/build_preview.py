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
    print("Embedding real assets for standalone web preview...")
    
    # 1. Alex Sprites
    alex_idle_se = to_base64("characters/alex/idle/Alex-—-Animation-Idle03.png")
    alex_idle_sw = to_base64("characters/alex/idle/Alex-—-Animation-Idle04.png")
    alex_idle_ne = to_base64("characters/alex/idle/Alex-—-Animation-Idle06.png")
    alex_idle_nw = to_base64("characters/alex/idle/Alex-—-Animation-Idle07.png")
    alex_walk = to_base64("characters/alex/walk/Alex-—-Marche01.png")
    
    # 2. Buildings & Environment
    family_house = to_base64("environments/family_house/exterior/Maison-familiale-extérieure01.png")
    church = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet05.png")
    cottage = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet01.png")
    iron_gate = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet15.png")
    stone_slab = to_base64("environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet25.png")
    well = to_base64("environments/village/decor/Village-abandonné-—-Route-&-décor-extérieur01.png")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>L'Écho des Ombres — Phase 2 Flame World Preview</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; user-select: none; -webkit-tap-highlight-color: transparent; }}
    html, body {{ width: 100%; height: 100%; overflow: hidden; background: #070B12; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, monospace; color: #E2E8F0; }}
    #canvas-container {{ width: 100%; height: 100%; position: relative; }}
    canvas {{ display: block; width: 100%; height: 100%; }}
    
    /* Top HUD */
    #hud {{
      position: absolute; top: 12px; left: 12px;
      background: rgba(15, 23, 42, 0.88);
      border: 1px solid rgba(148, 163, 184, 0.25);
      border-radius: 10px;
      padding: 10px 14px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.5);
      font-size: 12px; line-height: 1.5; pointer-events: none;
    }}
    #hud-title {{ font-weight: 700; color: #F1F5F9; font-size: 13px; letter-spacing: 1px; }}
    #hud-alex {{ color: #38BDF8; font-family: monospace; }}
    #hud-status {{ color: #10B981; font-weight: 600; margin-top: 4px; }}
    
    /* Top Controls */
    #top-controls {{
      position: absolute; top: 12px; right: 12px;
      display: flex; gap: 8px; align-items: center;
    }}
    .btn {{
      background: #1E293B; border: 1px solid #475569; color: #F8FAFC;
      padding: 8px 14px; border-radius: 8px; font-size: 12px; font-weight: 600;
      cursor: pointer; display: flex; align-items: center; gap: 6px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.4);
    }}
    .btn:active {{ transform: scale(0.96); }}
    .btn-save {{ background: #2563EB; border-color: #3B82F6; }}
    .btn-load {{ background: #334155; border-color: #64748B; }}
    
    /* Mobile Touch Joystick */
    #joystick-zone {{
      position: absolute; bottom: 24px; left: 24px;
      width: 120px; height: 120px;
      border-radius: 50%;
      background: rgba(15, 23, 42, 0.45);
      border: 2px solid rgba(148, 163, 184, 0.4);
      touch-action: none;
      display: flex; align-items: center; justify-content: center;
    }}
    #joystick-knob {{
      width: 50px; height: 50px; border-radius: 50%;
      background: radial-gradient(circle, #64748B, #334155);
      border: 2px solid #E2E8F0;
      box-shadow: 0 3px 8px rgba(0,0,0,0.6);
      pointer-events: none;
      transform: translate(0px, 0px);
    }}

    /* Sprint Toggle */
    #sprint-btn {{
      position: absolute; bottom: 30px; right: 24px;
      background: rgba(30, 41, 59, 0.85);
      border: 1px solid rgba(148, 163, 184, 0.4);
      color: #FFF; padding: 12px 18px; border-radius: 24px;
      font-size: 13px; font-weight: 700; cursor: pointer;
      display: flex; align-items: center; gap: 6px;
    }}
    #sprint-btn.active {{ background: #DC2626; border-color: #EF4444; }}
  </style>
</head>
<body>
  <div id="canvas-container">
    <canvas id="gameCanvas"></canvas>
    
    <!-- HUD Panel -->
    <div id="hud">
      <div id="hud-title">L'ÉCHO DES OMBRES — VILLAGE WORLD</div>
      <div id="hud-alex">Alex: [0.0, 0.0] | IDLE (SE)</div>
      <div id="hud-depth">Z-Order: Dynamic Depth Sorting Active</div>
      <div id="hud-status"></div>
    </div>
    
    <!-- Top Action Buttons -->
    <div id="top-controls">
      <button class="btn" onclick="zoomIn()">Zoom +</button>
      <button class="btn" onclick="zoomOut()">Zoom -</button>
      <button class="btn btn-save" onclick="saveGame()">💾 SAVE</button>
      <button class="btn btn-load" onclick="loadGame()">↺ LOAD</button>
    </div>
    
    <!-- Touch Joystick -->
    <div id="joystick-zone">
      <div id="joystick-knob"></div>
    </div>

    <!-- Sprint Button -->
    <div id="sprint-btn" onclick="toggleSprint()">🏃 SPRINT: OFF</div>
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

    // 1. Centralized Isometric Coordinates (128x64)
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
    function loadImage(key, src) {{
      const img = new Image();
      img.src = src;
      images[key] = img;
    }}

    loadImage('idleSE', '{alex_idle_se}');
    loadImage('idleSW', '{alex_idle_sw}');
    loadImage('idleNE', '{alex_idle_ne}');
    loadImage('idleNW', '{alex_idle_nw}');
    loadImage('walkStrip', '{alex_walk}');
    loadImage('familyHouse', '{family_house}');
    loadImage('church', '{church}');
    loadImage('cottage', '{cottage}');
    loadImage('gate', '{iron_gate}');
    loadImage('slab', '{stone_slab}');
    loadImage('well', '{well}');

    // 3. Collision Manager
    const obstacles = [
      {{ id: 'house', wx: 0.0, wy: 8.0, hw: 0.6, hh: 0.6 }},
      {{ id: 'church', wx: 6.0, wy: 5.0, hw: 0.7, hh: 0.7 }},
      {{ id: 'cottage', wx: -5.0, wy: 5.0, hw: 0.6, hh: 0.6 }},
      {{ id: 'well', wx: 0.0, wy: 4.0, hw: 0.4, hh: 0.4 }},
      {{ id: 'gate_r', wx: 2.2, wy: 4.0, hw: 0.45, hh: 0.2 }},
      {{ id: 'gate_l', wx: -2.2, wy: 4.0, hw: 0.45, hh: 0.2 }},
    ];

    function checkCollision(x, y, r = 0.28) {{
      for (const o of obstacles) {{
        const cx = Math.max(o.wx - o.hw, Math.min(x, o.wx + o.hw));
        const cy = Math.max(o.wy - o.hh, Math.min(y, o.wy + o.hh));
        const dx = x - cx;
        const dy = y - cy;
        if (dx * dx + dy * dy < r * r) return true;
      }}
      // Map boundaries
      if (x < -11 || x > 11 || y < -11 || y > 11) return true;
      return false;
    }}

    function resolveMovement(cx, cy, tx, ty, r = 0.28) {{
      if (!checkCollision(tx, ty, r)) return {{ x: tx, y: ty }};
      if (!checkCollision(tx, cy, r)) return {{ x: tx, y: cy }};
      if (!checkCollision(cx, ty, r)) return {{ x: cx, y: ty }};
      return {{ x: cx, y: cy }};
    }}

    // 4. Alex Player State
    const alex = {{
      wx: 0.0,
      wy: 0.0,
      orientation: 'SE',
      state: 'IDLE',
      walkFrame: 0,
      frameTimer: 0,
      radius: 0.28,
      isSprinting: false
    }};

    // 5. Camera & Zoom
    const camera = {{
      x: 0,
      y: 0,
      zoom: 1.0
    }};

    function zoomIn() {{ camera.zoom = Math.min(camera.zoom + 0.15, 1.6); }}
    function zoomOut() {{ camera.zoom = Math.max(camera.zoom - 0.15, 0.75); }}

    // 6. Input Management
    let inputX = 0;
    let inputY = 0;
    const keys = {{}};

    window.addEventListener('keydown', e => {{
      keys[e.key.toLowerCase()] = true;
      if (e.key === 'Shift') alex.isSprinting = true;
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
        btn.textContent = '🏃 SPRINT: ON';
      }} else {{
        btn.classList.remove('active');
        btn.textContent = '🏃 SPRINT: OFF';
      }}
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

    // 7. Save & Load System (100% Local Storage, No Firebase)
    function saveGame() {{
      const saveState = {{
        currentMap: 'VILLAGE_ABANDONED',
        position: {{ x: alex.wx, y: alex.wy, orientation: alex.orientation }},
        chapter: 'ACT_I_THE_RETURN',
        timestamp: new Date().toISOString()
      }};
      localStorage.setItem('echo_save_default', JSON.stringify(saveState));
      showStatus('✓ Position & État sauvegardés localement');
    }}

    function loadGame() {{
      const raw = localStorage.getItem('echo_save_default');
      if (raw) {{
        const state = JSON.parse(raw);
        alex.wx = state.position.x;
        alex.wy = state.position.y;
        alex.orientation = state.position.orientation || 'SE';
        showStatus('✓ Sauvegarde locale restaurée');
      }} else {{
        showStatus('Aucune sauvegarde locale trouvée');
      }}
    }}

    function showStatus(msg) {{
      const el = document.getElementById('hud-status');
      el.textContent = msg;
      setTimeout(() => {{ if (el.textContent === msg) el.textContent = ''; }}, 3000);
    }}

    // Auto-load on boot
    loadGame();

    // 8. Game Loop & Render
    let lastTime = performance.now();

    function gameLoop(now) {{
      const dt = Math.min((now - lastTime) / 1000, 0.1);
      lastTime = now;

      // Update Input
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
        const speed = isRunning ? 4.8 : 2.4;

        // Orientation
        const angle = Math.atan2(normY, normX);
        if (angle >= 0 && angle < Math.PI / 2) alex.orientation = 'SE';
        else if (angle >= Math.PI / 2 && angle <= Math.PI) alex.orientation = 'SW';
        else if (angle >= -Math.PI && angle < -Math.PI / 2) alex.orientation = 'NW';
        else alex.orientation = 'NE';

        // Isometric displacement
        const worldDx = (normX + normY) * speed * dt * 0.707;
        const worldDy = (-normX + normY) * speed * dt * 0.707;

        const resolved = resolveMovement(alex.wx, alex.wy, alex.wx + worldDx, alex.wy + worldDy, alex.radius);
        alex.wx = resolved.x;
        alex.wy = resolved.y;

        // Walk anim frames
        alex.frameTimer += dt;
        if (alex.frameTimer > 0.14) {{
          alex.frameTimer = 0;
          alex.walkFrame = (alex.walkFrame + 1) % 4;
        }}
      }} else {{
        alex.state = 'IDLE';
        alex.walkFrame = 0;
      }}

      // Camera Follow Alex
      const alexScreen = worldToScreen(alex.wx, alex.wy);
      camera.x += (alexScreen.x - camera.x) * Math.min(6.0 * dt, 1.0);
      camera.y += (alexScreen.y - camera.y) * Math.min(6.0 * dt, 1.0);

      // Render
      render();

      // Update HUD
      document.getElementById('hud-alex').textContent = 
        `Alex: [${{alex.wx.toFixed(1)}}, ${{alex.wy.toFixed(1)}}] | ${{alex.state}} (${{alex.orientation}})`;

      requestAnimationFrame(gameLoop);
    }}

    function render() {{
      ctx.fillStyle = '#0F172A';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      ctx.save();
      // Center and scale camera
      ctx.translate(canvas.width / 2, canvas.height / 2);
      ctx.scale(camera.zoom * window.devicePixelRatio, camera.zoom * window.devicePixelRatio);
      ctx.translate(-camera.x, -camera.y);

      // 1. Ground Layer
      const gridR = 12;
      for (let x = -gridR; x <= gridR; x++) {{
        for (let y = -gridR; y <= gridR; y++) {{
          if (Math.abs(x) + Math.abs(y) > gridR + 3) continue;
          const pos = worldToScreen(x, y);
          if (images.slab && images.slab.complete && images.slab.naturalWidth > 0) {{
            ctx.drawImage(images.slab, pos.x - HALF_W, pos.y - HALF_H, TILE_W, TILE_H);
          }} else {{
            ctx.beginPath();
            ctx.moveTo(pos.x, pos.y - HALF_H);
            ctx.lineTo(pos.x + HALF_W, pos.y);
            ctx.lineTo(pos.x, pos.y + HALF_H);
            ctx.lineTo(pos.x - HALF_W, pos.y);
            ctx.closePath();
            ctx.fillStyle = '#1E293B';
            ctx.fill();
            ctx.strokeStyle = '#0F172A';
            ctx.stroke();
          }}
        }}
      }}

      // 2. Road Layer
      ctx.fillStyle = 'rgba(51, 65, 85, 0.4)';
      const roadPts = [
        worldToScreen(0, 0), worldToScreen(0, 2), worldToScreen(0, 4),
        worldToScreen(0, 6), worldToScreen(0, 8), worldToScreen(3, 4),
        worldToScreen(-3, 4), worldToScreen(5, 5), worldToScreen(-5, 5)
      ];
      for (const pt of roadPts) {{
        ctx.beginPath();
        ctx.ellipse(pt.x, pt.y, HALF_W * 1.5, HALF_H * 1.5, 0, 0, Math.PI * 2);
        ctx.fill();
      }}

      // 3. Dynamic Z-Ordered Renderables (Buildings, Props, Alex)
      const renderables = [
        {{
          type: 'building', id: 'house', wx: 0.0, wy: 8.0,
          z: calculateZ(0.0, 8.0, 20000),
          img: images.familyHouse, w: 220, h: 205, pivotY: 0.88
        }},
        {{
          type: 'building', id: 'church', wx: 6.0, wy: 5.0,
          z: calculateZ(6.0, 5.0, 20000),
          img: images.church, w: 200, h: 260, pivotY: 0.90
        }},
        {{
          type: 'building', id: 'cottage', wx: -5.0, wy: 5.0,
          z: calculateZ(-5.0, 5.0, 20000),
          img: images.cottage, w: 200, h: 190, pivotY: 0.88
        }},
        {{
          type: 'prop', id: 'well', wx: 0.0, wy: 4.0,
          z: calculateZ(0.0, 4.0, 30000),
          img: images.well, w: 90, h: 100, pivotY: 0.85
        }},
        {{
          type: 'prop', id: 'gate_r', wx: 2.2, wy: 4.0,
          z: calculateZ(2.2, 4.0, 30000),
          img: images.gate, w: 110, h: 70, pivotY: 0.85
        }},
        {{
          type: 'prop', id: 'gate_l', wx: -2.2, wy: 4.0,
          z: calculateZ(-2.2, 4.0, 30000),
          img: images.gate, w: 110, h: 70, pivotY: 0.85
        }},
        {{
          type: 'alex', id: 'alex', wx: alex.wx, wy: alex.wy,
          z: calculateZ(alex.wx, alex.wy, 40000)
        }}
      ];

      // Sort by Z-order strictly
      renderables.sort((a, b) => a.z - b.z);

      for (const r of renderables) {{
        const pt = worldToScreen(r.wx, r.wy);

        if (r.type === 'alex') {{
          // Draw Ground Shadow
          ctx.beginPath();
          ctx.ellipse(pt.x, pt.y - 2, 20, 8, 0, 0, Math.PI * 2);
          ctx.fillStyle = 'rgba(0, 0, 0, 0.4)';
          ctx.fill();

          // Render Sprite
          const alexW = 72;
          const alexH = 144;
          const dx = pt.x - alexW / 2;
          const dy = pt.y - alexH;

          if (alex.state === 'IDLE') {{
            let img = images.idleSE;
            if (alex.orientation === 'SW') img = images.idleSW;
            else if (alex.orientation === 'NE') img = images.idleNE;
            else if (alex.orientation === 'NW') img = images.idleNW;

            if (img && img.complete) {{
              ctx.drawImage(img, dx, dy, alexW, alexH);
            }}
          }} else {{
            // Walk Strip Frame
            const strip = images.walkStrip;
            if (strip && strip.complete && strip.naturalWidth > 0) {{
              const frameW = strip.naturalWidth / 4;
              const frameH = strip.naturalHeight;
              const sx = alex.walkFrame * frameW;
              ctx.drawImage(strip, sx, 0, frameW, frameH, dx, dy, alexW, alexH);
            }} else {{
              ctx.drawImage(images.idleSE, dx, dy, alexW, alexH);
            }}
          }}
        }} else {{
          // Building / Prop
          if (r.img && r.img.complete && r.img.naturalWidth > 0) {{
            const dx = pt.x - r.w / 2;
            const dy = pt.y - r.h * r.pivotY;
            ctx.drawImage(r.img, dx, dy, r.w, r.h);
          }}
        }}
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
    
    print(f"=== Successfully generated {OUT_FILE} ===")

if __name__ == "__main__":
    build()
