import frappe
import stripe

@frappe.whitelist(allow_guest=True)
def confirm_payment(payment_method, amount):
    stripe.api_key = 'sk_test_51PiZtxJhBWaDQDpMip5ak4Fg2leKimFqophSn3kB6u0XXc2uLVxb8Rpk9CXOrqIqfYhwIrYRUitqSpcy5Vi78QFt00BdIoY39a'  # Replace with your Stripe secret key

    try:
    
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd', 
            payment_method=payment_method,
            confirm=True,
            return_url="http://localhost:8080/frontend/movies/",
        )
        return {"status": "success"}
    except stripe.error.CardError as e:
        return {"status": "error", "message": str(e)}



@frappe.whitelist(allow_guest=True)

def get_movie_price():
   
    title = frappe.request.args.get('title')
    try:
        movie = frappe.get_all("Movie", filters={"title": title}, fields=["price_per_ticket"])
        if movie:
            return {
                "status": "success",
                "price": movie[0]["price_per_ticket"],
                "message": "Price fetched successfully"  #
            }
        else:
            return {
                "status": "error",
                "message": "Movie not found"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)  # Ensure this is a string
        }
    
    
import json

@frappe.whitelist(allow_guest=True)
def create_booking_and_confirm_payment(payment_method, amount, movieName, show_id, number_of_tickets, selected_seats, date):
    stripe.api_key = 'sk_test_51PiZtxJhBWaDQDpMip5ak4Fg2leKimFqophSn3kB6u0XXc2uLVxb8Rpk9CXOrqIqfYhwIrYRUitqSpcy5Vi78QFt00BdIoY39a'  
    
    try:
     
        if isinstance(selected_seats, dict):
            selected_seats_json = json.dumps(selected_seats)  
        else:
            selected_seats_json = selected_seats

       
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="usd",
            payment_method=payment_method,
            confirmation_method="manual",
            confirm=True,
            return_url="http://localhost:8080/frontend/confirmation",
        )

        
        booking = frappe.get_doc({
            "doctype": "Ticket Booking",
            "movie": movieName,  
            "show": show_id, 
            "number_of_tickets": number_of_tickets,
            "selected_seats": selected_seats_json, 
            "amount": amount / 100,  
            "payment_method": payment_method,
            "payment_status": intent.status,
            "date": date
        })
        booking.insert()
        booking.submit()

        return {"status": "success"}
    except stripe.error.CardError as e:
        return {"status": "error", "message": e.user_message}
    except Exception as e:
        return {"status": "error", "message": str(e)}

