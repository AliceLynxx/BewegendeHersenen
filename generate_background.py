#!/usr/bin/env python3
"""
Script om afbeelding_achtergrond.png te genereren voor de demo.
Dit script wordt uitgevoerd om de benodigde achtergrond afbeelding te maken.
"""

import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def create_background_image():
    """Creëer de achtergrond afbeelding en sla deze op als PNG."""
    
    # Maak een professionele achtergrond
    width, height = 100, 100
    
    # Creëer coördinaten
    y_coords, x_coords = np.ogrid[:height, :width]
    
    # Maak een landschap-achtige achtergrond
    # Lucht gradient (licht boven, donkerder beneden)
    sky_gradient = np.linspace(0.85, 0.45, height).reshape(-1, 1)
    background = np.tile(sky_gradient, (1, width))
    
    # Voeg wolken toe
    np.random.seed(42)  # Voor reproduceerbare resultaten
    for i in range(4):
        cloud_x = np.random.randint(width//6, 5*width//6)
        cloud_y = np.random.randint(height//8, height//3)
        cloud_size_x = np.random.randint(width//10, width//5)
        cloud_size_y = np.random.randint(height//15, height//8)
        
        # Gaussische wolkvorm
        cloud_pattern = np.exp(-((x_coords - cloud_x)**2 / (2 * cloud_size_x**2) + 
                                (y_coords - cloud_y)**2 / (2 * cloud_size_y**2)))
        
        # Voeg wolken toe als lichtere gebieden
        background += 0.12 * cloud_pattern
    
    # Voeg een horizon lijn toe
    horizon_y = int(height * 0.72)
    background[horizon_y:horizon_y+1, :] *= 0.88
    
    # Voeg textuur toe aan de grond
    ground_texture = np.random.normal(0, 0.015, (height - horizon_y, width))
    background[horizon_y:, :] += ground_texture
    
    # Voeg enkele heuvels toe
    for i in range(3):
        hill_center = np.random.randint(width//5, 4*width//5)
        hill_width = np.random.randint(width//8, width//4)
        hill_height = np.random.randint(height//25, height//12)
        
        # Creëer heuvel vorm
        hill_x = np.arange(max(0, hill_center - hill_width), 
                          min(width, hill_center + hill_width))
        if len(hill_x) > 0:
            hill_profile = hill_height * np.exp(-((hill_x - hill_center)**2) / (2 * (hill_width/4)**2))
            
            for j, x in enumerate(hill_x):
                hill_top = horizon_y - int(hill_profile[j])
                if hill_top >= 0:
                    background[hill_top:horizon_y, x] *= 0.82  # Donkerder voor heuvel silhouet
    
    # Voeg subtiele ruis toe voor realisme
    noise = 0.025 * np.random.normal(0, 1, (height, width))
    background += noise
    
    # Normaliseer naar 0-1 range
    background = np.clip(background, 0, 1)
    
    # Sla op als PNG
    plt.figure(figsize=(10, 10), dpi=100)
    plt.imshow(background, cmap='gray', vmin=0, vmax=1)
    plt.axis('off')
    plt.tight_layout()
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    
    # Sla op zonder marges
    plt.savefig('afbeelding_achtergrond.png', 
                dpi=150, 
                bbox_inches='tight', 
                pad_inches=0,
                facecolor='white',
                edgecolor='none')
    plt.close()
    
    print("✅ afbeelding_achtergrond.png succesvol gegenereerd!")
    print(f"📊 Afbeelding: {width}x{height} pixels, grijswaarden")
    print(f"🎯 Intensiteit range: {background.min():.3f} - {background.max():.3f}")
    
    return background

if __name__ == "__main__":
    create_background_image()