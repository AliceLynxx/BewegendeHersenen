#!/usr/bin/env python3
"""
BewegendeHersenen Demo Script

Dit script demonstreert de volledige functionaliteit van de BewegendeHersenen library
voor het maken van fMRI-achtige animaties van numpy arrays.

Voor neurowetenschappers, onderzoekers en studenten biedt dit script:
- Realistische test data generatie die lijkt op fMRI signalen
- Verschillende visualisatie opties en colormaps
- Voorbeelden van basis en geavanceerde functionaliteit
- Hersenachtergrond overlay demonstraties
- Statische achtergrond ondersteuning (NIEUW!)
- Export naar verschillende formaten (GIF, MP4)

Auteur: BewegendeHersenen Project
Doel: Educatieve demonstratie en snelle start voor nieuwe gebruikers
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from bewegende_hersenen import (BewegendHersenAnimatie, maak_snelle_animatie, 
                               maak_animatie_met_achtergrond, maak_animatie_met_statische_achtergrond,
                               zoek_standaard_achtergrond)


def generate_brain_like_data(width=64, height=64, frames=50, noise_level=0.1):
    """
    Genereer realistische fMRI-achtige test data.
    
    Deze functie simuleert hersenactiviteit door:
    - Meerdere activatiecentra te creëren
    - Temporele dynamiek toe te voegen (activiteit die verandert over tijd)
    - Realistische ruis toe te voegen
    - Spatiale correlatie tussen nabije pixels
    
    Args:
        width (int): Breedte van de hersenscan in pixels
        height (int): Hoogte van de hersenscan in pixels  
        frames (int): Aantal tijdframes voor de animatie
        noise_level (float): Hoeveelheid ruis (0.0 = geen ruis, 1.0 = veel ruis)
        
    Returns:
        np.ndarray: 3D array met shape (height, width, frames) met fMRI-achtige data
    """
    print(f"🧠 Genereren van realistische hersendata ({width}x{height}, {frames} frames)...")
    
    # Initialiseer lege data array
    data = np.zeros((height, width, frames))
    
    # Definieer meerdere activatiecentra (simuleren verschillende hersengebieden)
    activation_centers = [
        {'x': width//4, 'y': height//4, 'intensity': 0.8, 'frequency': 0.1},      # Langzame oscillatie
        {'x': 3*width//4, 'y': height//4, 'intensity': 0.6, 'frequency': 0.2},    # Medium oscillatie  
        {'x': width//2, 'y': 3*height//4, 'intensity': 0.9, 'frequency': 0.05},   # Zeer langzame oscillatie
        {'x': width//6, 'y': 2*height//3, 'intensity': 0.4, 'frequency': 0.3},    # Snelle oscillatie
        {'x': 5*width//6, 'y': height//2, 'intensity': 0.7, 'frequency': 0.15},   # Medium-langzame oscillatie
    ]
    
    # Genereer tijdreeks voor elk frame
    time_points = np.linspace(0, 4*np.pi, frames)  # 4π radialen over alle frames
    
    for frame in range(frames):
        frame_data = np.zeros((height, width))
        
        # Voor elk activatiecentrum
        for center in activation_centers:
            # Bereken temporele activiteit (sinusoïdale oscillatie)
            temporal_activity = center['intensity'] * (
                0.5 + 0.5 * np.sin(center['frequency'] * time_points[frame])
            )
            
            # Creëer spatiale Gaussische verdeling rond het centrum
            y_coords, x_coords = np.ogrid[:height, :width]
            
            # Bereken afstand tot centrum
            distance_sq = (x_coords - center['x'])**2 + (y_coords - center['y'])**2
            
            # Gaussische activatie met realistische spreiding
            sigma = min(width, height) / 8  # Spreiding van activatie
            spatial_pattern = np.exp(-distance_sq / (2 * sigma**2))
            
            # Combineer temporele en spatiale componenten
            frame_data += temporal_activity * spatial_pattern
        
        # Voeg realistische ruis toe
        noise = noise_level * np.random.normal(0, 0.1, (height, width))
        frame_data += noise
        
        # Zorg ervoor dat waarden binnen redelijke range blijven
        frame_data = np.clip(frame_data, 0, 1)
        
        data[:, :, frame] = frame_data
    
    print(f"✅ Hersendata gegenereerd! Intensiteit range: {data.min():.3f} - {data.max():.3f}")
    return data


def create_sample_brain_background(width=64, height=64, filename="sample_brain_background.png"):
    """
    Creëer een voorbeeld hersenachtergrond afbeelding voor demonstratie.
    
    Args:
        width (int): Breedte van de achtergrond
        height (int): Hoogte van de achtergrond
        filename (str): Bestandsnaam voor opslaan
        
    Returns:
        str: Pad naar de gemaakte achtergrond afbeelding
    """
    print(f"🎨 Creëren van voorbeeld hersenachtergrond ({width}x{height})...")
    
    # Maak een hersenvormige achtergrond
    y_coords, x_coords = np.ogrid[:height, :width]
    center_x, center_y = width // 2, height // 2
    
    # Creëer een ovaalvormige basis vorm
    ellipse_a = width * 0.4  # Horizontale radius
    ellipse_b = height * 0.35  # Verticale radius
    
    # Basis ellips
    ellipse = ((x_coords - center_x) / ellipse_a)**2 + ((y_coords - center_y) / ellipse_b)**2
    brain_mask = ellipse <= 1.0
    
    # Voeg wat structuur toe (simuleer hersenvouwen/sulci)
    structure = np.zeros((height, width))
    
    # Voeg enkele "hersenvouwen" toe
    for i in range(5):
        # Willekeurige golfpatronen
        freq_x = np.random.uniform(0.1, 0.3)
        freq_y = np.random.uniform(0.1, 0.3)
        phase_x = np.random.uniform(0, 2*np.pi)
        phase_y = np.random.uniform(0, 2*np.pi)
        
        wave = 0.3 * np.sin(freq_x * x_coords + phase_x) * np.sin(freq_y * y_coords + phase_y)
        structure += wave
    
    # Combineer basis vorm met structuur
    background = np.where(brain_mask, 0.6 + 0.2 * structure, 0.0)
    
    # Voeg wat ruis toe voor realisme
    noise = 0.05 * np.random.normal(0, 1, (height, width))
    background += noise
    
    # Normaliseer naar 0-1 range
    background = np.clip(background, 0, 1)
    
    # Sla op als PNG
    plt.figure(figsize=(8, 8))
    plt.imshow(background, cmap='gray', vmin=0, vmax=1)
    plt.title("Voorbeeld Hersenachtergrond")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='black')
    plt.close()
    
    print(f"✅ Voorbeeld hersenachtergrond opgeslagen als: {filename}")
    return filename


def create_brain_background_advanced(width=80, height=80, filename="afbeelding_achtergrond.png"):
    """
    Creëer een geavanceerde hersenachtergrond afbeelding met meer detail.
    Deze wordt opgeslagen als de standaard 'afbeelding_achtergrond.png'.
    
    Args:
        width (int): Breedte van de achtergrond
        height (int): Hoogte van de achtergrond
        filename (str): Bestandsnaam voor opslaan
        
    Returns:
        str: Pad naar de gemaakte achtergrond afbeelding
    """
    print(f"🧠 Creëren van geavanceerde hersenachtergrond ({width}x{height})...")
    
    # Maak een meer realistische hersenvorm
    y_coords, x_coords = np.ogrid[:height, :width]
    center_x, center_y = width // 2, height // 2
    
    # Creëer complexere hersenvorm
    # Basis ellips
    ellipse_a = width * 0.45  # Horizontale radius
    ellipse_b = height * 0.4   # Verticale radius
    
    ellipse = ((x_coords - center_x) / ellipse_a)**2 + ((y_coords - center_y) / ellipse_b)**2
    brain_mask = ellipse <= 1.0
    
    # Voeg inhammen toe voor meer realistische vorm
    # Linker inham (temporale kwab)
    left_indent_x = center_x - width * 0.3
    left_indent_y = center_y + height * 0.1
    left_indent = ((x_coords - left_indent_x) / (width * 0.15))**2 + ((y_coords - left_indent_y) / (height * 0.2))**2
    brain_mask = brain_mask & (left_indent > 1.0)
    
    # Rechter inham
    right_indent_x = center_x + width * 0.3
    right_indent_y = center_y + height * 0.1
    right_indent = ((x_coords - right_indent_x) / (width * 0.15))**2 + ((y_coords - right_indent_y) / (height * 0.2))**2
    brain_mask = brain_mask & (right_indent > 1.0)
    
    # Creëer complexe interne structuur
    structure = np.zeros((height, width))
    
    # Voeg meerdere lagen van "hersenvouwen" toe
    for i in range(8):
        # Verschillende frequenties voor verschillende schalen
        freq_x = np.random.uniform(0.05, 0.4)
        freq_y = np.random.uniform(0.05, 0.4)
        phase_x = np.random.uniform(0, 2*np.pi)
        phase_y = np.random.uniform(0, 2*np.pi)
        
        # Verschillende amplitudes
        amplitude = np.random.uniform(0.1, 0.4)
        
        wave = amplitude * np.sin(freq_x * x_coords + phase_x) * np.sin(freq_y * y_coords + phase_y)
        structure += wave
    
    # Voeg radiale patronen toe (simuleer cortex structuur)
    distance_from_center = np.sqrt((x_coords - center_x)**2 + (y_coords - center_y)**2)
    radial_pattern = 0.2 * np.sin(distance_from_center * 0.3) * np.exp(-distance_from_center / (width * 0.3))
    structure += radial_pattern
    
    # Combineer basis vorm met complexe structuur
    background = np.where(brain_mask, 0.5 + 0.3 * structure, 0.0)
    
    # Voeg subtiele ruis toe voor textuur
    noise = 0.03 * np.random.normal(0, 1, (height, width))
    background += noise
    
    # Voeg gradient toe voor diepte effect
    gradient_y = (y_coords - height/2) / height
    gradient_effect = 0.1 * gradient_y
    background += gradient_effect * brain_mask
    
    # Normaliseer naar 0-1 range
    background = np.clip(background, 0, 1)
    
    # Sla op als PNG met hoge kwaliteit
    plt.figure(figsize=(10, 10))
    plt.imshow(background, cmap='gray', vmin=0, vmax=1)
    plt.title("Geavanceerde Hersenachtergrond")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(filename, dpi=200, bbox_inches='tight', facecolor='black')
    plt.close()
    
    print(f"✅ Geavanceerde hersenachtergrond opgeslagen als: {filename}")
    return filename


def demo_basic_animation():
    """
    Demonstreer basis animatie functionaliteit.
    
    Deze functie toont:
    - Hoe data te laden in BewegendHersenAnimatie
    - Basis animatie instellingen
    - Opslaan als GIF bestand
    """
    print("\n" + "="*60)
    print("🎬 DEMO 1: BASIS ANIMATIE FUNCTIONALITEIT")
    print("="*60)
    
    # Genereer test data
    print("Stap 1: Test data genereren...")
    brain_data = generate_brain_like_data(width=48, height=48, frames=30)
    
    # Maak animatie object
    print("Stap 2: Animatie object aanmaken...")
    animatie = BewegendHersenAnimatie(
        colormap='hot',      # Klassieke 'hete' colormap voor hersenscans
        interval=150         # 150ms tussen frames = ~6.7 FPS
    )
    
    # Laad data
    print("Stap 3: Data laden...")
    animatie.load_data(brain_data)
    
    # Maak animatie
    print("Stap 4: Animatie genereren en opslaan...")
    animation_obj = animatie.create_animation(
        output_path="demo_basis_animatie.gif",
        figsize=(10, 8),
        title="Demo: Basis fMRI-achtige Hersenactiviteit",
        show_colorbar=True
    )
    
    print("✅ Basis demo voltooid! Bestand: demo_basis_animatie.gif")
    return animation_obj


def demo_background_overlay():
    """
    Demonstreer hersenachtergrond overlay functionaliteit.
    
    Deze functie toont:
    - Hoe een hersenachtergrond te laden
    - Verschillende transparantie niveaus
    - Zowel basis als convenience functie gebruik
    """
    print("\n" + "="*60)
    print("🧠 DEMO 2: HERSENACHTERGROND OVERLAY")
    print("="*60)
    
    # Genereer test data
    print("Stap 1: fMRI test data genereren...")
    fmri_data = generate_brain_like_data(width=64, height=64, frames=40, noise_level=0.05)
    
    # Creëer voorbeeld achtergrond
    print("Stap 2: Voorbeeld hersenachtergrond creëren...")
    background_path = create_sample_brain_background(width=64, height=64)
    
    # Demo verschillende transparantie niveaus
    alpha_levels = [0.5, 0.7, 0.9]
    
    for i, alpha in enumerate(alpha_levels):
        print(f"Stap 3.{i+1}: Animatie maken met transparantie α={alpha}...")
        
        # Gebruik basis klasse
        animatie = BewegendHersenAnimatie(
            colormap='plasma',
            interval=120,
            background_image=background_path,
            overlay_alpha=alpha
        )
        
        animatie.load_data(fmri_data)
        
        output_file = f"demo_background_alpha_{alpha:.1f}.gif"
        animation_obj = animatie.create_animation(
            output_path=output_file,
            figsize=(10, 8),
            title=f"fMRI met Hersenachtergrond (α={alpha})",
            show_colorbar=True
        )
        
        print(f"   💾 Opgeslagen als: {output_file}")
    
    # Demonstreer convenience functie
    print("Stap 4: Convenience functie demonstratie...")
    convenience_animation = maak_animatie_met_achtergrond(
        fmri_data,
        background_path,
        output_path="demo_convenience_background.gif",
        overlay_alpha=0.8,
        colormap='inferno',
        interval=100
    )
    
    print("   💾 Convenience functie animatie: demo_convenience_background.gif")
    
    # Maak vergelijkingsplot
    print("Stap 5: Vergelijkingsplot maken...")
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("Hersenachtergrond Overlay Vergelijking", fontsize=16, fontweight='bold')
    
    # Toon achtergrond alleen
    background_img = plt.imread(background_path)
    axes[0, 0].imshow(background_img, cmap='gray')
    axes[0, 0].set_title("Hersenachtergrond Alleen")
    axes[0, 0].axis('off')
    
    # Toon fMRI data alleen
    axes[0, 1].imshow(fmri_data[:, :, 20], cmap='plasma')
    axes[0, 1].set_title("fMRI Data Alleen")
    axes[0, 1].axis('off')
    
    # Toon overlay met lage transparantie
    axes[1, 0].imshow(background_img, cmap='gray')
    im1 = axes[1, 0].imshow(fmri_data[:, :, 20], cmap='plasma', alpha=0.5)
    axes[1, 0].set_title("Overlay α=0.5 (Transparant)")
    axes[1, 0].axis('off')
    
    # Toon overlay met hoge transparantie
    axes[1, 1].imshow(background_img, cmap='gray')
    im2 = axes[1, 1].imshow(fmri_data[:, :, 20], cmap='plasma', alpha=0.9)
    axes[1, 1].set_title("Overlay α=0.9 (Ondoorzichtig)")
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    plt.savefig("demo_background_comparison.png", dpi=150, bbox_inches='tight')
    plt.close()
    
    print("   💾 Vergelijkingsplot: demo_background_comparison.png")
    print("✅ Hersenachtergrond demo voltooid!")


def demo_statische_achtergrond():
    """
    Demonstreer de nieuwe statische achtergrond functionaliteit.
    
    Deze functie toont:
    - Automatische detectie van afbeelding_achtergrond.png
    - Gebruik van maak_animatie_met_statische_achtergrond()
    - Vergelijking tussen gegenereerde en statische achtergronden
    - Error handling voor ontbrekende bestanden
    """
    print("\n" + "="*60)
    print("🖼️  DEMO 5: STATISCHE ACHTERGROND ONDERSTEUNING (NIEUW!)")
    print("="*60)
    
    # Genereer test data
    print("Stap 1: fMRI test data genereren...")
    fmri_data = generate_brain_like_data(width=80, height=80, frames=35, noise_level=0.03)
    
    # Creëer de standaard achtergrond afbeelding
    print("Stap 2: Standaard achtergrond afbeelding creëren...")
    static_background_path = create_brain_background_advanced(width=80, height=80)
    
    # Test automatische detectie
    print("Stap 3: Automatische detectie testen...")
    detected_path = zoek_standaard_achtergrond()
    if detected_path:
        print(f"   ✅ Automatische detectie succesvol: {detected_path}")
    else:
        print("   ❌ Automatische detectie gefaald")
    
    # Demonstreer nieuwe convenience functie met automatische detectie
    print("Stap 4: Animatie maken met automatische achtergrond detectie...")
    try:
        static_animation = maak_animatie_met_statische_achtergrond(
            fmri_data,
            # Geen achtergrond_pad opgegeven - automatische detectie!
            output_path="demo_statische_achtergrond_auto.gif",
            overlay_alpha=0.8,
            colormap='plasma',
            interval=120
        )
        print("   ✅ Automatische detectie animatie: demo_statische_achtergrond_auto.gif")
    except FileNotFoundError as e:
        print(f"   ❌ Automatische detectie gefaald: {e}")
    
    # Demonstreer met expliciet pad
    print("Stap 5: Animatie maken met expliciet achtergrond pad...")
    explicit_animation = maak_animatie_met_statische_achtergrond(
        fmri_data,
        achtergrond_pad=static_background_path,
        output_path="demo_statische_achtergrond_expliciet.gif",
        overlay_alpha=0.7,
        colormap='inferno',
        interval=100
    )
    print("   💾 Expliciete pad animatie: demo_statische_achtergrond_expliciet.gif")
    
    # Vergelijking maken tussen verschillende achtergrond types
    print("Stap 6: Vergelijkingsplot maken...")
    
    # Creëer ook een gegenereerde achtergrond voor vergelijking
    generated_bg_path = create_sample_brain_background(width=80, height=80, 
                                                     filename="generated_background_comparison.png")
    
    # Maak animatie met gegenereerde achtergrond
    generated_animation = maak_animatie_met_achtergrond(
        fmri_data,
        generated_bg_path,
        output_path="demo_gegenereerde_achtergrond.gif",
        overlay_alpha=0.7,
        colormap='inferno',
        interval=100
    )
    print("   💾 Gegenereerde achtergrond animatie: demo_gegenereerde_achtergrond.gif")
    
    # Maak vergelijkingsplot
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle("Statische vs Gegenereerde Achtergrond Vergelijking", fontsize=16, fontweight='bold')
    
    # Laad achtergronden
    static_bg = plt.imread(static_background_path)
    generated_bg = plt.imread(generated_bg_path)
    
    # Rij 1: Achtergronden alleen
    axes[0, 0].imshow(static_bg, cmap='gray')
    axes[0, 0].set_title("Statische Achtergrond\n(afbeelding_achtergrond.png)")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(generated_bg, cmap='gray')
    axes[0, 1].set_title("Gegenereerde Achtergrond\n(sample_brain_background.png)")
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(fmri_data[:, :, 17], cmap='inferno')
    axes[0, 2].set_title("fMRI Data Alleen")
    axes[0, 2].axis('off')
    
    # Rij 2: Overlays
    axes[1, 0].imshow(static_bg, cmap='gray')
    axes[1, 0].imshow(fmri_data[:, :, 17], cmap='inferno', alpha=0.7)
    axes[1, 0].set_title("Statische Achtergrond\n+ fMRI Overlay")
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(generated_bg, cmap='gray')
    axes[1, 1].imshow(fmri_data[:, :, 17], cmap='inferno', alpha=0.7)
    axes[1, 1].set_title("Gegenereerde Achtergrond\n+ fMRI Overlay")
    axes[1, 1].axis('off')
    
    # Verschil plot
    diff = np.abs(static_bg - generated_bg)
    im_diff = axes[1, 2].imshow(diff, cmap='hot')
    axes[1, 2].set_title("Verschil tussen\nAchtergronden")
    axes[1, 2].axis('off')
    plt.colorbar(im_diff, ax=axes[1, 2], shrink=0.6)
    
    plt.tight_layout()
    plt.savefig("demo_statische_vs_gegenereerde_vergelijking.png", dpi=150, bbox_inches='tight')
    plt.close()
    
    print("   💾 Vergelijkingsplot: demo_statische_vs_gegenereerde_vergelijking.png")
    
    # Test error handling
    print("Stap 7: Error handling demonstratie...")
    
    # Verwijder tijdelijk het standaard bestand om error te testen
    if os.path.exists("afbeelding_achtergrond.png"):
        os.rename("afbeelding_achtergrond.png", "afbeelding_achtergrond_backup.png")
        
        try:
            # Dit zou een error moeten geven
            error_animation = maak_animatie_met_statische_achtergrond(fmri_data)
            print("   ❌ Error handling gefaald - geen error gegooid")
        except FileNotFoundError as e:
            print(f"   ✅ Error handling werkt correct: {str(e)[:80]}...")
        
        # Herstel het bestand
        os.rename("afbeelding_achtergrond_backup.png", "afbeelding_achtergrond.png")
    
    print("✅ Statische achtergrond demo voltooid!")
    
    # Return informatie over gegenereerde bestanden
    return {
        'static_background': static_background_path,
        'generated_background': generated_bg_path,
        'animations': [
            'demo_statische_achtergrond_auto.gif',
            'demo_statische_achtergrond_expliciet.gif', 
            'demo_gegenereerde_achtergrond.gif'
        ]
    }


def demo_advanced_features():
    """
    Demonstreer geavanceerde features en verschillende instellingen.
    
    Deze functie toont:
    - Verschillende colormaps
    - Verschillende resoluties en frame rates
    - MP4 export functionaliteit
    - Geavanceerde data manipulatie
    """
    print("\n" + "="*60)
    print("🚀 DEMO 3: GEAVANCEERDE FEATURES")
    print("="*60)
    
    # Genereer hogere resolutie data
    print("Stap 1: Hoge resolutie hersendata genereren...")
    hd_brain_data = generate_brain_like_data(width=80, height=80, frames=60, noise_level=0.05)
    
    # Test verschillende colormaps
    colormaps = ['plasma', 'inferno', 'viridis', 'hot']
    
    for i, cmap in enumerate(colormaps):
        print(f"Stap 2.{i+1}: Animatie maken met '{cmap}' colormap...")
        
        animatie = BewegendHersenAnimatie(
            colormap=cmap,
            interval=100  # Snellere animatie (10 FPS)
        )
        
        animatie.load_data(hd_brain_data)
        
        # Voor de eerste twee: GIF, voor de laatste twee: MP4
        if i < 2:
            output_file = f"demo_advanced_{cmap}.gif"
            print(f"   💾 Opslaan als GIF: {output_file}")
        else:
            output_file = f"demo_advanced_{cmap}.mp4"
            print(f"   🎥 Opslaan als MP4: {output_file}")
        
        animation_obj = animatie.create_animation(
            output_path=output_file,
            figsize=(12, 10),
            dpi=120,  # Hogere resolutie
            title=f"Geavanceerd Demo: {cmap.title()} Colormap",
            show_colorbar=True
        )
    
    print("✅ Geavanceerde demo voltooid!")
    
    # Demonstreer frame extractie
    print("\nBonus: Frame extractie demonstratie...")
    animatie = BewegendHersenAnimatie()
    animatie.load_data(hd_brain_data)
    
    # Extraheer enkele interessante frames
    interesting_frames = [0, 15, 30, 45]
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("Geëxtraheerde Frames uit Hersenactiviteit", fontsize=16, fontweight='bold')
    
    for idx, frame_num in enumerate(interesting_frames):
        row, col = idx // 2, idx % 2
        frame_data = animatie.get_frame(frame_num)
        
        im = axes[row, col].imshow(frame_data, cmap='plasma', vmin=hd_brain_data.min(), vmax=hd_brain_data.max())
        axes[row, col].set_title(f"Frame {frame_num + 1}")
        axes[row, col].set_xlabel("X-positie")
        axes[row, col].set_ylabel("Y-positie")
    
    plt.tight_layout()
    plt.savefig("demo_frame_extractie.png", dpi=150, bbox_inches='tight')
    print("💾 Frame extractie opgeslagen als: demo_frame_extractie.png")
    plt.close()


def demo_convenience_function():
    """
    Demonstreer de convenience functie voor snelle animaties.
    
    Deze functie toont hoe je met één regel code een animatie kunt maken.
    """
    print("\n" + "="*60)
    print("⚡ DEMO 4: SNELLE ANIMATIE (CONVENIENCE FUNCTIE)")
    print("="*60)
    
    print("Genereren van compacte test data...")
    compact_data = generate_brain_like_data(width=32, height=32, frames=20, noise_level=0.2)
    
    print("Maken van snelle animatie met één functie-aanroep...")
    
    # Dit is de eenvoudigste manier om een animatie te maken!
    quick_animation = maak_snelle_animatie(
        compact_data,
        output_path="demo_snelle_animatie.gif",
        colormap='viridis',
        interval=200  # Langzamere animatie voor duidelijkheid
    )
    
    print("✅ Snelle animatie demo voltooid! Bestand: demo_snelle_animatie.gif")
    return quick_animation


def print_usage_tips():
    """
    Print handige tips voor gebruikers van de BewegendeHersenen library.
    """
    print("\n" + "="*60)
    print("💡 TIPS VOOR GEBRUIK VAN BEWEGENDEHERSENEN")
    print("="*60)
    
    tips = [
        "🎨 Colormap keuze:",
        "   • 'hot' - Klassiek voor hersenscans (zwart→rood→geel→wit)",
        "   • 'plasma' - Modern en kleurenblind-vriendelijk (paars→roze→geel)",
        "   • 'inferno' - Donker en dramatisch (zwart→paars→oranje→geel)",
        "   • 'viridis' - Wetenschappelijk standaard (paars→blauw→groen→geel)",
        "",
        "🧠 Hersenachtergrond tips:",
        "   • Gebruik PNG of JPG formaten voor achtergrond afbeeldingen",
        "   • Overlay transparantie (α): 0.5-0.8 voor subtiele overlay",
        "   • Overlay transparantie (α): 0.8-1.0 voor prominente activiteit",
        "   • Achtergrond wordt automatisch geschaald naar fMRI data grootte",
        "   • Kleurafbeeldingen worden automatisch naar grijswaarden geconverteerd",
        "",
        "🖼️  Statische achtergrond tips (NIEUW!):",
        "   • Plaats 'afbeelding_achtergrond.png' in je werkdirectory voor automatische detectie",
        "   • Gebruik maak_animatie_met_statische_achtergrond() voor eenvoudige implementatie",
        "   • Hogere resolutie achtergronden (200+ DPI) voor professionele resultaten",
        "   • Test verschillende achtergrond stijlen voor optimale visualisatie",
        "   • Statische achtergronden bieden meer controle dan gegenereerde achtergronden",
        "",
        "⚙️ Performance tips:",
        "   • Kleinere arrays (32x32) voor snelle prototyping",
        "   • Grotere arrays (128x128+) voor publicatie-kwaliteit",
        "   • Minder frames voor snellere verwerking",
        "   • Hogere DPI (150+) voor scherpe prints",
        "",
        "📁 Bestandsformaten:",
        "   • GIF: Universeel ondersteund, kleinere bestanden",
        "   • MP4: Betere compressie, professioneler voor presentaties",
        "",
        "🔬 Voor echte fMRI data:",
        "   • Normaliseer je data naar 0-1 range voor beste resultaten",
        "   • Overweeg spatiale smoothing voor ruis reductie",
        "   • Experimenteer met verschillende frame intervals",
        "   • Gebruik anatomische achtergronden voor context",
        "",
        "🚀 Snelle start:",
        "   • Gebruik maak_snelle_animatie() voor eenvoudige gevallen",
        "   • Gebruik maak_animatie_met_achtergrond() voor overlay animaties",
        "   • Gebruik maak_animatie_met_statische_achtergrond() voor statische achtergronden",
        "   • Gebruik BewegendHersenAnimatie klasse voor volledige controle"
    ]
    
    for tip in tips:
        print(tip)


def main():
    """
    Hoofdfunctie die alle demo's uitvoert.
    
    Deze functie:
    - Voert alle demonstraties uit in logische volgorde
    - Toont verschillende use cases van de library
    - Genereert voorbeeldbestanden voor gebruikers
    - Biedt educatieve informatie over best practices
    """
    print("🧠" + "="*58 + "🧠")
    print("    BEWEGENDEHERSENEN - COMPLETE DEMO SUITE")
    print("🧠" + "="*58 + "🧠")
    print()
    print("Welkom bij de BewegendeHersenen library demonstratie!")
    print("Deze demo toont alle functionaliteit voor het maken van")
    print("fMRI-achtige animaties van numpy arrays.")
    print()
    print("Perfect voor:")
    print("• 🔬 Neurowetenschappers en onderzoekers")
    print("• 🎓 Studenten die hersenactiviteit willen visualiseren") 
    print("• 📊 Data scientists die temporele patronen willen tonen")
    print("• 🎨 Iedereen die mooie wetenschappelijke animaties wil maken")
    print()
    print("🆕 NIEUW in deze versie: Statische achtergrond ondersteuning!")
    print("   Plaats 'afbeelding_achtergrond.png' voor automatische detectie")
    
    try:
        # Demo 1: Basis functionaliteit
        basic_anim = demo_basic_animation()
        
        # Demo 2: Hersenachtergrond overlay
        demo_background_overlay()
        
        # Demo 3: Geavanceerde features
        demo_advanced_features()
        
        # Demo 4: Convenience functie
        quick_anim = demo_convenience_function()
        
        # Demo 5: Statische achtergrond (NIEUW!)
        static_demo_results = demo_statische_achtergrond()
        
        # Toon handige tips
        print_usage_tips()
        
        # Samenvatting van gegenereerde bestanden
        print("\n" + "="*60)
        print("📁 GEGENEREERDE BESTANDEN")
        print("="*60)
        
        expected_files = [
            "demo_basis_animatie.gif",
            "sample_brain_background.png",
            "demo_background_alpha_0.5.gif",
            "demo_background_alpha_0.7.gif", 
            "demo_background_alpha_0.9.gif",
            "demo_convenience_background.gif",
            "demo_background_comparison.png",
            "demo_advanced_plasma.gif", 
            "demo_advanced_inferno.gif",
            "demo_advanced_viridis.mp4",
            "demo_advanced_hot.mp4",
            "demo_snelle_animatie.gif",
            "demo_frame_extractie.png",
            # Nieuwe bestanden voor statische achtergrond
            "afbeelding_achtergrond.png",
            "generated_background_comparison.png",
            "demo_statische_achtergrond_auto.gif",
            "demo_statische_achtergrond_expliciet.gif",
            "demo_gegenereerde_achtergrond.gif",
            "demo_statische_vs_gegenereerde_vergelijking.png"
        ]
        
        print("De volgende bestanden zijn gegenereerd:")
        for filename in expected_files:
            print(f"  📄 {filename}")
        
        print("\n🎉 Alle demo's succesvol voltooid!")
        print("\nJe kunt nu:")
        print("• De gegenereerde animaties bekijken")
        print("• De code aanpassen voor je eigen data")
        print("• Experimenteren met verschillende instellingen")
        print("• Je eigen hersenachtergrond afbeeldingen gebruiken")
        print("• 🆕 'afbeelding_achtergrond.png' gebruiken voor automatische achtergrond detectie")
        print("• De library gebruiken in je eigen projecten")
        
        print(f"\n📚 Voor meer informatie, bekijk de documentatie in bewegende_hersenen.py")
        print("🚀 Veel plezier met het visualiseren van je hersendata!")
        
    except Exception as e:
        print(f"\n❌ Er is een fout opgetreden tijdens de demo: {e}")
        print("Controleer of alle vereiste packages zijn geïnstalleerd:")
        print("pip install numpy matplotlib scipy")
        print("\nVoor MP4 ondersteuning is ffmpeg vereist:")
        print("conda install ffmpeg  # of via je package manager")
        raise


if __name__ == "__main__":
    # Voer de complete demo suite uit
    main()