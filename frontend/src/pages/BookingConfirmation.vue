<template>
    
    <div class="w-full flex items-center flex-col mt-7">
        <h1 class="text-[110px]">🍿</h1>
        <h2 class="font-medium text-xl mt-7 text-gray-900">Enjoy the movie!</h2>

      
        <img :src="barcodeUrl" alt="QR Code" class="mt-4 w-64 h-64" v-if="barcodeUrl" />

        <Button size="lg" variant="solid" class="mt-4" @click="downloadPDF">
            Download PDF
        </Button>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import jsPDF from 'jspdf';

const route = useRoute();

const movieName = route.query.movieName || '';
const show = route.query.show || '';
const numberOfSeats = route.query.numberOfSeats || '';
const selectedSeats = route.query.selectedSeats || '';
const date = route.query.date || '';
const paidAmount = route.query.paidAmount || '';

const barcodeUrl = ref('');


const generateQRCode = () => {
    const qrData = {
        movieName,
        show,
        numberOfSeats,
        selectedSeats,
        date
        
    };

    const qrDataString = encodeURIComponent(JSON.stringify(qrData));
    barcodeUrl.value = `https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=${qrDataString}`;
};

const downloadPDF = () => {
    const doc = new jsPDF();

    doc.setFont('Helvetica');
    doc.setFontSize(16); 


    doc.text('Booking Details', 10, 10);

    doc.setFontSize(12); 
    doc.text(`Movie: ${movieName}`, 10, 30);
    doc.text(`Show: ${show}`, 10, 40);
    doc.text(`Number of Seats: ${numberOfSeats}`, 10, 50);
    doc.text(`Selected Seats: ${selectedSeats}`, 10, 60);
    doc.text(`Date: ${date}`, 10, 70);
    doc.text(`Paid Amount: ${paidAmount} USD`, 10, 80);


    if (barcodeUrl.value) {
        doc.addImage(barcodeUrl.value, 'PNG', 10, 90, 50, 50); 
    }

    
    const sanitizedMovieName = movieName.replace(/[^a-zA-Z0-9]/g, '_'); 
    const filename = `${sanitizedMovieName}.pdf`;

    doc.save(filename); 
};


onMounted(() => {
    generateQRCode();
});
</script>


<style scoped>
.w-64 {
    width: 200px;
}

.h-64 {
    height: 200px;
}
</style>