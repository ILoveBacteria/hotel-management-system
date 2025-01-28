<script lang="ts">
	// Imports
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { PUBLIC_BASE_URL } from '$env/static/public';
	import type { UserProfile, Reserve } from '$lib/types';
	import DashboardLayout from '$lib/components/layout/DashboardLayout.svelte';
	import {
		Calendar,
		Search,
		AlertTriangle,
		Loader2,
		XCircle,
		Check,
		Clock,
		BanIcon,
		LogIn,
		LogOut,
	} from 'lucide-svelte';

	// State variables
	let userProfile: UserProfile | null = null;
	let reservations: Reserve[] = [];
	let isLoading = true;
	let error: string | null = null;
	let currentPage = 1;
	let totalPages = 1;
	let searchQuery = '';
	let showCancelModal = false;
	let selectedReservation: Reserve | null = null;
	let isCancelling = false;

	// Reactive declarations
	$: filteredReservations = reservations.filter(
		(reservation) =>
			reservation.room
				.toString()
				.toLowerCase()
				.includes(searchQuery.toLowerCase()) ||
			reservation.status
				.toLowerCase()
				.includes(searchQuery.toLowerCase()),
	);

	$: reservationStats = {
		total: reservations.length,
		active: reservations.filter((r) => r.status === 'check-in').length,
		upcoming: reservations.filter(
			(r) => r.status === 'registered' || r.status === 'paid',
		).length,
		completed: reservations.filter((r) => r.status === 'check-out').length,
		cancelled: reservations.filter((r) => r.status === 'canceled').length,
	};

	// Utility functions
	function formatDate(dateString: string): string {
		return new Date(dateString).toLocaleDateString('en-IN', {
			year: 'numeric',
			month: 'short',
			day: 'numeric',
		});
	}

	function formatAmount(amount: number): string {
		return new Intl.NumberFormat('en-IN', {
			style: 'currency',
			currency: 'INR',
		}).format(amount);
	}

	function getStatusIcon(status: string) {
		switch (status) {
			case 'registered':
				return Clock;
			case 'canceled':
				return BanIcon;
			case 'paid':
				return Check;
			case 'check-in':
				return LogIn;
			case 'check-out':
				return LogOut;
			default:
				return Clock;
		}
	}

	function getStatusColor(status: string): string {
		switch (status) {
			case 'registered':
				return 'bg-blue-100 text-blue-800 dark:bg-blue-900/20';
			case 'canceled':
				return 'bg-red-100 text-red-800 dark:bg-red-900/20';
			case 'paid':
				return 'bg-green-100 text-green-800 dark:bg-green-900/20';
			case 'check-in':
				return 'bg-purple-100 text-purple-800 dark:bg-purple-900/20';
			case 'check-out':
				return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20';
			default:
				return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20';
		}
	}

	// API functions
	async function loadReservations(page = 1) {
		isLoading = true;
		error = null;

		try {
			const [profileResponse, reservationsResponse] = await Promise.all([
				fetch(`${PUBLIC_BASE_URL}/users/profile/`, {
					credentials: 'include',
				}),
				fetch(`${PUBLIC_BASE_URL}/users/reserves/?page=${page}`, {
					credentials: 'include',
				}),
			]);

			if (!profileResponse.ok) {
				goto('/');
				return;
			}

			userProfile = await profileResponse.json();

			if (reservationsResponse.ok) {
				const data = await reservationsResponse.json();
				reservations = data.results;
				totalPages = Math.ceil(data.count / 10);
				currentPage = page;
			} else {
				throw new Error('Failed to fetch reservations');
			}
		} catch (err) {
			console.error('Failed to load reservations:', err);
			error = 'Failed to load reservation history';
		} finally {
			isLoading = false;
		}
	}

	async function handleCancel() {
		if (!selectedReservation) return;

		isCancelling = true;
		error = null;

		try {
			const response = await fetch(
				`${PUBLIC_BASE_URL}/reservations/reserves/${selectedReservation.id}/cancel/`,
				{
					method: 'POST',
					credentials: 'include',
					headers: {
						'Content-Type': 'application/json',
					},
				},
			);

			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(
					errorData.message || 'Failed to cancel reservation',
				);
			}

			await loadReservations(currentPage);
			showCancelModal = false;
			selectedReservation = null;
			alert('Reservation cancelled successfully');
		} catch (err) {
			console.error('Cancel failed:', err);
			error =
				err instanceof Error
					? err.message
					: 'Failed to cancel reservation';
		} finally {
			isCancelling = false;
		}
	}

	onMount(() => {
		loadReservations();
	});
</script>

<DashboardLayout username={userProfile?.username || 'Guest'}>
	<div class="max-w-7xl mx-auto space-y-6">
		<!-- Page Header -->
		<div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
			<h1
				class="text-2xl font-semibold text-gray-900 dark:text-white flex items-center"
			>
				<Calendar class="w-6 h-6 mr-2" />
				My Reservations
			</h1>
			<p class="mt-2 text-gray-600 dark:text-gray-400">
				View and manage your hotel reservations
			</p>
		</div>

		<!-- Reservation Statistics -->
		<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
			<!-- Total Reservations -->
			<div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
				<div class="flex items-center justify-between">
					<div>
						<p class="text-sm text-gray-500 dark:text-gray-400">
							Total Reservations
						</p>
						<p
							class="text-2xl font-semibold text-gray-900 dark:text-white"
						>
							{reservationStats.total}
						</p>
					</div>
					<div
						class="p-3 bg-blue-100 dark:bg-blue-900/20 rounded-full"
					>
						<Calendar class="w-6 h-6 text-blue-600" />
					</div>
				</div>
			</div>

			<!-- Active Stays -->
			<div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
				<div class="flex items-center justify-between">
					<div>
						<p class="text-sm text-gray-500 dark:text-gray-400">
							Active Stays
						</p>
						<p
							class="text-2xl font-semibold text-gray-900 dark:text-white"
						>
							{reservationStats.active}
						</p>
					</div>
					<div
						class="p-3 bg-green-100 dark:bg-green-900/20 rounded-full"
					>
						<LogIn class="w-6 h-6 text-green-600" />
					</div>
				</div>
			</div>

			<!-- Upcoming Stays -->
			<div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
				<div class="flex items-center justify-between">
					<div>
						<p class="text-sm text-gray-500 dark:text-gray-400">
							Upcoming
						</p>
						<p
							class="text-2xl font-semibold text-gray-900 dark:text-white"
						>
							{reservationStats.upcoming}
						</p>
					</div>
					<div
						class="p-3 bg-purple-100 dark:bg-purple-900/20 rounded-full"
					>
						<Clock class="w-6 h-6 text-purple-600" />
					</div>
				</div>
			</div>

			<!-- Completed Stays -->
			<div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
				<div class="flex items-center justify-between">
					<div>
						<p class="text-sm text-gray-500 dark:text-gray-400">
							Completed
						</p>
						<p
							class="text-2xl font-semibold text-gray-900 dark:text-white"
						>
							{reservationStats.completed}
						</p>
					</div>
					<div
						class="p-3 bg-gray-100 dark:bg-gray-900/20 rounded-full"
					>
						<Check class="w-6 h-6 text-gray-600" />
					</div>
				</div>
			</div>
		</div>

		<!-- Reservations Table -->
		<div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm">
			<div class="p-6 border-b border-gray-200 dark:border-gray-700">
				<div
					class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4"
				>
					<h2
						class="text-lg font-medium text-gray-900 dark:text-white"
					>
						Reservation History
					</h2>
					<div class="relative">
						<Search
							class="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"
						/>
						<input
							type="text"
							bind:value={searchQuery}
							placeholder="Search reservations..."
							class="pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
						/>
					</div>
				</div>
			</div>

			{#if error}
				<div class="p-6">
					<div
						class="bg-red-50 dark:bg-red-900/50 text-red-600 dark:text-red-200 p-4 rounded-lg flex items-center"
					>
						<AlertTriangle class="w-5 h-5 mr-2" />
						{error}
					</div>
				</div>
			{/if}

			{#if isLoading}
				<div class="p-6">
					<div class="flex justify-center">
						<Loader2 class="w-8 h-8 animate-spin text-blue-600" />
					</div>
				</div>
			{:else if filteredReservations.length === 0}
				<div class="p-6 text-center text-gray-500 dark:text-gray-400">
					No reservations found
				</div>
			{:else}
				<div class="overflow-x-auto">
					<table
						class="min-w-full divide-y divide-gray-200 dark:divide-gray-700"
					>
						<thead class="bg-gray-50 dark:bg-gray-700/50">
							<tr>
								<th
									class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider"
								>
									Reservation ID
								</th>
								<th
									class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider"
								>
									Room
								</th>
								<th
									class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider"
								>
									Check In
								</th>
								<th
									class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider"
								>
									Check Out
								</th>
								<th
									class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider"
								>
									Price
								</th>
								<th
									class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider"
								>
									Status
								</th>
								<th
									class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider"
								>
									Actions
								</th>
							</tr>
						</thead>
						<tbody
							class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700"
						>
							{#each filteredReservations as reservation}
								<tr>
									<td
										class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white"
									>
										#{reservation.id}
									</td>
									<td
										class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white"
									>
										Room #{reservation.room}
									</td>
									<td
										class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white"
									>
										{formatDate(reservation.check_in)}
									</td>
									<td
										class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white"
									>
										{formatDate(reservation.check_out)}
									</td>
									<td
										class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white"
									>
										{formatAmount(reservation.price)}
									</td>
									<td class="px-6 py-4 whitespace-nowrap">
										<span
											class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium {getStatusColor(
												reservation.status,
											)}"
										>
											<svelte:component
												this={getStatusIcon(
													reservation.status,
												)}
												class="w-4 h-4 mr-1"
											/>
											{reservation.status
												.charAt(0)
												.toUpperCase() +
												reservation.status.slice(1)}
										</span>
									</td>
									<td
										class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium"
									>
										{#if reservation.status === 'registered' || reservation.status === 'paid'}
											<button
												class="text-red-600 hover:text-red-700 font-medium"
												on:click={() => {
													selectedReservation =
														reservation;
													showCancelModal = true;
												}}
											>
												Cancel
											</button>
										{:else}
											<span class="text-gray-400"
												>No actions</span
											>
										{/if}
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>

				<!-- Pagination -->
				{#if totalPages > 1}
					<div
						class="px-6 py-4 border-t border-gray-200 dark:border-gray-700"
					>
						<div class="flex items-center justify-between">
							<div
								class="text-sm text-gray-500 dark:text-gray-400"
							>
								Showing page {currentPage} of {totalPages}
							</div>
							<div class="flex space-x-2">
								<button
									class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
									disabled={currentPage === 1}
									on:click={() =>
										loadReservations(currentPage - 1)}
								>
									Previous
								</button>
								<button
									class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
									disabled={currentPage === totalPages}
									on:click={() =>
										loadReservations(currentPage + 1)}
								>
									Next
								</button>
							</div>
						</div>
					</div>
				{/if}
			{/if}
		</div>
	</div>

	<!-- Cancel Confirmation Modal -->
	{#if showCancelModal && selectedReservation}
		<div
			class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4"
		>
			<div
				class="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md w-full mx-4"
			>
				<h3
					class="text-lg font-medium text-gray-900 dark:text-white mb-4"
				>
					Cancel Reservation
				</h3>
				<p class="text-gray-500 dark:text-gray-400 mb-4">
					Are you sure you want to cancel this reservation? This
					action cannot be undone.
				</p>
				<div class="flex justify-end gap-3">
					<button
						class="px-4 py-2 text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
						on:click={() => {
							showCancelModal = false;
							selectedReservation = null;
						}}
						disabled={isCancelling}
					>
						Keep Reservation
					</button>
					<button
						class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center gap-2 disabled:opacity-50"
						on:click={handleCancel}
						disabled={isCancelling}
					>
						{#if isCancelling}
							<Loader2 class="w-4 h-4 animate-spin" />
							Cancelling...
						{:else}
							Cancel Reservation
						{/if}
					</button>
				</div>
			</div>
		</div>
	{/if}
</DashboardLayout>
