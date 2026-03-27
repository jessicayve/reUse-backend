import base64
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY was not found in the .env file.")

client = OpenAI(api_key=api_key)

MODEL = "gpt-4.1-mini"
DEFAULT_LOCATION = "Brazil"


def analyze_image_with_openai(image_bytes: bytes, location: str = DEFAULT_LOCATION) -> dict:
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    prompt = f"""
You are an eco-friendly assistant for an app called ReUse.

A user will upload a photo containing one main object.
Your job is to analyze the object and recommend the most sustainable action.

User location:
{location}

Possible actions:
- reuse
- repair
- donate
- recycle

Return ONLY valid JSON in this exact structure:
{{
  "objectName": "string",
  "materialType": "string",
  "condition": "string",
  "decision": "reuse | repair | donate | recycle",
  "reason": "string",
  "reuseIdeas": ["string", "string", "string"],
  "recyclingTip": "string",
  "recyclable": true,
  "environmentalImpact": "string",
  "disposalCategory": "string",
  "location": "string",
  "localDisposalGuidance": "string",
  "confidence": 0.0
}}

Rules:
- Respond in English only.
- Identify only one main object.
- Ignore background objects.
- Keep objectName short and simple.
- Keep materialType short, for example: plastic, metal, glass, fabric, paper, wood, rubber, ceramic, electronic.
- Keep condition short, ideally 1 to 3 words.
- Choose exactly one decision.
- reason MUST NOT be empty.
- Keep reason short and practical.
- reuseIdeas must contain exactly 3 simple ideas.
- confidence must be a number between 0.0 and 1.0.
- recyclable must be true only when decision is "recycle".
- recyclable must be false for reuse, repair, and donate.
- environmentalImpact must be one short sentence.
- disposalCategory must be short, for example: plastic recycling, textile reuse, e-waste, glass recycling, donation.
- location must be "{location}".
- localDisposalGuidance must be one short practical sentence for that location.
- If decision is "recycle", provide a simple recyclingTip telling the user not to throw it in regular trash and to check a recycling bin, collection point, or local recycling rules.
- If decision is not "recycle", recyclingTip must be an empty string.
- Keep localDisposalGuidance general and practical. Do not invent specific addresses or institutions.

Decision logic:
- Choose "donate" only if the item is still clean, safe, and usable by another person without repair.
- If the item is worn, torn, raggedy, stained, broken, damaged, or visibly degraded, do not choose "donate".
- Choose "repair" only if the object can realistically be fixed and used again with reasonable effort.
- Choose "reuse" when the item is no longer suitable for donation but can still be repurposed for DIY, crafts, storage, cleaning, or another practical use.
- Choose "recycle" only when the object is no longer suitable for donate, repair, or reuse.

Special rule for clothes and fabric items:
- Choose "donate" only if wearable and in good condition.
- Choose "repair" if minor damage can realistically be fixed.
- Choose "reuse" if too worn for donation but still useful for rags, crafts, patches, bags, or upcycling.
- Choose "recycle" only if unusable even for practical fabric reuse.

Reuse ideas:
- If decision is "reuse", provide 3 practical DIY or repurposing ideas that match the object and its condition.
- If decision is "repair", provide 3 simple ideas related to fixing, reinforcing, or extending the item's life.
- If decision is "donate", provide 3 simple ideas related to donating, passing it on, or preparing it for reuse by others.
- If decision is "recycle", provide 3 simple ideas related to sorting, disassembling if appropriate, or preparing it for correct recycling.
"""

    schema = {
        "type": "object",
        "properties": {
            "objectName": {"type": "string"},
            "materialType": {"type": "string"},
            "condition": {"type": "string"},
            "decision": {
                "type": "string",
                "enum": ["reuse", "repair", "donate", "recycle"]
            },
            "reason": {"type": "string"},
            "reuseIdeas": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 3,
                "maxItems": 3
            },
            "recyclingTip": {"type": "string"},
            "recyclable": {"type": "boolean"},
            "environmentalImpact": {"type": "string"},
            "disposalCategory": {"type": "string"},
            "location": {"type": "string"},
            "localDisposalGuidance": {"type": "string"},
            "confidence": {
                "type": "number",
                "minimum": 0.0,
                "maximum": 1.0
            }
        },
        "required": [
            "objectName",
            "materialType",
            "condition",
            "decision",
            "reason",
            "reuseIdeas",
            "recyclingTip",
            "recyclable",
            "environmentalImpact",
            "disposalCategory",
            "location",
            "localDisposalGuidance",
            "confidence"
        ],
        "additionalProperties": False
    }

    response = client.responses.create(
        model=MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{image_base64}",
                        "detail": "auto"
                    }
                ]
            }
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "reuse_scan_result",
                "schema": schema,
                "strict": True
            }
        }
    )

    raw_text = response.output_text

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError:
        return {
            "objectName": "Unknown object",
            "materialType": "unknown",
            "condition": "unknown",
            "decision": "reuse",
            "reason": "Could not parse the model response.",
            "reuseIdeas": [
                "Use it as storage",
                "Repurpose it for organization",
                "Turn it into a DIY project"
            ],
            "recyclingTip": "",
            "recyclable": False,
            "environmentalImpact": "Improper disposal can increase environmental waste.",
            "disposalCategory": "general reuse",
            "location": location,
            "localDisposalGuidance": "Check your local waste and recycling rules before disposing of this item.",
            "confidence": 0.45
        }

    if not parsed.get("objectName"):
        parsed["objectName"] = "Unknown object"

    if not parsed.get("materialType"):
        parsed["materialType"] = "unknown"

    if not parsed.get("condition"):
        parsed["condition"] = "unknown"

    if not parsed.get("reason"):
        parsed["reason"] = "This is the most sustainable option based on the object's condition."

    reuse_ideas = parsed.get("reuseIdeas", [])
    if not isinstance(reuse_ideas, list) or len(reuse_ideas) != 3:
        parsed["reuseIdeas"] = [
            "Use it as storage",
            "Repurpose it for organization",
            "Turn it into a DIY project"
        ]

    decision = parsed.get("decision", "reuse")
    if decision not in {"reuse", "repair", "donate", "recycle"}:
        decision = "reuse"
        parsed["decision"] = "reuse"

    condition = str(parsed.get("condition", "")).lower()
    material_type = str(parsed.get("materialType", "")).lower()
    object_name = str(parsed.get("objectName", "")).lower()

    bad_conditions = {
        "worn",
        "torn",
        "raggedy",
        "damaged",
        "broken",
        "stained",
        "dirty",
        "ripped",
        "frayed",
        "old",
        "heavily worn",
        "very worn",
        "visibly damaged",
        "worn and torn",
        "worn, torn"
    }

    fabric_like_objects = {
        "shirt", "t-shirt", "tshirt", "pants", "jeans", "dress", "skirt", "jacket",
        "hoodie", "sweater", "fabric", "cloth", "clothing", "clothes", "textile"
    }

    is_bad_condition = any(term in condition for term in bad_conditions)
    is_fabric_item = material_type == "fabric" or object_name in fabric_like_objects

    if decision == "donate" and is_bad_condition:
        if is_fabric_item:
            parsed["decision"] = "reuse"
            parsed["reason"] = "Too worn for donation but still suitable for practical DIY reuse."
            parsed["disposalCategory"] = "textile reuse"
            parsed["reuseIdeas"] = [
                "Use it as cleaning rags",
                "Turn it into a reusable bag",
                "Cut it into pieces for craft projects"
            ]
        else:
            parsed["decision"] = "reuse"
            parsed["reason"] = "Too damaged for donation but still suitable for practical repurposing."
            parsed["disposalCategory"] = "general reuse"
            parsed["reuseIdeas"] = [
                "Repurpose it for storage",
                "Use parts of it in a DIY project",
                "Reuse it for household organization"
            ]

    decision = parsed.get("decision", "reuse")

    if decision == "recycle":
        if not parsed.get("recyclingTip"):
            parsed["recyclingTip"] = (
                "Do not throw it in regular trash. Check a recycling bin, collection point, or local recycling rules."
            )
    else:
        parsed["recyclingTip"] = ""

    parsed["recyclable"] = decision == "recycle"

    if not parsed.get("environmentalImpact"):
        parsed["environmentalImpact"] = "Improper disposal can increase environmental waste."

    if not parsed.get("disposalCategory"):
        parsed["disposalCategory"] = "general reuse" if decision != "recycle" else "recycling"

    parsed["location"] = location

    if not parsed.get("localDisposalGuidance"):
        parsed["localDisposalGuidance"] = (
            "Check your local waste and recycling rules before disposing of this item."
        )

    confidence = parsed.get("confidence", 0.5)
    if not isinstance(confidence, (int, float)):
        parsed["confidence"] = 0.7
    elif confidence < 0.0:
        parsed["confidence"] = 0.0
    elif confidence > 1.0:
        parsed["confidence"] = 1.0

    return parsed


def analyze_image_pipeline(image_bytes: bytes, location: str = DEFAULT_LOCATION) -> dict:
    return analyze_image_with_openai(image_bytes, location)