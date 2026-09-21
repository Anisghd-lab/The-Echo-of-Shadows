import os
import math
from PIL import Image, ImageDraw, ImageFont

def create_comparison():
    out_path = "/root/the_echo_of_shadows/tile_size_comparison.png"
    artifact_path = "/root/.gemini/antigravity-cli/brain/531d4802-1264-49d0-8c33-5283cbc86daf/tile_size_comparison.png"

    # Assets
    slab_path = "/root/the_echo_of_shadows/assets/images/environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet25.png"
    snow_path = "/root/the_echo_of_shadows/assets/images/environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet31.png"
    alex_path = "/root/the_echo_of_shadows/assets/images/characters/alex/idle/Alex-—-Animation-Idle03.png"
    well_path = "/root/the_echo_of_shadows/assets/images/environments/village/decor/Village-abandonné-—-Route-&-décor-extérieur01.png"

    raw_slab = Image.open(slab_path).convert("RGBA")
    raw_snow = Image.open(snow_path).convert("RGBA")
    raw_alex = Image.open(alex_path).convert("RGBA")
    raw_well = Image.open(well_path).convert("RGBA")

    # Dimensions
    panel_w = 400
    panel_h = 660
    gap = 20
    margin = 30
    header_h = 140
    footer_h = 80

    total_w = margin * 2 + panel_w * 4 + gap * 3
    total_h = header_h + panel_h + footer_h + margin

    canvas = Image.new("RGBA", (total_w, total_h), (15, 23, 42, 255))
    draw = ImageDraw.Draw(canvas)

    # Header
    draw.rectangle([(0, 0), (total_w, header_h)], fill=(11, 17, 32, 255))
    draw.line([(0, header_h), (total_w, header_h)], fill=(51, 65, 85, 255), width=2)

    # Title
    draw.text((margin, 25), "L'ÉCHO DES OMBRES — DIRECTION ARTISTIQUE DU SOL (PHASE 3.3)", fill=(248, 250, 252, 255))
    draw.text((margin, 60), "Comparaison de la taille des dalles & validation du standard canonique 80 × 40 px", fill=(56, 189, 248, 255))
    draw.text((margin, 95), "Ratio dimétrique 2:1 strict conservé | Alignement physique invariant des bâtiments & collisions", fill=(148, 163, 184, 255))

    configs = [
        {
            "name": "128 × 64 px",
            "tw": 128, "th": 64,
            "density": "1.00× (Baseline)",
            "alex_pct": "21.9%",
            "status": "ANCIENNE RÉFÉRENCE",
            "desc": "Grandes dalles espacées\nFaible densité de pavés\nAspect trop grossier",
            "badge_color": (100, 116, 139),
            "border_color": (71, 85, 105),
            "is_selected": False
        },
        {
            "name": "96 × 48 px",
            "tw": 96, "th": 48,
            "density": "1.78× (+78%)",
            "alex_pct": "29.2%",
            "status": "PREMIER TEST",
            "desc": "Dalles intermédiaires\nDensité accrue\nEncore un peu large",
            "badge_color": (148, 163, 184),
            "border_color": (71, 85, 105),
            "is_selected": False
        },
        {
            "name": "80 × 40 px",
            "tw": 80, "th": 40,
            "density": "2.56× (+156%)",
            "alex_pct": "35.0%",
            "status": "CHOIX VALIDÉ (MEILLEURE)",
            "desc": "Dalles fines & détaillées\nDensité idéale de pavés\nÉquilibre parfait avec Alex",
            "badge_color": (34, 197, 94),
            "border_color": (34, 197, 94),
            "is_selected": True
        },
        {
            "name": "60 × 30 px",
            "tw": 60, "th": 30,
            "density": "4.55× (+355%)",
            "alex_pct": "46.7%",
            "status": "TEST ALTERNATIF",
            "desc": "Dalles ultra-fines\nTrès forte répétition\nTexture très dense",
            "badge_color": (148, 163, 184),
            "border_color": (71, 85, 105),
            "is_selected": False
        }
    ]

    for i, cfg in enumerate(configs):
        px = margin + i * (panel_w + gap)
        py = header_h + 20

        # Panel Background
        bg_col = (20, 30, 48, 255) if not cfg["is_selected"] else (18, 38, 48, 255)
        draw.rectangle([(px, py), (px + panel_w, py + panel_h)], fill=bg_col, outline=cfg["border_color"], width=3 if cfg["is_selected"] else 1)

        # Panel Header
        header_bg = (30, 41, 59, 255) if not cfg["is_selected"] else (22, 101, 52, 255)
        draw.rectangle([(px, py), (px + panel_w, py + 45)], fill=header_bg)
        draw.text((px + 14, py + 12), cfg["name"], fill=(255, 255, 255, 255))
        draw.text((px + panel_w - 180, py + 14), cfg["status"], fill=(255, 255, 255, 255) if cfg["is_selected"] else (148, 163, 184, 255))

        # Viewport rendering for ground tiles
        view_w = panel_w - 20
        view_h = 320
        view_x = px + 10
        view_y = py + 55

        viewport = Image.new("RGBA", (view_w, view_h), (18, 27, 40, 255))
        vp_draw = ImageDraw.Draw(viewport)

        tw = cfg["tw"]
        th = cfg["th"]
        hw = tw // 2
        hh = th // 2
        world_scale = 128.0 / tw

        # Scaled tile images
        tile_slab = raw_slab.resize((tw + 1, th + 1), Image.Resampling.LANCZOS)
        tile_snow = raw_snow.resize((tw + 1, th + 1), Image.Resampling.LANCZOS)

        # Render ground grid centered in viewport
        cx = view_w // 2
        cy = view_h // 2 - 20

        grid_r = int(math.ceil(7 * world_scale))
        for gx in range(-grid_r, grid_r + 1):
            for gy in range(-grid_r, grid_r + 1):
                sx = cx + (gx - gy) * hw
                sy = cy + (gx + gy) * hh

                # Cull to viewport
                if -tw <= sx <= view_w + tw and -th <= sy <= view_h + th:
                    # Checker/path pattern
                    is_road = abs(gx) <= int(1.2 * world_scale)
                    tile = tile_slab if is_road else tile_snow
                    viewport.paste(tile, (int(sx - hw), int(sy - hh)), tile)

        # Paste well prop at invariant screen location (cx, cy - 30)
        well_w = 70
        well_h = int(well_w * (raw_well.size[1] / raw_well.size[0]))
        scaled_well = raw_well.resize((well_w, well_h), Image.Resampling.LANCZOS)
        viewport.paste(scaled_well, (cx - well_w // 2, cy - 40 - well_h + 10), scaled_well)

        # Paste Alex at invariant physical scale (28x56) at center
        alex_w = 28
        alex_h = 56
        scaled_alex = raw_alex.resize((alex_w, alex_h), Image.Resampling.LANCZOS)
        # Add a subtle ground shadow
        vp_draw.ellipse([(cx - 10, cy + 22), (cx + 10, cy + 28)], fill=(0, 0, 0, 120))
        viewport.paste(scaled_alex, (cx - alex_w // 2, cy - alex_h + 25), scaled_alex)

        # Paste viewport into panel
        canvas.paste(viewport, (view_x, view_y), viewport)
        draw.rectangle([(view_x, view_y), (view_x + view_w, view_y + view_h)], outline=(51, 65, 85, 255), width=1)

        # Metrics box below viewport
        my = view_y + view_h + 15
        draw.rectangle([(view_x, my), (view_x + view_w, my + 85)], fill=(15, 23, 42, 200), outline=(51, 65, 85, 255))
        draw.text((view_x + 12, my + 8), f"Densité de pavés : {cfg['density']}", fill=(56, 189, 248, 255))
        draw.text((view_x + 12, my + 32), f"Surface de dalle : {tw * th // 2} px²", fill=(203, 213, 225, 255))
        draw.text((view_x + 12, my + 56), f"Largeur Alex / dalle : {cfg['alex_pct']}", fill=(234, 179, 8, 255))

        # Description text
        dy = my + 105
        for line in cfg["desc"].split("\n"):
            draw.text((view_x + 12, dy), line, fill=(148, 163, 184, 255))
            dy += 22

        # Special badge for 80x40
        if cfg["is_selected"]:
            badge_y = py + panel_h - 45
            draw.rectangle([(view_x, badge_y), (view_x + view_w, badge_y + 35)], fill=(34, 197, 94, 255))
            draw.text((view_x + 24, badge_y + 9), "★ VALIDÉ PAR LE JOUEUR (80 × 40)", fill=(15, 23, 42, 255))

    # Footer
    draw.rectangle([(0, total_h - footer_h), (total_w, total_h)], fill=(11, 17, 32, 255))
    draw.line([(0, total_h - footer_h), (total_w, total_h - footer_h)], fill=(51, 65, 85, 255), width=1)
    draw.text((margin, total_h - 52), "STATUS : Standard 80 × 40 px activé par défaut dans le moteur Dart Flame & le Web Preview interactif.", fill=(34, 197, 94, 255))
    draw.text((margin, total_h - 26), "Testable en temps réel via les touches 1, 2, 3, 4 du clavier ou les boutons de la barre supérieure.", fill=(148, 163, 184, 255))

    canvas.save(out_path, format="PNG")
    os.makedirs(os.path.dirname(artifact_path), exist_ok=True)
    canvas.save(artifact_path, format="PNG")
    print(f"Comparison contact sheet created successfully: {out_path} & {artifact_path} ({total_w}x{total_h})")

if __name__ == "__main__":
    create_comparison()
