import openai
import requests

# === API Keys ===
openai.api_key = "your-openai-api-key"
shopify_access_token = "your-shopify-access-token"
shopify_store_url = "your-store.myshopify.com"

# === Shopify API Helpers ===
def get_order_status(order_number):
    headers = {
        "X-Shopify-Access-Token": shopify_access_token,
        "Content-Type": "application/json"
    }
    url = f"https://{shopify_store_url}/admin/api/2023-10/orders.json?name={order_number}"

    response = requests.get(url, headers=headers)
    data = response.json()
    
    if 'orders' in data and data['orders']:
        order = data['orders'][0]
        return f"Order #{order_number} is currently '{order['fulfillment_status']}' and was placed on {order['created_at']}."
    else:
        return f"Sorry, I couldn't find an order with number #{order_number}."

# === GPT Chatbot Function ===
def ecommerce_chatbot(user_input):
    # Detect keywords to act accordingly
    if "order" in user_input.lower() and "number" in user_input.lower():
        # Very basic order number extractor (you should improve it in production)
        import re
        match = re.search(r'\d{4,}', user_input)
        if match:
            order_number = f"#{match.group()}"
            return get_order_status(order_number)
        else:
            return "Could you please provide your order number?"

    # Otherwise, fall back to GPT
    system_prompt = (
        "You are a helpful e-commerce assistant for a Shopify store. "
        "If the customer doesn't ask about an order, provide general support like return policies, shipping, and recommendations."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.5,
        max_tokens=300
    )

    return response['choices'][0]['message']['content']

# === Chat Interface ===
if __name__ == "__main__":
    print("Welcome to the Shopify Assistant!")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Assistant: Thank you! Let us know if you need anything else.")
            break
        reply = ecommerce_chatbot(user_input)
        print("Assistant:", reply)
