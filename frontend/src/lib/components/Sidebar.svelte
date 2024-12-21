<!-- src/lib/components/dashboard/Sidebar.svelte -->
<script lang="ts">
  import { Home, Calendar, CreditCard, User, LogOut } from "lucide-svelte";
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";

  export let username: string;

  const navItems = [
      { href: "/dashboard", label: "Dashboard", icon: Home },
      { href: "/dashboard/booking", label: "My Bookings", icon: Calendar },
      { href: "/dashboard/payments", label: "Payments", icon: CreditCard },
      { href: "/dashboard/profile", label: "Profile", icon: User }
  ];

  async function logout() {
      try {
          await fetch("/auth/logout", {
              method: "POST",
              credentials: "include"
          });
          goto("/");
      } catch (error) {
          console.error("Logout failed:", error);
      }
  }

  function isActive(href: string): boolean {
      return $page.url.pathname === href;
  }
</script>

<aside class="fixed inset-y-0 left-0 w-64 bg-white dark:bg-gray-800 shadow-lg">
  <div class="flex flex-col h-full">
      <div class="flex items-center justify-center h-16 border-b dark:border-gray-700">
          <span class="text-xl font-bold text-blue-600">Hotel Name</span>
      </div>

      <nav class="flex-1 p-4 space-y-2">
          {#each navItems as { href, label, icon: Icon }}
              <a
                  {href}
                  class="flex items-center px-4 py-2 rounded-lg transition-colors duration-200
                         {isActive(href) 
                             ? 'bg-blue-50 text-blue-600 dark:bg-gray-700 dark:text-blue-400'
                             : 'text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700'}"
              >
                  <Icon class="w-5 h-5 mr-3" />
                  {label}
              </a>
          {/each}
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