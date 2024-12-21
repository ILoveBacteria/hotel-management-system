<!-- src/lib/components/admin/layout/AdminLayout.svelte -->
<script lang="ts">
    import { page } from "$app/stores";
    import AdminSidebar from "./AdminSidebar.svelte";
    import AdminHeader from "./AdminHeader.svelte";
    import { navigating } from "$app/stores";
    import { fade } from "svelte/transition";
    import type { UserProfile } from "$lib/types";

    export let user: UserProfile;
</script>

<div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <AdminSidebar {user} />
    
    <!-- Main content wrapper with proper sidebar spacing -->
    <div class="lg:ml-72">  <!-- Changed from pl-72 to ml-72 for better spacing -->
        <AdminHeader {user} />
        
        <main class="p-6 max-w-[1600px]"> <!-- Added max-width for larger screens -->
            <!-- Loading Overlay -->
            {#if $navigating}
                <div 
                    class="fixed inset-0 bg-white/50 dark:bg-gray-900/50 backdrop-blur-sm z-40 flex items-center justify-center"
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

            <!-- Main Content -->
            <div class="w-full">
                <slot />
            </div>
        </main>
    </div>
</div>