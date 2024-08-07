<template>
    <div>
        <h1 class="text-gray-900 font-bold text-2xl">Complete Your Payment</h1>
        <form @submit.prevent="handleSubmit">
            <div id="card-element" class="mt-4"></div>
            <button type="submit" :disabled="isProcessing" class="mt-4 bg-blue-500 text-white py-2 px-4 rounded">
                Pay {{ price }} USD
            </button>
        </form>
        <p v-if="paymentSuccess" class="mt-4 text-green-600">Payment Successful! Redirecting...</p>
        <p v-if="paymentError" class="mt-4 text-red-600">{{ paymentError }}</p>
    </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import { useRouter } from 'vue-router'; 
import { loadStripe } from '@stripe/stripe-js';
import { CardElement } from '@stripe/react-stripe-js';

const stripePromise = loadStripe('pk_test_51PiZtxJhBWaDQDpMKW8oJrbRbzTHey9riUtzeiDotZxBNVALTOB2Wrc873kBeVty88agKdLeG7hfl8lVIyhv8elk00RPeyYVlI');

const props = defineProps({
    price: Number,
    movieName: String,
    bookingData: Object,
});

const emit = defineEmits(['payment-success']);

const router = useRouter(); 

const price = ref(props.price);
const paymentError = ref('');
const isProcessing = ref(false);
const paymentSuccess = ref(false);

let elements;

async function handleSubmit() {

    if (price.value <= 0) {
        paymentError.value = 'Please enter a valid amount.';
        return;
    }
    isProcessing.value = true;

    const stripe = await stripePromise;
  
    if (!stripe || !elements) {
        paymentError.value = 'Stripe has not loaded properly. Please try again.';
        isProcessing.value = false;
        return;
    }

    const cardElement = elements.getElement(CardElement);

    if (!cardElement) {
        paymentError.value = 'Card Element is not available. Please reload the page.';
        isProcessing.value = false;
        return;
    }

    const { error, paymentMethod } = await stripe.createPaymentMethod({
        type: 'card',
        card: cardElement,
    });

    if (error) {
        paymentError.value = error.message;
        isProcessing.value = false;
        return;
    }

    console.log('Booking Data:', {
        show_id: props.bookingData.show,
        number_of_tickets: props.bookingData.numberOfSeats,
        selected_seats: props.bookingData.selectedSeats,
        date: props.bookingData.date,
    });


    const formattedSelectedSeats = {
        seats: props.bookingData.selectedSeats
    };

    const response = await fetch('/api/method/movie_tickets.api.api.create_booking_and_confirm_payment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            payment_method: paymentMethod.id,
            amount: props.price * 100, 
            movieName: props.movieName,
            show_id: props.bookingData.show,
            number_of_tickets: props.bookingData.numberOfSeats,
            selected_seats: formattedSelectedSeats, 
            date: props.bookingData.date,
        }),
    });

    setTimeout(() => {
    router.push({
        path: '/confirmation',
        query: {
            movieName: props.movieName,
            show: props.bookingData.show,
            numberOfSeats: props.bookingData.numberOfSeats,
            selectedSeats: JSON.stringify(props.bookingData.selectedSeats),
            date: props.bookingData.date,
            paidAmount:props.price 
        }
    });
}, 2000);

    isProcessing.value = false;
}

onMounted(async () => {
    await nextTick();
    const stripe = await stripePromise;
    elements = stripe.elements();
    const cardElement = elements.create('card');
    cardElement.mount('#card-element');
    console.log('StripePayment Mounted Props:', props);
});
</script>




<style scoped>

</style>
