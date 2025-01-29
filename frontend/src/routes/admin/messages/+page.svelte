<!-- src/routes/admin/rooms/+page.svelte -->
<script lang="ts">
	import { onMount } from 'svelte';
	import type { UserProfile, Room, RoomType } from '$lib/types';
	import { goto } from '$app/navigation';
	import { PUBLIC_BASE_URL } from '$env/static/public';
	import AdminLayout from '$lib/components/admin/AdminLayout.svelte';
	import {
		Loader2,
		Plus,
		Pencil,
		Trash2,
		AlertTriangle,
		BedDouble,
		CheckCircle,
	} from 'lucide-svelte';

	let user: UserProfile | null = null;
	let rooms: Room[] = [];
	let roomTypes: RoomType[] = [];
	let isLoading = true;
	let error: string | null = null;

	// Modal states
	let showDeleteModal = false;
	let showRoomModal = false;
	let selectedRoom: Room | null = null;
	let isDeleting = false;
	let isSubmitting = false;

	// Form data
	let formData = {
		room_number: 0,
		room_type: '',
		is_active: true,
		status: 'available' as 'available' | 'occupied' | 'maintenance',
		last_maintained: null as string | null,
	};

	// Check admin and fetch initial data
	async function loadInitialData() {
		try {
			// Check admin authentication
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

			// Ensure user is a superuser
			if (!userProfile.is_superuser) {
				goto('/admin/login');
				return;
			}

			user = userProfile;

			// Fetch rooms and room types
			const [roomsResponse, roomTypesResponse] = await Promise.all([
				fetch(`${PUBLIC_BASE_URL}/messages/`, {
					credentials: 'include',
				}),
				fetch(`${PUBLIC_BASE_URL}/rooms/types/`, {
					credentials: 'include',
				}),
			]);

			if (!roomsResponse.ok || !roomTypesResponse.ok) {
				throw new Error('Failed to fetch room data');
			}

			const roomsData = await roomsResponse.json();
			const roomTypesData = await roomTypesResponse.json();

			rooms = roomsData.results;
			roomTypes = roomTypesData.results;
		} catch (err) {
			console.error('Failed to load room data:', err);
			error = 'Failed to load room data';
		} finally {
			isLoading = false;
		}
	}

	// Handle room creation/update
	async function handleSubmit() {
		isSubmitting = true;
		error = null;

		try {
			const url = selectedRoom
				? `${PUBLIC_BASE_URL}/rooms/inventories/${selectedRoom.room_number}/`
				: `${PUBLIC_BASE_URL}/rooms/types/${formData.room_type}/inventories/`;

			const method = selectedRoom ? 'PUT' : 'POST';
			const body = selectedRoom
				? { ...formData }
				: {
						room_number: formData.room_number,
						is_active: formData.is_active,
						status: formData.status,
					};

			const response = await fetch(url, {
				method,
				credentials: 'include',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify(body),
			});

			if (!response.ok) {
				throw new Error('Failed to save room');
			}

			// Reload rooms
			await loadInitialData();

			// Reset form and close modal
			resetForm();
		} catch (err) {
			console.error('Failed to save room:', err);
			error = 'Failed to save room';
		} finally {
			isSubmitting = false;
		}
	}

	// Delete room
	async function handleDelete() {
		if (!selectedRoom) return;

		isDeleting = true;
		error = null;

		try {
			const response = await fetch(
				`${PUBLIC_BASE_URL}/rooms/inventories/${selectedRoom.room_number}/`,
				{
					method: 'DELETE',
					credentials: 'include',
				},
			);

			if (!response.ok) {
				throw new Error('Failed to delete room');
			}

			// Reload rooms
			await loadInitialData();

			// Reset modals
			showDeleteModal = false;
			selectedRoom = null;
		} catch (err) {
			console.error('Failed to delete room:', err);
			error = 'Failed to delete room';
		} finally {
			isDeleting = false;
		}
	}

	// Reset form to initial state
	function resetForm() {
		formData = {
			room_number: 0,
			room_type: '',
			is_active: true,
			status: 'available',
			last_maintained: null,
		};
		selectedRoom = null;
		showRoomModal = false;
	}

	// Edit room
	function editRoom(room: Room) {
		selectedRoom = room;
		formData = {
			room_number: room.room_number,
			room_type: room.room_type.toString(),
			is_active: room.is_active,
			status: room.status,
			last_maintained: room.last_maintained,
		};
		showRoomModal = true;
	}

	// Lifecycle
	onMount(loadInitialData);
</script>

{#if user}
	<div class="space-y-6">
		<!-- Header -->
		<div class="flex justify-between items-center">
			<h1 class="text-2xl font-semibold text-gray-900 dark:text-white">
				Messages
			</h1>
		</div>

		{#if error}
			<div
				class="bg-red-50 dark:bg-red-900/50 text-red-600 dark:text-red-200 p-4 rounded-lg flex items-center"
			>
				<AlertTriangle class="w-5 h-5 mr-2" />
				{error}
			</div>
		{/if}

		

		<!-- Rooms List -->
		{#if isLoading}
			<div class="flex items-center justify-center h-64">
				<Loader2 class="w-8 h-8 animate-spin text-blue-600" />
			</div>
		{:else}
			<div
				class="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden"
			>
				<table
					class="min-w-full divide-y divide-gray-200 dark:divide-gray-700"
				>
					<thead class="bg-gray-50 dark:bg-gray-700">
						<tr>
							<th
								class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
							>
								ID
							</th>
							<th
								class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
							>
								Name
							</th>
							<th
								class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
							>
								Email
							</th>
							<th
								class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
							>
								Text
							</th>
						</tr>
					</thead>
					<tbody
						class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700"
					>
						{#each rooms as room}
							<tr>
								<td
									class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white"
								>
									{room.id}
								</td>
								<td
									class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400"
								>
									{room.name}
								</td>
								<td
									class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400"
								>
									{room.email}
								</td>
								<td
									class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400"
								>
									{room.message}
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		{/if}

		<!-- Delete Modal -->
		{#if showDeleteModal}
			<div
				class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
			>
				<div
					class="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md w-full mx-4"
				>
					<h3
						class="text-lg font-medium text-gray-900 dark:text-white mb-4"
					>
						Delete Room
					</h3>
					<p class="text-gray-500 dark:text-gray-400 mb-4">
						Are you sure you want to delete Room {selectedRoom?.room_number}?
						This action cannot be undone.
					</p>
					<div class="flex justify-end gap-3">
						<button
							class="px-4 py-2 text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
							on:click={() => {
								showDeleteModal = false;
								selectedRoom = null;
							}}
							disabled={isDeleting}
						>
							Cancel
						</button>
						<button
							class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center gap-2 disabled:opacity-50"
							on:click={handleDelete}
							disabled={isDeleting}
						>
							{#if isDeleting}
								<Loader2 class="w-4 h-4 animate-spin" />
								Deleting...
							{:else}
								Delete
							{/if}
						</button>
					</div>
				</div>
			</div>
		{/if}
	</div>
{/if}
