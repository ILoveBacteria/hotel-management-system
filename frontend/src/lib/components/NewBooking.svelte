<!-- NewBooking.svelte -->
<script lang="ts">
  import { onMount } from "svelte";

  // Form data
  let bookingData = {
    guestName: "",
    email: "",
    phone: "",
    checkIn: "",
    checkOut: "",
    adults: 1,
    children: 0,
    roomType: "",
    specialRequests: "",
    totalNights: 0,
    roomRate: 4500,
    totalAmount: 0,
    availableRooms: 12,
  };

  $: {
    if (bookingData.checkIn && bookingData.checkOut) {
      const start = new Date(bookingData.checkIn);
      const end = new Date(bookingData.checkOut);
      const diffTime = Math.abs(end.getTime() - start.getTime());
      bookingData.totalNights = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      bookingData.totalAmount = bookingData.totalNights * bookingData.roomRate;
    }
  }

  // Available room types
  const roomTypes = [
    { id: "standard", name: "Standard Room", price: "₹3,500" },
    { id: "deluxe", name: "Deluxe Room", price: "₹4,500" },
    { id: "suite", name: "Suite", price: "₹6,500" },
  ];

  function handleSubmit() {
    // Handle form submission
    console.log("Booking Data:", bookingData);
  }
</script>

<div class="max-w-4xl mx-auto">
  <!-- Quick Actions -->
  <div class="flex justify-between items-center mb-6">
    <div>
      <h1 class="text-2xl font-semibold text-gray-800">New Booking</h1>
      <p class="text-gray-600">Create a new reservation</p>
    </div>
    <div class="flex gap-3">
      <button
        type="button"
        class="flex items-center gap-2 px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
      >
        <span>📋</span>
        <span>Draft</span>
      </button>
      <button
        type="button"
        class="flex items-center gap-2 px-4 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700"
      >
        <span>✨</span>
        <span>Quick Book</span>
      </button>
    </div>
  </div>

  <!-- Booking Form -->
  <form on:submit|preventDefault={handleSubmit} class="space-y-6">
    <!-- Stats Overview -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <div class="bg-white p-4 rounded-lg shadow-sm">
        <p class="text-sm text-gray-500">Room Rate</p>
        <p class="text-lg font-semibold">₹4,500/night</p>
      </div>
      <div class="bg-white p-4 rounded-lg shadow-sm">
        <p class="text-sm text-gray-500">Total Nights</p>
        <p class="text-lg font-semibold">0</p>
      </div>
      <div class="bg-white p-4 rounded-lg shadow-sm">
        <p class="text-sm text-gray-500">Total Amount</p>
        <p class="text-lg font-semibold">₹0</p>
      </div>
      <div class="bg-white p-4 rounded-lg shadow-sm">
        <p class="text-sm text-gray-500">Available Rooms</p>
        <p class="text-lg font-semibold text-green-600">12</p>
      </div>
    </div>

    <!-- Guest Information -->
    <div class="bg-white rounded-lg shadow-sm">
      <div class="p-4 border-b border-gray-200 bg-gray-50">
        <h2 class="text-lg font-medium text-gray-800">Guest Information</h2>
      </div>
      <div class="p-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Guest Name *
            </label>
            <input
              type="text"
              bind:value={bookingData.guestName}
              required
              class="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Email *
            </label>
            <input
              type="email"
              bind:value={bookingData.email}
              required
              class="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Phone Number *
            </label>
            <input
              type="tel"
              bind:value={bookingData.phone}
              required
              class="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        </div>
      </div>

      <!-- Stay Information -->
      <div class="bg-white rounded-lg shadow-sm mt-6">
        <div class="p-4 border-b border-gray-200 bg-gray-50">
          <h2 class="text-lg font-medium text-gray-800">Stay Information</h2>
        </div>
        <div class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Check-in Date *
              </label>
              <input
                type="date"
                bind:value={bookingData.checkIn}
                required
                class="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Check-out Date *
              </label>
              <input
                type="date"
                bind:value={bookingData.checkOut}
                required
                class="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Number of Adults *
              </label>
              <input
                type="number"
                bind:value={bookingData.adults}
                min="1"
                required
                class="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Number of Children
              </label>
              <input
                type="number"
                bind:value={bookingData.children}
                min="0"
                class="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>
        </div>

        <!-- Room Selection -->
        <div class="bg-white rounded-lg shadow-sm mt-6">
          <div class="p-4 border-b border-gray-200 bg-gray-50">
            <h2 class="text-lg font-medium text-gray-800">Room Selection</h2>
          </div>
          <div class="p-6">
            <div class="grid grid-cols-1 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Room Type *
                </label>
                <select
                  bind:value={bookingData.roomType}
                  required
                  class="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="">Select a room type</option>
                  {#each roomTypes as room}
                    <option value={room.id}
                      >{room.name} - {room.price}/night</option
                    >
                  {/each}
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Special Requests
                </label>
                <textarea
                  bind:value={bookingData.specialRequests}
                  rows="3"
                  class="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Any special requests or preferences..."
                ></textarea>
              </div>
            </div>
          </div>

          <!-- Form Actions -->
          <div class="bg-white rounded-lg shadow-sm mt-6">
            <div class="p-6 flex justify-between">
              <button
                type="button"
                class="flex items-center gap-2 px-4 py-2 text-red-600 bg-red-50 hover:bg-red-100 rounded-lg"
              >
                <span>🗑️</span>
                <span>Cancel Booking</span>
              </button>
              <div class="flex gap-3">
                <button
                  type="button"
                  class="flex items-center gap-2 px-4 py-2 text-gray-700 bg-white border border-gray-300 hover:bg-gray-50 rounded-lg"
                >
                  <span>💾</span>
                  <span>Save as Draft</span>
                </button>
                <button
                  type="submit"
                  class="flex items-center gap-2 px-6 py-2 text-white bg-blue-600 hover:bg-blue-700 rounded-lg"
                >
                  <span>✅</span>
                  <span>Confirm Booking</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </form>
</div>
