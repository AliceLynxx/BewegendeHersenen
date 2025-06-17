#!/usr/bin/env python3
"""
BewegendeHersenen Demo Script

Dit script demonstreert de volledige functionaliteit van de BewegendeHersenen library
voor het maken van fMRI-achtige animaties van numpy arrays.

Voor neurowetenschappers, onderzoekers en studenten biedt dit script:
- Realistische test data generatie die lijkt op fMRI signalen
- Verschillende visualisatie opties en colormaps
- Voorbeelden van basis en geavanceerde functionaliteit
- Export naar verschillende formaten (GIF, MP4)

Auteur: BewegendeHersenen Project
Doel: Educatieve demonstratie en snelle start voor nieuwe gebruikers
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from bewegende_hersenen import BewegendHersenAnimatie, maak_snelle_animatie


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
    print("🚀 DEMO 2: GEAVANCEERDE FEATURES")
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
    print("⚡ DEMO 3: SNELLE ANIMATIE (CONVENIENCE FUNCTIE)")
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
        "",
        "🚀 Snelle start:",
        "   • Gebruik maak_snelle_animatie() voor eenvoudige gevallen",
        "   • Gebruik BewegendHersenAnimatie klasse voor meer controle"
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
    
    try:
        # Demo 1: Basis functionaliteit
        basic_anim = demo_basic_animation()
        
        # Demo 2: Geavanceerde features
        demo_advanced_features()
        
        # Demo 3: Convenience functie
        quick_anim = demo_convenience_function()
        
        # Toon handige tips
        print_usage_tips()
        
        # Samenvatting van gegenereerde bestanden
        print("\n" + "="*60)
        print("📁 GEGENEREERDE BESTANDEN")
        print("="*60)
        
        expected_files = [
            "demo_basis_animatie.gif",
            "demo_advanced_plasma.gif", 
            "demo_advanced_inferno.gif",
            "demo_advanced_viridis.mp4",
            "demo_advanced_hot.mp4",
            "demo_snelle_animatie.gif",
            "demo_frame_extractie.png"
        ]
        
        print("De volgende bestanden zijn gegenereerd:")
        for filename in expected_files:
            print(f"  📄 {filename}")
        
        print("\n🎉 Alle demo's succesvol voltooid!")
        print("\nJe kunt nu:")
        print("• De gegenereerde animaties bekijken")
        print("• De code aanpassen voor je eigen data")
        print("• Experimenteren met verschillende instellingen")
        print("• De library gebruiken in je eigen projecten")
        
        print(f"\n📚 Voor meer informatie, bekijk de documentatie in bewegende_hersenen.py")
        print("🚀 Veel plezier met het visualiseren van je hersendata!")
        
    except Exception as e:
        print(f"\n❌ Er is een fout opgetreden tijdens de demo: {e}")
        print("Controleer of alle vereiste packages zijn geïnstalleerd:")
        print("pip install numpy matplotlib")
        print("\nVoor MP4 ondersteuning is ffmpeg vereist:")
        print("conda install ffmpeg  # of via je package manager")
        raise


if __name__ == "__main__":
    # Voer de complete demo suite uit
    main()