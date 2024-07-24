<template>
    <div class="p-6 bg-gray-50 min-h-screen">
      <h1 class="font-bold text-3xl text-gray-800 mb-6">List of Movies</h1>
      
      <ul v-if="movies.data" class="space-y-4">
        <router-link 
          v-for="movie in movies.data" 
          :key="movie.name" 
          :to="{ name: 'MovieDetail', params: { movieName: movie.name } }" 
          class="block"
        >
          <li class="bg-white p-4 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 cursor-pointer">
            <h2 class="text-xl text-blue-500 hover:text-blue-700">{{ movie.title }}</h2>
            <div class="mt-2 text-gray-600">
              <p><strong>Director:</strong> {{ movie.director }}</p>
              <p><strong>Release Date:</strong> {{ movie.release_date }}</p>
            </div>
          </li>
        </router-link>
      </ul>
    </div>
  </template>
  
  <script setup>
  import { createListResource } from 'frappe-ui';
  
  const movies = createListResource({
    doctype: 'Movie',
    fields: ['name', 'title', 'director', 'release_date'],
    auto: true
  });
  </script>
  