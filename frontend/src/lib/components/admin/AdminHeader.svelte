
<script lang="ts">
    import { goto } from "$app/navigation";
    import { Bell, Settings, Menu, LogOut } from "lucide-svelte";
    import type { UserProfile } from "$lib/types";
    import { PUBLIC_BASE_URL } from "$env/static/public";
  import { fade } from "svelte/transition";

    export let user: UserProfile;
    let showUserMenu = false;

    async function handleLogout() {
        try {
            const response = await fetch(`${PUBLIC_BASE_URL}/auth/logout/`, {
                method: 'POST',
                credentials: 'include'
            });

            if (response.ok) {
                goto('/admin');
            }
        } catch (error) {
            console.error('Logout failed:', error);
        }
    }
</script>

<header class="sticky top-0 z-40 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
    <div class="flex h-16 items-center gap-x-4 px-6">
        <!-- Mobile menu button -->
        <button type="button" class="lg:hidden text-gray-700 dark:text-gray-200">
            <Menu class="w-6 h-6" />
        </button>

        <!-- Search -->
        <div class="flex flex-1 gap-x-4">
            <div class="w-full max-w-md">
                <input
                    type="text"
                    placeholder="Search..."
                    class="w-full bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:text-white"
                />
            </div>
        </div>

        <!-- Actions -->
        <div class="flex items-center gap-x-4">
            <button class="text-gray-700 dark:text-gray-200 hover:text-gray-900 dark:hover:text-white">
                <Bell class="w-6 h-6" />
            </button>

            <!-- User Dropdown -->
            <div class="relative">
                <button 
                    class="flex items-center gap-x-3"
                    on:click={() => showUserMenu = !showUserMenu}
                >
                    <div class="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white font-semibold">
                        {user.first_name[0]}{user.last_name[0]}
                    </div>
                </button>

                {#if showUserMenu}
                    <div 
                        class="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 py-1"
                        transition:fade
                    >
                        <div class="px-4 py-2 border-b border-gray-200 dark:border-gray-700">
                            <p class="text-sm font-medium text-gray-900 dark:text-white">
                                {user.first_name} {user.last_name}
                            </p>
                            <p class="text-xs text-gray-500 dark:text-gray-400">
                                {user.email}
                            </p>
                        </div>

                        <a 
                            href="/admin/settings" 
                            class="flex items-center gap-x-2 px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700"
                        >
                            <Settings class="w-4 h-4" />
                            Settings
                        </a>

                        <button 
                            on:click={handleLogout}
                            class="flex items-center gap-x-2 px-4 py-2 text-sm text-red-600 hover:bg-gray-100 dark:hover:bg-gray-700 w-full"
                        >
                            <LogOut class="w-4 h-4" />
                            Sign out
                        </button>
                    </div>
                {/if}
            </div>
        </div>
    </div>
</header>