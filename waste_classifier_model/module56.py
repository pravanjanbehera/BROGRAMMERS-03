
def smart_action_recommendation(waste_label):
    """
    Suggests best reuse / recycle / compost action
    based on detected waste type.
    """

    label = waste_label.lower()

    if "plastic" in label:
        return "Recycle or reuse plastic products."
    elif "cardboard" in label or "paper" in label:
        return "Send for paper recycling."
    elif "organic" in label:
        return "Compost to produce natural fertilizer."
    elif "battery" in label:
        return "Dispose at certified e-waste center."
    elif "aluminium" in label or "metal" in label:
        return "Scrap recycling recommended."
    else:
        return "Manual segregation required."


def environmental_impact_message(waste_label):
    """
    Generates environmental awareness message
    based on detected waste type.
    """

    label = waste_label.lower()

    if "plastic" in label:
        return "Recycling plastic reduces ocean pollution and protects marine life."
    elif "organic" in label:
        return "Composting organic waste reduces methane gas and improves soil fertility."
    elif "paper" in label or "cardboard" in label:
        return "Recycling paper saves trees and reduces deforestation."
    elif "metal" in label or "aluminium" in label:
        return "Metal recycling saves energy and reduces mining impact."
    elif "battery" in label:
        return "Proper battery disposal prevents soil and water contamination."
    else:
        return "Responsible waste handling keeps the environment clean and sustainable."