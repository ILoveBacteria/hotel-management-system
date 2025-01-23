<!-- src/routes/admin/images/+page.svelte -->
<script lang="ts">
	import { onMount } from 'svelte';
	import type { UserProfile, RoomImage, RoomType } from '$lib/types';
	import { goto } from '$app/navigation';
	import { PUBLIC_BASE_URL } from '$env/static/public';
	import AdminLayout from '$lib/components/admin/AdminLayout.svelte';
	import {
		Loader2,
		Plus,
		Pencil,
		Trash2,
		AlertTriangle,
		Image as ImageIcon,
	} from 'lucide-svelte';

	let user: UserProfile | null = null;
	let roomImages: RoomImage[] = [];
	let roomTypes: RoomType[] = [];
	let isLoading = true;
	let error: string | null = null;
	let showImageModal = false;
	let selectedImage: RoomImage | null = null;
	let showDeleteModal = false;
	let isSubmitting = false;
	let isDeleting = false;

	// Form data
	let formData = {
		caption: '',
		image: null as File | null,
		room_type: '',
		is_primary: false,
	};

	let imagePreview: string | null = null;

	async function loadInitialData() {
		try {
			const [profileResponse, imagesResponse, roomTypesResponse] =
				await Promise.all([
					fetch(`${PUBLIC_BASE_URL}/users/profile/`, {
						credentials: 'include',
					}),
					fetch(`${PUBLIC_BASE_URL}/rooms/images/`, {
						credentials: 'include',
					}),
					fetch(`${PUBLIC_BASE_URL}/rooms/types/`, {
						credentials: 'include',
					}),
				]);

			if (!profileResponse.ok) {
				goto('/admin/login');
				return;
			}

			user = await profileResponse.json();

			if (!user?.is_superuser) {
				goto('/admin/login');
				return;
			}

			if (imagesResponse.ok && roomTypesResponse.ok) {
				const imagesData = await imagesResponse.json();
				const roomTypesData = await roomTypesResponse.json();

				roomImages = imagesData.results;
				roomTypes = roomTypesData.results;
			} else {
				throw new Error('Failed to fetch data');
			}
		} catch (err) {
			console.error('Failed to load data:', err);
			error = 'Failed to load images data';
		} finally {
			isLoading = false;
		}
	}

	function handleImageChange(event: Event) {
		const input = event.target as HTMLInputElement;
		if (!input.files?.length) return;

		const file = input.files[0];
		if (!file.type.startsWith('image/')) {
			error = 'Please select an image file';
			return;
		}

		if (file.size > 5 * 1024 * 1024) {
			// 5MB limit
			error = 'Image size should be less than 5MB';
			return;
		}

		formData.image = file;
		imagePreview = URL.createObjectURL(file);
	}

	async function handleSubmit() {
		if (!formData.room_type || (!formData.image && !selectedImage)) {
			error = 'Please fill in all required fields';
			return;
		}

		isSubmitting = true;
		error = null;

		try {
			const formDataToSend = new FormData();
			formDataToSend.append('caption', formData.caption);
			formDataToSend.append('is_primary', formData.is_primary.toString());

			if (formData.image) {
				formDataToSend.append('image', formData.image);
			}

			const url = selectedImage
				? `${PUBLIC_BASE_URL}/rooms/images/${selectedImage.id}/` // Fixed update route
				: `${PUBLIC_BASE_URL}/rooms/types/${formData.room_type}/images/`;

			const method = selectedImage ? 'PATCH' : 'POST';

			const response = await fetch(url, {
				method,
				credentials: 'include',
				body: formDataToSend,
			});

			if (!response.ok) {
				throw new Error('Failed to save image');
			}

			await loadInitialData();
			resetForm();
		} catch (err) {
			console.error('Failed to save image:', err);
			error = 'Failed to save image';
		} finally {
			isSubmitting = false;
		}
	}

	async function handleDelete() {
		if (!selectedImage) return;

		isDeleting = true;
		error = null;

		try {
			const response = await fetch(
				`${PUBLIC_BASE_URL}/rooms/images/${selectedImage.id}/`,
				{
					method: 'DELETE',
					credentials: 'include',
				},
			);

			if (!response.ok) {
				throw new Error('Failed to delete image');
			}

			await loadInitialData();
			showDeleteModal = false;
			selectedImage = null;
		} catch (err) {
			console.error('Failed to delete image:', err);
			error = 'Failed to delete image';
		} finally {
			isDeleting = false;
		}
	}

	function editImage(image: RoomImage) {
		selectedImage = image;
		formData = {
			caption: image.caption,
			image: null,
			room_type: roomTypes
				.find((rt) => rt.id === image.room_type)
				?.id.toString()!,
			is_primary: image.is_primary,
		};
		imagePreview = image.image;
		showImageModal = true;
	}

	function resetForm() {
		formData = {
			caption: '',
			image: null,
			room_type: '',
			is_primary: false,
		};
		imagePreview = null;
		selectedImage = null;
		showImageModal = false;
	}

	onMount(loadInitialData);
</script>

<svelte:head>
	<title>Room Images Management - Admin Panel</title>
</svelte:head>

{#if user}
	<div class="space-y-6">
		<!-- Header -->
		<div class="flex justify-between items-center">
			<h1 class="text-2xl font-semibold text-gray-900 dark:text-white">
				Room Images
			</h1>
			<button
				class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
				on:click={() => {
					resetForm();
					showImageModal = true;
				}}
			>
				<Plus class="w-5 h-5" />
				Add Image
			</button>
		</div>

		{#if error}
			<div
				class="bg-red-50 dark:bg-red-900/50 text-red-600 dark:text-red-200 p-4 rounded-lg flex items-center"
			>
				<AlertTriangle class="w-5 h-5 mr-2" />
				{error}
			</div>
		{/if}

		<!-- Image Modal -->
		{#if showImageModal}
			<div
				class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4"
			>
				<div
					class="bg-white dark:bg-gray-800 rounded-xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-hidden"
				>
					<!-- Modal Header -->
					<div
						class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between"
					>
						<h2
							class="text-xl font-semibold text-gray-900 dark:text-white"
						>
							{selectedImage ? 'Edit' : 'Add'} Room Image
						</h2>
						<button
							class="text-gray-400 hover:text-gray-500 dark:hover:text-gray-300"
							on:click={resetForm}
						>
							<svg
								class="w-6 h-6"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M6 18L18 6M6 6l12 12"
								/>
							</svg>
						</button>
					</div>

					<!-- Modal Body -->
					<form
						on:submit|preventDefault={handleSubmit}
						class="p-6 space-y-6"
					>
						<!-- Room Type Selection -->
						<div>
							<label
								class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
							>
								Room Type *
							</label>
							<select
								bind:value={formData.room_type}
								required
								class="w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
							>
								<option value="">Select Room Type</option>
								{#each roomTypes as roomType}
									<option value={roomType.id}
										>{roomType.name}</option
									>
								{/each}
							</select>
						</div>

						<!-- Image Upload -->
						<div>
							<label
								class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
							>
								Image {selectedImage
									? '(Leave empty to keep current)'
									: '*'}
							</label>
							<div
								class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 dark:border-gray-600 border-dashed rounded-lg"
							>
								<div class="space-y-1 text-center">
									{#if imagePreview}
										<img
											src={imagePreview}
											alt="Preview"
											class="mx-auto h-32 w-auto object-cover mb-4"
										/>
									{:else}
										<ImageIcon
											class="mx-auto h-12 w-12 text-gray-400"
										/>
									{/if}
									<div
										class="flex text-sm text-gray-600 dark:text-gray-400"
									>
										<label
											class="relative cursor-pointer bg-white dark:bg-gray-700 rounded-md font-medium text-blue-600 hover:text-blue-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-blue-500"
										>
											<span>Upload a file</span>
											<input
												type="file"
												accept="image/jpeg,image/png"
												class="sr-only"
												on:change={handleImageChange}
											/>
										</label>
										<p class="pl-1">or drag and drop</p>
									</div>
									<p
										class="text-xs text-gray-500 dark:text-gray-400"
									>
										PNG, JPG up to 5MB
									</p>
								</div>
							</div>
						</div>

						<!-- Caption -->
						<div>
							<label
								class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
							>
								Caption
							</label>
							<input
								type="text"
								bind:value={formData.caption}
								class="w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
								placeholder="Enter image caption"
							/>
						</div>

						<!-- Is Primary Toggle -->
						<div class="flex items-center">
							<input
								type="checkbox"
								bind:checked={formData.is_primary}
								class="rounded text-blue-600 focus:ring-blue-500 dark:bg-gray-700"
							/>
							<label
								class="ml-2 text-sm text-gray-700 dark:text-gray-300"
							>
								Set as primary image
							</label>
						</div>

						<!-- Submit Button -->
						<div class="flex justify-end gap-3">
							<button
								type="button"
								class="px-4 py-2 text-gray-700 dark:text-gray-200 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 rounded-lg transition-colors"
								on:click={resetForm}
								disabled={isSubmitting}
							>
								Cancel
							</button>
							<button
								type="submit"
								class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2 disabled:opacity-50"
								disabled={isSubmitting}
							>
								{#if isSubmitting}
									<Loader2 class="w-4 h-4 animate-spin" />
									Saving...
								{:else}
									Save Image
								{/if}
							</button>
						</div>
					</form>
				</div>
			</div>
		{/if}

		<!-- Images Grid -->
		{#if isLoading}
			<div class="flex items-center justify-center h-64">
				<Loader2 class="w-8 h-8 animate-spin text-blue-600" />
			</div>
		{:else}
			<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
				{#each roomImages as image}
					<div
						class="bg-white dark:bg-gray-800 rounded-lg shadow-sm overflow-hidden"
					>
						<img
							src={image.image}
							alt={image.caption}
							class="w-full h-48 object-cover"
						/>
						<div class="p-4">
							<div class="flex items-center justify-between mb-2">
								<h3
									class="font-medium text-gray-900 dark:text-white"
								>
									{image.caption || 'No caption'}
								</h3>
								{#if image.is_primary}
									<span
										class="px-2 py-1 text-xs font-medium text-blue-600 bg-blue-100 dark:bg-blue-900/20 rounded-full"
									>
										Primary
									</span>
								{/if}
							</div>
							<div class="flex justify-end gap-2">
								<button
									class="text-blue-600 hover:text-blue-900 dark:hover:text-blue-400"
									on:click={() => editImage(image)}
								>
									<Pencil class="w-5 h-5" />
								</button>
								<button
									class="text-red-600 hover:text-red-900 dark:hover:text-red-400"
									on:click={() => {
										selectedImage = image;
										showDeleteModal = true;
									}}
								>
									<Trash2 class="w-5 h-5" />
								</button>
							</div>
						</div>
					</div>
				{/each}
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
						Delete Image
					</h3>
					<p class="text-gray-500 dark:text-gray-400 mb-4">
						Are you sure you want to delete this image? This action
						cannot be undone.
					</p>
					<div class="flex justify-end gap-3">
						<button
							class="px-4 py-2 text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
							on:click={() => {
								showDeleteModal = false;
								selectedImage = null;
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
