<script lang="ts">
    import { onMount } from 'svelte';
    import type { UserProfile } from '$lib/types';
    import { goto } from '$app/navigation';
    import { PUBLIC_BASE_URL } from '$env/static/public';
    import {
        Users,
        Search,
        AlertTriangle,
        Loader2,
        Pencil,
        X,
        Mail,
        Phone,
        User,
        MapPin,
    } from 'lucide-svelte';

    let users: UserProfile[] = [];
    let isLoading = true;
    let error: string | null = null;
    let searchQuery = '';
    let showEditModal = false;
    let selectedUser: UserProfile | null = null;
    let isSubmitting = false;

    // Form data
    let formData = {
        first_name: '',
        last_name: '',
        guest_profile: {
            phone_number: '',
            national_id: '',
            address: '',
        }
    };

    $: filteredUsers = users.filter(user => 
        user.first_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        user.last_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        user.email.toLowerCase().includes(searchQuery.toLowerCase()) ||
        user.username.toLowerCase().includes(searchQuery.toLowerCase())
    );

    async function loadUsers() {
        try {
            const [profileResponse, usersResponse] = await Promise.all([
                fetch(`${PUBLIC_BASE_URL}/users/profile/`, {
                    credentials: 'include'
                }),
                fetch(`${PUBLIC_BASE_URL}/users/`, {
                    credentials: 'include'
                })
            ]);

            if (!profileResponse.ok) {
                if (profileResponse.status === 401) {
                    goto('/admin/login');
                    return;
                }
                throw new Error('Not authorized');
            }

            const profile = await profileResponse.json();
            if (!profile.is_superuser) {
                goto('/admin/login');
                return;
            }

            if (usersResponse.ok) {
                const data = await usersResponse.json();
                users = data.results;
            } else {
                throw new Error('Failed to fetch users');
            }
        } catch (err) {
            console.error('Failed to load users:', err);
            error = 'Failed to load user data';
        } finally {
            isLoading = false;
        }
    }

    function editUser(user: UserProfile) {
        selectedUser = user;
        formData = {
            first_name: user.first_name,
            last_name: user.last_name,
            guest_profile: {
                phone_number: user.guest_profile?.phone_number || '',
                national_id: user.guest_profile?.national_id || '',
                address: user.guest_profile?.address || '',
            }
        };
        showEditModal = true;
    }

    async function handleSubmit() {
        if (!selectedUser) return;

        isSubmitting = true;
        error = null;

        try {
            const response = await fetch(`${PUBLIC_BASE_URL}/users/profile/${selectedUser.id}/`, {
                method: 'PATCH',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                throw new Error('Failed to update user');
            }

            await loadUsers();
            showEditModal = false;
            selectedUser = null;
        } catch (err) {
            console.error('Failed to update user:', err);
            error = 'Failed to update user profile';
        } finally {
            isSubmitting = false;
        }
    }

    onMount(loadUsers);
</script>

<div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
        <h1 class="text-2xl font-semibold text-gray-900 dark:text-white flex items-center">
            <Users class="w-6 h-6 mr-2" />
            User Management
        </h1>
        <div class="flex items-center space-x-4">
            <div class="relative">
                <Search class="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                <input
                    type="text"
                    bind:value={searchQuery}
                    placeholder="Search users..."
                    class="pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                />
            </div>
        </div>
    </div>

    {#if error}
        <div class="bg-red-50 dark:bg-red-900/50 text-red-600 dark:text-red-200 p-4 rounded-lg flex items-center">
            <AlertTriangle class="w-5 h-5 mr-2" />
            {error}
        </div>
    {/if}

    <!-- Users Table -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm">
        {#if isLoading}
            <div class="flex items-center justify-center h-64">
                <Loader2 class="w-8 h-8 animate-spin text-blue-600" />
            </div>
        {:else if filteredUsers.length === 0}
            <div class="p-6 text-center text-gray-500 dark:text-gray-400">
                No users found
            </div>
        {:else}
            <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                    <thead class="bg-gray-50 dark:bg-gray-700">
                        <tr>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">User</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Contact</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Role</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Status</th>
                            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Actions</th>
                        </tr>
                    </thead>
                    <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                        {#each filteredUsers as user}
                            <tr>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <div class="flex items-center">
                                        <div class="flex-shrink-0 h-10 w-10">
                                            {#if user.guest_profile?.avatar}
                                                <img class="h-10 w-10 rounded-full" src={user.guest_profile.avatar} alt="" />
                                            {:else}
                                                <div class="h-10 w-10 rounded-full bg-blue-600 flex items-center justify-center text-white font-semibold">
                                                    {user.first_name[0]}{user.last_name[0]}
                                                </div>
                                            {/if}
                                        </div>
                                        <div class="ml-4">
                                            <div class="text-sm font-medium text-gray-900 dark:text-white">
                                                {user.first_name} {user.last_name}
                                            </div>
                                            <div class="text-sm text-gray-500 dark:text-gray-400">
                                                @{user.username}
                                            </div>
                                        </div>
                                    </div>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <div class="text-sm text-gray-900 dark:text-white">{user.email}</div>
                                    <div class="text-sm text-gray-500 dark:text-gray-400">
                                        {user.guest_profile?.phone_number || 'No phone'}
                                    </div>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full
                                        {user.is_superuser 
                                            ? 'bg-purple-100 text-purple-800 dark:bg-purple-900/20' 
                                            : user.is_staff
                                                ? 'bg-blue-100 text-blue-800 dark:bg-blue-900/20'
                                                : 'bg-green-100 text-green-800 dark:bg-green-900/20'}">
                                        {user.is_superuser ? 'Admin' : user.is_staff ? 'Staff' : 'Guest'}
                                    </span>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full
                                        {user.is_active
                                            ? 'bg-green-100 text-green-800 dark:bg-green-900/20'
                                            : 'bg-red-100 text-red-800 dark:bg-red-900/20'}">
                                        {user.is_active ? 'Active' : 'Inactive'}
                                    </span>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                    <button
                                        class="text-blue-600 hover:text-blue-900 dark:hover:text-blue-400"
                                        on:click={() => editUser(user)}
                                    >
                                        <Pencil class="w-5 h-5" />
                                    </button>
                                </td>
                            </tr>
                        {/each}
                    </tbody>
                </table>
            </div>
        {/if}
    </div>

    <!-- Edit User Modal -->
    {#if showEditModal && selectedUser}
        <div class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
            <div class="bg-white dark:bg-gray-800 rounded-xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-hidden">
                <!-- Modal Header -->
                <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
                    <h2 class="text-xl font-semibold text-gray-900 dark:text-white">
                        Edit User Profile
                    </h2>
                    <button
                        class="text-gray-400 hover:text-gray-500 dark:hover:text-gray-300"
                        on:click={() => {
                            showEditModal = false;
                            selectedUser = null;
                        }}
                    >
                        <X class="w-6 h-6" />
                    </button>
                </div>

                <!-- Modal Body -->
                <form on:submit|preventDefault={handleSubmit} class="p-6 space-y-6">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                First Name
                            </label>
                            <input
                                type="text"
                                bind:value={formData.first_name}
                                required
                                class="w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                            />
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                Last Name
                            </label>
                            <input
                                type="text"
                                bind:value={formData.last_name}
                                required
                                class="w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                            />
                        </div>
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                            Phone Number
                        </label>
                        <input
                            type="tel"
                            bind:value={formData.guest_profile.phone_number}
                            placeholder="+989123456789"
                            class="w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                        />
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                            National ID
                        </label>
                        <input
                            type="text"
                            bind:value={formData.guest_profile.national_id}
                            placeholder="1234567890"
                            class="w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                        />
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                            Address
                        </label>
                        <textarea
                            bind:value={formData.guest_profile.address}
                            rows="3"
                            class="w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                        ></textarea>
                    </div>

                    <div class="flex justify-end gap-3">
                        <button
                            type="button"
                            class="px-4 py-2 text-gray-700 dark:text-gray-200 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 rounded-lg transition-colors"
                            on:click={() => {
                                showEditModal = false;
                                selectedUser = null;
                            }}
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
                                Save Changes
                            {/if}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    {/if}
</div>