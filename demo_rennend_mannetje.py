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
    Creëer een eenvoudig rennend mannetje sprite.
    
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
    
    # Animatie cyclus voor rennende beweging (4 frames cyclus)
    pose = frame % 4
    
    # Hoofd (altijd aanwezig)
    sprite[center_y-size//2:center_y-size//4, center_x-size//4:center_x+size//4] = intensity
    
    # Lichaam
    sprite[center_y-size//4:center_y+size//2, center_x-size//6:center_x+size//6] = intensity
    
    # Armen (bewegen tijdens rennen)
    if pose in [0, 2]:  # Armen naar voren/achteren
        # Linker arm
        sprite[center_y-size//6:center_y+size//6, center_x-size//2:center_x-size//4] = intensity * 0.8
        # Rechter arm  
        sprite[center_y-size//6:center_y+size//6, center_x+size//4:center_x+size//2] = intensity * 0.8
    else:  # Armen in andere positie
        # Linker arm
        sprite[center_y:center_y+size//3, center_x-size//2:center_x-size//4] = intensity * 0.8
        # Rechter arm
        sprite[center_y-size//6:center_y+size//6, center_x+size//4:center_x+size//2] = intensity * 0.8
    
    # Benen (rennende beweging)
    if pose == 0:  # Linker been vooruit
        sprite[center_y+size//2:center_y+size, center_x-size//4:center_x-size//8] = intensity * 0.9
        sprite[center_y+size//3:center_y+3*size//4, center_x+size//8:center_x+size//4] = intensity * 0.9
    elif pose == 1:  # Beide benen samen
        sprite[center_y+size//2:center_y+size, center_x-size//6:center_x+size//6] = intensity * 0.9
    elif pose == 2:  # Rechter been vooruit
        sprite[center_y+size//2:center_y+size, center_x+size//8:center_x+size//4] = intensity * 0.9
        sprite[center_y+size//3:center_y+3*size//4, center_x-size//4:center_x-size//8] = intensity * 0.9
    else:  # Beide benen samen (andere fase)
        sprite[center_y+size//2:center_y+size, center_x-size//6:center_x+size//6] = intensity * 0.9
    
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
    Creëer een geavanceerde hersenachtergrond met meer detail.
    
    Args:
        width (int): Breedte van de achtergrond
        height (int): Hoogte van de achtergrond
        
    Returns:
        np.ndarray: 2D array met hersenachtergrond
    """
    print(f"🧠 Creëren van geavanceerde hersenachtergrond ({width}x{height})...")
    
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
    
    # Voeg hersenvouwen toe (sulci en gyri)
    structure = np.zeros((height, width))
    
    # Meerdere lagen van structuur
    for i in range(8):
        # Verschillende frequenties voor verschillende structuren
        freq_x = np.random.uniform(0.05, 0.4)
        freq_y = np.random.uniform(0.05, 0.4)
        phase_x = np.random.uniform(0, 2*np.pi)
        phase_y = np.random.uniform(0, 2*np.pi)
        amplitude = np.random.uniform(0.1, 0.3)
        
        wave = amplitude * np.sin(freq_x * x_coords + phase_x) * np.sin(freq_y * y_coords + phase_y)
        structure += wave
    
    # Voeg radiale patronen toe (zoals echte hersenvouwen)
    distance_from_center = np.sqrt((x_coords - center_x)**2 + (y_coords - center_y)**2)
    radial_pattern = 0.2 * np.sin(distance_from_center * 0.3) * np.exp(-distance_from_center / (width * 0.3))
    structure += radial_pattern
    
    # Combineer alles
    background = np.where(brain_mask, 0.5 + 0.3 * structure, 0.0)
    
    # Voeg subtiele ruis toe
    noise = 0.03 * np.random.normal(0, 1, (height, width))
    background += noise
    
    # Normaliseer en clip
    background = np.clip(background, 0, 1)
    
    # Maak de randen zachter
    edge_softness = 3
    for i in range(edge_softness):
        mask_soft = ellipse <= (1.0 + i * 0.1)
        background = np.where(mask_soft, background, background * (1 - i * 0.3))
    
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
    print(f"🏃 Genereren van rennend mannetje animatie ({width}x{height}, {frames} frames)...")
    
    # Initialiseer animatie data
    animation_data = np.zeros((height, width, frames))
    
    # Creëer bewegingspad
    path = create_brain_path(width, height, frames)
    
    print(f"📍 Bewegingspad gecreëerd met {len(path)} posities")
    
    # Voor elk frame
    for frame in range(frames):
        # Krijg huidige positie
        pos_x, pos_y = path[frame]
        
        # Creëer rennend figuur sprite voor dit frame
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
            dust_intensity = 0.3 * np.exp(-0.1 * frame)  # Vervaging over tijd
            
            # Voeg kleine stofwolkjes toe
            for i in range(3):
                dust_x = int(prev_pos_x + np.random.normal(0, 2))
                dust_y = int(prev_pos_y + np.random.normal(0, 2))
                
                if 0 <= dust_x < width and 0 <= dust_y < height:
                    animation_data[dust_y, dust_x, frame] += dust_intensity * np.random.uniform(0.5, 1.0)
    
    print(f"✅ Rennend mannetje animatie gegenereerd!")
    print(f"   Intensiteit range: {animation_data.min():.3f} - {animation_data.max():.3f}")
    
    return animation_data


def create_running_demo():
    """
    Hoofdfunctie om de rennend mannetje demo te creëren.
    
    Returns:
        str: Pad naar het gegenereerde GIF bestand
    """
    print("🎬" + "="*58 + "🎬")
    print("    DEMO: RENNEND MANNETJE DOOR HERSENEN")
    print("🎬" + "="*58 + "🎬")
    print()
    print("Welkom bij deze speelse demonstratie van BewegendeHersenen!")
    print("In plaats van traditionele fMRI activatie, zien we een")
    print("rennend mannetje dat door verschillende hersengebieden beweegt.")
    print()
    
    # Instellingen
    width, height = 80, 80
    frames = 60
    sprite_size = 6
    
    print("⚙️  Animatie instellingen:")
    print(f"   📐 Resolutie: {width}x{height} pixels")
    print(f"   🎞️  Frames: {frames}")
    print(f"   🏃 Sprite grootte: {sprite_size}x{sprite_size}")
    print()
    
    # Stap 1: Creëer hersenachtergrond
    print("Stap 1: Hersenachtergrond creëren...")
    brain_background = create_brain_background_advanced(width, height)
    
    # Sla achtergrond op als PNG voor gebruik
    background_filename = "rennend_mannetje_brain_background.png"
    plt.figure(figsize=(8, 8))
    plt.imshow(brain_background, cmap='gray', vmin=0, vmax=1)
    plt.title("Hersenachtergrond voor Rennend Mannetje Demo")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(background_filename, dpi=150, bbox_inches='tight', facecolor='black')
    plt.close()
    print(f"   💾 Achtergrond opgeslagen als: {background_filename}")
    
    # Stap 2: Genereer rennend mannetje animatie data
    print("\nStap 2: Rennend mannetje animatie genereren...")
    running_data = generate_running_animation_data(width, height, frames, sprite_size)
    
    # Stap 3: Creëer animatie met hersenachtergrond
    print("\nStap 3: Animatie met hersenachtergrond combineren...")
    
    # Gebruik de BewegendeHersenen library
    animatie = BewegendHersenAnimatie(
        colormap='plasma',  # Mooie kleurovergang voor het rennende figuur
        interval=120,       # 120ms tussen frames = ~8.3 FPS
        background_image=background_filename,
        overlay_alpha=0.9   # Rennend figuur goed zichtbaar
    )
    
    # Laad de rennende data
    animatie.load_data(running_data)
    
    # Genereer de finale animatie
    output_filename = "rennend_mannetje_door_hersenen.gif"
    print(f"   🎬 Creëren van finale animatie: {output_filename}")
    
    animation_obj = animatie.create_animation(
        output_path=output_filename,
        figsize=(10, 10),
        dpi=120,
        title="🏃 Rennend Mannetje Door de Hersenen 🧠",
        show_colorbar=False  # Geen colorbar nodig voor deze demo
    )
    
    # Stap 4: Maak een vergelijkingsplot
    print("\nStap 4: Vergelijkingsplot maken...")
    create_comparison_plot(brain_background, running_data, frames)
    
    # Stap 5: Maak een bewegingspad visualisatie
    print("\nStap 5: Bewegingspad visualisatie...")
    create_path_visualization(width, height, frames, brain_background)
    
    print("\n🎉 Rennend mannetje demo voltooid!")
    print(f"\n📁 Gegenereerde bestanden:")
    print(f"   🎬 {output_filename} - Hoofdanimatie")
    print(f"   🖼️  {background_filename} - Hersenachtergrond")
    print(f"   📊 rennend_mannetje_vergelijking.png - Vergelijkingsplot")
    print(f"   🗺️  rennend_mannetje_bewegingspad.png - Pad visualisatie")
    
    print(f"\n💡 Deze demo toont hoe de BewegendeHersenen library gebruikt")
    print(f"   kan worden voor creatieve en educatieve visualisaties!")
    print(f"   Perfect voor presentaties over hersenactiviteit en")
    print(f"   wetenschapscommunicatie.")
    
    return output_filename


def create_comparison_plot(background, running_data, frames):
    """
    Creëer een vergelijkingsplot van verschillende aspecten van de animatie.
    
    Args:
        background (np.ndarray): Hersenachtergrond data
        running_data (np.ndarray): Rennende animatie data
        frames (int): Aantal frames
    """
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle("🏃 Rennend Mannetje Door Hersenen - Analyse", fontsize=16, fontweight='bold')
    
    # Plot 1: Hersenachtergrond alleen
    axes[0, 0].imshow(background, cmap='gray')
    axes[0, 0].set_title("🧠 Hersenachtergrond")
    axes[0, 0].axis('off')
    
    # Plot 2: Eerste frame van rennend figuur
    axes[0, 1].imshow(running_data[:, :, 0], cmap='plasma')
    axes[0, 1].set_title("🏃 Rennend Figuur (Frame 1)")
    axes[0, 1].axis('off')
    
    # Plot 3: Midden frame
    mid_frame = frames // 2
    axes[0, 2].imshow(running_data[:, :, mid_frame], cmap='plasma')
    axes[0, 2].set_title(f"🏃 Rennend Figuur (Frame {mid_frame})")
    axes[0, 2].axis('off')
    
    # Plot 4: Overlay voorbeeld (achtergrond + figuur)
    axes[1, 0].imshow(background, cmap='gray')
    axes[1, 0].imshow(running_data[:, :, 0], cmap='plasma', alpha=0.9)
    axes[1, 0].set_title("🎭 Overlay (Frame 1)")
    axes[1, 0].axis('off')
    
    # Plot 5: Bewegingsspoor (maximum projectie)
    movement_trace = np.max(running_data, axis=2)
    axes[1, 1].imshow(background, cmap='gray')
    axes[1, 1].imshow(movement_trace, cmap='plasma', alpha=0.7)
    axes[1, 1].set_title("🗺️ Bewegingsspoor (Max Projectie)")
    axes[1, 1].axis('off')
    
    # Plot 6: Intensiteit over tijd
    # Bereken gemiddelde intensiteit per frame
    intensities = [np.sum(running_data[:, :, f]) for f in range(frames)]
    axes[1, 2].plot(intensities, 'b-', linewidth=2)
    axes[1, 2].set_title("📈 Activiteit Over Tijd")
    axes[1, 2].set_xlabel("Frame")
    axes[1, 2].set_ylabel("Totale Intensiteit")
    axes[1, 2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("rennend_mannetje_vergelijking.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("   📊 Vergelijkingsplot opgeslagen als: rennend_mannetje_vergelijking.png")


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
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Toon hersenachtergrond
    ax.imshow(background, cmap='gray', alpha=0.7)
    
    # Plot het bewegingspad
    x_coords = [pos[0] for pos in path]
    y_coords = [pos[1] for pos in path]
    
    # Plot pad als lijn met kleurverloop
    for i in range(len(path) - 1):
        color_intensity = i / len(path)
        ax.plot([x_coords[i], x_coords[i+1]], [y_coords[i], y_coords[i+1]], 
                color=plt.cm.plasma(color_intensity), linewidth=3, alpha=0.8)
    
    # Markeer start en eind punten
    ax.plot(x_coords[0], y_coords[0], 'go', markersize=12, label='🏁 Start')
    ax.plot(x_coords[-1], y_coords[-1], 'ro', markersize=12, label='🎯 Eind')
    
    # Markeer enkele interessante punten
    waypoint_indices = [len(path)//4, len(path)//2, 3*len(path)//4]
    for i, idx in enumerate(waypoint_indices):
        ax.plot(x_coords[idx], y_coords[idx], 'yo', markersize=8, alpha=0.8)
        ax.annotate(f'Punt {i+1}', (x_coords[idx], y_coords[idx]), 
                   xytext=(5, 5), textcoords='offset points', 
                   fontsize=10, color='yellow', fontweight='bold')
    
    ax.set_title("🗺️ Bewegingspad van het Rennende Mannetje Door de Hersenen", 
                fontsize=14, fontweight='bold')
    ax.set_xlabel("X-positie (pixels)")
    ax.set_ylabel("Y-positie (pixels)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Voeg wat annotaties toe over hersengebieden
    annotations = [
        (width * 0.2, height * 0.3, "Frontale\nCortex"),
        (width * 0.6, height * 0.4, "Pariëtale\nCortex"),
        (width * 0.5, height * 0.7, "Cerebellum\nGebied"),
        (width * 0.8, height * 0.3, "Temporale\nCortex")
    ]
    
    for x, y, label in annotations:
        ax.annotate(label, (x, y), xytext=(10, 10), textcoords='offset points',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.7),
                   fontsize=9, ha='center')
    
    plt.tight_layout()
    plt.savefig("rennend_mannetje_bewegingspad.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("   🗺️ Bewegingspad visualisatie opgeslagen als: rennend_mannetje_bewegingspad.png")


def main():
    """
    Hoofdfunctie voor de rennend mannetje demo.
    """
    try:
        # Voer de demo uit
        output_file = create_running_demo()
        
        print(f"\n🚀 Demo succesvol voltooid!")
        print(f"\n🎬 Je kunt nu de animatie bekijken: {output_file}")
        print(f"🔍 Bekijk ook de analyse bestanden voor meer details.")
        print(f"\n💡 Deze demo laat zien hoe creatief je kunt zijn met")
        print(f"   de BewegendeHersenen library. Experimenteer met:")
        print(f"   • Verschillende bewegingspatronen")
        print(f"   • Andere sprite vormen")
        print(f"   • Verschillende hersenachtergronden")
        print(f"   • Meerdere figuren tegelijk")
        print(f"\n🧠 Veel plezier met je eigen hersenvisualisaties!")
        
    except Exception as e:
        print(f"\n❌ Er is een fout opgetreden: {e}")
        print(f"Controleer of alle vereiste packages zijn geïnstalleerd:")
        print(f"pip install numpy matplotlib scipy")
        raise


if __name__ == "__main__":
    main()