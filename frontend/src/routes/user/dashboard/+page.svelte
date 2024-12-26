<script lang="ts">
    import { onMount } from "svelte";
    import type { UserProfile, Reserve } from "$lib/types";
    import DashboardLayout from "$lib/components/layout/DashboardLayout.svelte";
    import QuickStats from "$lib/components/dashboard/QuickStats.svelte";
    import BookingTable from "$lib/components/dashboard/BookingTable.svelte";
    import BookingForm from "$lib/components/dashboard/BookingForm.svelte";
    import ServiceForm from "$lib/components/dashboard/ServiceForm.svelte";
    import { goto } from "$app/navigation";
    import { page } from "$app/stores";
    import { PUBLIC_BASE_URL } from "$env/static/public";
    import axios from "axios";

    let userProfile: UserProfile | null = null;
    let reservations: Reserve[] = [];
    let isLoading = true;
    let error: string | null = null;

    // Dashboard stats
    let currentRoom = "Not checked in";
    let totalReservations = 0;
    let activeReservation: Reserve | null = null;
    let upcomingReservation: Reserve | null = null;

    // Service booking
    let selectedService = "";
    let serviceDate = "";
    let serviceTime = "";

    async function loadDashboardData() {
        isLoading = true;
        error = null;
        
        try {
            const [profileResponse, reservationsResponse] = await Promise.all([
                axios.get<UserProfile>(
                    `${PUBLIC_BASE_URL}/users/profile/`,
                    { withCredentials: true }
                ),
                axios.get<{ results: Reserve[] }>(
                    `${PUBLIC_BASE_URL}/users/reserves/`,
                    { withCredentials: true }
                )
            ]);

            if (profileResponse.status === 200) {
                userProfile = profileResponse.data;
            }

            if (reservationsResponse.status === 200) {
                reservations = reservationsResponse.data.results;
                totalReservations = reservations.length;
                activeReservation = reservations.find(r => r.status === 'check-in') || null;
                upcomingReservation = reservations.find(r => r.status === 'registered') || null;
                
                if (activeReservation) {
                    currentRoom = `Room ${activeReservation.room}`;
                }
            }
        } catch (err) {
            console.error('Failed to load dashboard data:', err);
            error = 'Failed to load dashboard data';
            if (axios.isAxiosError(err) && err.response?.status === 401) {
                goto("/");
            }
        } finally {
            isLoading = false;
        }
    }

    // Reload data when navigating back to dashboard
    $: if ($page.url.pathname === '/user/dashboard') {
        loadDashboardData();
    }

    onMount(() => {
        loadDashboardData();
    });
</script>

<DashboardLayout username={userProfile?.username || 'Guest'}>
    <div class="space-y-6">
        {#if userProfile}
            <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
                <h1 class="text-2xl font-semibold text-gray-900 dark:text-white">
                    Welcome back, {userProfile.first_name} {userProfile.last_name}
                </h1>
                <p class="text-gray-600 dark:text-gray-400 mt-2">
                    {userProfile.email}
                </p>
                {#if userProfile.guest_profile.phone_number}
                    <p class="text-gray-600 dark:text-gray-400">
                        Phone: {userProfile.guest_profile.phone_number}
                    </p>
                {/if}
            </div>
        {/if}

        <QuickStats 
            currentRoom={currentRoom}
            totalReservations={totalReservations}
            nextBooking={upcomingReservation ? upcomingReservation.check_in : 'No upcoming bookings'}
            activeBooking={activeReservation ? 'Active' : 'None'}
        />
        
        <BookingTable bookings={reservations} />

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <BookingForm />
            <ServiceForm 
                {selectedService} 
                {serviceDate} 
                {serviceTime} 
            />
        </div>
    </div>
</DashboardLayout>