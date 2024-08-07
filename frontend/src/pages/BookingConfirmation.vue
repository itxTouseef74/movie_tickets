<template>
    <!-- Confirmation and QR Code -->
    <div class="w-full flex items-center flex-col mt-7">
        <h1 class="text-[110px]">🍿</h1>
        <h2 class="font-medium text-xl mt-7 text-gray-900">Enjoy the movie!</h2>

        <!-- Display QR Code and PDF download button -->
        <img :src="barcodeUrl" alt="QR Code" class="mt-4 w-64 h-64" v-if="barcodeUrl" />

        <Button size="lg" variant="solid" class="mt-4" @click="downloadPDF">
            Download PDF
        </Button>
    </div>
</template>

<script setup>
import { ref, watch } from "vue";
import jsPDF from "jspdf";

const props = defineProps({
    movieName: {
        type: String,
        required: true,
    },
});

// Example booking data (You can replace this with actual data)
const bookingData = ref({
    numberOfSeats: 2,
    selectedSeats: ["A1", "A2"],
    date: new Date().toISOString().split("T")[0],
    show: "Evening",
});
const barcodeUrl = ref("");

// Generate QR code URL
const generateQRCode = () => {
    const qrData = {
        movie: props.movieName,
        date: bookingData.value.date,
        show: bookingData.value.show,
        selected_seats: bookingData.value.selectedSeats.join(","),
        number_of_tickets: bookingData.value.numberOfSeats,
    };

    const qrDataString = encodeURIComponent(JSON.stringify(qrData));
    barcodeUrl.value = `https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=${qrDataString}`;
};

// Download PDF
const downloadPDF = () => {
    const doc = new jsPDF();
    doc.text(`Movie: ${props.movieName}`, 10, 10);
    doc.text(`Date: ${bookingData.value.date}`, 10, 20);
    doc.text(`Show: ${bookingData.value.show}`, 10, 30);
    doc.text(`Number of Tickets: ${bookingData.value.numberOfSeats}`, 10, 40);
    doc.text(`Selected Seats: ${bookingData.value.selectedSeats.join(", ")}`, 10, 50);

    if (barcodeUrl.value) {
        doc.addImage(barcodeUrl.value, "PNG", 10, 60, 50, 50);
    }

    doc.save("booking-details.pdf");
};

// Generate QR code when component is created
generateQRCode();
</script>

<style scoped>
.w-64 {
    width: 200px;
}

.h-64 {
    height: 200px;
}
</style>