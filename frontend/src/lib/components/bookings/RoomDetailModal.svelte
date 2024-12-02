
<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    import { fade, fly } from 'svelte/transition';
    import type { Room } from '$lib/types';
    import { X } from 'lucide-svelte';

    export let room: Room;
    export let show: boolean;

    const dispatch = createEventDispatcher();

    function close() {
        dispatch('close');
    }

    function bookRoom() {
        // Add booking logic
        dispatch('book', { roomId: room.id });
    }
</script>

{#if show}
    <div class="fixed inset-0 z-50 overflow-y-auto" transition:fade>
        <div class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center">
            <!-- Overlay -->
            <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" 
                 on:click={close}></div>

            <!-- Modal -->
            <div 
                class="relative bg-white dark:bg-gray-800 rounded-lg max-w-3xl w-full p-6 text-left shadow-xl transform transition-all"
                transition:fly={{ y: 20 }}
            >
                <!-- Close button -->
                <button 
                    class="absolute top-4 right-4 text-gray-400 hover:text-gray-500"
                    on:click={close}
                >
                    <X class="w-6 h-6" />
                </button>

                <!-- Content -->
                <div class="mt-2">
                    <div class="flex flex-col md:flex-row gap-6">
                        <div class="md:w-1/2">
                            <img 
                                src={room.imageUrl || "/api/placeholder/600/400"} 
                                alt={`Room ${room.number}`}
                                class="w-full h-64 object-cover rounded-lg"
                            />
                            <div class="grid grid-cols-3 gap-2 mt-2">
                                {#each room.images?.slice(0, 3) || [] as image}
                                    <img 
                                        src={image} 
                                        alt="Room view"
                                        class="w-full h-20 object-cover rounded-lg"
                                    />
                                {/each}
                            </div>
                        </div>
                        <div class="md:w-1/2">
                            <h2 class="text-2xl font-bold text-gray-900 dark:text-white">
                                {room.type} - Room {room.number}
                            </h2>
                            <p class="mt-2 text-lg text-blue-600 font-semibold">
                                ₹{room.pricePerNight} per night
                            </p>
                            <div class="mt-4">
                                <h3 class="font-semibold text-gray-900 dark:text-white">Room Features</h3>
                                <ul class="mt-2 space-y-2">
                                    <li class="text-gray-600 dark:text-gray-400">• {room.capacity} Guest Capacity</li>
                                    <li class="text-gray-600 dark:text-gray-400">• {room.bedType}</li>
                                    <li class="text-gray-600 dark:text-gray-400">• {room.sqft} sq ft</li>
                                </ul>
                            </div>
                            <div class="mt-4">
                                <h3 class="font-semibold text-gray-900 dark:text-white">Amenities</h3>
                                <div class="mt-2 flex flex-wrap gap-2">
                                    {#each room.amenities as amenity}
                                        <span class="px-2 py-1 text-sm rounded-full bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300">
                                            {amenity}
                                        </span>
                                    {/each}
                                </div>
                            </div>
                            <div class="mt-6">
                                <h3 class="font-semibold text-gray-900 dark:text-white">Description</h3>
                                <p class="mt-2 text-gray-600 dark:text-gray-400">
                                    {room.description}
                                </p>
                            </div>
                            <button
                                class="mt-6 w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 transition-colors"
                                on:click={bookRoom}
                            >
                                Book Now
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
{/if}