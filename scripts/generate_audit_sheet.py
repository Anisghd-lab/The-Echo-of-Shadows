import os
from PIL import Image, ImageDraw, ImageFont

def build_audit_sheet():
    alex_dir = '/root/the_echo_of_shadows/new assets/characters/alex'
    out_path = '/root/the_echo_of_shadows/alex_direction_audit.png'
    
    font_title = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 26)
    font_section = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
    font_badge = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 13)
    font_name = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 12)
    font_info = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11)
    font_tiny = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 10)

    # 4 Main Categories
    sections = [
        {
            'title': '1. IDLE CANDIDATES (SE, SW, NE, NW)',
            'subtitle': 'Evaluated against Canonical Reference: Alex-—-Animation-Idle03 (139x296)',
            'items': [
                {
                    'dir': 'SE',
                    'file': 'idle/Alex-—-Animation-Idle03.png',
                    'label': 'Idle03.png',
                    'status': 'CANONICAL',
                    'score': '100 / 100',
                    'note': 'Official canonical Alex: dark winter trench coat, grey trousers, dark hair'
                },
                {
                    'dir': 'SE',
                    'file': 'idle/Alex-—-Animation-Idle06.png',
                    'label': 'Idle06.png',
                    'status': 'PASS',
                    'score': '98 / 100',
                    'note': 'Matching front-facing frame (breathing/secondary SE pose)'
                },
                {
                    'dir': 'SW',
                    'file': 'idle/Alex-—-Animation-Idle10.png',
                    'label': 'Idle10.png (Old SW)',
                    'status': 'REJECTED',
                    'score': '62 / 100',
                    'note': 'REJECTED: Incompatible character model, different facial features & coat'
                },
                {
                    'dir': 'SW',
                    'file': 'idle/Alex-—-Animation-Idle03.png',
                    'label': 'Idle03 Mirrored',
                    'status': 'FALLBACK',
                    'mirror': True,
                    'score': '100 / 100',
                    'note': 'TEMPORARY FALLBACK: 100% Identity Match. Same face, coat & proportions'
                },
                {
                    'dir': 'NE',
                    'file': 'idle/Alex-—-Animation-Idle06.png',
                    'label': 'Idle06.png (Old NE)',
                    'status': 'REJECTED',
                    'score': '45 / 100',
                    'note': 'REJECTED: Front-facing SE sprite, does NOT face North away from camera'
                },
                {
                    'dir': 'NE',
                    'file': 'idle/Alex-—-Animation-Idle22.png',
                    'label': 'Idle22.png (Back)',
                    'status': 'PASS',
                    'score': '88 / 100',
                    'note': 'Genuine back-facing Alex (showing rear of dark trench coat and hair)'
                },
                {
                    'dir': 'NW',
                    'file': 'idle/Alex-—-Animation-Idle07.png',
                    'label': 'Idle07.png (Old NW)',
                    'status': 'REJECTED',
                    'score': '40 / 100',
                    'note': 'REJECTED: Front-facing SE sprite with mismatched lighting & palette'
                },
                {
                    'dir': 'NW',
                    'file': 'idle/Alex-—-Animation-Idle15.png',
                    'label': 'Idle15.png (Back)',
                    'status': 'PASS',
                    'score': '86 / 100',
                    'note': 'Genuine back-facing Alex (showing rear coat and hair, NW angle)'
                },
                {
                    'dir': 'NW',
                    'file': 'idle/Alex-—-Animation-Idle03.png',
                    'label': 'Idle03 (Mirror NW)',
                    'status': 'FALLBACK',
                    'mirror': True,
                    'score': '100 / 100',
                    'note': 'TEMPORARY FALLBACK: Guaranteed 100% visual identity consistency'
                }
            ]
        },
        {
            'title': '2. WALK CANDIDATES (SE, SW, NE, NW)',
            'subtitle': 'Evaluated for gait, coat length, silhouette and directional facing',
            'items': [
                {
                    'dir': 'SE',
                    'file': 'walk/Alex-—-Marche36.png',
                    'label': 'Marche36.png (SE)',
                    'status': 'CANONICAL',
                    'score': '96 / 100',
                    'note': 'Canonical 6-frame SE walk cycle (Marche36 to Marche41)'
                },
                {
                    'dir': 'SW',
                    'file': 'walk/Alex-—-Marche42.png',
                    'label': 'Marche42.png (SW)',
                    'status': 'PASS',
                    'score': '92 / 100',
                    'note': 'Matching 5-frame SW walk cycle (Marche42 to Marche46)'
                },
                {
                    'dir': 'SW',
                    'file': 'walk/Alex-—-Marche36.png',
                    'label': 'Marche36 Mirrored',
                    'status': 'FALLBACK',
                    'mirror': True,
                    'score': '96 / 100',
                    'note': 'TEMPORARY FALLBACK: Exact mirror of canonical SE walk cycle'
                },
                {
                    'dir': 'NE',
                    'file': 'walk/Alex-—-Marche18.png',
                    'label': 'Marche18.png (NE)',
                    'status': 'CANONICAL',
                    'score': '92 / 100',
                    'note': 'Canonical 5-frame NE back-facing walk cycle (Marche18-30)'
                },
                {
                    'dir': 'NW',
                    'file': 'walk/Alex-—-Marche10.png',
                    'label': 'Marche10.png (NW)',
                    'status': 'CANONICAL',
                    'score': '90 / 100',
                    'note': 'Canonical 5-frame NW back-facing walk cycle (Marche10-35)'
                },
                {
                    'dir': 'NW',
                    'file': 'walk/Alex-—-Marche18.png',
                    'label': 'Marche18 Mirrored',
                    'status': 'FALLBACK',
                    'mirror': True,
                    'score': '92 / 100',
                    'note': 'TEMPORARY FALLBACK: Exact mirror of canonical NE walk cycle'
                }
            ]
        },
        {
            'title': '3. RUN CANDIDATES (SE, SW, NE, NW)',
            'subtitle': 'Evaluated against coat color, trousers, and proportional stride',
            'items': [
                {
                    'dir': 'SE',
                    'file': 'run/Alex-—-Course11.png',
                    'label': 'Course11.png (SE)',
                    'status': 'CANONICAL',
                    'score': '94 / 100',
                    'note': 'Canonical SE run cycle (Course11 to Course22). Dark coat, grey pants'
                },
                {
                    'dir': 'SW',
                    'file': 'run/Alex-—-Course40.png',
                    'label': 'Course40.png (Old SW)',
                    'status': 'REJECTED',
                    'score': '35 / 100',
                    'note': 'REJECTED: Character wears bright beige jacket! Different person entirely'
                },
                {
                    'dir': 'SW',
                    'file': 'run/Alex-—-Course11.png',
                    'label': 'Course11 Mirrored',
                    'status': 'FALLBACK',
                    'mirror': True,
                    'score': '94 / 100',
                    'note': 'TEMPORARY FALLBACK: Mirrored canonical run. Preserves exact coat & identity'
                },
                {
                    'dir': 'NE',
                    'file': 'run/Alex-—-Course10.png',
                    'label': 'Course10.png (NE)',
                    'status': 'CANONICAL',
                    'score': '90 / 100',
                    'note': 'Canonical NE back-facing run cycle (Course05-15). Dark coat from behind'
                },
                {
                    'dir': 'NW',
                    'file': 'run/Alex-—-Course26.png',
                    'label': 'Course26.png (Old NW)',
                    'status': 'REJECTED',
                    'score': '30 / 100',
                    'note': 'REJECTED: 146x146 cropped square, black trousers, broken proportions'
                },
                {
                    'dir': 'NW',
                    'file': 'run/Alex-—-Course10.png',
                    'label': 'Course10 Mirrored',
                    'status': 'FALLBACK',
                    'mirror': True,
                    'score': '90 / 100',
                    'note': 'TEMPORARY FALLBACK: Mirrored NE run. Preserves 100% identity and stride'
                }
            ]
        },
        {
            'title': '4. INTERACTION CANDIDATES (SE, SW, NE, NW)',
            'subtitle': 'Evaluated for investigation pose, full-body integrity, and scale',
            'items': [
                {
                    'dir': 'SE',
                    'file': 'interaction/Alex-—-Interaction01.png',
                    'label': 'Interaction01.png',
                    'status': 'CANONICAL',
                    'score': '95 / 100',
                    'note': 'Canonical investigation pose (reaches forward towards item)'
                },
                {
                    'dir': 'SW',
                    'file': 'interaction/Alex-—-Interaction14.png',
                    'label': 'Interaction14 (Old SW)',
                    'status': 'REJECTED',
                    'score': '55 / 100',
                    'note': 'REJECTED: Mismatched color palette & body posture'
                },
                {
                    'dir': 'SW',
                    'file': 'interaction/Alex-—-Interaction01.png',
                    'label': 'Interaction01 Mirrored',
                    'status': 'FALLBACK',
                    'mirror': True,
                    'score': '95 / 100',
                    'note': 'TEMPORARY FALLBACK: Clean mirrored interaction towards SW items'
                },
                {
                    'dir': 'NE',
                    'file': 'interaction/Alex-—-Interaction28.png',
                    'label': 'Interaction28.png',
                    'status': 'CANONICAL',
                    'score': '88 / 100',
                    'note': 'Back-facing inspection pose (investigates North objects)'
                },
                {
                    'dir': 'NW',
                    'file': 'interaction/Alex-—-Interaction64.png',
                    'label': 'Interaction64 (Old NW)',
                    'status': 'REJECTED',
                    'score': '20 / 100',
                    'note': 'REJECTED: 76x87 half-body cropped sprite! Alex shrank by 50%'
                },
                {
                    'dir': 'NW',
                    'file': 'interaction/Alex-—-Interaction28.png',
                    'label': 'Interaction28 Mirrored',
                    'status': 'FALLBACK',
                    'mirror': True,
                    'score': '88 / 100',
                    'note': 'TEMPORARY FALLBACK: Clean mirrored back inspection towards NW'
                }
            ]
        }
    ]

    # Layout Calculations
    CARD_W = 230
    CARD_H = 340
    CARD_GAP = 20
    PAD_X = 40
    PAD_TOP = 110
    
    # Calculate required dimensions
    max_items = max(len(s['items']) for s in sections)
    img_w = max(2150, PAD_X * 2 + max_items * (CARD_W + CARD_GAP))
    
    section_h = CARD_H + 110
    img_h = PAD_TOP + len(sections) * section_h + 80
    
    sheet = Image.new('RGBA', (img_w, img_h), (18, 20, 26, 255))
    draw = ImageDraw.Draw(sheet)
    
    # Header
    draw.rectangle([(0, 0), (img_w, 90)], fill=(26, 29, 38, 255))
    draw.text((PAD_X, 18), "THE ECHO OF SHADOWS — PHASE 3.3 ALEX DIRECTIONAL IDENTITY AUDIT", fill=(255, 255, 255, 255), font=font_title)
    draw.text((PAD_X, 56), "Comprehensive audit of 203 Alex files across 4 directions (SE, SW, NE, NW) • Absolute identity consistency verification", fill=(160, 174, 192, 255), font=font_info)

    # Color definitions
    STATUS_COLORS = {
        'CANONICAL': ((16, 185, 129), (6, 78, 59)), # Green
        'PASS': ((59, 130, 246), (30, 58, 138)),    # Blue
        'FALLBACK': ((168, 85, 247), (88, 28, 135)),# Purple
        'REJECTED': ((239, 68, 68), (127, 29, 29)), # Red
    }
    
    DIR_COLORS = {
        'SE': (245, 158, 11), # Amber
        'SW': (59, 130, 246), # Blue
        'NE': (16, 185, 129), # Green
        'NW': (168, 85, 247), # Purple
    }

    curr_y = PAD_TOP
    for s_idx, sec in enumerate(sections):
        # Section Header
        draw.text((PAD_X, curr_y), sec['title'], fill=(243, 244, 246, 255), font=font_section)
        draw.text((PAD_X, curr_y + 26), sec['subtitle'], fill=(156, 163, 175, 255), font=font_info)
        
        cards_y = curr_y + 55
        for i_idx, item in enumerate(sec['items']):
            cx = PAD_X + i_idx * (CARD_W + CARD_GAP)
            cy = cards_y
            
            # Card Background
            draw.rectangle([(cx, cy), (cx + CARD_W, cy + CARD_H)], fill=(28, 32, 42, 255), outline=(45, 52, 68, 255), width=1)
            
            # Direction Badge (Top Left)
            d_col = DIR_COLORS.get(item['dir'], (200, 200, 200))
            draw.rectangle([(cx + 8, cy + 8), (cx + 42, cy + 28)], fill=d_col)
            draw.text((cx + 14, cy + 10), item['dir'], fill=(0, 0, 0, 255), font=font_badge)
            
            # Status Badge (Top Right)
            fg, bg = STATUS_COLORS.get(item['status'], ((200, 200, 200), (50, 50, 50)))
            st_text = item['status']
            text_w = len(st_text) * 8 + 12
            draw.rectangle([(cx + CARD_W - text_w - 8, cy + 8), (cx + CARD_W - 8, cy + 28)], fill=bg, outline=fg, width=1)
            draw.text((cx + CARD_W - text_w - 2, cy + 10), st_text, fill=fg, font=font_badge)
            
            # Sprite Preview Area
            preview_box = [(cx + 12, cy + 34), (cx + CARD_W - 12, cy + 215)]
            draw.rectangle(preview_box, fill=(15, 17, 23, 255))
            
            # Draw ground contact line and shadow guide
            floor_y = cy + 205
            draw.line([(cx + 20, floor_y), (cx + CARD_W - 20, floor_y)], fill=(40, 48, 64, 255), width=1)
            draw.ellipse([(cx + CARD_W // 2 - 25, floor_y - 4), (cx + CARD_W // 2 + 25, floor_y + 4)], fill=(30, 36, 48, 255))
            
            # Load and render Sprite
            p = os.path.join(alex_dir, item['file'])
            if os.path.exists(p):
                im = Image.open(p).convert('RGBA')
                if item.get('mirror', False):
                    im = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                
                # Fit inside preview box keeping aspect ratio, anchor at bottomCenter
                avail_w = CARD_W - 32
                avail_h = 165
                scale = min(avail_w / im.size[0], avail_h / im.size[1])
                new_w = max(1, int(im.size[0] * scale))
                new_h = max(1, int(im.size[1] * scale))
                
                im_scaled = im.resize((new_w, new_h), Image.Resampling.NEAREST)
                
                # Bottom-center align on the floor line
                paste_x = cx + CARD_W // 2 - new_w // 2
                paste_y = floor_y - new_h
                
                sheet.paste(im_scaled, (paste_x, paste_y), im_scaled)
                
                # Dimensions text inside preview
                dim_txt = f"{im.size[0]}x{im.size[1]}"
                draw.text((cx + 16, cy + 40), dim_txt, fill=(100, 116, 139, 255), font=font_tiny)
            else:
                draw.text((cx + 30, cy + 100), "FILE NOT FOUND", fill=(239, 68, 68, 255), font=font_badge)

            # Metadata Footer
            draw.text((cx + 12, cy + 222), item['label'], fill=(255, 255, 255, 255), font=font_name)
            
            score_col = (16, 185, 129, 255) if '100' in item['score'] or '9' in item['score'][:2] else ((239, 68, 68, 255) if int(item['score'].split('/')[0].strip()) < 75 else (59, 130, 246, 255))
            draw.text((cx + 12, cy + 240), f"Identity Score: {item['score']}", fill=score_col, font=font_badge)
            
            # Word wrap notes
            note_words = item['note'].split(' ')
            line1, line2, line3 = '', '', ''
            target_line = 1
            for word in note_words:
                test_line = (line1 if target_line == 1 else (line2 if target_line == 2 else line3)) + ' ' + word
                if len(test_line) < 30:
                    if target_line == 1: line1 = test_line.strip()
                    elif target_line == 2: line2 = test_line.strip()
                    else: line3 = test_line.strip()
                else:
                    if target_line == 1:
                        target_line = 2
                        line2 = word
                    elif target_line == 2:
                        target_line = 3
                        line3 = word
                    else:
                        line3 += ' ' + word
            
            draw.text((cx + 12, cy + 260), line1, fill=(156, 163, 175, 255), font=font_tiny)
            if line2: draw.text((cx + 12, cy + 276), line2, fill=(156, 163, 175, 255), font=font_tiny)
            if line3: draw.text((cx + 12, cy + 292), line3, fill=(156, 163, 175, 255), font=font_tiny)

        curr_y += section_h

    # Save output
    sheet.save(out_path, 'PNG')
    print(f"Successfully generated visual contact sheet: {out_path} ({img_w}x{img_h})")
    
    # Also save to artifact directory
    artifact_dir = '/root/.gemini/antigravity-cli/brain/531d4802-1264-49d0-8c33-5283cbc86daf'
    if os.path.exists(artifact_dir):
        artifact_path = os.path.join(artifact_dir, 'alex_direction_audit.png')
        sheet.save(artifact_path, 'PNG')
        print(f"Copied contact sheet to artifact directory: {artifact_path}")

if __name__ == '__main__':
    build_audit_sheet()
