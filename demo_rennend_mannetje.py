#!/usr/bin/env python3
"""
Demo: Rennend Mannetje met Achtergrondafbeelding

Deze demo toont een rennend mannetje animatie met gebruik van het lokale 
afbeelding_achtergrond.png bestand als achtergrond. Het rennende mannetje 
wordt gevisualiseerd in oranje/gele/rode kleuren (plasma colormap) en 
beweegt over de statische achtergrondafbeelding.

Features:
- Gebruik van lokale afbeelding_achtergrond.png als achtergrond
- Rennend mannetje in plasma colormap (oranje/geel/rood)
- Professionele overlay met correcte transparantie
- Hoge resolutie output als rennend_mannetje_met_achtergrond.gif
- Automatische achtergrond generatie indien niet aanwezig

Auteur: BewegendeHersenen Project
Versie: 1.2
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from bewegende_hersenen import (BewegendHersenAnimatie, 
                               maak_animatie_met_statische_achtergrond,
                               zoek_standaard_achtergrond)

def generate_running_animation_data(width=80, height=80, frames=40):
    """
    Genereer animatie data voor een rennend mannetje.
    
    Het mannetje beweegt van links naar rechts over het scherm met
    realistische loop-bewegingen en plasma colormap kleuren.
    
    Args:
        width (int): Breedte van de animatie in pixels
        height (int): Hoogte van de animatie in pixels
        frames (int): Aantal frames voor de animatie
        
    Returns:
        np.ndarray: 3D array met shape (height, width, frames) met rennende figuur data
    """
    print(f"🏃 Genereren van rennende mannetje animatie data ({width}x{height}, {frames} frames)...")
    
    # Initialiseer lege data array
    data = np.zeros((height, width, frames))
    
    # Parameters voor het rennende mannetje
    figure_width = width // 12   # Breedte van het mannetje
    figure_height = height // 8  # Hoogte van het mannetje
    ground_level = int(height * 0.75)  # Grond niveau (75% van de hoogte)
    
    # Bewegingsparameters
    start_x = figure_width
    end_x = width - figure_width * 2
    
    for frame in range(frames):
        frame_data = np.zeros((height, width))
        
        # Bereken positie van het mannetje (lineaire beweging van links naar rechts)
        progress = frame / (frames - 1)
        current_x = int(start_x + progress * (end_x - start_x))
        
        # Bereken verticale beweging (subtiele op-en-neer beweging tijdens rennen)
        bounce_amplitude = 3  # Pixels op en neer
        bounce_frequency = 4  # Aantal bounces tijdens de hele animatie
        vertical_offset = int(bounce_amplitude * np.sin(2 * np.pi * bounce_frequency * progress))
        current_y = ground_level + vertical_offset
        
        # Creëer het rennende mannetje als een eenvoudige figuur
        figure_sprite = create_running_figure_sprite(figure_width, figure_height, frame, frames)
        
        # Plaats de figuur in het frame
        y_start = max(0, current_y - figure_height//2)
        y_end = min(height, current_y + figure_height//2)
        x_start = max(0, current_x - figure_width//2)
        x_end = min(width, current_x + figure_width//2)
        
        # Bereken de daadwerkelijke dimensies voor de sprite
        actual_height = y_end - y_start
        actual_width = x_end - x_start
        
        if actual_height > 0 and actual_width > 0:
            # Schaal de sprite naar de beschikbare ruimte
            sprite_resized = np.resize(figure_sprite, (actual_height, actual_width))
            frame_data[y_start:y_end, x_start:x_end] = sprite_resized
        
        # Voeg wat stofwolkjes toe achter het rennende mannetje (voor effect)
        if frame > 0:  # Alleen na de eerste frame
            dust_intensity = 0.3
            dust_x = max(0, current_x - figure_width)
            dust_y = ground_level
            
            # Creëer kleine stofwolk
            dust_size = 5
            if (dust_x >= 0 and dust_x < width - dust_size and 
                dust_y >= 0 and dust_y < height - dust_size):
                
                # Gaussische stofwolk
                y_dust, x_dust = np.ogrid[:dust_size, :dust_size]
                dust_center = dust_size // 2
                dust_pattern = dust_intensity * np.exp(
                    -((x_dust - dust_center)**2 + (y_dust - dust_center)**2) / (2 * (dust_size/3)**2)
                )
                
                frame_data[dust_y:dust_y+dust_size, dust_x:dust_x+dust_size] += dust_pattern
        
        # Voeg subtiele ruis toe voor textuur
        noise = 0.02 * np.random.normal(0, 1, (height, width))
        frame_data += noise
        
        # Zorg ervoor dat waarden binnen 0-1 range blijven
        frame_data = np.clip(frame_data, 0, 1)
        
        data[:, :, frame] = frame_data
    
    print(f"✅ Rennende mannetje data gegenereerd!")
    print(f"📊 Data eigenschappen: intensiteit range {data.min():.3f} - {data.max():.3f}")
    print(f"🎯 Figuur beweegt van x={start_x} naar x={end_x} over {frames} frames")
    
    return data

def create_running_figure_sprite(width, height, frame, total_frames):
    """
    Creëer een sprite van een rennende figuur voor een specifieke frame.
    
    Args:
        width (int): Breedte van de sprite
        height (int): Hoogte van de sprite
        frame (int): Huidige frame nummer
        total_frames (int): Totaal aantal frames
        
    Returns:
        np.ndarray: 2D array met de figuur sprite
    """
    sprite = np.zeros((height, width))
    
    # Animatie cyclus voor been beweging (2 cycli tijdens de hele animatie)
    leg_cycle = (frame / total_frames) * 4 * np.pi
    leg_offset = int(2 * np.sin(leg_cycle))  # Been beweging offset
    
    # Hoofd (bovenkant)
    head_size = max(1, width // 4)
    head_y = height // 6
    head_x_start = max(0, width//2 - head_size//2)
    head_x_end = min(width, width//2 + head_size//2)
    head_y_start = max(0, head_y - head_size//2)
    head_y_end = min(height, head_y + head_size//2)
    
    if head_y_end > head_y_start and head_x_end > head_x_start:
        sprite[head_y_start:head_y_end, head_x_start:head_x_end] = 0.9
    
    # Lichaam (midden)
    body_width = max(1, width // 6)
    body_height = max(1, height // 3)
    body_x_start = max(0, width//2 - body_width//2)
    body_x_end = min(width, width//2 + body_width//2)
    body_y_start = max(0, height//3)
    body_y_end = min(height, height//3 + body_height)
    
    if body_y_end > body_y_start and body_x_end > body_x_start:
        sprite[body_y_start:body_y_end, body_x_start:body_x_end] = 0.8
    
    # Benen (onderkant) - met animatie
    leg_width = max(1, width // 8)
    leg_height = max(1, height // 3)
    
    # Linker been
    left_leg_x = max(0, width//2 - leg_width - abs(leg_offset))
    left_leg_x_end = min(width, left_leg_x + leg_width)
    leg_y_start = max(0, 2*height//3)
    leg_y_end = min(height, leg_y_start + leg_height)
    
    if leg_y_end > leg_y_start and left_leg_x_end > left_leg_x:
        sprite[leg_y_start:leg_y_end, left_leg_x:left_leg_x_end] = 0.7
    
    # Rechter been
    right_leg_x = max(0, width//2 + abs(leg_offset))
    right_leg_x_end = min(width, right_leg_x + leg_width)
    
    if leg_y_end > leg_y_start and right_leg_x_end > right_leg_x:
        sprite[leg_y_start:leg_y_end, right_leg_x:right_leg_x_end] = 0.7
    
    # Armen (met tegengestelde beweging van benen)
    arm_offset = -leg_offset  # Armen bewegen tegengesteld aan benen
    arm_width = max(1, width // 10)
    arm_height = max(1, height // 4)
    arm_y_start = max(0, height//3 + height//6)
    arm_y_end = min(height, arm_y_start + arm_height)
    
    # Linker arm
    left_arm_x = max(0, width//4 + arm_offset//2)
    left_arm_x_end = min(width, left_arm_x + arm_width)
    
    if arm_y_end > arm_y_start and left_arm_x_end > left_arm_x:
        sprite[arm_y_start:arm_y_end, left_arm_x:left_arm_x_end] = 0.6
    
    # Rechter arm
    right_arm_x = max(0, 3*width//4 - arm_offset//2)
    right_arm_x_end = min(width, right_arm_x + arm_width)
    
    if arm_y_end > arm_y_start and right_arm_x_end > right_arm_x:
        sprite[arm_y_start:arm_y_end, right_arm_x:right_arm_x_end] = 0.6
    
    return sprite

def create_brain_path():
    """
    Definieer een bewegingspad dat lijkt op een hersenvorm (voor toekomstige uitbreiding).
    
    Returns:
        list: Lijst van (x, y) coördinaten voor het pad
    """
    # Voor nu een eenvoudig lineair pad, maar kan uitgebreid worden naar hersenvorm
    path_points = []
    
    # Lineair pad van links naar rechts
    for i in range(40):
        x = i * 2
        y = 40 + 5 * np.sin(i * 0.3)  # Lichte golfbeweging
        path_points.append((x, y))
    
    return path_points

def ensure_background_exists():
    """
    Zorg ervoor dat afbeelding_achtergrond.png bestaat.
    Als het bestand niet bestaat, genereer het automatisch.
    
    Returns:
        str: Pad naar de achtergrond afbeelding
    """
    background_filename = "afbeelding_achtergrond.png"
    
    # Controleer of het bestand al bestaat
    if os.path.exists(background_filename):
        print(f"✅ Achtergrond afbeelding gevonden: {background_filename}")
        return background_filename
    
    print(f"⚠️  Achtergrond afbeelding niet gevonden: {background_filename}")
    print("🎨 Automatisch genereren van achtergrond afbeelding...")
    
    # Importeer en gebruik het create_background script
    try:
        # Inline implementatie van achtergrond generatie
        width, height = 100, 100
        y_coords, x_coords = np.ogrid[:height, :width]
        
        # Creëer een landschap-achtige achtergrond
        sky_gradient = np.linspace(0.8, 0.4, height).reshape(-1, 1)
        background = np.tile(sky_gradient, (1, width))
        
        # Voeg wolken toe
        for i in range(3):
            cloud_x = np.random.randint(width//4, 3*width//4)
            cloud_y = np.random.randint(height//6, height//3)
            cloud_size_x = np.random.randint(width//8, width//4)
            cloud_size_y = np.random.randint(height//12, height//8)
            
            cloud_pattern = np.exp(-((x_coords - cloud_x)**2 / (2 * cloud_size_x**2) + 
                                    (y_coords - cloud_y)**2 / (2 * cloud_size_y**2)))
            background += 0.15 * cloud_pattern
        
        # Horizon en grond textuur
        horizon_y = int(height * 0.7)
        background[horizon_y:horizon_y+2, :] *= 0.9
        ground_texture = np.random.normal(0, 0.02, (height - horizon_y, width))
        background[horizon_y:, :] += ground_texture
        
        # Heuvels
        for i in range(2):
            hill_center = np.random.randint(width//4, 3*width//4)
            hill_width = np.random.randint(width//6, width//3)
            hill_height = np.random.randint(height//20, height//10)
            
            hill_x = np.arange(max(0, hill_center - hill_width), 
                              min(width, hill_center + hill_width))
            if len(hill_x) > 0:
                hill_profile = hill_height * np.exp(-((hill_x - hill_center)**2) / (2 * (hill_width/3)**2))
                
                for j, x in enumerate(hill_x):
                    hill_top = horizon_y - int(hill_profile[j])
                    if hill_top >= 0:
                        background[hill_top:horizon_y, x] *= 0.85
        
        # Ruis en normalisatie
        noise = 0.03 * np.random.normal(0, 1, (height, width))
        background += noise
        background = np.clip(background, 0, 1)
        
        # Opslaan
        plt.figure(figsize=(12, 12))
        plt.imshow(background, cmap='gray', vmin=0, vmax=1)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(background_filename, dpi=200, bbox_inches='tight', 
                   facecolor='white', edgecolor='none', pad_inches=0)
        plt.close()
        
        print(f"✅ Achtergrond automatisch gegenereerd: {background_filename}")
        return background_filename
        
    except Exception as e:
        print(f"❌ Fout bij genereren achtergrond: {e}")
        print("💡 Plaats handmatig een 'afbeelding_achtergrond.png' bestand in de directory")
        return None

def create_running_demo():
    """
    Hoofdfunctie voor het creëren van de rennende mannetje demo.
    
    Deze functie:
    1. Zorgt ervoor dat afbeelding_achtergrond.png bestaat
    2. Genereert rennende mannetje animatie data
    3. Creëert de animatie met achtergrond overlay
    4. Slaat de animatie op als rennend_mannetje_met_achtergrond.gif
    
    Returns:
        matplotlib.animation.FuncAnimation: De gemaakte animatie
    """
    print("🏃‍♂️" + "="*58 + "🏃‍♂️")
    print("    RENNEND MANNETJE DEMO MET ACHTERGROND AFBEELDING")
    print("🏃‍♂️" + "="*58 + "🏃‍♂️")
    print()
    print("Deze demo toont:")
    print("• 🖼️  Gebruik van lokale afbeelding_achtergrond.png")
    print("• 🏃 Rennend mannetje in plasma colormap (oranje/geel/rood)")
    print("• 🎨 Professionele overlay met correcte transparantie")
    print("• 📁 Output als rennend_mannetje_met_achtergrond.gif")
    print("• 🔄 Automatische achtergrond generatie indien nodig")
    print()
    
    try:
        # Stap 1: Zorg ervoor dat achtergrond bestaat
        print("Stap 1: Controleren en voorbereiden achtergrond afbeelding...")
        background_path = ensure_background_exists()
        
        if background_path is None:
            raise FileNotFoundError("Kon geen achtergrond afbeelding maken of vinden")
        
        # Stap 2: Genereer rennende mannetje data
        print("\\nStap 2: Genereren rennende mannetje animatie data...")
        running_data = generate_running_animation_data(width=100, height=100, frames=50)
        
        # Stap 3: Maak animatie met achtergrond
        print("\\nStap 3: Creëren animatie met achtergrond overlay...")
        
        # Gebruik de convenience functie voor statische achtergrond
        animation_obj = maak_animatie_met_statische_achtergrond(
            running_data,
            achtergrond_pad=background_path,
            output_path="rennend_mannetje_met_achtergrond.gif",
            overlay_alpha=0.8,  # Hoge transparantie voor duidelijke zichtbaarheid
            colormap='plasma',  # Oranje/gele/rode kleuren zoals gevraagd
            interval=120        # 120ms tussen frames = ~8.3 FPS
        )
        
        print("\\n✅ Rennende mannetje demo succesvol voltooid!")
        print("📁 Output bestand: rennend_mannetje_met_achtergrond.gif")
        print("🎨 Achtergrond: afbeelding_achtergrond.png")
        print("🎯 Colormap: plasma (oranje/geel/rood)")
        print("⚡ Frame rate: ~8.3 FPS")
        print("🔍 Overlay transparantie: 80%")
        
        # Toon enkele statistieken
        print("\\n📊 Animatie statistieken:")
        print(f"   • Resolutie: {running_data.shape[1]}x{running_data.shape[0]} pixels")
        print(f"   • Frames: {running_data.shape[2]}")
        print(f"   • Data range: {running_data.min():.3f} - {running_data.max():.3f}")
        print(f"   • Achtergrond: {background_path}")
        
        return animation_obj
        
    except Exception as e:
        print(f"\\n❌ Fout tijdens demo uitvoering: {e}")
        print("\\n🔧 Mogelijke oplossingen:")
        print("   • Controleer of numpy, matplotlib en scipy zijn geïnstalleerd")
        print("   • Zorg voor schrijfrechten in de huidige directory")
        print("   • Controleer of er voldoende schijfruimte is")
        raise

def main():
    """
    Hoofdfunctie die de demo uitvoert.
    """
    try:
        # Voer de demo uit
        animation = create_running_demo()
        
        print("\\n🎉 Demo voltooid!")
        print("\\n💡 Tips:")
        print("   • Open rennend_mannetje_met_achtergrond.gif om de animatie te bekijken")
        print("   • Pas overlay_alpha aan in de code voor verschillende transparantie effecten")
        print("   • Experimenteer met verschillende colormaps (hot, inferno, viridis)")
        print("   • Vervang afbeelding_achtergrond.png door je eigen achtergrond afbeelding")
        
        print("\\n🚀 Klaar voor gebruik in presentaties en publicaties!")
        
    except Exception as e:
        print(f"\\n💥 Demo gefaald: {e}")
        print("\\nControleer de error berichten hierboven voor meer details.")
        return False
    
    return True

if __name__ == "__main__":
    # Voer de rennende mannetje demo uit
    success = main()
    
    if success:
        print("\\n🏆 Rennende mannetje demo succesvol uitgevoerd!")
    else:
        print("\\n⚠️  Demo niet succesvol voltooid - controleer error berichten")
        exit(1)