<script lang="ts">
    import Header from "../dashboard/Header.svelte";
    import Sidebar from "../dashboard/Sidebar.svelte";
    import LoadingBar from "../common/LoadingBar.svelte";
    import { navigating } from "$app/stores";
    import { fade } from "svelte/transition";

    export let username: string = "Guest";
    export let notifications: number = 0;
</script>

<LoadingBar />

<div class="flex h-screen bg-gray-50 dark:bg-gray-900">
    <Sidebar {username} />
    <div class="flex-1 ml-64">
        <Header {username} {notifications} />
        <main class="p-6 space-y-6 relative">
            {#if $navigating}
                <div 
                    class="absolute inset-0 bg-white/50 dark:bg-gray-900/50 backdrop-blur-sm z-40 flex items-center justify-center"
                    in:fade={{ duration: 200 }}
                    out:fade={{ duration: 200 }}
                >
                    <div class="flex items-center space-x-2">
                        <div class="w-3 h-3 bg-blue-600 rounded-full animate-bounce" style="animation-delay: 0ms" />
                        <div class="w-3 h-3 bg-blue-600 rounded-full animate-bounce" style="animation-delay: 150ms" />
                        <div class="w-3 h-3 bg-blue-600 rounded-full animate-bounce" style="animation-delay: 300ms" />
                    </div>
                </div>
            {/if}
            <slot />
        </main>
    </div>
</div>