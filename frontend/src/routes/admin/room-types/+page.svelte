<!-- src/routes/admin/room-types/+page.svelte -->
<script lang="ts">
  import { onMount } from "svelte";
  import type { UserProfile, RoomType } from "$lib/types";
  import { goto } from "$app/navigation";
  import { PUBLIC_BASE_URL } from "$env/static/public";
  import AdminLayout from "$lib/components/admin/AdminLayout.svelte";
  import { Loader2, Plus, Pencil, Trash2, AlertTriangle } from "lucide-svelte";

  let user: UserProfile | null = null;
  let roomTypes: RoomType[] = [];
  let isLoading = true;
  let error: string | null = null;
  let showDeleteModal = false;
  let selectedRoomType: RoomType | null = null;
  let isDeleting = false;

  // Form state
  let showForm = false;
  let formData = {
    name: "",
    price: 0,
    double_beds: 0,
    single_beds: 0,
    description: "",
  };
  let isSubmitting = false;
  let editingId: number | null = null;

  async function checkAdmin() {
    try {
      const response = await fetch(`${PUBLIC_BASE_URL}/users/profile/`, {
        credentials: "include",
      });

      if (!response.ok) throw new Error("Not authenticated");

      const userProfile: UserProfile = await response.json();
      if (!userProfile.is_superuser) throw new Error("Not authorized");

      user = userProfile;
    } catch (err) {
      goto("/admin/login");
    }
  }

  async function fetchRoomTypes() {
    try {
      const response = await fetch(`${PUBLIC_BASE_URL}/rooms/types/`, {
        credentials: "include",
      });

      if (!response.ok) throw new Error("Failed to fetch room types");

      const data = await response.json();
      roomTypes = data.results;
    } catch (err) {
      console.error("Failed to fetch room types:", err);
      error = "Failed to load room types";
    } finally {
      isLoading = false;
    }
  }

  async function handleSubmit() {
    isSubmitting = true;
    error = null;

    try {
      const url = editingId
        ? `${PUBLIC_BASE_URL}/rooms/types/${editingId}/`
        : `${PUBLIC_BASE_URL}/rooms/types/`;

      const response = await fetch(url, {
        method: editingId ? "PUT" : "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) throw new Error("Failed to save room type");

      await fetchRoomTypes();
      resetForm();
    } catch (err) {
      console.error("Failed to save room type:", err);
      error = "Failed to save room type";
    } finally {
      isSubmitting = false;
    }
  }

  async function handleDelete() {
    if (!selectedRoomType) return;

    isDeleting = true;
    error = null;

    try {
      const response = await fetch(
        `${PUBLIC_BASE_URL}/rooms/types/${selectedRoomType.id}/`,
        {
          method: "DELETE",
          credentials: "include",
        }
      );

      if (!response.ok) throw new Error("Failed to delete room type");

      await fetchRoomTypes();
      showDeleteModal = false;
      selectedRoomType = null;
    } catch (err) {
      console.error("Failed to delete room type:", err);
      error = "Failed to delete room type";
    } finally {
      isDeleting = false;
    }
  }

  function editRoomType(roomType: RoomType) {
    formData = {
      name: roomType.name,
      price: roomType.price,
      double_beds: roomType.double_beds,
      single_beds: roomType.single_beds,
      description: roomType.description,
    };
    editingId = roomType.id;
    showForm = true;
  }

  function resetForm() {
    formData = {
      name: "",
      price: 0,
      double_beds: 0,
      single_beds: 0,
      description: "",
    };
    editingId = null;
    showForm = false;
  }

  onMount(async () => {
    await checkAdmin();
    await fetchRoomTypes();
  });
</script>

{#if user}
  <AdminLayout {user}>
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex justify-between items-center">
        <h1 class="text-2xl font-semibold text-gray-900 dark:text-white">
          Room Types
        </h1>
        <button
          class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          on:click={() => {
            resetForm();
            showForm = true;
          }}
        >
          <Plus class="w-5 h-5" />
          Add Room Type
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

      <!-- Add/Edit Room Type Modal -->
      {#if showForm}
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
              <h2 class="text-xl font-semibold text-gray-900 dark:text-white">
                {editingId ? "Edit" : "Add"} Room Type
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
            <div class="px-6 py-4 overflow-y-auto max-h-[calc(90vh-130px)]">
              <form on:submit|preventDefault={handleSubmit} class="space-y-6">
                <!-- Name Field -->
                <div>
                  <label
                    class="text-sm font-medium text-gray-700 dark:text-gray-300"
                  >
                    Room Type Name
                  </label>
                  <input
                    type="text"
                    bind:value={formData.name}
                    required
                    placeholder="e.g., Deluxe Suite"
                    class="mt-1 block w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  />
                </div>

                <!-- Price Field with Currency Symbol -->
                <div>
                  <label
                    class="text-sm font-medium text-gray-700 dark:text-gray-300"
                  >
                    Price per Night (₹)
                  </label>
                  <div class="mt-1 relative rounded-lg shadow-sm">
                    <div
                      class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
                    >
                      <span class="text-gray-500 dark:text-gray-400">₹</span>
                    </div>
                    <input
                      type="number"
                      bind:value={formData.price}
                      required
                      min="0"
                      placeholder="0.00"
                      class="pl-8 block w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    />
                  </div>
                </div>

                <!-- Bed Configuration -->
                <div class="space-y-4">
                  <label
                    class="text-sm font-medium text-gray-700 dark:text-gray-300"
                  >
                    Bed Configuration
                  </label>
                  <div class="grid grid-cols-2 gap-4">
                    <div class="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                      <label
                        class="text-sm text-gray-600 dark:text-gray-300 block mb-2"
                      >
                        Double Beds
                      </label>
                      <input
                        type="number"
                        bind:value={formData.double_beds}
                        required
                        min="0"
                        class="block w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-blue-500 focus:ring-blue-500"
                      />
                    </div>
                    <div class="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                      <label
                        class="text-sm text-gray-600 dark:text-gray-300 block mb-2"
                      >
                        Single Beds
                      </label>
                      <input
                        type="number"
                        bind:value={formData.single_beds}
                        required
                        min="0"
                        class="block w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-blue-500 focus:ring-blue-500"
                      />
                    </div>
                  </div>
                </div>

                <!-- Description Field -->
                <div>
                  <label
                    class="text-sm font-medium text-gray-700 dark:text-gray-300"
                  >
                    Description
                  </label>
                  <textarea
                    bind:value={formData.description}
                    required
                    rows="4"
                    placeholder="Describe the room type, amenities, and special features..."
                    class="mt-1 block w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  ></textarea>
                </div>
              </form>
            </div>

            <!-- Modal Footer -->
            <div
              class="px-6 py-4 border-t border-gray-200 dark:border-gray-700 flex justify-end gap-3"
            >
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
                on:click={handleSubmit}
                class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2 disabled:opacity-50"
                disabled={isSubmitting}
              >
                {#if isSubmitting}
                  <Loader2 class="w-4 h-4 animate-spin" />
                  Saving...
                {:else}
                  Save Room Type
                {/if}
              </button>
            </div>
          </div>
        </div>
      {/if}

      <!-- Room Types List -->
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
                  Name
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
                >
                  Price
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
                >
                  Beds
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
                >
                  Description
                </th>
                <th
                  class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
                >
                  Actions
                </th>
              </tr>
            </thead>
            <tbody
              class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700"
            >
              {#each roomTypes as roomType}
                <tr>
                  <td
                    class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white"
                  >
                    {roomType.name}
                  </td>
                  <td
                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400"
                  >
                    ₹{roomType.price}
                  </td>
                  <td
                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400"
                  >
                    {roomType.double_beds} Double, {roomType.single_beds} Single
                  </td>
                  <td
                    class="px-6 py-4 text-sm text-gray-500 dark:text-gray-400"
                  >
                    {roomType.description}
                  </td>
                  <td
                    class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium"
                  >
                    <div class="flex justify-end gap-2">
                      <button
                        class="text-blue-600 hover:text-blue-900 dark:hover:text-blue-400"
                        on:click={() => editRoomType(roomType)}
                      >
                        <Pencil class="w-5 h-5" />
                      </button>
                      <button
                        class="text-red-600 hover:text-red-900 dark:hover:text-red-400"
                        on:click={() => {
                          selectedRoomType = roomType;
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

      <!-- Delete Modal -->
      {#if showDeleteModal}
        <div
          class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
        >
          <div
            class="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md w-full mx-4"
          >
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">
              Delete Room Type
            </h3>
            <p class="text-gray-500 dark:text-gray-400 mb-4">
              Are you sure you want to delete {selectedRoomType?.name}? This
              action cannot be undone.
            </p>
            <div class="flex justify-end gap-3">
              <button
                class="px-4 py-2 text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
                on:click={() => {
                  showDeleteModal = false;
                  selectedRoomType = null;
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
  </AdminLayout>
{/if}
