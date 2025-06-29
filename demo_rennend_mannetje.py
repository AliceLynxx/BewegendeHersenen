#!/usr/bin/env python3
"""
Demo: Rennend Mannetje Door Hersenen

Een speelse demonstratie van de BewegendeHersenen library waarbij een rennend
mannetje door de hersenen beweegt in plaats van traditionele fMRI activatie.

Deze demo toont:
- Creatief gebruik van de hersenvisualisatie toolkit
- Aangepaste bewegingspatronen door hersengebieden
- Combinatie van anatomische achtergrond met speelse animatie
- Educatieve en presentatie-vriendelijke visualisatie

Perfect voor:
• Presentaties over hersenactiviteit
• Educatieve demonstraties
• Creatieve wetenschapscommunicatie
• Inspiratie voor andere visualisaties

Auteur: BewegendeHersenen Project
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from bewegende_hersenen import BewegendHersenAnimatie
import math


def create_running_figure_sprite(size=5, frame=0):
    """
    Creëer een realistisch rennend mannetje sprite met schuine armen.
    
    Args:
        size (int): Grootte van het sprite in pixels
        frame (int): Animatie frame voor verschillende poses
        
    Returns:
        np.ndarray: 2D array met het rennende figuur
    """
    sprite = np.zeros((size*2, size*2))
    center_x, center_y = size, size
    
    # Basis figuur intensiteit
    intensity = 1.0
    
    # Animatie cyclus voor rennende beweging (8 frames cyclus voor vloeiendere beweging)
    pose = frame % 8
    
    # Hoofd (altijd aanwezig, iets groter voor betere zichtbaarheid)
    head_size = max(2, size//3)
    sprite[center_y-size//2:center_y-size//2+head_size, 
           center_x-head_size//2:center_x+head_size//2] = intensity
    
    # Lichaam (verticale lijn)
    body_height = size//2 + size//4
    sprite[center_y-size//4:center_y-size//4+body_height, 
           center_x-1:center_x+2] = intensity
    
    # Armen met schuine beweging (meer realistisch)
    arm_length = size//3
    if pose in [0, 1]:  # Linker arm naar voren, rechter arm naar achteren
        # Linker arm (schuin naar voren-beneden)
        for i in range(arm_length):
            arm_x = center_x - size//6 - i
            arm_y = center_y - size//8 + i//2
            if 0 <= arm_x < size*2 and 0 <= arm_y < size*2:
                sprite[arm_y, arm_x] = intensity * 0.8
        
        # Rechter arm (schuin naar achteren-boven)
        for i in range(arm_length):
            arm_x = center_x + size//6 + i
            arm_y = center_y - size//8 - i//2
            if 0 <= arm_x < size*2 and 0 <= arm_y < size*2:
                sprite[arm_y, arm_x] = intensity * 0.8
                
    elif pose in [2, 3]:  # Armen meer horizontaal
        # Linker arm (meer horizontaal naar voren)
        for i in range(arm_length):
            arm_x = center_x - size//6 - i
            arm_y = center_y - size//12
            if 0 <= arm_x < size*2 and 0 <= arm_y < size*2:
                sprite[arm_y, arm_x] = intensity * 0.8
        
        # Rechter arm (meer horizontaal naar achteren)
        for i in range(arm_length):
            arm_x = center_x + size//6 + i
            arm_y = center_y - size//12
            if 0 <= arm_x < size*2 and 0 <= arm_y < size*2:
                sprite[arm_y, arm_x] = intensity * 0.8
                
    elif pose in [4, 5]:  # Rechter arm naar voren, linker arm naar achteren
        # Rechter arm (schuin naar voren-beneden)
        for i in range(arm_length):
            arm_x = center_x + size//6 + i
            arm_y = center_y - size//8 + i//2
            if 0 <= arm_x < size*2 and 0 <= arm_y < size*2:
                sprite[arm_y, arm_x] = intensity * 0.8
        
        # Linker arm (schuin naar achteren-boven)
        for i in range(arm_length):
            arm_x = center_x - size//6 - i
            arm_y = center_y - size//8 - i//2
            if 0 <= arm_x < size*2 and 0 <= arm_y < size*2:
                sprite[arm_y, arm_x] = intensity * 0.8
                
    else:  # pose in [6, 7] - Armen in neutrale positie
        # Linker arm (licht schuin)
        for i in range(arm_length):
            arm_x = center_x - size//6 - i//2
            arm_y = center_y - size//12 + i//3
            if 0 <= arm_x < size*2 and 0 <= arm_y < size*2:
                sprite[arm_y, arm_x] = intensity * 0.8
        
        # Rechter arm (licht schuin andere kant)
        for i in range(arm_length):
            arm_x = center_x + size//6 + i//2
            arm_y = center_y - size//12 + i//3
            if 0 <= arm_x < size*2 and 0 <= arm_y < size*2:
                sprite[arm_y, arm_x] = intensity * 0.8
    
    # Benen met meer realistische rennende beweging
    leg_length = size//2 + size//4
    if pose in [0, 7]:  # Linker been ver vooruit
        # Linker been (schuin naar voren)
        for i in range(leg_length):
            leg_x = center_x - size//4 - i//3
            leg_y = center_y + size//4 + i
            if 0 <= leg_x < size*2 and 0 <= leg_y < size*2:
                sprite[leg_y, leg_x] = intensity * 0.9
        
        # Rechter been (meer verticaal, achter)
        sprite[center_y+size//4:center_y+size//4+leg_length, 
               center_x+size//8:center_x+size//4] = intensity * 0.9
               
    elif pose in [1, 2]:  # Beide benen dichter bij elkaar
        # Linker been
        sprite[center_y+size//4:center_y+size//4+leg_length, 
               center_x-size//4:center_x-size//8] = intensity * 0.9
        # Rechter been
        sprite[center_y+size//4:center_y+size//4+leg_length, 
               center_x+size//8:center_x+size//4] = intensity * 0.9
               
    elif pose in [3, 4]:  # Rechter been ver vooruit
        # Rechter been (schuin naar voren)
        for i in range(leg_length):
            leg_x = center_x + size//4 + i//3
            leg_y = center_y + size//4 + i
            if 0 <= leg_x < size*2 and 0 <= leg_y < size*2:
                sprite[leg_y, leg_x] = intensity * 0.9
        
        # Linker been (meer verticaal, achter)
        sprite[center_y+size//4:center_y+size//4+leg_length, 
               center_x-size//4:center_x-size//8] = intensity * 0.9
               
    else:  # pose in [5, 6] - Beide benen in andere fase
        # Linker been (licht naar achteren)
        for i in range(leg_length):
            leg_x = center_x - size//6 + i//4
            leg_y = center_y + size//4 + i
            if 0 <= leg_x < size*2 and 0 <= leg_y < size*2:
                sprite[leg_y, leg_x] = intensity * 0.9
        
        # Rechter been (licht naar voren)
        for i in range(leg_length):
            leg_x = center_x + size//6 - i//4
            leg_y = center_y + size//4 + i
            if 0 <= leg_x < size*2 and 0 <= leg_y < size*2:
                sprite[leg_y, leg_x] = intensity * 0.9
    
    return sprite


def create_brain_path(width, height, frames):
    """
    Creëer een interessant bewegingspad door de hersenen.
    
    Args:
        width (int): Breedte van het hersengebied
        height (int): Hoogte van het hersengebied  
        frames (int): Aantal frames voor de animatie
        
    Returns:
        list: Lijst van (x, y) coördinaten voor elk frame
    """
    path = []
    
    # Definieer interessante punten in de hersenen om langs te gaan
    # Deze punten representeren verschillende hersengebieden
    waypoints = [
        (width * 0.2, height * 0.3),   # Frontale cortex
        (width * 0.4, height * 0.2),   # Motorische cortex
        (width * 0.6, height * 0.4),   # Pariëtale cortex
        (width * 0.8, height * 0.3),   # Temporale cortex
        (width * 0.7, height * 0.6),   # Visuele cortex
        (width * 0.5, height * 0.7),   # Cerebellum gebied
        (width * 0.3, height * 0.6),   # Auditieve cortex
        (width * 0.2, height * 0.4),   # Terug naar start gebied
    ]
    
    # Bereken smooth pad tussen waypoints
    total_segments = len(waypoints)
    frames_per_segment = frames // total_segments
    
    for i in range(total_segments):
        start_point = waypoints[i]
        end_point = waypoints[(i + 1) % total_segments]  # Loop terug naar begin
        
        # Interpoleer tussen start en eind punt
        for frame in range(frames_per_segment):
            t = frame / frames_per_segment
            
            # Gebruik easing functie voor natuurlijkere beweging
            t_smooth = 0.5 * (1 - math.cos(math.pi * t))
            
            x = start_point[0] + t_smooth * (end_point[0] - start_point[0])
            y = start_point[1] + t_smooth * (end_point[1] - start_point[1])
            
            path.append((int(x), int(y)))
    
    # Vul aan tot exact het juiste aantal frames
    while len(path) < frames:
        path.append(path[-1])  # Herhaal laatste positie
    
    return path[:frames]  # Zorg dat we exact het juiste aantal frames hebben


def create_brain_background_advanced(width=64, height=64):
    """
    Creëer een geavanceerde hersenachtergrond in grijstinten met hoog contrast.
    
    Args:
        width (int): Breedte van de achtergrond
        height (int): Hoogte van de achtergrond
        
    Returns:
        np.ndarray: 2D array met hersenachtergrond in grijstinten
    """
    print(f"🧠 Creëren van geavanceerde hersenachtergrond in grijstinten ({width}x{height})...")
    
    # Maak coördinaat grids
    y_coords, x_coords = np.ogrid[:height, :width]
    center_x, center_y = width // 2, height // 2
    
    # Creëer hersenvorm (meer realistisch)
    # Basis ellips voor hersenvorm
    ellipse_a = width * 0.42  # Horizontale radius
    ellipse_b = height * 0.38  # Verticale radius
    
    # Hoofdvorm
    ellipse = ((x_coords - center_x) / ellipse_a)**2 + ((y_coords - center_y) / ellipse_b)**2
    brain_mask = ellipse <= 1.0
    
    # Voeg hersenvouwen toe (sulci en gyri) met meer contrast
    structure = np.zeros((height, width))
    
    # Meerdere lagen van structuur met hogere contrasten
    for i in range(12):  # Meer lagen voor meer detail
        # Verschillende frequenties voor verschillende structuren
        freq_x = np.random.uniform(0.03, 0.5)
        freq_y = np.random.uniform(0.03, 0.5)
        phase_x = np.random.uniform(0, 2*np.pi)
        phase_y = np.random.uniform(0, 2*np.pi)
        amplitude = np.random.uniform(0.2, 0.6)  # Hogere amplitude voor meer contrast
        
        wave = amplitude * np.sin(freq_x * x_coords + phase_x) * np.sin(freq_y * y_coords + phase_y)
        structure += wave
    
    # Voeg radiale patronen toe (zoals echte hersenvouwen) met meer contrast
    distance_from_center = np.sqrt((x_coords - center_x)**2 + (y_coords - center_y)**2)
    radial_pattern = 0.4 * np.sin(distance_from_center * 0.25) * np.exp(-distance_from_center / (width * 0.35))
    structure += radial_pattern
    
    # Voeg concentrische ringen toe voor meer hersenstructuur
    for ring in range(3):
        ring_radius = (ring + 1) * width * 0.15
        ring_pattern = 0.3 * np.exp(-((distance_from_center - ring_radius) / (width * 0.05))**2)
        structure += ring_pattern
    
    # Combineer alles met hogere basis grijswaarde
    background = np.where(brain_mask, 0.4 + 0.5 * structure, 0.0)  # Hogere basis + meer contrast
    
    # Voeg subtiele ruis toe
    noise = 0.05 * np.random.normal(0, 1, (height, width))
    background += noise
    
    # Normaliseer en clip voor optimaal contrast
    background = np.clip(background, 0, 1)
    
    # Verhoog contrast verder door histogram stretching
    if background.max() > background.min():
        background = (background - background.min()) / (background.max() - background.min())
    
    # Pas gamma correctie toe voor betere zichtbaarheid
    gamma = 0.8  # Iets donkerder voor betere contrast
    background = np.power(background, gamma)
    
    # Maak de randen zachter maar behoud contrast
    edge_softness = 4
    for i in range(edge_softness):
        mask_soft = ellipse <= (1.0 + i * 0.08)
        fade_factor = max(0.1, 1 - i * 0.2)  # Langzamere fade voor betere zichtbaarheid
        background = np.where(mask_soft, background, background * fade_factor)
    
    print(f"   ✅ Grijstinten achtergrond met hoog contrast gecreëerd")
    print(f"   📊 Contrast range: {background.min():.3f} - {background.max():.3f}")
    
    return background


def generate_running_animation_data(width, height, frames, sprite_size=6):
    """
    Genereer animatie data met een rennend mannetje.
    
    Args:
        width (int): Breedte van de animatie
        height (int): Hoogte van de animatie
        frames (int): Aantal frames
        sprite_size (int): Grootte van het rennende figuur
        
    Returns:
        np.ndarray: 3D array met animatie data
    """
    print(f"🏃 Genereren van verbeterd rennend mannetje animatie ({width}x{height}, {frames} frames)...")
    
    # Initialiseer animatie data
    animation_data = np.zeros((height, width, frames))
    
    # Creëer bewegingspad
    path = create_brain_path(width, height, frames)
    
    print(f"📍 Bewegingspad gecreëerd met {len(path)} posities")
    
    # Voor elk frame
    for frame in range(frames):
        # Krijg huidige positie
        pos_x, pos_y = path[frame]
        
        # Creëer rennend figuur sprite voor dit frame (verbeterde versie)
        sprite = create_running_figure_sprite(sprite_size, frame)
        sprite_h, sprite_w = sprite.shape
        
        # Bereken positie om sprite te plaatsen (gecentreerd op pad positie)
        start_y = max(0, min(height - sprite_h, int(pos_y - sprite_h // 2)))
        end_y = start_y + sprite_h
        start_x = max(0, min(width - sprite_w, int(pos_x - sprite_w // 2)))
        end_x = start_x + sprite_w
        
        # Plaats sprite in de animatie data
        sprite_crop_y = slice(0, end_y - start_y)
        sprite_crop_x = slice(0, end_x - start_x)
        
        animation_data[start_y:end_y, start_x:end_x, frame] = sprite[sprite_crop_y, sprite_crop_x]
        
        # Voeg wat "stofwolkjes" toe achter het rennende figuur voor effect
        if frame > 0:
            prev_pos_x, prev_pos_y = path[frame - 1]
            dust_intensity = 0.2 * np.exp(-0.05 * (frame % 10))  # Cyclische vervaging
            
            # Voeg kleine stofwolkjes toe
            for i in range(2):  # Minder stof voor schonere look
                dust_x = int(prev_pos_x + np.random.normal(0, 1.5))
                dust_y = int(prev_pos_y + np.random.normal(0, 1.5))
                
                if 0 <= dust_x < width and 0 <= dust_y < height:
                    animation_data[dust_y, dust_x, frame] += dust_intensity * np.random.uniform(0.3, 0.7)
    
    print(f"✅ Verbeterd rennend mannetje animatie gegenereerd!")
    print(f"   Intensiteit range: {animation_data.min():.3f} - {animation_data.max():.3f}")
    print(f"   🎨 Kleurenschema: geel/rood/oranje (plasma colormap)")
    
    return animation_data


def create_running_demo():
    """
    Hoofdfunctie om de rennend mannetje demo te creëren.
    
    Returns:
        str: Pad naar het gegenereerde GIF bestand
    """
    print("🎬" + "="*58 + "🎬")
    print("    DEMO: HOGE RESOLUTIE RENNEND MANNETJE DOOR HERSENEN")
    print("🎬" + "="*58 + "🎬")
    print()
    print("Welkom bij de hoge resolutie versie van deze speelse demonstratie!")
    print("Het rennende mannetje heeft nu:")
    print("• Verdubbelde resolutie (160x160 pixels)")
    print("• Verhoogde DPI (200) voor scherpere weergave")
    print("• Groter sprite (12x12) voor betere zichtbaarheid")
    print("• Grijstinten hersenachtergrond met hoog contrast")
    print("• Behoud van mooie geel/rood/oranje kleuren")
    print()
    
    # Instellingen - VERHOOGDE RESOLUTIE
    width, height = 160, 160  # Verdubbeld van 80x80 naar 160x160
    frames = 64  # Behoud aantal frames voor zelfde animatiesnelheid
    sprite_size = 12  # Verdubbeld van 6 naar 12 voor betere zichtbaarheid
    
    print("⚙️  Hoge resolutie animatie instellingen:")
    print(f"   📐 Resolutie: {width}x{height} pixels (VERDUBBELD)")
    print(f"   🎞️  Frames: {frames}")
    print(f"   🏃 Sprite grootte: {sprite_size}x{sprite_size} (VERDUBBELD)")
    print(f"   🎨 Achtergrond: Grijstinten met hoog contrast")
    print(f"   🌈 Mannetje: Geel/rood/oranje (plasma)")
    print(f"   🔍 DPI: 200 (VERHOOGD voor scherpere weergave)")
    print()
    
    # Stap 1: Creëer verbeterde hersenachtergrond met hogere resolutie
    print("Stap 1: Hoge resolutie hersenachtergrond in grijstinten creëren...")
    brain_background = create_brain_background_advanced(width, height)
    
    # Sla achtergrond op als PNG voor gebruik (in grijstinten)
    background_filename = "rennend_mannetje_brain_background_hd.png"
    plt.figure(figsize=(10, 10))  # Groter figuur voor hoge resolutie
    plt.imshow(brain_background, cmap='gray', vmin=0, vmax=1)
    plt.title("Hersenachtergrond (Hoge Resolutie, Grijstinten, Hoog Contrast)", fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(background_filename, dpi=200, bbox_inches='tight', facecolor='black')  # Verhoogde DPI
    plt.close()
    print(f"   💾 Hoge resolutie grijstinten achtergrond opgeslagen als: {background_filename}")
    
    # Stap 2: Genereer hoge resolutie rennend mannetje animatie data
    print("\nStap 2: Hoge resolutie rennend mannetje animatie genereren...")
    running_data = generate_running_animation_data(width, height, frames, sprite_size)
    
    # Stap 3: Creëer animatie met grijstinten hersenachtergrond
    print("\nStap 3: Hoge resolutie animatie met grijstinten hersenachtergrond combineren...")
    
    # Gebruik de BewegendeHersenen library
    animatie = BewegendHersenAnimatie(
        colormap='plasma',  # Behoud mooie geel/rood/oranje kleuren voor het mannetje
        interval=100,       # 100ms tussen frames = 10 FPS (behoud animatiesnelheid)
        background_image=background_filename,
        overlay_alpha=0.9   # Rennend figuur goed zichtbaar tegen grijze achtergrond
    )
    
    # Laad de rennende data
    animatie.load_data(running_data)
    
    # Genereer de finale animatie met verhoogde DPI
    output_filename = "rennend_mannetje_door_hersenen.gif"
    print(f"   🎬 Creëren van hoge resolutie finale animatie: {output_filename}")
    
    animation_obj = animatie.create_animation(
        output_path=output_filename,
        figsize=(12, 12),  # Groter figuur voor hoge resolutie
        dpi=200,           # VERHOOGDE DPI van 120 naar 200
        title="🏃 Hoge Resolutie Rennend Mannetje Door de Hersenen 🧠",
        show_colorbar=False  # Geen colorbar nodig voor deze demo
    )
    
    # Stap 4: Maak een vergelijkingsplot
    print("\nStap 4: Hoge resolutie vergelijkingsplot maken...")
    create_comparison_plot(brain_background, running_data, frames)
    
    # Stap 5: Maak een bewegingspad visualisatie
    print("\nStap 5: Hoge resolutie bewegingspad visualisatie...")
    create_path_visualization(width, height, frames, brain_background)
    
    print("\n🎉 Hoge resolutie rennend mannetje demo voltooid!")
    print(f"\n📁 Gegenereerde bestanden:")
    print(f"   🎬 {output_filename} - Hoofdanimatie (HOGE RESOLUTIE)")
    print(f"   🖼️  {background_filename} - Hoge resolutie grijstinten hersenachtergrond")
    print(f"   📊 rennend_mannetje_vergelijking_hd.png - Hoge resolutie vergelijkingsplot")
    print(f"   🗺️  rennend_mannetje_bewegingspad_hd.png - Hoge resolutie pad visualisatie")
    
    print(f"\n💡 Verbeteringen in deze hoge resolutie versie:")
    print(f"   🔍 Verdubbelde pixeldichtheid (160x160 vs 80x80)")
    print(f"   ✨ Verhoogde DPI (200 vs 120) voor scherpere weergave")
    print(f"   🏃 Groter rennend figuur (12x12 vs 6x6) voor betere zichtbaarheid")
    print(f"   🎨 Behoud van grijstinten achtergrond met hoog contrast")
    print(f"   🌈 Behoud van mooie geel/rood/oranje kleuren")
    print(f"   ⚡ Behoud van animatiesnelheid en timing")
    print(f"   🌐 Geoptimaliseerd voor web gebruik")
    
    return output_filename


def create_comparison_plot(background, running_data, frames):
    """
    Creëer een vergelijkingsplot van verschillende aspecten van de animatie.
    
    Args:
        background (np.ndarray): Hersenachtergrond data
        running_data (np.ndarray): Rennende animatie data
        frames (int): Aantal frames
    """
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))  # Groter voor hoge resolutie
    fig.suptitle("🏃 Hoge Resolutie Rennend Mannetje Door Hersenen - Analyse", fontsize=18, fontweight='bold')
    
    # Plot 1: Grijstinten hersenachtergrond
    axes[0, 0].imshow(background, cmap='gray')
    axes[0, 0].set_title("🧠 Hoge Resolutie Grijstinten\nHersenachtergrond (Hoog Contrast)")
    axes[0, 0].axis('off')
    
    # Plot 2: Eerste frame van verbeterd rennend figuur
    axes[0, 1].imshow(running_data[:, :, 0], cmap='plasma')
    axes[0, 1].set_title("🏃 Hoge Resolutie Rennend Figuur\n(Frame 1 - Schuine Armen)")
    axes[0, 1].axis('off')
    
    # Plot 3: Midden frame
    mid_frame = frames // 2
    axes[0, 2].imshow(running_data[:, :, mid_frame], cmap='plasma')
    axes[0, 2].set_title(f"🏃 Hoge Resolutie Rennend Figuur\n(Frame {mid_frame} - Natuurlijke Pose)")
    axes[0, 2].axis('off')
    
    # Plot 4: Overlay voorbeeld (grijze achtergrond + gekleurde figuur)
    axes[1, 0].imshow(background, cmap='gray')
    axes[1, 0].imshow(running_data[:, :, 0], cmap='plasma', alpha=0.9)
    axes[1, 0].set_title("🎭 Hoge Resolutie Overlay\n(Grijs + Geel/Rood/Oranje)")
    axes[1, 0].axis('off')
    
    # Plot 5: Bewegingsspoor (maximum projectie)
    movement_trace = np.max(running_data, axis=2)
    axes[1, 1].imshow(background, cmap='gray')
    axes[1, 1].imshow(movement_trace, cmap='plasma', alpha=0.7)
    axes[1, 1].set_title("🗺️ Hoge Resolutie Bewegingsspoor\n(Max Projectie op Grijs)")
    axes[1, 1].axis('off')
    
    # Plot 6: Intensiteit over tijd
    # Bereken gemiddelde intensiteit per frame
    intensities = [np.sum(running_data[:, :, f]) for f in range(frames)]
    axes[1, 2].plot(intensities, 'orange', linewidth=3, alpha=0.8)
    axes[1, 2].set_title("📈 Activiteit Over Tijd\n(Hoge Resolutie Beweging)")
    axes[1, 2].set_xlabel("Frame")
    axes[1, 2].set_ylabel("Totale Intensiteit")
    axes[1, 2].grid(True, alpha=0.3)
    axes[1, 2].set_facecolor('lightgray')
    
    plt.tight_layout()
    plt.savefig("rennend_mannetje_vergelijking_hd.png", dpi=200, bbox_inches='tight')  # Verhoogde DPI
    plt.close()
    print("   📊 Hoge resolutie vergelijkingsplot opgeslagen als: rennend_mannetje_vergelijking_hd.png")


def create_path_visualization(width, height, frames, background):
    """
    Visualiseer het bewegingspad van het rennende mannetje.
    
    Args:
        width (int): Breedte van het gebied
        height (int): Hoogte van het gebied
        frames (int): Aantal frames
        background (np.ndarray): Hersenachtergrond
    """
    # Genereer het pad opnieuw voor visualisatie
    path = create_brain_path(width, height, frames)
    
    fig, ax = plt.subplots(figsize=(14, 12))  # Groter voor hoge resolutie
    
    # Toon grijstinten hersenachtergrond
    ax.imshow(background, cmap='gray', alpha=0.8)
    
    # Plot het bewegingspad
    x_coords = [pos[0] for pos in path]
    y_coords = [pos[1] for pos in path]
    
    # Plot pad als lijn met kleurverloop (plasma colormap voor consistentie)
    for i in range(len(path) - 1):
        color_intensity = i / len(path)
        ax.plot([x_coords[i], x_coords[i+1]], [y_coords[i], y_coords[i+1]], 
                color=plt.cm.plasma(color_intensity), linewidth=5, alpha=0.9)  # Dikkere lijn voor hoge resolutie
    
    # Markeer start en eind punten
    ax.plot(x_coords[0], y_coords[0], 'go', markersize=18, label='🏁 Start', markeredgecolor='white', markeredgewidth=3)
    ax.plot(x_coords[-1], y_coords[-1], 'ro', markersize=18, label='🎯 Eind', markeredgecolor='white', markeredgewidth=3)
    
    # Markeer enkele interessante punten
    waypoint_indices = [len(path)//4, len(path)//2, 3*len(path)//4]
    for i, idx in enumerate(waypoint_indices):
        ax.plot(x_coords[idx], y_coords[idx], 'yo', markersize=12, alpha=0.9, markeredgecolor='orange', markeredgewidth=3)
        ax.annotate(f'Punt {i+1}', (x_coords[idx], y_coords[idx]), 
                   xytext=(10, 10), textcoords='offset points', 
                   fontsize=12, color='yellow', fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.4", facecolor='orange', alpha=0.8))
    
    ax.set_title("🗺️ Bewegingspad van het Hoge Resolutie Rennende Mannetje\nDoor de Grijstinten Hersenen", 
                fontsize=16, fontweight='bold')
    ax.set_xlabel("X-positie (pixels)")
    ax.set_ylabel("Y-positie (pixels)")
    ax.legend(fontsize=14)
    ax.grid(True, alpha=0.3, color='white')
    
    # Voeg wat annotaties toe over hersengebieden
    annotations = [
        (width * 0.2, height * 0.3, "Frontale\nCortex"),
        (width * 0.6, height * 0.4, "Pariëtale\nCortex"),
        (width * 0.5, height * 0.7, "Cerebellum\nGebied"),
        (width * 0.8, height * 0.3, "Temporale\nCortex")
    ]
    
    for x, y, label in annotations:
        ax.annotate(label, (x, y), xytext=(15, 15), textcoords='offset points',
                   bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue', alpha=0.9, edgecolor='navy'),
                   fontsize=11, ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig("rennend_mannetje_bewegingspad_hd.png", dpi=200, bbox_inches='tight')  # Verhoogde DPI
    plt.close()
    print("   🗺️ Hoge resolutie bewegingspad visualisatie opgeslagen als: rennend_mannetje_bewegingspad_hd.png")


def main():
    """
    Hoofdfunctie voor de hoge resolutie rennend mannetje demo.
    """
    try:
        # Voer de hoge resolutie demo uit
        output_file = create_running_demo()
        
        print(f"\n🚀 Hoge resolutie demo succesvol voltooid!")
        print(f"\n🎬 Je kunt nu de hoge resolutie animatie bekijken: {output_file}")
        print(f"🔍 Bekijk ook de analyse bestanden voor meer details.")
        print(f"\n💡 Deze hoge resolutie demo toont:")
        print(f"   🔍 Verdubbelde pixeldichtheid voor scherpere weergave")
        print(f"   ✨ Verhoogde DPI (200) voor professionele kwaliteit")
        print(f"   🏃 Groter rennend figuur voor betere zichtbaarheid")
        print(f"   🎨 Grijstinten hersenachtergrond met hoog contrast")
        print(f"   🌈 Behoud van mooie geel/rood/oranje kleuren")
        print(f"   ⚡ Behoud van animatiesnelheid en timing")
        print(f"   🌐 Geoptimaliseerd voor web gebruik")
        print(f"\n🧠 Veel plezier met je eigen hoge resolutie hersenvisualisaties!")
        
    except Exception as e:
        print(f"\n❌ Er is een fout opgetreden: {e}")
        print(f"Controleer of alle vereiste packages zijn geïnstalleerd:")
        print(f"pip install numpy matplotlib scipy")
        raise


if __name__ == "__main__":
    main()