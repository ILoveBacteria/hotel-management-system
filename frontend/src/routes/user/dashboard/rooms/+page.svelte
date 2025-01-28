<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { PUBLIC_BASE_URL } from '$env/static/public';
	import type { RoomType, RoomImage, UserProfile } from '$lib/types';
	import DashboardLayout from '$lib/components/layout/DashboardLayout.svelte';
	import {
		Search,
		BedDouble,
		Users,
		CreditCard,
		Filter,
		Loader2,
		AlertTriangle,
	} from 'lucide-svelte';

	let userProfile: UserProfile | null = null;
	let roomTypes: RoomType[] = [];
	let roomImages: Record<number, RoomImage[]> = {};
	let isLoading = true;
	let error: string | null = null;

	// Filter states
	let searchQuery = '';
	let priceRange = {
		min: 0,
		max: 10000,
	};
	let occupancyFilter = {
		singleBeds: 0,
		doubleBeds: 0,
	};
	let showFilters = false;

	// Computed room types based on filters
	$: filteredRoomTypes = roomTypes.filter((room) => {
		const matchesSearch =
			room.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
			room.description.toLowerCase().includes(searchQuery.toLowerCase());
		const matchesPrice =
			room.price >= priceRange.min && room.price <= priceRange.max;
		const matchesOccupancy =
			(!occupancyFilter.singleBeds ||
				room.single_beds >= occupancyFilter.singleBeds) &&
			(!occupancyFilter.doubleBeds ||
				room.double_beds >= occupancyFilter.doubleBeds);

		return matchesSearch && matchesPrice && matchesOccupancy;
	});

	async function loadRoomData() {
		try {
			const [profileResponse, roomTypesResponse, imagesResponse] =
				await Promise.all([
					fetch(`${PUBLIC_BASE_URL}/users/profile/`, {
						credentials: 'include',
					}),
					fetch(`${PUBLIC_BASE_URL}/rooms/types/`, {
						credentials: 'include',
					}),
					fetch(`${PUBLIC_BASE_URL}/rooms/images/`, {
						credentials: 'include',
					}),
				]);

			if (!profileResponse.ok) {
				goto('/user/login');
				return;
			}

			userProfile = await profileResponse.json();

			if (roomTypesResponse.ok && imagesResponse.ok) {
				const roomTypesData = await roomTypesResponse.json();
				const imagesData = await imagesResponse.json();

				roomTypes = roomTypesData.results;

				// Group images by room type
				roomImages = imagesData.results.reduce(
					(acc: Record<number, RoomImage[]>, img: RoomImage) => {
						const id = img.room_type.split('/');
						if (!acc[+id[id.length - 2]])
							acc[+id[id.length - 2]] = [];
						acc[+id[id.length - 2]].push(img);
						return acc;
					},
					{},
				);

				// Set price range based on available rooms
				if (roomTypes.length > 0) {
					priceRange.min = Math.min(...roomTypes.map((r) => r.price));
					priceRange.max = Math.max(...roomTypes.map((r) => r.price));
				}
			} else {
				throw new Error('Failed to fetch room data');
			}
		} catch (err) {
			console.error('Failed to load room data:', err);
			error = 'Failed to load room data';
		} finally {
			isLoading = false;
		}
	}

	function handleBookRoom(roomType: RoomType) {
		goto(`/user/dashboard/reservations?roomType=${roomType.id}`);
	}

	onMount(loadRoomData);
</script>

<DashboardLayout username={userProfile?.username || 'Guest'}>
	<div class="max-w-7xl mx-auto space-y-6">
		<!-- Page Header -->
		<div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
			<div class="flex justify-between items-center">
				<div>
					<h1
						class="text-2xl font-semibold text-gray-900 dark:text-white"
					>
						Available Rooms
					</h1>
					<p class="mt-2 text-gray-600 dark:text-gray-400">
						Browse and book our selection of comfortable rooms
					</p>
				</div>
				<button
					class="flex items-center gap-2 px-4 py-2 text-gray-700 dark:text-gray-200 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
					on:click={() => (showFilters = !showFilters)}
				>
					<Filter class="w-5 h-5" />
					Filters
				</button>
			</div>

			<!-- Search and Filters -->
			<div class="mt-6 space-y-4">
				<div class="relative">
					<Search
						class="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"
					/>
					<input
						type="text"
						bind:value={searchQuery}
						placeholder="Search rooms..."
						class="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
					/>
				</div>

				{#if showFilters}
					<div
						class="grid grid-cols-1 md:grid-cols-3 gap-4 p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg"
					>
						<!-- Price Range -->
						<div>
							<label
								class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
							>
								Price Range (₹)
							</label>
							<div class="flex gap-4">
								<input
									type="number"
									bind:value={priceRange.min}
									min="0"
									class="w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
									placeholder="Min"
								/>
								<input
									type="number"
									bind:value={priceRange.max}
									min="0"
									class="w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
									placeholder="Max"
								/>
							</div>
						</div>

						<!-- Bed Configuration -->
						<div>
							<label
								class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
							>
								Single Beds
							</label>
							<input
								type="number"
								bind:value={occupancyFilter.singleBeds}
								min="0"
								class="w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
								placeholder="Minimum single beds"
							/>
						</div>

						<div>
							<label
								class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
							>
								Double Beds
							</label>
							<input
								type="number"
								bind:value={occupancyFilter.doubleBeds}
								min="0"
								class="w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
								placeholder="Minimum double beds"
							/>
						</div>
					</div>
				{/if}
			</div>
		</div>

		<!-- Error State -->
		{#if error}
			<div
				class="bg-red-50 dark:bg-red-900/50 text-red-600 dark:text-red-200 p-4 rounded-lg flex items-center"
			>
				<AlertTriangle class="w-5 h-5 mr-2" />
				{error}
			</div>
		{/if}

		<!-- Loading State -->
		{#if isLoading}
			<div class="flex items-center justify-center h-64">
				<Loader2 class="w-8 h-8 animate-spin text-blue-600" />
			</div>
		{:else if filteredRoomTypes.length === 0}
			<div
				class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-8 text-center"
			>
				<BedDouble class="w-12 h-12 text-gray-400 mx-auto mb-4" />
				<p class="text-gray-600 dark:text-gray-400">
					No rooms found matching your criteria
				</p>
			</div>
		{:else}
			<!-- Room Grid -->
			<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
				{#each filteredRoomTypes as room}
					<div
						class="bg-white dark:bg-gray-800 rounded-lg shadow-sm overflow-hidden"
					>
						<!-- Room Image -->
						<div class="relative h-48">
							{#if roomImages[room.id]?.[0]}
								<img
									src={roomImages[room.id][0].image}
									alt={room.name}
									class="w-full h-full object-cover"
								/>
							{:else}
								<div
									class="w-full h-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center"
								>
									<BedDouble
										class="w-12 h-12 text-gray-400"
									/>
								</div>
							{/if}
						</div>

						<!-- Room Details -->
						<div class="p-6">
							<div class="flex justify-between items-start mb-4">
								<div>
									<h3
										class="text-lg font-semibold text-gray-900 dark:text-white"
									>
										{room.name}
									</h3>
									<p
										class="text-sm text-gray-500 dark:text-gray-400 mt-1"
									>
										{room.description}
									</p>
								</div>
								<p class="text-lg font-bold text-blue-600">
									₹{room.price}
									<span
										class="text-sm font-normal text-gray-500"
										>/night</span
									>
								</p>
							</div>

							<!-- Room Features -->
							<div class="space-y-3 mb-6">
								<div
									class="flex items-center text-gray-600 dark:text-gray-400"
								>
									<BedDouble class="w-5 h-5 mr-2" />
									<span
										>{room.double_beds} Double, {room.single_beds}
										Single beds</span
									>
								</div>
								<div
									class="flex items-center text-gray-600 dark:text-gray-400"
								>
									<Users class="w-5 h-5 mr-2" />
									<span
										>Sleeps {room.double_beds * 2 +
											room.single_beds}</span
									>
								</div>
							</div>

							<!-- Book Button -->
							<button
								class="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors flex items-center justify-center gap-2"
								on:click={() => handleBookRoom(room)}
							>
								<CreditCard class="w-5 h-5" />
								Book Now
							</button>
						</div>
					</div>
				{/each}
			</div>
		{/if}
	</div>
</DashboardLayout>
