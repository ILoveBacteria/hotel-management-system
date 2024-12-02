<!-- Sidebar.svelte -->
<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { fade, slide } from "svelte/transition";

  // Type definitions
  type SubMenuItem = {
    id: string;
    label: string;
    badge: string | null;
  };

  type MenuItem = {
    id: string;
    label: string;
    icon: string;
    badge: string | null;
    subItems?: SubMenuItem[];
  };

  export let currentPage: string;
  const dispatch = createEventDispatcher();

  // State for collapsible sections
  let expandedSection = "";
  let isSidebarCollapsed = false;

  // Main Navigation Items
  const mainMenuItems: MenuItem[] = [
    {
      id: "dashboard",
      label: "Dashboard",
      icon: "📊",
      badge: null,
    },
    {
      id: "bookings",
      label: "Bookings & Reservations",
      icon: "📅",
      badge: "12",
      subItems: [
        { id: "new-booking", label: "New Booking", badge: null },
        { id: "upcoming", label: "Upcoming", badge: "8" },
        { id: "current", label: "Current Stay", badge: "4" },
        { id: "history", label: "History", badge: null },
      ],
    },
    {
      id: "rooms",
      label: "Room Management",
      icon: "🛏️",
      badge: "3",
      subItems: [
        { id: "room-status", label: "Room Status", badge: null },
        { id: "maintenance", label: "Maintenance", badge: "3" },
        { id: "housekeeping", label: "Housekeeping", badge: null },
        { id: "room-types", label: "Room Types", badge: null },
      ],
    },
    {
      id: "guests",
      label: "Guest Management",
      icon: "👥",
      badge: null,
      subItems: [
        { id: "guest-list", label: "Guest List", badge: null },
        { id: "vip-guests", label: "VIP Guests", badge: "2" },
        { id: "requests", label: "Guest Requests", badge: "5" },
        { id: "reviews", label: "Guest Reviews", badge: null },
      ],
    },
  ];

  // Operations Menu Items
  const operationsItems: MenuItem[] = [
    {
      id: "staff",
      label: "Staff Management",
      icon: "👤",
      badge: null,
      subItems: [
        { id: "staff-list", label: "Staff List", badge: null },
        { id: "scheduling", label: "Scheduling", badge: null },
        { id: "performance", label: "Performance", badge: null },
      ],
    },
    {
      id: "services",
      label: "Hotel Services",
      icon: "🛎️",
      badge: "7",
      subItems: [
        { id: "room-service", label: "Room Service", badge: "4" },
        { id: "restaurant", label: "Restaurant", badge: "3" },
        { id: "spa", label: "Spa & Wellness", badge: null },
        { id: "activities", label: "Activities", badge: null },
      ],
    },
  ];

  // Reports & Analytics Items
  const reportsItems: MenuItem[] = [
    {
      id: "reports",
      label: "Reports & Analytics",
      icon: "📈",
      badge: null,
      subItems: [
        { id: "financial", label: "Financial Reports", badge: null },
        { id: "occupancy", label: "Occupancy Reports", badge: null },
        { id: "revenue", label: "Revenue Analysis", badge: null },
        { id: "guest-analytics", label: "Guest Analytics", badge: null },
      ],
    },
  ];

  // System Settings Items
  const settingsItems: MenuItem[] = [
    {
      id: "settings",
      label: "System Settings",
      icon: "⚙️",
      badge: null,
      subItems: [
        { id: "hotel-profile", label: "Hotel Profile", badge: null },
        { id: "rates", label: "Rates & Pricing", badge: null },
        { id: "integrations", label: "Integrations", badge: null },
        { id: "permissions", label: "User Permissions", badge: null },
      ],
    },
  ];

  type QuickShortcut = {
    id: string;
    label: string;
    icon: string;
  };

  // Quick Access Shortcuts
  const quickShortcuts: QuickShortcut[] = [
    { id: "quick-checkin", label: "Quick Check-in", icon: "✅" },
    { id: "quick-checkout", label: "Quick Check-out", icon: "🚪" },
    { id: "new-reservation", label: "New Reservation", icon: "📝" },
  ];

  type SupportInfo = {
    version: string;
    supportEmail: string;
    helpCenter: string;
    training: string;
  };

  // Support & Help
  const supportInfo: SupportInfo = {
    version: "v2.1.0",
    supportEmail: "support@hotelmanager.com",
    helpCenter: "Help Center",
    training: "Training Videos",
  };

  function toggleSection(sectionId: string): void {
    expandedSection = expandedSection === sectionId ? "" : sectionId;
  }

  function toggleSidebar(): void {
    isSidebarCollapsed = !isSidebarCollapsed;
  }

  function navigate(pageId: string, subItemId: string | null = null): void {
    const fullPageId = subItemId ? `${pageId}-${subItemId}` : pageId;
    dispatch("navigate", fullPageId);
  }

  // Function to render menu items
  function renderMenuItem(item: MenuItem, isSubItem = false): string {
    const isActive = currentPage === (isSubItem ? `${item.id}` : item.id);
    const baseClasses = `
        w-full px-4 py-2 text-left
        flex items-center justify-between
        transition-colors duration-200
        ${isSubItem ? "pl-12 text-sm" : "font-medium"}
        ${isActive ? "bg-blue-50 text-blue-600" : "text-gray-600 hover:bg-gray-50"}
      `;

    return `
        <button class="${baseClasses}" on:click={() => navigate(item.id)}>
          <div class="flex items-center gap-3">
            ${!isSubItem ? `<span class="text-xl">${item.icon}</span>` : ""}
            <span>${item.label}</span>
          </div>
          ${
            item.badge
              ? `
            <span class="px-2 py-1 text-xs bg-blue-100 text-blue-600 rounded-full">
              ${item.badge}
            </span>
          `
              : ""
          }
        </button>
      `;
  }
</script>

<aside
  class="flex flex-col h-full bg-white shadow-lg {isSidebarCollapsed
    ? 'w-20'
    : 'w-64'}
                  transition-all duration-300 ease-in-out"
>
  <!-- Header -->
  <div class="p-4 bg-blue-600 flex items-center justify-between">
    {#if !isSidebarCollapsed}
      <h1 class="text-white text-xl font-bold">Hotel Manager</h1>
    {:else}
      <h1 class="text-white text-xl font-bold">HM</h1>
    {/if}
    <button
      class="text-white hover:bg-blue-700 p-2 rounded-lg"
      on:click={toggleSidebar}
    >
      {isSidebarCollapsed ? "→" : "←"}
    </button>
  </div>

  <!-- Quick Shortcuts -->
  {#if !isSidebarCollapsed}
    <div class="p-4 border-b border-gray-200">
      <div class="grid grid-cols-3 gap-2">
        {#each quickShortcuts as shortcut}
          <button
            class="p-2 text-center text-sm bg-gray-50 hover:bg-gray-100 rounded-lg
                     flex flex-col items-center gap-1"
            on:click={() => navigate(shortcut.id)}
          >
            <span class="text-xl">{shortcut.icon}</span>
            <span class="text-xs">{shortcut.label}</span>
          </button>
        {/each}
      </div>
    </div>
  {/if}

  <!-- Navigation Sections -->
  <div class="flex-1 overflow-y-auto">
    <!-- Main Navigation -->
    <nav class="p-2">
      <div class="space-y-1">
        {#each mainMenuItems as item}
          <div>
            <button
              class="w-full px-4 py-2 text-left hover:bg-gray-50 flex items-center justify-between
                       {currentPage === item.id
                ? 'bg-blue-50 text-blue-600'
                : 'text-gray-600'}"
              on:click={() =>
                item.subItems ? toggleSection(item.id) : navigate(item.id)}
            >
              <div class="flex items-center gap-3">
                <span class="text-xl">{item.icon}</span>
                {#if !isSidebarCollapsed}
                  <span>{item.label}</span>
                {/if}
              </div>
              {#if !isSidebarCollapsed && item.subItems}
                <span
                  class="transform transition-transform duration-200
                             {expandedSection === item.id ? 'rotate-180' : ''}"
                >
                  ▼
                </span>
              {/if}
            </button>

            {#if !isSidebarCollapsed && item.subItems && expandedSection === item.id}
              <div class="mt-1 space-y-1" transition:slide>
                {#each item.subItems as subItem}
                  <button
                    class="w-full pl-12 pr-4 py-2 text-sm text-left hover:bg-gray-50
                             {currentPage === `${item.id}-${subItem.id}`
                      ? 'bg-blue-50 text-blue-600'
                      : 'text-gray-600'}"
                    on:click={() => navigate(item.id, subItem.id)}
                  >
                    <div class="flex items-center justify-between">
                      <span>{subItem.label}</span>
                      {#if subItem.badge}
                        <span
                          class="px-2 py-1 text-xs bg-blue-100 text-blue-600 rounded-full"
                        >
                          {subItem.badge}
                        </span>
                      {/if}
                    </div>
                  </button>
                {/each}
              </div>
            {/if}
          </div>
        {/each}
      </div>
    </nav>

    <!-- Operations Section -->
    {#if !isSidebarCollapsed}
      <div class="p-2 border-t border-gray-200">
        <p class="px-4 py-2 text-xs font-semibold text-gray-400 uppercase">
          Operations
        </p>
        {#each operationsItems as item}
          <!-- Similar structure as main navigation items -->
          <div class="space-y-1">
            <!-- Operations menu items rendering -->
          </div>
        {/each}
      </div>
    {/if}

    <!-- Reports Section -->
    {#if !isSidebarCollapsed}
      <div class="p-2 border-t border-gray-200">
        <p class="px-4 py-2 text-xs font-semibold text-gray-400 uppercase">
          Reports & Analytics
        </p>
        {#each reportsItems as item}
          <!-- Similar structure as main navigation items -->
          <div class="space-y-1">
            <!-- Reports menu items rendering -->
          </div>
        {/each}
      </div>
    {/if}
  </div>

  <!-- Footer Section -->
  {#if !isSidebarCollapsed}
    <div class="p-4 border-t border-gray-200 bg-gray-50">
      <div class="space-y-2">
        <div class="flex items-center justify-between text-sm text-gray-600">
          <span>Version</span>
          <span>{supportInfo.version}</span>
        </div>
        <button
          class="w-full px-3 py-2 text-sm text-blue-600 hover:bg-blue-50 rounded-lg"
        >
          {supportInfo.helpCenter}
        </button>
        <button
          class="w-full px-3 py-2 text-sm text-blue-600 hover:bg-blue-50 rounded-lg"
        >
          {supportInfo.training}
        </button>
      </div>
    </div>
  {/if}
</aside>
