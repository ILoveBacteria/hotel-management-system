<script lang="ts">
    import { Bell, Settings } from "lucide-svelte";
    export let username: string;
    export let notifications: number;

    function handleNotificationClick() {
        // Add notification handling logic
    }

    function handleSettingsClick() {
        // Add settings handling logic
    }
</script>

<header class="bg-white dark:bg-gray-800 shadow-md">
    <div class="flex items-center justify-between px-6 h-16">
        <h1 class="text-xl font-semibold text-gray-800 dark:text-white">
            Dashboard
        </h1>

        <div class="flex items-center space-x-4">
            <button
                class="relative p-2 text-gray-600 hover:text-gray-800 dark:text-gray-300 dark:hover:text-white"
                on:click={handleNotificationClick}
            >
                <Bell class="w-6 h-6" />
                {#if notifications > 0}
                    <span
                        class="absolute top-0 right-0 w-4 h-4 bg-red-500 rounded-full text-xs text-white flex items-center justify-center"
                    >
                        {notifications}
                    </span>
                {/if}
            </button>

            <button
                class="p-2 text-gray-600 hover:text-gray-800 dark:text-gray-300 dark:hover:text-white"
                on:click={handleSettingsClick}
            >
                <Settings class="w-6 h-6" />
            </button>

            <div class="flex items-center space-x-3">
                <div
                    class="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center text-white font-semibold"
                >
                    {username.charAt(0)}
                </div>
                <span class="text-gray-800 dark:text-white font-medium"
                    >{username}</span
                >
            </div>
        </div>
    </div>
</header>
