
<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    import { Search, Calendar, Users } from 'lucide-svelte';

    export let checkIn = '';
    export let checkOut = '';
    export let guests = 1;
    export let roomType = '';

    const dispatch = createEventDispatcher();

    function handleSearch() {
        dispatch('search', {
            checkIn,
            checkOut,
            guests,
            roomType
        });
    }
</script>

<div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 mb-6">
    <form 
        class="grid grid-cols-1 md:grid-cols-4 gap-4"
        on:submit|preventDefault={handleSearch}
    >
        <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Check In
            </label>
            <div class="relative">
                <Calendar class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                    type="date"
                    bind:value={checkIn}
                    class="pl-10 w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                    required
                />
            </div>
        </div>

        <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Check Out
            </label>
            <div class="relative">
                <Calendar class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                    type="date"
                    bind:value={checkOut}
                    class="pl-10 w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                    required
                />
            </div>
        </div>

        <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Guests
            </label>
            <div class="relative">
                <Users class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <select
                    bind:value={guests}
                    class="pl-10 w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                >
                    {#each Array(6) as _, i}
                        <option value={i + 1}>{i + 1} Guest{i !== 0 ? 's' : ''}</option>
                    {/each}
                </select>
            </div>
        </div>

        <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Room Type
            </label>
            <select
                bind:value={roomType}
                class="w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
            >
                <option value="">Any Type</option>
                <option value="standard">Standard</option>
                <option value="deluxe">Deluxe</option>
                <option value="suite">Suite</option>
            </select>
        </div>

        <div class="md:col-span-4">
            <button
                type="submit"
                class="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors"
            >
                Search Rooms
            </button>
        </div>
    </form>
</div>