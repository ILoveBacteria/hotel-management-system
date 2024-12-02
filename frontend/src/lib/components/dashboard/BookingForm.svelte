<script lang="ts">
    let checkInDate: string = "";
    let checkOutDate: string = "";
    let roomType: string = "standard";

    async function handleSubmit(e: Event) {
        e.preventDefault();
        try {
            // Add booking logic here
            const bookingData = {
                checkInDate,
                checkOutDate,
                roomType,
            };
            // Example: await bookingService.createBooking(bookingData);
            alert("Booking successful!");
        } catch (error) {
            console.error("Booking failed:", error);
            alert("Booking failed. Please try again.");
        }
    }
</script>

<div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
    <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">
        Book a Room
    </h2>
    <form class="space-y-4" on:submit|preventDefault={handleSubmit}>
        <div>
            <label
                class="block text-sm font-medium text-gray-700 dark:text-gray-300"
            >
                Check In Date
            </label>
            <input
                type="date"
                bind:value={checkInDate}
                class="mt-1 block w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                required
            />
        </div>
        <div>
            <label
                class="block text-sm font-medium text-gray-700 dark:text-gray-300"
            >
                Check Out Date
            </label>
            <input
                type="date"
                bind:value={checkOutDate}
                class="mt-1 block w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                required
            />
        </div>
        <div>
            <label
                class="block text-sm font-medium text-gray-700 dark:text-gray-300"
            >
                Room Type
            </label>
            <select
                bind:value={roomType}
                class="mt-1 block w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
            >
                <option value="standard">Standard Room</option>
                <option value="deluxe">Deluxe Room</option>
                <option value="suite">Suite</option>
            </select>
        </div>
        <button
            type="submit"
            class="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors"
        >
            Book Now
        </button>
    </form>
</div>
