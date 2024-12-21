<!-- src/lib/components/admin/layout/AdminSidebar.svelte -->
<script lang="ts">
    import { page } from "$app/stores";
    import type { UserProfile } from "$lib/types";
    import { 
        LayoutDashboard, 
        Hotel, 
        Users, 
        CalendarDays, 
        Settings,
        LogOut,
        Image,
        BedDouble
    } from "lucide-svelte";

    export let user: UserProfile;

    const navigation = [
        { 
            name: 'Dashboard', 
            href: '/admin/dashboard', 
            icon: LayoutDashboard 
        },
        { 
            name: 'Room Types', 
            href: '/admin/room-types', 
            icon: Hotel,
            count: '3'
        },
        { 
            name: 'Room Inventory', 
            href: '/admin/rooms', 
            icon: BedDouble,
            count: '12'
        },
        { 
            name: 'Room Images', 
            href: '/admin/images', 
            icon: Image
        },
        { 
            name: 'Reservations', 
            href: '/admin/reservations', 
            icon: CalendarDays,
            count: '5'
        },
        { 
            name: 'Users', 
            href: '/admin/users', 
            icon: Users,
            count: '2'
        },
    ];

    const secondaryNavigation = [
        { name: 'Settings', href: '/admin/settings', icon: Settings },
    ];

    function isActive(href: string): boolean {
        return $page.url.pathname === href;
    }
</script>

<!-- Fixed sidebar with proper z-index and width -->
<aside class="fixed inset-y-0 left-0 z-50 w-72 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700">
    <div class="flex flex-col h-full">
        <!-- Logo -->
        <div class="flex h-16 items-center gap-x-3 px-6 border-b border-gray-200 dark:border-gray-700">
            <span class="text-2xl font-bold text-blue-600">Hotel Admin</span>
        </div>

        <!-- Navigation -->
        <div class="flex-1 flex flex-col min-h-0">  <!-- Added min-h-0 to fix flexbox height -->
            <div class="flex-1 px-4 py-4 overflow-y-auto">
                <nav class="space-y-1">
                    {#each navigation as item}
                        <a
                            href={item.href}
                            class="flex items-center gap-x-3 px-3 py-2 text-sm font-medium rounded-lg
                                {isActive(item.href)
                                    ? 'bg-gray-100 dark:bg-gray-700 text-blue-600 dark:text-blue-400'
                                    : 'text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700'}"
                        >
                            <svelte:component this={item.icon} class="w-5 h-5" />
                            <span class="flex-1">{item.name}</span>
                            {#if item.count}
                                <span class="px-2 py-1 text-xs rounded-full bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300">
                                    {item.count}
                                </span>
                            {/if}
                        </a>
                    {/each}
                </nav>

                <!-- Secondary Navigation -->
                <nav class="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700 space-y-1">
                    {#each secondaryNavigation as item}
                        <a
                            href={item.href}
                            class="flex items-center gap-x-3 px-3 py-2 text-sm font-medium rounded-lg
                                {isActive(item.href)
                                    ? 'bg-gray-100 dark:bg-gray-700 text-blue-600 dark:text-blue-400'
                                    : 'text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700'}"
                        >
                            <svelte:component this={item.icon} class="w-5 h-5" />
                            {item.name}
                        </a>
                    {/each}
                </nav>
            </div>

            <!-- User Profile -->
            <div class="flex-shrink-0 p-4 border-t border-gray-200 dark:border-gray-700">
                <div class="flex items-center gap-x-3">
                    <div class="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center text-white font-semibold">
                        {user.first_name[0]}{user.last_name[0]}
                    </div>
                    <div class="flex-1 min-w-0">
                        <p class="text-sm font-medium text-gray-900 dark:text-white truncate">
                            {user.first_name} {user.last_name}
                        </p>
                        <p class="text-xs text-gray-500 dark:text-gray-400 truncate">
                            {user.email}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</aside>