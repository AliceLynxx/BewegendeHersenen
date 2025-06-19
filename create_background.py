#!/usr/bin/env python3
"""
Script voor het genereren van afbeelding_achtergrond.png
Dit script maakt een professionele achtergrondafbeelding voor de rennende mannetje demo.
"""

import numpy as np
import matplotlib.pyplot as plt
import os

def create_professional_background(width=100, height=100, filename="afbeelding_achtergrond.png"):
    """
    Creëer een professionele achtergrondafbeelding voor de rennende mannetje demo.
    
    Args:
        width (int): Breedte van de achtergrond
        height (int): Hoogte van de achtergrond  
        filename (str): Bestandsnaam voor opslaan
        
    Returns:
        str: Pad naar de gemaakte achtergrond afbeelding
    """
    print(f"🎨 Creëren van professionele achtergrondafbeelding ({width}x{height})...")
    
    # Maak een landschap-achtige achtergrond voor het rennende mannetje
    y_coords, x_coords = np.ogrid[:height, :width]
    
    # Creëer een subtiele gradient voor de lucht (boven) naar grond (onder)
    sky_gradient = np.linspace(0.8, 0.4, height).reshape(-1, 1)
    background = np.tile(sky_gradient, (1, width))
    
    # Voeg wat wolken toe (subtiele patronen in de lucht)
    for i in range(3):
        cloud_x = np.random.randint(width//4, 3*width//4)
        cloud_y = np.random.randint(height//6, height//3)
        cloud_size_x = np.random.randint(width//8, width//4)
        cloud_size_y = np.random.randint(height//12, height//8)
        
        # Gaussische wolkvorm
        cloud_pattern = np.exp(-((x_coords - cloud_x)**2 / (2 * cloud_size_x**2) + 
                                (y_coords - cloud_y)**2 / (2 * cloud_size_y**2)))
        
        # Voeg wolken toe als lichtere gebieden
        background += 0.15 * cloud_pattern
    
    # Voeg een horizon lijn toe (subtiel)
    horizon_y = int(height * 0.7)
    background[horizon_y:horizon_y+2, :] *= 0.9
    
    # Voeg wat textuur toe aan de grond
    ground_texture = np.random.normal(0, 0.02, (height - horizon_y, width))
    background[horizon_y:, :] += ground_texture
    
    # Voeg enkele subtiele heuvels toe
    for i in range(2):
        hill_center = np.random.randint(width//4, 3*width//4)
        hill_width = np.random.randint(width//6, width//3)
        hill_height = np.random.randint(height//20, height//10)
        
        # Creëer heuvel vorm
        hill_x = np.arange(max(0, hill_center - hill_width), 
                          min(width, hill_center + hill_width))
        if len(hill_x) > 0:
            hill_profile = hill_height * np.exp(-((hill_x - hill_center)**2) / (2 * (hill_width/3)**2))
            
            for j, x in enumerate(hill_x):
                hill_top = horizon_y - int(hill_profile[j])
                if hill_top >= 0:
                    background[hill_top:horizon_y, x] *= 0.85  # Donkerder voor heuvel silhouet
    
    # Voeg wat subtiele ruis toe voor realisme
    noise = 0.03 * np.random.normal(0, 1, (height, width))
    background += noise
    
    # Normaliseer naar 0-1 range
    background = np.clip(background, 0, 1)
    
    # Sla op als PNG met hoge kwaliteit
    plt.figure(figsize=(12, 12))
    plt.imshow(background, cmap='gray', vmin=0, vmax=1)
    plt.title("Professionele Achtergrond voor Rennende Mannetje Demo")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(filename, dpi=200, bbox_inches='tight', facecolor='white', 
                edgecolor='none', pad_inches=0)
    plt.close()
    
    print(f"✅ Professionele achtergrond opgeslagen als: {filename}")
    print(f"📊 Afbeelding eigenschappen: {width}x{height} pixels, grijswaarden")
    print(f"🎯 Intensiteit range: {background.min():.3f} - {background.max():.3f}")
    
    return filename

if __name__ == "__main__":
    # Genereer de standaard achtergrond
    background_path = create_professional_background()
    print(f"\n🎉 Achtergrond succesvol gegenereerd!")
    print(f"📁 Bestand: {background_path}")
    print(f"💡 Deze achtergrond kan nu gebruikt worden in demo_rennend_mannetje.py")