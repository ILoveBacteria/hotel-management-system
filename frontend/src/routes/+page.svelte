<!-- src/routes/+page.svelte -->
<script lang="ts">
  import { goto } from "$app/navigation";
  import { Hotel, Phone, Mail, MapPin, ArrowRight, Send } from "lucide-svelte";

  const rooms = [
    {
      name: "Deluxe Room",
      description: "Spacious room with city view",
      price: 4500,
      image: "/api/placeholder/400/300",
    },
    {
      name: "Suite",
      description: "Luxury suite with separate living area",
      price: 6500,
      image: "/api/placeholder/400/300",
    },
    {
      name: "Standard Room",
      description: "Comfortable room for budget travelers",
      price: 3500,
      image: "/api/placeholder/400/300",
    },
  ];

  const goals = [
    {
      title: "Exceptional Service",
      description: "Committed to providing outstanding hospitality",
    },
    {
      title: "Comfort & Luxury",
      description: "Modern amenities with traditional charm",
    },
    {
      title: "Sustainable Tourism",
      description: "Eco-friendly practices for a better future",
    },
  ];

  let contactForm = {
    name: "",
    email: "",
    message: "",
  };

  function handleContact() {
    console.log("Contact form submitted:", contactForm);
    // Reset form
    contactForm = { name: "", email: "", message: "" };
  }
</script>

<!-- Header -->
<header
  class="fixed top-0 left-0 right-0 bg-white/90 backdrop-blur-sm z-50 border-b border-gray-200"
>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex justify-between items-center h-16">
      <div class="flex items-center">
        <Hotel class="w-8 h-8 text-blue-600" />
        <span class="ml-2 text-xl font-bold text-gray-900">Bacteria Hotel</span>
      </div>
      <button
        class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        on:click={() => goto("/user/login")}
      >
        Login
      </button>
    </div>
  </div>
</header>

<!-- Main Content -->
<main class="mt-16">
  <!-- Hero Banner -->
  <div
    class="relative h-[70vh] bg-gradient-to-r from-blue-600 to-blue-400 flex items-center justify-center"
  >
    <div class="absolute inset-0">
      <img
        src="/api/placeholder/1920/1080"
        alt="Hotel"
        class="w-full h-full object-cover opacity-20"
      />
    </div>
    <div class="relative text-center text-white px-4">
      <h1 class="text-4xl md:text-6xl font-bold mb-4">
        Welcome to Luxury & Comfort
      </h1>
      <p class="text-xl md:text-2xl max-w-2xl mx-auto">
        Experience unparalleled hospitality in the heart of the city
      </p>
      <button
        class="mt-8 bg-white text-blue-600 px-8 py-3 rounded-lg font-medium
                       hover:bg-blue-50 transition-colors inline-flex items-center"
        on:click={() => goto("/login")}
      >
        Book Now
        <ArrowRight class="ml-2 w-5 h-5" />
      </button>
    </div>
  </div>

  <!-- Room Cards -->
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
    <h2 class="text-3xl font-bold text-gray-900 mb-8">Featured Rooms</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {#each rooms as room}
        <div class="bg-white rounded-lg shadow-lg overflow-hidden">
          <img
            src={room.image}
            alt={room.name}
            class="w-full h-48 object-cover"
          />
          <div class="p-6">
            <h3 class="text-xl font-semibold text-gray-900">{room.name}</h3>
            <p class="mt-2 text-gray-600">{room.description}</p>
            <div class="mt-4 flex items-center justify-between">
              <span class="text-2xl font-bold text-blue-600">₹{room.price}</span
              >
              <button
                class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                on:click={() => goto("/login")}
              >
                Book Now
              </button>
            </div>
          </div>
        </div>
      {/each}
    </div>
  </div>

  <!-- Goals Section -->
  <div class="bg-gray-50 py-16">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h2 class="text-3xl font-bold text-gray-900 mb-8 text-center">
        Our Goals
      </h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        {#each goals as goal}
          <div class="bg-white p-6 rounded-lg shadow-lg">
            <h3 class="text-xl font-semibold text-gray-900 mb-2">
              {goal.title}
            </h3>
            <p class="text-gray-600">{goal.description}</p>
          </div>
        {/each}
      </div>
    </div>
  </div>

  <!-- Contact Form -->
  <div class="bg-gradient-to-br from-blue-50 to-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
      <div class="max-w-3xl mx-auto text-center mb-16">
        <h2 class="text-4xl font-bold text-gray-900 mb-4">Get in Touch</h2>
        <p class="text-xl text-gray-600">
          We'd love to hear from you. Your feedback helps us improve our
          services.
        </p>
      </div>
      <div class="max-w-2xl mx-auto bg-white rounded-2xl shadow-xl p-8 md:p-12">
        <form on:submit|preventDefault={handleContact} class="space-y-8">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div class="space-y-2">
              <label class="block text-lg font-medium text-gray-700">
                Your Name
              </label>
              <input
                type="text"
                bind:value={contactForm.name}
                required
                placeholder="John Doe"
                class="w-full px-4 py-3 rounded-lg border-2 border-gray-200
                                       focus:border-blue-500 focus:ring-2 focus:ring-blue-200
                                       transition-all text-lg"
              />
            </div>
            <div class="space-y-2">
              <label class="block text-lg font-medium text-gray-700">
                Email Address
              </label>
              <input
                type="email"
                bind:value={contactForm.email}
                required
                placeholder="john@example.com"
                class="w-full px-4 py-3 rounded-lg border-2 border-gray-200
                                       focus:border-blue-500 focus:ring-2 focus:ring-blue-200
                                       transition-all text-lg"
              />
            </div>
          </div>
          <div class="space-y-2">
            <label class="block text-lg font-medium text-gray-700">
              Your Message
            </label>
            <textarea
              bind:value={contactForm.message}
              required
              rows="6"
              placeholder="Tell us what's on your mind..."
              class="w-full px-4 py-3 rounded-lg border-2 border-gray-200
                                   focus:border-blue-500 focus:ring-2 focus:ring-blue-200
                                   transition-all text-lg resize-none"
            ></textarea>
          </div>
          <div class="flex flex-col items-center space-y-4">
            <button
              type="submit"
              class="w-full md:w-auto px-8 py-4 bg-blue-600 text-white rounded-lg
                                   hover:bg-blue-700 transform hover:scale-105 transition-all
                                   flex items-center justify-center text-lg font-medium"
            >
              <Send class="w-5 h-5 mr-2" />
              Send Message
            </button>
            <p class="text-gray-500 text-center">
              We typically respond within 24 hours
            </p>
          </div>
        </form>
      </div>
    </div>
  </div>
</main>

<!-- Footer -->
<footer class="bg-gray-900 text-white">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
      <div>
        <div class="flex items-center mb-4">
          <Hotel class="w-8 h-8" />
          <span class="ml-2 text-xl font-bold">Bacteria Hotel</span>
        </div>
        <p class="text-gray-400">
          Experience luxury and comfort in the heart of the city.
        </p>
      </div>
      <div>
        <h3 class="text-lg font-semibold mb-4">Contact</h3>
        <div class="space-y-2">
          <p class="flex items-center text-gray-400">
            <MapPin class="w-5 h-5 mr-2" />
            123 Hotel Street, City, Country
          </p>
          <p class="flex items-center text-gray-400">
            <Phone class="w-5 h-5 mr-2" />
            +1 234 567 890
          </p>
          <p class="flex items-center text-gray-400">
            <Mail class="w-5 h-5 mr-2" />
            info@bacteriahotel.com
          </p>
        </div>
      </div>
      <div>
        <h3 class="text-lg font-semibold mb-4">Quick Links</h3>
        <ul class="space-y-2">
          <li>
            <a href="/about" class="text-gray-400 hover:text-white">About Us</a>
          </li>
          <li>
            <a href="/services" class="text-gray-400 hover:text-white"
              >Services</a
            >
          </li>
          <li>
            <a href="/rooms" class="text-gray-400 hover:text-white">Rooms</a>
          </li>
          <li>
            <a href="/contact" class="text-gray-400 hover:text-white">Contact</a
            >
          </li>
        </ul>
      </div>
    </div>
    <div class="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
      <p>&copy; 2024 Bacteria Hotel. All rights reserved.</p>
    </div>
  </div>
</footer>
