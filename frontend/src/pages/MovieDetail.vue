<template>
  <div v-if="!movieResource.loading && movieResource.doc">
    <!-- Movie Information Section -->
    <h1 class="text-gray-900 font-bold text-[32px]">{{ movieDoc.title }}</h1>
    <div class="mt-11 flex flex-row items-center justify-between">
      <div class="flex flex-col space-y-3">
        <h2 class="text-gray-700 text-base font-bold uppercase">Director</h2>
        <h2 class="text-gray-600 text-xl font-semibold">{{ movieDoc.director }}</h2>
      </div>
      <div class="flex flex-col space-y-3">
        <h2 class="text-gray-700 text-base font-bold uppercase">Release Date</h2>
        <h2 class="text-gray-600 text-xl font-semibold">{{ movieDoc.release_date }}</h2>
      </div>
    </div>

    <!-- Booking Steps -->
    <div class="max-w-full">
      <div class="mx-12" v-if="currentStep === 0">
        <!-- Movie Poster and Button -->
        <div class="flex justify-center mt-7">
          <div class="bg-white shadow-2xl rounded p-1">
            <img
              :src="movieDoc.poster"
              alt="Movie Poster"
              class="w-80 h-70 object-cover rounded"
            />
          </div>
        </div>
        <div class="w-full flex items-center justify-center mt-7">
          <Button size="xl" variant="solid" @click="currentStep++">Book Tickets</Button>
        </div>
        <div class="flex flex-col space-y-3 mt-14">
          <h2 class="text-gray-700 text-base font-bold uppercase">Synopsis</h2>
          <h2 class="text-gray-600 text-lg font-normal">{{ movieDoc.synopsis }}</h2>
        </div>
      </div>

      <div v-else-if="currentStep === 1">
        <!-- Number of Seats Selection -->
        <h2 class="font-medium text-xl mt-7 text-gray-900">How many seats?</h2>
        <div class="flex flex-col w-full space-y-5 mt-6">
          <Button
            size="lg"
            :variant="index === bookingData.numberOfSeats ? 'subtle' : 'white'"
            class="shadow-lg"
            v-for="index in 8"
            @click="setNumberOfSeats(index)"
            >{{ index }}</Button
          >
        </div>
      </div>

      <div v-else-if="currentStep === 2">
        <!-- Date and Show Selection -->
        <div class="flex flex-col space-y-4">
          <h2 class="font-medium text-xl mt-7 text-gray-900">Date</h2>
          <input type="date" v-model="bookingData.date" />

          <h2 class="font-medium text-xl mt-7 text-gray-900">Cinema & Show</h2>
          <div class="space-y-2">
            <div
              class="bg-white shadow-xl p-4 rounded flex flex-col space-y-4"
              v-for="theater in Object.keys(theaters.data)"
              :key="theater"
            >
              <h3 class="text-sm font-bold text-gray-800">{{ theater }}</h3>
              <div class="flex flex-row space-x-2">
                <Button
                  size="sm"
                  :variant="show.name === bookingData.show ? 'subtle' : 'outline'"
                  @click="bookingData.show = show.name"
                  :key="show.name"
                  v-for="show in theaters.data[theater]"
                  >{{ show.start_time }}</Button
                >
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="currentStep === 3">
        <!-- Seat Selection -->
        <h2 class="font-medium text-xl mt-7 text-gray-900">Select seats?</h2>
        <div class="w-full flex items-center flex-col mt-7">
          <div v-for="(seats, row) in seatStructure" :key="row" class="flex flex-row">
            <span
              @click="selectSeat(row, seat[0])"
              v-for="(seat, index) in seats"
              :key="index"
              class="w-8 h-8 m-2 rounded-[2px]"
              :class="[
                seat[1] === 'Available'
                  ? 'bg-blue-300'
                  : seat[1] === 'Selected'
                  ? 'bg-blue-600'
                  : 'bg-gray-300',
                hasSelectedCorrectNumberOfSeats ? 'cursor-not-allowed' : 'cursor-pointer',
              ]"
            >
            </span>
          </div>
        </div>
      </div>

      <div v-else-if="currentStep === 4">
        <!-- Confirmation and QR Code -->
        <div class="w-full flex items-center flex-col mt-7">
          <h1 class="text-[110px]">🍿</h1>
          <h2 class="font-medium text-xl mt-7 text-gray-900">Enjoy the movie!</h2>

          <img :src="barcodeUrl" alt="QR Code" class="mt-4 w-64 h-64" v-if="barcodeUrl" />

          <Button size="lg" variant="solid" class="mt-4" @click="downloadPDF"
            >Download PDF</Button
          >
        </div>
      </div>
    </div>
    

    
    <!-- Navigation Buttons -->
    <div class="flex flex-row mt-6 space-x-2">
      <Button
        size="lg"
        variant="subtle"
        v-if="currentStep !== 0 && currentStep !== 4"
        @click="currentStep--"
        >Go Back</Button
      >
      <Button
        size="lg"
        variant="solid"
        v-if="currentStep !== 0 && currentStep !== 4"
        :disabled="!nextButtonEnabled"
        @click="handleNextClick()"
        >Next</Button
      >
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from "vue";
import { createDocumentResource, createListResource } from "frappe-ui";
import jsPDF from "jspdf";

const props = defineProps({
  movieName: {
    type: String,
    required: true,
  },
});

const movieResource = createDocumentResource({
  doctype: "Movie",
  name: props.movieName,
  onSuccess(doc) {
    console.log("Movie fetched successfully", doc);
  },
  auto: true,
});

const theaters = createListResource({
  doctype: "Theater Show",
  fields: ["theater", "start_time", "name"],
  onSuccess(doc) {
    console.log("Theater shows fetched successfully", doc);
  },
  auto: true,
  transform: (shows) => {
    const groupedShows = {};
    for (const show of shows) {
      if (!groupedShows[show.theater]) {
        groupedShows[show.theater] = [];
      }
      groupedShows[show.theater].push(show);
    }
    return groupedShows;
  },
});

const movieBooking = createListResource({
  doctype: "Ticket Booking",
  insert: {
    onSuccess() {
      console.log("Booking created successfully");
      currentStep.value++;
    },
  },
});

function getSeatStructure(alphabets, numbers) {
  const structure = {};
  for (const alphabet of alphabets) {
    structure[alphabet] = [];
    for (const number of numbers) {
      structure[alphabet].push([number, "Available"]);
    }
  }
  return structure;
}

const seatStructure = reactive(
  getSeatStructure(["A", "B", "C", "D", "E"], [1, 2, 3, 4, 5, 6, 7])
);

const currentStep = ref(0);
const today = new Date().toISOString().split("T")[0];
const bookingData = reactive({
  numberOfSeats: 0,
  selectedSeats: [],
  date: today,
  show: null,
});

function setNumberOfSeats(n) {
  bookingData.numberOfSeats = n;
}

function selectSeat(row, number) {
  if (hasSelectedCorrectNumberOfSeats.value) {
    return;
  }

  const seat = seatStructure[row].find((seat) => seat[0] === number);
  seat[1] = "Selected";
  bookingData.selectedSeats.push(`${row}${number}`);
}

const hasSelectedCorrectNumberOfSeats = computed(() => {
  return bookingData.selectedSeats.length === bookingData.numberOfSeats;
});

const movieDoc = computed(() => movieResource.doc);

const nextButtonEnabled = computed(() => {
  if (currentStep.value === 1) {
    return bookingData.numberOfSeats;
  } else if (currentStep.value === 2) {
    return bookingData.date && bookingData.show;
  } else if (currentStep.value === 3) {
    return hasSelectedCorrectNumberOfSeats.value;
  } else if (currentStep.value === 4) {
    return true;
  }
  return false;
});

function handleNextClick() {
  if (currentStep.value === 3) {
    movieBooking.insert.submit({
      movie: props.movieName,
      date: bookingData.date,
      show: bookingData.show,
      selected_seats: JSON.stringify(bookingData.selectedSeats),
      number_of_tickets: bookingData.numberOfSeats,
    });
    generateQRCode();
  } else {
    currentStep.value++;
  }
}

function generateQRCode() {
  const qrData = {
    movie: props.movieName,
    date: bookingData.date,
    show: bookingData.show,
    selected_seats: bookingData.selectedSeats.join(","),
    number_of_tickets: bookingData.numberOfSeats,
  };
  const qrDataString = encodeURIComponent(JSON.stringify(qrData));
  barcodeUrl.value = `https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=${qrDataString}`;
}



function downloadPDF() {
  const doc = new jsPDF();
  doc.text(`Movie: ${props.movieName}`, 10, 10);
  doc.text(`Date: ${bookingData.date}`, 10, 20);
  doc.text(`Show: ${bookingData.show}`, 10, 30);
  doc.text(`Number of Tickets: ${bookingData.numberOfSeats}`, 10, 40);
  doc.text(`Selected Seats: ${bookingData.selectedSeats.join(", ")}`, 10, 50);
  doc.save("booking-details.pdf");
}

const barcodeUrl = ref("");
</script>

<style scoped>
.w-64 {
  width: 200px;
}
.h-64 {
  height: 200px;
}
</style>
