<script lang="ts">
    import { onMount } from "svelte";
    import type { Room } from "$lib/types";
    import DashboardLayout from "$lib/components/layout/DashboardLayout.svelte";
    import RoomCard from "$lib/components/bookings/RoomCard.svelte";
    import RoomDetailModal from "$lib/components/bookings/RoomDetailModal.svelte";
    import RoomSearch from "$lib/components/bookings/RoomSearch.svelte";

    let rooms: Room[] = [];
    let filteredRooms: Room[] = [];
    let selectedRoom: Room | null = null;
    let showModal = false;
    let loading = true;
    let error = "";

    // Search params
    let checkIn = "";
    let checkOut = "";
    let guests = 1;
    let roomType = "";

    onMount(async () => {
        try {
            const response = await fetch("/api/rooms");
            rooms = await response.json();
            filteredRooms = rooms;
            loading = false;
        } catch (err) {
            error = "Failed to load rooms";
            loading = false;
        }
    });

    function handleSearch(event: CustomEvent) {
        const { checkIn, checkOut, guests, roomType } = event.detail;
        filteredRooms = rooms.filter((room) => {
            if (roomType && room.type.toLowerCase() !== roomType.toLowerCase())
                return false;
            if (guests > room.capacity) return false;
            // Add more filtering logic based on availability
            return true;
        });
    }

    function handleViewDetails(event: CustomEvent) {
        const { roomId } = event.detail;
        selectedRoom = rooms.find((r) => r.id === roomId) || null;
        showModal = true;
    }

    function handleCloseModal() {
        showModal = false;
        selectedRoom = null;
    }

    function handleBookRoom(event: CustomEvent) {
        const { roomId } = event.detail;
        // Add booking logic
        console.log("Booking room:", roomId);
        showModal = false;
    }
</script>


<DashboardLayout>
    <div class="container mx-auto">
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">
            Available Rooms
        </h1>

        <RoomSearch
            {checkIn}
            {checkOut}
            {guests}
            {roomType}
            on:search={handleSearch}
        />

        {#if loading}
            <div class="text-center py-8">
                <p class="text-gray-600 dark:text-gray-400">Loading rooms...</p>
            </div>
        {:else if error}
            <div class="text-center py-8">
                <p class="text-red-600">{error}</p>
            </div>
        {:else if filteredRooms.length === 0}
            <div class="text-center py-8">
                <p class="text-gray-600 dark:text-gray-400">
                    No rooms found matching your criteria.
                </p>
            </div>
        {:else}
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {#each filteredRooms as room (room.id)}
                    <RoomCard {room} on:viewDetails={handleViewDetails} />
                {/each}
            </div>
        {/if}

        {#if selectedRoom}
            <RoomDetailModal
                room={selectedRoom}
                show={showModal}
                on:close={handleCloseModal}
                on:book={handleBookRoom}
            />
        {/if}
    </div>
</DashboardLayout>
