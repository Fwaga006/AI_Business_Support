def get_ai_response(question, business_info):

    # Temporary AI logic
    # Later we will connect a real AI model here

    question = question.lower()

    if "delivery" in question:
        return "Yes, we provide delivery services. " + business_info

    elif "price" in question or "cost" in question:
        return "Please check our prices. " + business_info

    elif "location" in question:
        return "We are located according to this information: " + business_info

    else:
        return "Thank you for contacting us. " + business_info