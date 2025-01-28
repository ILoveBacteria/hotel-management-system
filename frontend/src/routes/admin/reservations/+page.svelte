
<!-- src/routes/admin/reservations/+page.svelte -->
<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { PUBLIC_BASE_URL } from '$env/static/public';
    import type { UserProfile, Reserve, RoomType, Room } from '$lib/types';
    import {
        CalendarDays,
        Filter,
        Pencil,
        Trash2,
        RefreshCcw,
        AlertTriangle,
        Loader2,
        CheckCircle,
        X,
        Search,
        ChevronLeft,
        ChevronRight
    } from 'lucide-svelte';

    // Reservation status types
    type ReservationStatus =
        | 'registered'
        | 'canceled'
        | 'paid'
        | 'check-in'
        | 'check-out';

    // Filtering and pagination
    let currentPage = 1;
    let totalPages = 1;
    let pageSize = 10;
    let searchQuery = '';
    let statusFilter: ReservationStatus | '' = '';
    let dateRangeFilter = {
        start: '',
        end: '',
    };

    let selectedReservation: Reserve | null = null;

    // Data state
    let reservations: Reserve[] = [];
    let roomTypes: RoomType[] = [];
    let rooms: Room[] = [];

    // UI State
    let isLoading = true;
    let error: string | null = null;
    let showDeleteModal = false;
    let showEditModal = false;
    let isSaving = false;

    // Edit Reservation Form Data
    let editFormData: Partial<Reserve> = {};

    // Fetch initial data
    async function loadInitialData() {
        isLoading = true;
        error = null;

        try {
            // Verify admin access
            const profileResponse = await fetch(
                `${PUBLIC_BASE_URL}/users/profile/`,
                {
                    credentials: 'include',
                },
            );

            if (!profileResponse.ok) {
                goto('/admin/login');
                return;
            }

            const userProfile: UserProfile = await profileResponse.json();
            if (!userProfile.is_superuser) {
                goto('/admin/login');
                return;
            }

            // Fetch reservations with pagination and potential filters
            const reservationsUrl = new URL(
                `${PUBLIC_BASE_URL}/reservations/reserves/`,
            );
            reservationsUrl.searchParams.append('page', currentPage.toString());

            if (searchQuery) {
                reservationsUrl.searchParams.append('search', searchQuery);
            }
            if (statusFilter) {
                reservationsUrl.searchParams.append('status', statusFilter);
            }
            if (dateRangeFilter.start) {
                reservationsUrl.searchParams.append(
                    'check_in__gte',
                    dateRangeFilter.start,
                );
            }
            if (dateRangeFilter.end) {
                reservationsUrl.searchParams.append(
                    'check_out__lte',
                    dateRangeFilter.end,
                );
            }

            const [reservationsResponse, roomTypesResponse, roomsResponse] =
                await Promise.all([
                    fetch(reservationsUrl.toString(), {
                        credentials: 'include',
                    }),
                    fetch(`${PUBLIC_BASE_URL}/rooms/types/`, {
                        credentials: 'include',
                    }),
                    fetch(`${PUBLIC_BASE_URL}/rooms/inventories/`, {
                        credentials: 'include',
                    }),
                ]);

            if (
                !reservationsResponse.ok ||
                !roomTypesResponse.ok ||
                !roomsResponse.ok
            ) {
                throw new Error('Failed to fetch reservation data');
            }

            const reservationsData = await reservationsResponse.json();
            const roomTypesData = await roomTypesResponse.json();
            const roomsData = await roomsResponse.json();

            reservations = reservationsData.results;
            totalPages = Math.ceil(reservationsData.count / pageSize);
            roomTypes = roomTypesData.results;
            rooms = roomsData.results;
        } catch (err) {
            console.error('Failed to load reservation data:', err);
            error = 'Failed to load reservation data';
        } finally {
            isLoading = false;
        }
    }

    // Edit Reservation
    async function handleReservationEdit() {
        if (!selectedReservation) return;

        isSaving = true;
        error = null;

        try {
            const response = await fetch(
                `${PUBLIC_BASE_URL}/reservations/reserves/${selectedReservation.id}/`,
                {
                    method: 'PATCH',
                    credentials: 'include',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(editFormData),
                },
            );

            if (!response.ok) {
                throw new Error('Failed to update reservation');
            }

            await loadInitialData();
            showEditModal = false;
            selectedReservation = null;
        } catch (err) {
            console.error('Failed to edit reservation:', err);
            error = 'Failed to update reservation';
        } finally {
            isSaving = false;
        }
    }

    // Delete Reservation
    async function handleReservationDelete() {
        if (!selectedReservation) return;

        isSaving = true;
        error = null;

        try {
            const response = await fetch(
                `${PUBLIC_BASE_URL}/reservations/reserves/${selectedReservation.id}/`,
                {
                    method: 'DELETE',
                    credentials: 'include',
                },
            );

            if (!response.ok) {
                throw new Error('Failed to delete reservation');
            }

            await loadInitialData();
            showDeleteModal = false;
            selectedReservation = null;
        } catch (err) {
            console.error('Failed to delete reservation:', err);
            error = 'Failed to delete reservation';
        } finally {
            isSaving = false;
        }
    }

    // Utility Functions
    function formatDate(dateString: string): string {
        return new Date(dateString).toLocaleDateString('en-IN', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
        });
    }

    function getRoomTypeById(roomTypeId: number): string {
        const roomType = roomTypes.find((rt) => rt.id === roomTypeId);
        return roomType ? roomType.name : 'Unknown';
    }

    function getRoomNumberById(roomId: string): string {

        const extractRoomId = roomId.split("/")[roomId.split("/").length-2]

        const room = rooms.find((r) => r.room_number === +extractRoomId);
        return room ? room.room_number.toString() : 'N/A';
    }

    function getStatusColor(status: ReservationStatus): { bg: string; text: string } {
        switch (status) {
            case 'registered':
                return { bg: 'bg-yellow-100', text: 'text-yellow-800' };
            case 'paid':
                return { bg: 'bg-green-100', text: 'text-green-800' };
            case 'canceled':
                return { bg: 'bg-red-100', text: 'text-red-800' };
            case 'check-in':
                return { bg: 'bg-blue-100', text: 'text-blue-800' };
            case 'check-out':
                return { bg: 'bg-purple-100', text: 'text-purple-800' };
            default:
                return { bg: 'bg-gray-100', text: 'text-gray-800' };
        }
    }

    // Lifecycle
    onMount(loadInitialData);

    // Reactive pagination
    $: {
        if (currentPage > 0 && currentPage <= totalPages) {
            loadInitialData();
        }
    }
</script>

<div class="bg-gray-50 dark:bg-gray-900 min-h-screen p-8">
    <div class="max-w-7xl mx-auto space-y-6">
        <!-- Page Header -->
        <div class="flex justify-between items-center mb-6">
            <div>
                <h1 class="text-3xl font-bold text-gray-900 dark:text-white flex items-center">
                    <CalendarDays class="w-8 h-8 mr-3 text-blue-600" />
                    Reservations Management
                </h1>
                <p class="text-gray-500 dark:text-gray-400 mt-2">
                    View, manage, and track all hotel reservations
                </p>
            </div>
            <div class="flex items-center space-x-3">
                <button 
                    class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors shadow-md hover:shadow-lg"
                    on:click={loadInitialData}
                >
                    <RefreshCcw class="w-4 h-4" />
                    Refresh Data
                </button>
            </div>
        </div>

        <!-- Filters -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 border border-gray-200 dark:border-gray-700">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <!-- Search Input -->
                <div class="relative">
                    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <Search class="w-5 h-5 text-gray-400" />
                    </div>
                    <input
                        type="text"
                        bind:value={searchQuery}
                        placeholder="Search reservations..."
                        class="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white transition-all"
                    />
                </div>

                <!-- Status Filter -->
                <select
                    bind:value={statusFilter}
                    class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                >
                    <option value="">All Statuses</option>
                    <option value="registered">Registered</option>
                    <option value="paid">Paid</option>
                    <option value="canceled">Canceled</option>
                    <option value="check-in">Check-In</option>
                    <option value="check-out">Check-Out</option>
                </select>

                <!-- Date Range Start -->
                <input
                    type="date"
                    bind:value={dateRangeFilter.start}
                    class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                    placeholder="Start Date"
                />

                <!-- Date Range End -->
                <input
                    type="date"
                    bind:value={dateRangeFilter.end}
                    class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                    placeholder="End Date"
                />
            </div>
        </div>

        <!-- Error Handling -->
        {#if error}
            <div class="bg-red-50 dark:bg-red-900/50 text-red-600 dark:text-red-200 p-4 rounded-lg flex items-center border border-red-200 dark:border-red-900 shadow-md">
                <AlertTriangle class="w-6 h-6 mr-3" />
                {error}
            </div>
        {/if}

        <!-- Reservations Table -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden border border-gray-200 dark:border-gray-700">
            {#if isLoading}
                <div class="flex justify-center items-center h-64">
                    <Loader2 class="w-10 h-10 animate-spin text-blue-600" />
                </div>
            {:else if reservations.length === 0}
                <div class="text-center p-12 text-gray-500 dark:text-gray-400">
                    <CalendarDays class="w-16 h-16 mx-auto mb-4 text-gray-300 dark:text-gray-600" />
                    <p>No reservations found matching your criteria</p>
                </div>
            {:else}
                <div class="overflow-x-auto">
                    <table class="w-full divide-y divide-gray-200 dark:divide-gray-700">
                        <thead class="bg-gray-50 dark:bg-gray-700/50">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 dark:text-gray-300 uppercase tracking-wider">Reservation ID</th>
                                <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 dark:text-gray-300 uppercase tracking-wider">Guest</th>
                                <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 dark:text-gray-300 uppercase tracking-wider">Room</th>
                                <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 dark:text-gray-300 uppercase tracking-wider">Check-In</th>
                                <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 dark:text-gray-300 uppercase tracking-wider">Check-Out</th>
                                <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 dark:text-gray-300 uppercase tracking-wider">Price</th>
                                <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 dark:text-gray-300 uppercase tracking-wider">Status</th>
                                <th class="px-6 py-3 text-right text-xs font-semibold text-gray-600 dark:text-gray-300 uppercase tracking-wider">Actions</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
                            {#each reservations as reservation}
                                <tr class="hover:bg-gray-50 dark:hover:bg-gray-700/25 transition-colors">
                                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                                        #{reservation.id}
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                                        User #{reservation.user}
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                                        Room #{getRoomNumberById(reservation.room.toString())}
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                                        {formatDate(reservation.check_in)}
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                                        {formatDate(reservation.check_out)}
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white font-semibold">
                                        ₹{reservation.price.toLocaleString()}
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span class={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(reservation.status).bg} ${getStatusColor(reservation.status).text}`}>
                                            {reservation.status}
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                        <div class="flex justify-end space-x-2">
                                            <button
                                                class="text-blue-600 hover:text-blue-900 dark:hover:text-blue-400 transition-colors"
                                                on:click={() => {
                                                    selectedReservation = reservation;
                                                    editFormData = { ...reservation };
                                                    showEditModal = true;
                                                }}
                                            >
                                                <Pencil class="w-5 h-5" />
                                            </button>
                                            <button
                                                class="text-red-600 hover:text-red-900 dark:hover:text-red-400 transition-colors"
                                                on:click={() => {
                                                    selectedReservation = reservation;
                                                    showDeleteModal = true;
                                                }}
                                            >
                                                <Trash2 class="w-5 h-5" />
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                </div>
            {/if}
        </div>

        <!-- Pagination -->
        {#if totalPages > 1}
            <div class="flex justify-between items-center bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 border border-gray-200 dark:border-gray-700">
                <span class="text-sm text-gray-500 dark:text-gray-400">
                    Page {currentPage} of {totalPages}
                </span>
                <div class="flex space-x-2">
                    <button
                        class="p-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-600 disabled:opacity-50 transition-colors"
                        disabled={currentPage === 1}
                        on:click={() => currentPage--}
                    >
                        <ChevronLeft class="w-5 h-5 text-gray-600 dark:text-gray-300" />
                    </button>
                    <button
                        class="p-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-600 disabled:opacity-50 transition-colors"
                        disabled={currentPage === totalPages}
                        on:click={() => currentPage++}
                    >
                        <ChevronRight class="w-5 h-5 text-gray-600 dark:text-gray-300" />
                    </button>
                </div>
            </div>
        {/if}

        <!-- Edit Reservation Modal -->
        {#if showEditModal && selectedReservation}
            <div class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4 backdrop-blur-sm">
                <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-hidden animate-fade-in">
                    <!-- Modal Header -->
                    <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
                        <h2 class="text-xl font-bold text-gray-900 dark:text-white">
                            Edit Reservation ##{selectedReservation.id}
                        </h2>
                        <button
                            class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                            on:click={() => {
                                showEditModal = false;
                                selectedReservation = null;
                            }}
                        >
                            <X class="w-6 h-6" />
                        </button>
                    </div>

                    <!-- Modal Body -->
                    <form on:submit|preventDefault={handleReservationEdit} class="p-6 space-y-6">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <!-- Check-In Date -->
                            <div>
                                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                    Check-In Date
                                </label>
                                <input
                                    type="date"
                                    bind:value={editFormData.check_in}
                                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                                />
                            </div>

                            <!-- Check-Out Date -->
                            <div>
                                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                    Check-Out Date
                                </label>
                                <input
                                    type="date"
                                    bind:value={editFormData.check_out}
                                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                                />
                            </div>
                        </div>

                        <!-- Status -->
                        <div>
                            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                Reservation Status
                            </label>
                            <select
                                bind:value={editFormData.status}
                                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                            >
                                <option value="registered">Registered</option>
                                <option value="paid">Paid</option>
                                <option value="canceled">Canceled</option>
                                <option value="check-in">Check-In</option>
                                <option value="check-out">Check-Out</option>
                            </select>
                        </div>

                        <!-- Modal Actions -->
                        <div class="flex justify-end space-x-3">
                            <button
                                type="button"
                                class="px-4 py-2 text-gray-700 dark:text-gray-200 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 rounded-lg transition-colors"
                                on:click={() => {
                                    showEditModal = false;
                                    selectedReservation = null;
                                }}
                                disabled={isSaving}
                            >
                                Cancel
                            </button>
                            <button
                                type="submit"
                                class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2 disabled:opacity-50"
                                disabled={isSaving}
                            >
                                {#if isSaving}
                                    <Loader2 class="w-4 h-4 animate-spin" />
                                    Saving...
                                {:else}
                                    Save Changes
                                {/if}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        {/if}

        <!-- Delete Confirmation Modal -->
        {#if showDeleteModal && selectedReservation}
            <div class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4 backdrop-blur-sm">
                <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl w-full max-w-md p-6 animate-fade-in">
                    <div class="text-center">
                        <AlertTriangle class="w-16 h-16 mx-auto mb-4 text-red-500" />
                        <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">
                            Delete Reservation
                        </h3>
                        <p class="text-gray-600 dark:text-gray-400 mb-6">
                            Are you sure you want to delete Reservation ##{selectedReservation.id}? 
                            This action cannot be undone.
                        </p>
                    </div>
                    <div class="flex justify-center space-x-3">
                        <button
                            class="px-4 py-2 text-gray-700 dark:text-gray-200 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 rounded-lg transition-colors"
                            on:click={() => {
                                showDeleteModal = false;
                                selectedReservation = null;
                            }}
                            disabled={isSaving}
                        >
                            Cancel
                        </button>
                        <button
                            class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center gap-2 disabled:opacity-50"
                            on:click={handleReservationDelete}
                            disabled={isSaving}
                        >
                            {#if isSaving}
                                <Loader2 class="w-4 h-4 animate-spin" />
                                Deleting...
                            {:else}
                                Delete Reservation
                            {/if}
                        </button>
                    </div>
                </div>
            </div>
        {/if}
    </div>
</div>