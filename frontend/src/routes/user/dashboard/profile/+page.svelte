<!-- src/routes/dashboard/profile/+page.svelte -->
<script lang="ts">
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import { PUBLIC_BASE_URL } from "$env/static/public";
    import type { UserProfile } from "$lib/types";
    import DashboardLayout from "$lib/components/layout/DashboardLayout.svelte";
    import { User, Phone, Mail, MapPin, Camera, CheckCircle } from "lucide-svelte";
  import { CookieParser } from "$lib/helpers/cookie-parser";

    let userProfile: UserProfile | null = null;
    let isEditing = false;
    let isLoading = true;
    let isSaving = false;
    let error: string | null = null;
    let success = false;
    let avatarFile: File | null = null;
    let avatarPreview: string | null = null;

    // Form data
    let formData = {
        first_name: "",
        last_name: "",
        guest_profile: {
            phone_number: "",
            national_id: "",
            address: "",
            avatar: null as string | null
        }
    };

    async function loadProfile() {
        try {
            const response = await fetch(`${PUBLIC_BASE_URL}/users/profile/`, {
                credentials: "include"
            });

            if (!response.ok) {
                if (response.status === 401) {
                    goto("/");
                    return;
                }
                throw new Error("Failed to load profile");
            }

            userProfile = await response.json();

            console.log(userProfile);
            
            // Initialize form data with current profile
            formData = {
                first_name: userProfile?.first_name || "",
                last_name: userProfile?.last_name || "",
                guest_profile: {
                    phone_number: userProfile?.guest_profile.phone_number || "",
                    national_id: userProfile?.guest_profile.national_id || "",
                    address: userProfile?.guest_profile.address || "",
                    avatar: userProfile?.guest_profile.avatar || null
                }
            };
            
        } catch (err) {
            console.error("Failed to load profile:", err);
            error = "Failed to load profile data";
        } finally {
            isLoading = false;
        }
    }

    async function handleSubmit() {
        if (!userProfile) return;
        
        isSaving = true;
        error = null;
        success = false;

        try {
            const formDataUpload = new FormData();
            if (avatarFile) {
                formDataUpload.append('guest_profile.avatar', avatarFile);
            }
            formDataUpload.append('first_name', formData.first_name);
            formDataUpload.append('last_name', formData.last_name);
            formDataUpload.append('guest_profile.phone_number', formData.guest_profile.phone_number);
            formDataUpload.append('guest_profile.national_id', formData.guest_profile.national_id);
            formDataUpload.append('guest_profile.address', formData.guest_profile.address);

            const response = await fetch(`${PUBLIC_BASE_URL}/users/profile/${userProfile.id}/`, {
                method: 'PATCH',
                credentials: 'include',
                body: formDataUpload
            });

            if (!response.ok) {
                throw new Error("Failed to update profile");
            }

            const updatedProfile = await response.json();
            userProfile = updatedProfile;
            success = true;
            isEditing = false;

            // Reset file input
            avatarFile = null;
            avatarPreview = null;
        } catch (err) {
            console.error("Failed to update profile:", err);
            error = "Failed to update profile. Please try again.";
        } finally {
            isSaving = false;
        }
    }

    function handleAvatarChange(event: Event) {
        const input = event.target as HTMLInputElement;
        if (!input.files?.length) return;

        const file = input.files[0];
        if (!file.type.startsWith('image/')) {
            error = "Please select an image file";
            return;
        }

        if (file.size > 5 * 1024 * 1024) { // 5MB limit
            error = "Image size should be less than 5MB";
            return;
        }

        avatarFile = file;
        // Create preview URL
        avatarPreview = URL.createObjectURL(file);
    }

    function getInitials(firstName: string, lastName: string): string {
        return `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase();
    }

    onMount(() => {
        loadProfile();
        const cookies = CookieParser.getCookies();
        console.log(document.cookie);
        
        console.log(cookies)
    });
</script>

<DashboardLayout username={userProfile?.username || 'Guest'}>
    {#if userProfile}
        <div class="max-w-4xl mx-auto space-y-6">
            <!-- Profile Header -->
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
                <div class="flex items-center justify-between">
                    <div class="flex items-center space-x-4">
                        <div class="relative">
                            {#if userProfile.guest_profile.avatar || avatarPreview}
                                <img
                                    src={avatarPreview || userProfile.guest_profile.avatar || ''}
                                    alt={userProfile.first_name}
                                    class="w-20 h-20 rounded-full object-cover"
                                />
                            {:else}
                                <div class="w-20 h-20 rounded-full bg-blue-600 flex items-center justify-center text-white text-2xl font-semibold">
                                    {getInitials(userProfile.first_name, userProfile.last_name)}
                                </div>
                            {/if}
                            {#if isEditing}
                                <label class="absolute bottom-0 right-0 w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center cursor-pointer hover:bg-blue-700 transition-colors">
                                    <Camera class="w-4 h-4 text-white" />
                                    <input
                                        type="file"
                                        accept="image/*"
                                        class="hidden"
                                        on:change={handleAvatarChange}
                                    />
                                </label>
                            {/if}
                        </div>
                        <div>
                            <h1 class="text-2xl font-semibold text-gray-900 dark:text-white">
                                {userProfile.first_name} {userProfile.last_name}
                            </h1>
                            <p class="text-gray-500 dark:text-gray-400">
                                {userProfile.email}
                            </p>
                        </div>
                </div>
                <button
                    class="px-4 py-2 text-sm font-medium text-blue-600 hover:text-blue-700"
                    on:click={() => isEditing = !isEditing}
                >
                    {isEditing ? 'Cancel' : 'Edit Profile'}
                </button>
            </div>
        </div>

        {#if error}
            <div class="bg-red-50 dark:bg-red-900/50 text-red-600 dark:text-red-200 p-4 rounded-lg">
                {error}
            </div>
        {/if}

        {#if success}
            <div class="bg-green-50 dark:bg-green-900/50 text-green-600 dark:text-green-200 p-4 rounded-lg flex items-center">
                <CheckCircle class="w-5 h-5 mr-2" />
                Profile updated successfully!
            </div>
        {/if}

        <!-- Profile Form -->
        <form on:submit|preventDefault={handleSubmit} class="space-y-6">
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm divide-y divide-gray-200 dark:divide-gray-700">
                <!-- Personal Information -->
                <div class="p-6">
                    <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4 flex items-center">
                        <User class="w-5 h-5 mr-2" />
                        Personal Information
                    </h2>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                First Name
                            </label>
                            <input
                                type="text"
                                bind:value={formData.first_name}
                                disabled={!isEditing}
                                class="w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white disabled:opacity-60"
                            />
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                Last Name
                            </label>
                            <input
                                type="text"
                                bind:value={formData.last_name}
                                disabled={!isEditing}
                                class="w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white disabled:opacity-60"
                            />
                        </div>
                    </div>
                </div>

                <!-- Contact Information -->
                <div class="p-6">
                    <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4 flex items-center">
                        <Phone class="w-5 h-5 mr-2" />
                        Contact Information
                    </h2>
                    <div class="grid grid-cols-1 gap-6">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                Phone Number
                            </label>
                            <input
                                type="tel"
                                bind:value={formData.guest_profile.phone_number}
                                disabled={!isEditing}
                                placeholder="+989123456789"
                                class="w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white disabled:opacity-60"
                            />
                            <p class="mt-1 text-sm text-gray-500">Format: +989123456789</p>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                Email
                            </label>
                            <input
                                type="email"
                                value={userProfile.email}
                                disabled
                                class="w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white opacity-60"
                            />
                        </div>
                    </div>
                </div>

                <!-- Additional Information -->
                <div class="p-6">
                    <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4 flex items-center">
                        <MapPin class="w-5 h-5 mr-2" />
                        Additional Information
                    </h2>
                    <div class="grid grid-cols-1 gap-6">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                National ID
                            </label>
                            <input
                                type="text"
                                bind:value={formData.guest_profile.national_id}
                                disabled={!isEditing}
                                placeholder="1234567890"
                                class="w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white disabled:opacity-60"
                            />
                            <p class="mt-1 text-sm text-gray-500">10 digits required</p>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                Address
                            </label>
                            <textarea
                                bind:value={formData.guest_profile.address}
                                disabled={!isEditing}
                                rows="3"
                                class="w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white disabled:opacity-60"
                            ></textarea>
                        </div>
                    </div>
                </div>
            </div>

            {#if isEditing}
                <div class="flex justify-end">
                    <button
                        type="submit"
                        class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 
                               transition-colors flex items-center disabled:opacity-50"
                        disabled={isSaving}
                    >
                        {#if isSaving}
                            <svg class="animate-spin h-5 w-5 mr-2" viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"/>
                                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
                            </svg>
                            Saving...
                        {:else}
                            Save Changes
                        {/if}
                    </button>
                </div>
            {/if}
        </form>
    </div>
    {:else}
        <div class="flex items-center justify-center h-64">
            <svg class="animate-spin h-8 w-8 text-blue-600" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
            </svg>
        </div>
    {/if}
</DashboardLayout>