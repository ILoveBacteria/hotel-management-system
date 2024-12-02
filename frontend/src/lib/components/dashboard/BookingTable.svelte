<script lang="ts">
    import type { Booking } from "$lib/types";
    export let bookings: Booking[];

    function viewAllBookings() {
        // Add view all logic
    }
</script>

<div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
    <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold text-gray-900 dark:text-white">
            Your Bookings
        </h2>
        <button
            class="text-blue-600 hover:text-blue-700 text-sm font-medium"
            on:click={viewAllBookings}
        >
            View All
        </button>
    </div>
    <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead>
                <tr>
                    <th
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase"
                    >
                        Booking ID
                    </th>
                    <th
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase"
                    >
                        Room
                    </th>
                    <th
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase"
                    >
                        Check In
                    </th>
                    <th
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase"
                    >
                        Check Out
                    </th>
                    <th
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase"
                    >
                        Status
                    </th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
                {#each bookings as booking}
                    <tr>
                        <td
                            class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white"
                        >
                            {booking.id}
                        </td>
                        <td
                            class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white"
                        >
                            {booking.roomNumber}
                        </td>
                        <td
                            class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white"
                        >
                            {booking.checkIn}
                        </td>
                        <td
                            class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white"
                        >
                            {booking.checkOut}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span
                                class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full
                                {booking.status === 'Confirmed'
                                    ? 'bg-green-100 text-green-800'
                                    : booking.status === 'Pending'
                                      ? 'bg-yellow-100 text-yellow-800'
                                      : 'bg-blue-100 text-blue-800'}"
                            >
                                {booking.status}
                            </span>
                        </td>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>
</div>
