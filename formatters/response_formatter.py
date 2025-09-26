"""
Response formatter for Sigma Male facial analysis reports.
Handles formatting the combined jawline and Gemini analysis into readable text.
"""

def format_sigma_analysis_report(jawline_shape: str, jawline_assessment: str, other_features: dict) -> str:
    """
    Format the combined analysis results into a sigma male themed report.
    
    Args:
        jawline_shape: The classified face shape from jawline analysis
        jawline_assessment: Basic jawline assessment text
        other_features: Dictionary containing Gemini AI analysis results
        
    Returns:
        Formatted string containing the full analysis report
    """
    
    readable_response = f""" SIGMA MALE FACIAL ANALYSIS REPORT 

JAWLINE ASSESSMENT (MOST IMPORTANT):
• Current Shape: {jawline_shape}
• Basic Assessment: {jawline_assessment}
• Sigma Analysis: {other_features['jawline_enhancement']['current_definition']}
• Mogger Score: {other_features['jawline_enhancement']['definition_score']}/10

ADVANCED MEWING TECHNIQUES:
  - {other_features['jawline_enhancement']['mewing_tips'][0]}
  - {other_features['jawline_enhancement']['mewing_tips'][1]}

SIGMA GRINDSET TIPS:
  - {other_features['jawline_enhancement']['sigma_grindset'][0]}
  - {other_features['jawline_enhancement']['sigma_grindset'][1]}

GIGACHAD WISDOM:
  "{other_features['jawline_enhancement']['gigachad_quotes'][0]}"
  "{other_features['jawline_enhancement']['gigachad_quotes'][1]}"

HUNTER EYES ANALYSIS:
• Analysis: {other_features['eyes_and_eyebrows']['description']}
• Sigma Score: {other_features['eyes_and_eyebrows']['sigma_score']}/10
• How to Mog:
  - {other_features['eyes_and_eyebrows']['suggestions'][0]}
  - {other_features['eyes_and_eyebrows']['suggestions'][1]}

NOSE ASSESSMENT:
• Chad Analysis: {other_features['nose_structure']['description']}
• Mog Score: {other_features['nose_structure']['mog_score']}/10
• Ascension Tips:
  - {other_features['nose_structure']['suggestions'][0]}
  - {other_features['nose_structure']['suggestions'][1]}

BONE STRUCTURE:
• Gigachad Analysis: {other_features['cheekbones']['description']}
• Bone Score: {other_features['cheekbones']['bone_score']}/10
• How to Ascend:
  - {other_features['cheekbones']['suggestions'][0]}
  - {other_features['cheekbones']['suggestions'][1]}

SKIN MAXING:
• Based Analysis: {other_features['skin_quality']['description']}
• Zyzz Score: {other_features['skin_quality']['zyzz_score']}/10
• Skinmaxxing Tips:
  - {other_features['skin_quality']['care_recommendations'][0]}
  - {other_features['skin_quality']['care_recommendations'][1]}

OVERALL MOGGER POTENTIAL:
• Sigma Analysis: {other_features['facial_harmony']['balance_description']}
• Mogger Score: {other_features['facial_harmony']['mogger_score']}/10
• How to Become Gigachad:
  - {other_features['facial_harmony']['enhancement_suggestions'][0]}
  - {other_features['facial_harmony']['enhancement_suggestions'][1]}"""

    return readable_response