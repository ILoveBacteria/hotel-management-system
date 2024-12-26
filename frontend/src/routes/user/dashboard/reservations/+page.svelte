<!-- src/routes/dashboard/reservation/+page.svelte -->
<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { PUBLIC_BASE_URL } from "$env/static/public";
  import type { RoomType, UserProfile } from "$lib/types";
  import DashboardLayout from "$lib/components/layout/DashboardLayout.svelte";
  import {
    Calendar,
    CreditCard,
    BedDouble,
    Users,
    CheckCircle,
  } from "lucide-svelte";

  let userProfile: UserProfile | null = null;
  let roomTypes: RoomType[] = [];
  let selectedRoomType: RoomType | null = null;
  let checkIn = "";
  let checkOut = "";
  let guests = 1;
  let isLoading = false;
  let error: string | null = null;
  let success = false;

  // Calculate total nights and price
  $: totalNights =
    checkIn && checkOut
      ? Math.ceil(
          (new Date(checkOut).getTime() - new Date(checkIn).getTime()) /
            (1000 * 60 * 60 * 24)
        )
      : 0;
  $: totalPrice = selectedRoomType ? totalNights * selectedRoomType.price : 0;

  async function loadInitialData() {
    try {
      const [profileResponse, roomTypesResponse] = await Promise.all([
        fetch(`${PUBLIC_BASE_URL}/users/profile/`, {
          credentials: "include",
        }),
        fetch(`${PUBLIC_BASE_URL}/rooms/types/`, {
          credentials: "include",
        }),
      ]);

      if (!profileResponse.ok) {
        goto("/");
        return;
      }

      if (roomTypesResponse.ok) {
        const roomTypesData = await roomTypesResponse.json();
        roomTypes = roomTypesData.results;
      }

      userProfile = await profileResponse.json();
    } catch (err) {
      console.error("Failed to load data:", err);
      error = "Failed to load initial data";
    }
  }

  function getCookie(cname : string) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(";");
    for (var i = 0; i < ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) == " ") {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }

  async function handleSubmit() {
    if (!selectedRoomType || !checkIn || !checkOut) {
      error = "Please fill in all required fields";
      return;
    }

    isLoading = true;
    error = null;

    try {

      alert(getCookie("csrftoken"))
      const response = await fetch(
        `${PUBLIC_BASE_URL}/rooms/types/${selectedRoomType.id}/reserve/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
          body: JSON.stringify({
            check_in: checkIn,
            check_out: checkOut,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to create reservation");
      }

      success = true;
      setTimeout(() => {
        goto("/user/dashboard");
      }, 2000);
    } catch (err) {
      console.error("Reservation failed:", err);
      error = "Failed to create reservation. Please try again.";
    } finally {
      isLoading = false;
    }
  }

  onMount(() => {
    loadInitialData();
  });
</script>

<DashboardLayout username={userProfile?.username || "Guest"}>
  <div class="max-w-4xl mx-auto space-y-6">
    <!-- Page Header -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
      <h1 class="text-2xl font-semibold text-gray-900 dark:text-white">
        Make a Reservation
      </h1>
      <p class="mt-2 text-gray-600 dark:text-gray-400">
        Select your room type and dates to make a reservation
      </p>
    </div>

    <!-- Main Form -->
    <form on:submit|preventDefault={handleSubmit} class="space-y-6">
      {#if error}
        <div
          class="bg-red-50 dark:bg-red-900/50 text-red-600 dark:text-red-200 p-4 rounded-lg"
        >
          {error}
        </div>
      {/if}

      {#if success}
        <div
          class="bg-green-50 dark:bg-green-900/50 text-green-600 dark:text-green-200 p-4 rounded-lg flex items-center"
        >
          <CheckCircle class="w-5 h-5 mr-2" />
          Reservation created successfully! Redirecting to dashboard...
        </div>
      {/if}

      <!-- Room Selection -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
        <h2
          class="text-lg font-medium text-gray-900 dark:text-white mb-4 flex items-center"
        >
          <BedDouble class="w-5 h-5 mr-2" />
          Select Room Type
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          {#each roomTypes as roomType}
            <button
              type="button"
              class="p-4 border-2 rounded-lg text-left transition-all
                                {selectedRoomType?.id === roomType.id
                ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                : 'border-gray-200 dark:border-gray-700 hover:border-blue-200'}"
              on:click={() => (selectedRoomType = roomType)}
            >
              <div class="flex justify-between items-start">
                <div>
                  <h3 class="font-medium text-gray-900 dark:text-white">
                    {roomType.name}
                  </h3>
                  <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
                    {roomType.description}
                  </p>
                </div>
                <p class="text-lg font-semibold text-blue-600">
                  ₹{roomType.price}/night
                </p>
              </div>
              <div
                class="mt-4 flex items-center text-sm text-gray-500 dark:text-gray-400"
              >
                <span class="flex items-center">
                  <BedDouble class="w-4 h-4 mr-1" />
                  {roomType.double_beds} Double, {roomType.single_beds} Single
                </span>
              </div>
            </button>
          {/each}
        </div>
      </div>

      <!-- Dates and Guests -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
        <h2
          class="text-lg font-medium text-gray-900 dark:text-white mb-4 flex items-center"
        >
          <Calendar class="w-5 h-5 mr-2" />
          Select Dates
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label
              class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
            >
              Check-in Date
            </label>
            <input
              type="date"
              bind:value={checkIn}
              min={new Date().toISOString().split("T")[0]}
              required
              class="w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
            />
          </div>
          <div>
            <label
              class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
            >
              Check-out Date
            </label>
            <input
              type="date"
              bind:value={checkOut}
              min={checkIn || new Date().toISOString().split("T")[0]}
              required
              class="w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
            />
          </div>
        </div>

        <div class="mt-4">
          <label
            class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
          >
            Number of Guests
          </label>
          <div class="flex items-center">
            <Users class="w-5 h-5 mr-2 text-gray-400" />
            <input
              type="number"
              bind:value={guests}
              min="1"
              max="4"
              class="w-24 rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
            />
          </div>
        </div>
      </div>

      <!-- Price Summary -->
      {#if selectedRoomType && totalNights > 0}
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
          <h2
            class="text-lg font-medium text-gray-900 dark:text-white mb-4 flex items-center"
          >
            <CreditCard class="w-5 h-5 mr-2" />
            Price Summary
          </h2>
          <div class="space-y-3">
            <div class="flex justify-between text-gray-600 dark:text-gray-400">
              <span>Room Rate (per night)</span>
              <span>₹{selectedRoomType.price}</span>
            </div>
            <div class="flex justify-between text-gray-600 dark:text-gray-400">
              <span>Number of Nights</span>
              <span>{totalNights}</span>
            </div>
            <div class="flex justify-between text-gray-600 dark:text-gray-400">
              <span>Number of Guests</span>
              <span>{guests}</span>
            </div>
            <div class="pt-3 border-t border-gray-200 dark:border-gray-700">
              <div class="flex justify-between font-semibold text-lg">
                <span>Total Amount</span>
                <span class="text-blue-600">₹{totalPrice}</span>
              </div>
            </div>
          </div>
        </div>
      {/if}

      <!-- Submit Button -->
      <button
        type="submit"
        class="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700
                       transition-colors flex items-center justify-center disabled:opacity-50"
        disabled={isLoading ||
          !selectedRoomType ||
          !checkIn ||
          !checkOut ||
          success}
      >
        {#if isLoading}
          <svg class="animate-spin h-5 w-5 mr-2" viewBox="0 0 24 24">
            <circle
              class="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
              fill="none"
            />
            <path
              class="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
          Processing...
        {:else}
          Confirm Reservation
        {/if}
      </button>
    </form>
  </div>
</DashboardLayout>
