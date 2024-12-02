
<script lang="ts">
    import type { Room } from "$lib/types";
    import { createEventDispatcher } from 'svelte';
    
    export let room: Room;
    const dispatch = createEventDispatcher();

    function viewDetails() {
        dispatch('viewDetails', { roomId: room.id });
    }
</script>

<div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden">
    <img 
        src={room.imageUrl || "/api/placeholder/400/200"} 
        alt={`Room ${room.number}`}
        class="w-full h-48 object-cover"
    />
    <div class="p-4">
        <div class="flex justify-between items-start mb-2">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                Room {room.number}
            </h3>
            <span class="px-2 py-1 text-sm font-medium rounded-full bg-green-100 text-green-800">
                ₹{room.pricePerNight}/night
            </span>
        </div>
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">
            {room.type} • {room.capacity} Guests • {room.bedType}
        </p>
        <div class="flex flex-wrap gap-2 mb-4">
            {#each room.amenities.slice(0, 3) as amenity}
                <span class="px-2 py-1 text-xs rounded-full bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300">
                    {amenity}
                </span>
            {/each}
            {#if room.amenities.length > 3}
                <span class="px-2 py-1 text-xs rounded-full bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300">
                    +{room.amenities.length - 3} more
                </span>
            {/if}
        </div>
        <button
            class="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors"
            on:click={viewDetails}
        >
            View Details
        </button>
    </div>
</div>