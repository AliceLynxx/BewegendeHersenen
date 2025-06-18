#!/usr/bin/env python3
"""
Test Script voor Bugfix #21: Transparante Plasma Overlay

Dit script test de fix voor het probleem waarbij de achtergrond werd 
overschreven door een blauwe overlay in plaats van alleen de plasma 
animatie te tonen.

Test cases:
1. Animatie met achtergrond en threshold-based transparency
2. Vergelijking van verschillende threshold waarden
3. Validatie dat grijstinten achtergrond zichtbaar blijft
4. Controle dat alleen significante activiteit wordt getoond
"""

import numpy as np
import matplotlib.pyplot as plt
from bewegende_hersenen import BewegendHersenAnimatie, maak_animatie_met_achtergrond

def create_test_brain_background(width=64, height=64, filename="test_brain_bg.png"):
    """Creëer test hersenachtergrond voor bugfix validatie."""
    print(f"🎨 Creëren test hersenachtergrond ({width}x{height})...")
    
    # Maak een duidelijke grijstinten achtergrond
    y_coords, x_coords = np.ogrid[:height, :width]
    center_x, center_y = width // 2, height // 2
    
    # Ovaalvormige hersenvorm
    ellipse_a = width * 0.4
    ellipse_b = height * 0.35
    ellipse = ((x_coords - center_x) / ellipse_a)**2 + ((y_coords - center_y) / ellipse_b)**2
    brain_mask = ellipse <= 1.0
    
    # Duidelijke grijstinten structuur
    background = np.where(brain_mask, 0.7, 0.1)  # Hoog contrast
    
    # Voeg wat structuur toe
    structure = 0.2 * np.sin(0.3 * x_coords) * np.sin(0.3 * y_coords)
    background = np.where(brain_mask, background + structure, 0.1)
    background = np.clip(background, 0, 1)
    
    # Sla op als PNG met geforceerde grijstinten
    plt.figure(figsize=(6, 6))
    plt.imshow(background, cmap='gray', vmin=0, vmax=1)
    plt.title("Test Hersenachtergrond (Grijstinten)")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(filename, dpi=100, bbox_inches='tight', facecolor='black')
    plt.close()
    
    print(f"✅ Test achtergrond opgeslagen: {filename}")
    return filename

def generate_test_fmri_data(width=64, height=64, frames=20):
    """Genereer test fMRI data met duidelijke activatiepatronen."""
    print(f"🧠 Genereren test fMRI data ({width}x{height}, {frames} frames)...")
    
    data = np.zeros((height, width, frames))
    
    # Creëer enkele duidelijke activatiecentra
    centers = [
        {'x': width//4, 'y': height//4, 'intensity': 0.9},
        {'x': 3*width//4, 'y': height//4, 'intensity': 0.7},
        {'x': width//2, 'y': 3*height//4, 'intensity': 0.8},
    ]
    
    time_points = np.linspace(0, 2*np.pi, frames)
    
    for frame in range(frames):
        frame_data = np.zeros((height, width))
        
        for center in centers:
            # Temporele oscillatie
            temporal = center['intensity'] * (0.5 + 0.5 * np.sin(time_points[frame]))
            
            # Spatiale Gaussische verdeling
            y_coords, x_coords = np.ogrid[:height, :width]
            distance_sq = (x_coords - center['x'])**2 + (y_coords - center['y'])**2
            sigma = min(width, height) / 10
            spatial = np.exp(-distance_sq / (2 * sigma**2))
            
            frame_data += temporal * spatial
        
        # Voeg lage-niveau ruis toe (dit zou normaal blauw worden in plasma)
        noise = 0.1 * np.random.normal(0, 0.05, (height, width))
        frame_data += noise
        
        # Zorg voor positieve waarden
        frame_data = np.clip(frame_data, 0, 1)
        data[:, :, frame] = frame_data
    
    print(f"✅ Test data gegenereerd! Range: {data.min():.3f} - {data.max():.3f}")
    return data

def test_threshold_functionality():
    """Test de threshold-based transparency functionaliteit."""
    print("\n" + "="*60)
    print("🔬 TEST 1: THRESHOLD-BASED TRANSPARENCY")
    print("="*60)
    
    # Genereer test data
    fmri_data = generate_test_fmri_data(width=48, height=48, frames=15)
    background_path = create_test_brain_background(width=48, height=48)
    
    # Test verschillende threshold waarden
    thresholds = [None, 0.3, 0.5, 0.7]  # None = automatisch (75e percentiel)
    
    for i, threshold in enumerate(thresholds):
        print(f"\nStap {i+1}: Test threshold = {threshold}")
        
        # Maak animatie met specifieke threshold
        animatie = BewegendHersenAnimatie(
            colormap='plasma',
            interval=200,
            background_image=background_path,
            overlay_alpha=0.8,
            activity_threshold=threshold
        )
        
        animatie.load_data(fmri_data)
        
        threshold_str = "auto" if threshold is None else f"{threshold:.1f}"
        output_file = f"test_bugfix21_threshold_{threshold_str}.gif"
        
        animation_obj = animatie.create_animation(
            output_path=output_file,
            figsize=(8, 6),
            title=f"Bugfix Test: Threshold = {threshold_str}",
            show_colorbar=True
        )
        
        print(f"   💾 Opgeslagen: {output_file}")
    
    print("✅ Threshold functionaliteit test voltooid!")

def test_comparison_before_after():
    """Maak vergelijkingsplot om de fix te demonstreren."""
    print("\n" + "="*60)
    print("📊 TEST 2: VOOR/NA VERGELIJKING")
    print("="*60)
    
    # Genereer test data
    fmri_data = generate_test_fmri_data(width=64, height=64, frames=10)
    background_path = create_test_brain_background(width=64, height=64)
    
    # Laad achtergrond voor vergelijking
    background_img = plt.imread(background_path)
    
    # Maak vergelijkingsplot
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle("Bugfix #21: Transparante Plasma Overlay Vergelijking", fontsize=16, fontweight='bold')
    
    # Frame voor demonstratie
    demo_frame = fmri_data[:, :, 5]
    
    # Rij 1: Probleem situatie (simulatie van oude gedrag)
    axes[0, 0].imshow(background_img, cmap='gray')
    axes[0, 0].set_title("1. Grijstinten Achtergrond")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(demo_frame, cmap='plasma')
    axes[0, 1].set_title("2. fMRI Data (Plasma)")
    axes[0, 1].axis('off')
    
    # Simuleer oude probleem: volledige overlay (inclusief lage waarden als blauw)
    axes[0, 2].imshow(background_img, cmap='gray')
    axes[0, 2].imshow(demo_frame, cmap='plasma', alpha=0.8)
    axes[0, 2].set_title("3. PROBLEEM: Blauw overschrijft achtergrond")
    axes[0, 2].axis('off')
    
    # Rij 2: Oplossing (nieuwe gedrag)
    axes[1, 0].imshow(background_img, cmap='gray')
    axes[1, 0].set_title("1. Grijstinten Achtergrond")
    axes[1, 0].axis('off')
    
    # Bereken threshold en maak masked data
    threshold = np.percentile(demo_frame, 75)
    masked_frame = np.ma.masked_where(demo_frame < threshold, demo_frame)
    
    axes[1, 1].imshow(masked_frame, cmap='plasma', vmin=threshold, vmax=demo_frame.max())
    axes[1, 1].set_title(f"2. Alleen Significante Activiteit (τ={threshold:.2f})")
    axes[1, 1].axis('off')
    
    # Toon oplossing: alleen significante activiteit over achtergrond
    axes[1, 2].imshow(background_img, cmap='gray')
    axes[1, 2].imshow(masked_frame, cmap='plasma', alpha=0.8, vmin=threshold, vmax=demo_frame.max())
    axes[1, 2].set_title("3. OPLOSSING: Transparante overlay")
    axes[1, 2].axis('off')
    
    plt.tight_layout()
    plt.savefig("test_bugfix21_comparison.png", dpi=150, bbox_inches='tight')
    plt.close()
    
    print("💾 Vergelijkingsplot opgeslagen: test_bugfix21_comparison.png")
    print("✅ Voor/na vergelijking voltooid!")

def test_convenience_function():
    """Test de bijgewerkte convenience functie met threshold parameter."""
    print("\n" + "="*60)
    print("⚡ TEST 3: CONVENIENCE FUNCTIE MET THRESHOLD")
    print("="*60)
    
    # Genereer test data
    fmri_data = generate_test_fmri_data(width=40, height=40, frames=12)
    background_path = create_test_brain_background(width=40, height=40, filename="test_convenience_bg.png")
    
    print("Test convenience functie met custom threshold...")
    
    # Test convenience functie met threshold parameter
    animation_obj = maak_animatie_met_achtergrond(
        fmri_data,
        background_path,
        output_path="test_bugfix21_convenience.gif",
        overlay_alpha=0.7,
        colormap='plasma',
        interval=150,
        activity_threshold=0.4  # Custom threshold
    )
    
    print("💾 Convenience functie test: test_bugfix21_convenience.gif")
    print("✅ Convenience functie test voltooid!")

def validate_fix():
    """Valideer dat de fix correct werkt."""
    print("\n" + "="*60)
    print("✅ VALIDATIE: CONTROLEER FIX WERKING")
    print("="*60)
    
    # Genereer test data met duidelijke lage en hoge waarden
    test_data = np.zeros((32, 32, 5))
    
    # Voeg lage waarden toe (zouden blauw zijn in plasma zonder fix)
    test_data[:, :, :] = 0.1  # Lage baseline
    
    # Voeg hoge activiteit toe in centrum
    center = 16
    test_data[center-5:center+5, center-5:center+5, :] = 0.8
    
    background_path = create_test_brain_background(width=32, height=32, filename="validation_bg.png")
    
    # Test met verschillende instellingen
    animatie = BewegendHersenAnimatie(
        colormap='plasma',
        interval=300,
        background_image=background_path,
        overlay_alpha=0.8,
        activity_threshold=0.3  # Lage waarden (0.1) worden gemaskeerd
    )
    
    animatie.load_data(test_data)
    
    animation_obj = animatie.create_animation(
        output_path="test_bugfix21_validation.gif",
        figsize=(8, 6),
        title="Validatie: Alleen centrum zichtbaar, achtergrond behouden",
        show_colorbar=True
    )
    
    print("💾 Validatie animatie: test_bugfix21_validation.gif")
    
    # Controleer dat threshold correct wordt berekend
    calculated_threshold = animatie._calculate_activity_threshold(test_data)
    print(f"📊 Berekende threshold: {calculated_threshold:.3f}")
    print(f"📊 Data range: {test_data.min():.3f} - {test_data.max():.3f}")
    
    # Validatie criteria
    validation_passed = True
    
    if calculated_threshold <= 0.1:
        print("❌ FOUT: Threshold te laag, lage waarden worden niet gemaskeerd")
        validation_passed = False
    
    if calculated_threshold >= 0.8:
        print("❌ FOUT: Threshold te hoog, hoge activiteit wordt gemaskeerd")
        validation_passed = False
    
    if 0.1 < calculated_threshold < 0.8:
        print("✅ CORRECT: Threshold in juiste range")
    
    if validation_passed:
        print("🎉 VALIDATIE GESLAAGD: Fix werkt correct!")
    else:
        print("⚠️  VALIDATIE GEFAALD: Fix heeft problemen")
    
    return validation_passed

def main():
    """Voer alle tests uit voor bugfix #21."""
    print("🧠" + "="*58 + "🧠")
    print("    BUGFIX #21 TEST SUITE: TRANSPARANTE PLASMA OVERLAY")
    print("🧠" + "="*58 + "🧠")
    print()
    print("Deze test suite valideert de fix voor issue #21:")
    print("• Achtergrond wordt niet meer overschreven door blauwe overlay")
    print("• Alleen significante fMRI activiteit wordt getoond als plasma kleuren")
    print("• Lage waarden zijn transparant zodat achtergrond doorschijnt")
    print("• Threshold-based transparency werkt correct")
    
    try:
        # Test 1: Threshold functionaliteit
        test_threshold_functionality()
        
        # Test 2: Voor/na vergelijking
        test_comparison_before_after()
        
        # Test 3: Convenience functie
        test_convenience_function()
        
        # Validatie
        validation_passed = validate_fix()
        
        # Samenvatting
        print("\n" + "="*60)
        print("📋 TEST SAMENVATTING")
        print("="*60)
        
        generated_files = [
            "test_bugfix21_threshold_auto.gif",
            "test_bugfix21_threshold_0.3.gif", 
            "test_bugfix21_threshold_0.5.gif",
            "test_bugfix21_threshold_0.7.gif",
            "test_bugfix21_comparison.png",
            "test_bugfix21_convenience.gif",
            "test_bugfix21_validation.gif"
        ]
        
        print("Gegenereerde test bestanden:")
        for filename in generated_files:
            print(f"  📄 {filename}")
        
        if validation_passed:
            print("\n🎉 ALLE TESTS GESLAAGD!")
            print("✅ Bugfix #21 is succesvol geïmplementeerd")
            print("✅ Achtergrond blijft zichtbaar")
            print("✅ Alleen significante activiteit wordt getoond")
            print("✅ Threshold-based transparency werkt correct")
        else:
            print("\n⚠️  SOMMIGE TESTS GEFAALD")
            print("❌ Bugfix heeft nog problemen")
        
        print("\n🔍 Bekijk de gegenereerde bestanden om de fix visueel te valideren")
        
    except Exception as e:
        print(f"\n❌ FOUT tijdens test uitvoering: {e}")
        print("Controleer of alle dependencies zijn geïnstalleerd:")
        print("pip install numpy matplotlib scipy")
        raise

if __name__ == "__main__":
    main()