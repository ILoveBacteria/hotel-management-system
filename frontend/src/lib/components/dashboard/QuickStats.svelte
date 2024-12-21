<script lang="ts">
    export let currentRoom: string;
    export let totalReservations: number;
    export let nextBooking: string;
    export let activeBooking: string;
</script>

<div class="grid grid-cols-1 md:grid-cols-4 gap-6">
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
        <h3 class="text-gray-500 dark:text-gray-400 text-sm font-medium">
            Current Room
        </h3>
        <p class="mt-2 text-3xl font-semibold text-gray-900 dark:text-white">
            {currentRoom}
        </p>
    </div>
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
        <h3 class="text-gray-500 dark:text-gray-400 text-sm font-medium">
            Total Reservations
        </h3>
        <p class="mt-2 text-3xl font-semibold text-gray-900 dark:text-white">
            {totalReservations}
        </p>
    </div>
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
        <h3 class="text-gray-500 dark:text-gray-400 text-sm font-medium">
            Active Booking
        </h3>
        <p class="mt-2 text-3xl font-semibold text-gray-900 dark:text-white">
            {activeBooking}
        </p>
    </div>
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
        <h3 class="text-gray-500 dark:text-gray-400 text-sm font-medium">
            Next Booking
        </h3>
        <p class="mt-2 text-3xl font-semibold text-gray-900 dark:text-white">
            {nextBooking}
        </p>
    </div>
</div>