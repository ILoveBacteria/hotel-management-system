<script lang="ts">
    import { onMount } from "svelte";
    import type { Booking, HotelEvent } from "$lib/types";
    import DashboardLayout from "$lib/components/layout/DashboardLayout.svelte";
    import QuickStats from "$lib/components/dashboard/QuickStats.svelte";
    import BookingTable from "$lib/components/dashboard/BookingTable.svelte";
    import BookingForm from "$lib/components/dashboard/BookingForm.svelte";
    import ServiceForm from "$lib/components/dashboard/ServiceForm.svelte";
    import EventsTable from "$lib/components/dashboard/EventsTable.svelte";

    let currentRoom = "301";
    let loyaltyPoints = 2540;
    let totalStays = 12;
    let nextBooking = "Dec 24";

    let bookings: Booking[] = [];
    let events: HotelEvent[] = [];
    let selectedService = "";
    let serviceDate = "";
    let serviceTime = "";

    onMount(async () => {
        // Fetch data
    });
</script>


<DashboardLayout>
    <QuickStats {currentRoom} {loyaltyPoints} {totalStays} {nextBooking} />
    <BookingTable {bookings} />
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <BookingForm />
        <ServiceForm {selectedService} {serviceDate} {serviceTime} />
    </div>
    <EventsTable {events} />
</DashboardLayout>
