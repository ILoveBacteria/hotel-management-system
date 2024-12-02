<script lang="ts">
    import { Home, Calendar, CreditCard, User, LogOut } from "lucide-svelte";

    export let username: string;
    async function logout() {
        // Add your logout logic here
        try {
            // Example: await auth.logout();
            window.location.href = "/login";
        } catch (error) {
            console.error("Logout failed:", error);
        }
    }
</script>

<aside class="fixed inset-y-0 left-0 w-64 bg-white dark:bg-gray-800 shadow-lg">
    <div class="flex flex-col h-full">
        <div
            class="flex items-center justify-center h-16 border-b dark:border-gray-700"
        >
            <span class="text-xl font-bold text-blue-600">Hotel Name</span>
        </div>

        <nav class="flex-1 p-4 space-y-2">
            <a
                href="/dashboard"
                class="flex items-center px-4 py-2 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
            >
                <Home class="w-5 h-5 mr-3" />
                Dashboard
            </a>
            <a
                href="/dashboard/booking"
                class="flex items-center px-4 py-2 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
            >
                <Calendar class="w-5 h-5 mr-3" />
                My Bookings
            </a>
            <a
                href="/payments"
                class="flex items-center px-4 py-2 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
            >
                <CreditCard class="w-5 h-5 mr-3" />
                Payments
            </a>
            <a
                href="/profile"
                class="flex items-center px-4 py-2 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
            >
                <User class="w-5 h-5 mr-3" />
                Profile
            </a>
        </nav>

        <div class="p-4 border-t dark:border-gray-700">
            <button
                class="flex items-center w-full px-4 py-2 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
                on:click={logout}
            >
                <LogOut class="w-5 h-5 mr-3" />
                Logout
            </button>
        </div>
    </div>
</aside>
