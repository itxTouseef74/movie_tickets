import frappe
import stripe

stripe.api_key = "sk_test_51PiZtxJhBWaDQDpMip5ak4Fg2leKimFqophSn3kB6u0XXc2uLVxb8Rpk9CXOrqIqfYhwIrYRUitqSpcy5Vi78QFt00BdIoY39a"

@frappe.whitelist(allow_guest=True)
def create_payment_intent(movie_id, number_of_seats):
    movie = frappe.get_doc("Movie", movie_id)
    price_per_ticket = movie.price_per_ticket
    total_amount = price_per_ticket * number_of_seats * 100  # amount in cents

    payment_intent = stripe.PaymentIntent.create(
        amount=total_amount,
        currency="usd",
        payment_method_types=["card"]
    )
    return {"clientSecret": payment_intent.client_secret}

@frappe.whitelist(allow_guest=True)
def record_payment(payment_details):
    # This function records the payment details into your system
    # Adjust this part according to your needs
    doc = frappe.get_doc({
        "doctype": "Payment",
        "movie": payment_details.get("movie"),
        "date": payment_details.get("date"),
        "show": payment_details.get("show"),
        "selected_seats": payment_details.get("seats"),
        "number_of_tickets": payment_details.get("number_of_tickets"),
        "amount": payment_details.get("amount")
    })
    doc.insert()
    return {"status": "success"}
