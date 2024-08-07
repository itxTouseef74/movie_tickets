<template>
  <div class="min-h-screen flex flex-col">
    <!-- Menu Bar -->
    <header class="bg-gray-800 text-white p-4 shadow-md">
      <div class="container mx-auto flex items-center justify-between">
        <router-link to="/" class="flex items-center space-x-2">
          <!-- Logo -->
          <img src="../assets/download.jpeg" alt="Movies Logo" class="w-12 h-12 object-cover rounded-full"/>
          <span class="text-2xl font-bold">Movies</span>
        </router-link>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1 p-6 bg-gray-50 mt-10">

      <div v-if="movies.data" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <router-link 
          v-for="movie in movies.data" 
          :key="movie.name" 
          :to="{ name: 'MovieDetail', params: { movieName: movie.name } }" 
          class="block"
        >
          <li class="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 cursor-pointer overflow-hidden">
            <img :src="movie.poster || 'default-movie-poster.jpg'" alt="Movie Poster" class="w-full h-48 object-cover">
            <div class="p-4">
              <h2 class="text-xl text-blue-500 hover:text-blue-700 mb-2">{{ movie.title }}</h2>
              <div class="text-gray-600 mb-4">
                <p><strong>Director:</strong> {{ movie.director }}</p>
                <p><strong>Release Date:</strong> {{ movie.release_date }}</p>
              </div>
              <div class="bg-red-500 text-white p-2 rounded-lg flex items-center justify-between">
                <span class="text-lg font-semibold">{{ movie.price_per_ticket | currency }}</span>
                <span class="text-sm font-medium bg-red-700 px-2 py-1 rounded-full">Buy Now</span>
              </div>
            </div>
          </li>
        </router-link>
      </div>
    </main>
  </div>
</template>

<script setup>
import { createListResource } from 'frappe-ui';


const movies = createListResource({
  doctype: 'Movie',
  fields: ['name', 'title', 'director', 'release_date', 'price_per_ticket', 'poster'],
  auto: true
});
</script>

<style scoped>

img {
  object-fit: cover;
}
</style>
