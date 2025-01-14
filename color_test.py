from PIL import Image, ImageDraw
import os
from openai import OpenAI

# Set up OpenAI client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY") or "OPENAI_API_KEY"  # Replace with your actual API key if not using env var
)

# Function to generate pain color using OpenAI
def generate_pain_color(description, scale_value, chosen_color):
    """
    Uses OpenAI's LLM to generate a pain color based on semantic descriptions, pain scale, and color choice.
    """
    prompt = (
        f"Generate a unified RGB color representation for the following pain description:\n"
        f"Description: {description}\n"
        f"Pain Scale (0-10): {scale_value}\n"
        f"Chosen Color: {chosen_color}\n"
        f"ONLY OUTPUT a single RGB color in the format R, G, B. DO NOT INCLUDE ANY WORDS"
    )
    response = client.chat.completions.create(
        model="gpt-4o",  # Use the updated model version
        messages=[{"role": "user", "content": prompt}],
    )
    # Extract and return RGB values
    rgb_text = response.choices[0].message.content.strip()
    rgb_values = [int(value.strip()) for value in rgb_text.split(",")]
    return tuple(rgb_values)

# Function to create the grid-based color map
def create_color_map(age_color, ethnicity_color, education_color, profession_color, chronic_color, pain_color, output_path):
    """
    Creates a 4x5 grid-based color map image.
    """
    # Canvas dimensions (4x5 aspect ratio, 300 DPI scale assumption)
    canvas_width, canvas_height = 1200, 1500  # Example resolution for clarity
    grid = Image.new("RGB", (canvas_width, canvas_height), "white")
    draw = ImageDraw.Draw(grid)

    # Define grid zones
    grid_zones = {
        "Profession": ((0, 0), (600, 300), profession_color),
        "Chronic Pain": ((600, 0), (1200, 300), chronic_color),
        "Education": ((0, 300), (600, 600), education_color),
        "Ethnicity": ((0, 600), (600, 900), ethnicity_color),
        "Age": ((0, 900), (600, 1500), age_color),
        "Pain Color": ((600, 300), (1200, 1500), pain_color),
    }

    # Draw each section
    for section, ((x1, y1), (x2, y2), color) in grid_zones.items():
        draw.rectangle([x1, y1, x2, y2], fill=color)

    # Save the output image
    grid.save(output_path)
    return output_path

# Example input data
age_color = (0, 159, 255)  # Example age color (Blue)
ethnicity_color = (176, 196, 222)  # Example ethnicity color (Light Steel Blue)
education_color = (125, 206, 160)  # Example education color (Mint Green)
profession_color = (218, 165, 32)  # Example profession color (Goldenrod)
chronic_color = (255, 127, 80)  # Example chronic pain color (Coral)
pain_description = "Sharp, throbbing pain in the lower back."
pain_scale = 7
chosen_pain_color = "Red"

# Generate pain color using OpenAI
pain_color = generate_pain_color(pain_description, pain_scale, chosen_pain_color)

# Create the color map
output_path = "pain_color_map.png"
create_color_map(age_color, ethnicity_color, education_color, profession_color, chronic_color, pain_color, output_path)

print(f"Color map saved to: {output_path}")
