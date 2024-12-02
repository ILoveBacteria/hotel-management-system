<script lang="ts">
    import type { HotelEvent } from "$lib/types";
    export let events: HotelEvent[];

    function viewAllEvents() {
        // Add view all events logic
    }
</script>

<div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
    <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold text-gray-900 dark:text-white">
            Upcoming Events
        </h2>
        <button
            class="text-blue-600 hover:text-blue-700 text-sm font-medium"
            on:click={viewAllEvents}
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
                        >Event</th
                    >
                    <th
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase"
                        >Date</th
                    >
                    <th
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase"
                        >Time</th
                    >
                    <th
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase"
                        >Location</th
                    >
                    <th
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase"
                        >Status</th
                    >
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
                {#each events as event}
                    <tr>
                        <td
                            class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white"
                        >
                            {event.name}
                        </td>
                        <td
                            class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white"
                        >
                            {event.date}
                        </td>
                        <td
                            class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white"
                        >
                            {event.time}
                        </td>
                        <td
                            class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white"
                        >
                            {event.location}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span
                                class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800"
                            >
                                {event.status}
                            </span>
                        </td>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>
</div>
