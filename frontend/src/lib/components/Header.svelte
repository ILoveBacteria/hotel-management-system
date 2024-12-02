<!-- Header.svelte -->
<script>
  import { onMount } from "svelte";

  // User Information
  let currentUser = {
    name: "John Doe",
    role: "Hotel Manager",
    avatar: null,
    lastActive: "2 hours ago",
    shift: "Morning Shift (6:00 AM - 2:00 PM)",
  };

  // Notifications Data
  let notifications = [
    {
      id: 1,
      type: "urgent",
      message: "VIP Guest arriving in 30 minutes - Room 501",
      time: "5 min ago",
      read: false,
    },
    {
      id: 2,
      type: "maintenance",
      message: "Maintenance request for Room 302 - AC not working",
      time: "15 min ago",
      read: false,
    },
    {
      id: 3,
      type: "booking",
      message: "New booking confirmed for tomorrow",
      time: "1 hour ago",
      read: true,
    },
    {
      id: 4,
      type: "staff",
      message: "Staff meeting scheduled for 4:00 PM",
      time: "2 hours ago",
      read: true,
    },
  ];

  // Quick Actions
  let quickActions = [
    { id: 1, label: "New Booking", icon: "📝" },
    { id: 2, label: "Check In", icon: "✅" },
    { id: 3, label: "Check Out", icon: "🚪" },
    { id: 4, label: "Room Service", icon: "🛎️" },
  ];

  // Hotel Status
  let hotelStatus = {
    occupancyRate: "82%",
    avgDailyRate: "₹4,500",
    totalGuests: 78,
    pendingRequests: 5,
  };

  // Weather Information (would typically come from an API)
  let weather = {
    temp: "24°C",
    condition: "Sunny",
    icon: "☀️",
  };

  // Toggle states
  let showNotifications = false;
  let showUserMenu = false;
  let showQuickActions = false;

  // Notification functions
  function markAllAsRead() {
    notifications = notifications.map((n) => ({ ...n, read: true }));
  }

  function getUnreadCount() {
    return notifications.filter((n) => !n.read).length;
  }

  // Format current time
  function getCurrentTime() {
    return new Date().toLocaleTimeString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
    });
  }
</script>

<header class="bg-white shadow-sm">
  <!-- Top Status Bar -->
  <div
    class="bg-blue-600 text-white px-4 py-1 text-sm flex justify-between items-center"
  >
    <div class="flex items-center gap-4">
      <span>{getCurrentTime()}</span>
      <span>|</span>
      <span>Occupancy: {hotelStatus.occupancyRate}</span>
      <span>|</span>
      <span>{weather.temp} {weather.icon}</span>
    </div>
    <div class="flex items-center gap-4">
      <span>ADR: {hotelStatus.avgDailyRate}</span>
      <span>|</span>
      <span>Active Guests: {hotelStatus.totalGuests}</span>
    </div>
  </div>

  <!-- Main Header -->
  <div class="px-6 py-4">
    <div class="flex justify-between items-center">
      <!-- Left Section - Welcome & Time -->
      <div>
        <h2 class="text-xl font-semibold text-gray-800">
          Welcome Back, {currentUser.name}
        </h2>
        <div class="flex items-center gap-2 text-sm text-gray-600">
          <span>{currentUser.shift}</span>
          <span class="w-1 h-1 bg-gray-400 rounded-full"></span>
          <span>Last active: {currentUser.lastActive}</span>
        </div>
      </div>

      <!-- Right Section - Actions & Profile -->
      <div class="flex items-center gap-6">
        <!-- Quick Actions -->
        <div class="relative">
          <button
            class="p-2 hover:bg-gray-100 rounded-lg flex items-center gap-2"
            on:click={() => (showQuickActions = !showQuickActions)}
          >
            <span class="text-gray-600">Quick Actions</span>
            <span>⚡</span>
          </button>

          {#if showQuickActions}
            <div
              class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-100 z-50"
            >
              {#each quickActions as action}
                <button
                  class="w-full px-4 py-2 text-left hover:bg-gray-50 flex items-center gap-2"
                >
                  <span>{action.icon}</span>
                  <span>{action.label}</span>
                </button>
              {/each}
            </div>
          {/if}
        </div>

        <!-- Notifications -->
        <div class="relative">
          <button
            class="p-2 hover:bg-gray-100 rounded-lg relative"
            on:click={() => (showNotifications = !showNotifications)}
          >
            <span class="text-xl">🔔</span>
            {#if getUnreadCount() > 0}
              <span
                class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center"
              >
                {getUnreadCount()}
              </span>
            {/if}
          </button>

          {#if showNotifications}
            <div
              class="absolute right-0 mt-2 w-96 bg-white rounded-lg shadow-lg border border-gray-100 z-50"
            >
              <div class="p-4 border-b border-gray-100">
                <div class="flex justify-between items-center">
                  <h3 class="font-semibold">Notifications</h3>
                  <button
                    class="text-sm text-blue-600 hover:text-blue-800"
                    on:click={markAllAsRead}
                  >
                    Mark all as read
                  </button>
                </div>
              </div>
              <div class="max-h-96 overflow-y-auto">
                {#each notifications as notification}
                  <div
                    class="p-4 hover:bg-gray-50 border-b border-gray-100 {notification.read
                      ? 'opacity-70'
                      : ''}"
                  >
                    <div class="flex gap-3">
                      <span class="text-xl">
                        {#if notification.type === "urgent"}
                          🔴
                        {:else if notification.type === "maintenance"}
                          🔧
                        {:else if notification.type === "booking"}
                          📅
                        {:else}
                          👥
                        {/if}
                      </span>
                      <div>
                        <p class="text-sm">{notification.message}</p>
                        <p class="text-xs text-gray-500 mt-1">
                          {notification.time}
                        </p>
                      </div>
                    </div>
                  </div>
                {/each}
              </div>
            </div>
          {/if}
        </div>

        <!-- User Profile -->
        <div class="relative">
          <button
            class="flex items-center gap-3 hover:bg-gray-100 rounded-lg p-2"
            on:click={() => (showUserMenu = !showUserMenu)}
          >
            <div
              class="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white font-semibold"
            >
              {currentUser.name
                .split(" ")
                .map((n) => n[0])
                .join("")}
            </div>
            <div class="text-left">
              <p class="text-sm font-medium">{currentUser.name}</p>
              <p class="text-xs text-gray-500">{currentUser.role}</p>
            </div>
          </button>

          {#if showUserMenu}
            <div
              class="absolute right-0 mt-2 w-64 bg-white rounded-lg shadow-lg border border-gray-100 z-50"
            >
              <div class="p-4 border-b border-gray-100">
                <p class="font-medium">{currentUser.name}</p>
                <p class="text-sm text-gray-500">{currentUser.role}</p>
              </div>
              <div class="p-2">
                <button
                  class="w-full px-4 py-2 text-left hover:bg-gray-50 text-sm"
                  >View Profile</button
                >
                <button
                  class="w-full px-4 py-2 text-left hover:bg-gray-50 text-sm"
                  >Settings</button
                >
                <button
                  class="w-full px-4 py-2 text-left hover:bg-gray-50 text-sm"
                  >Help Center</button
                >
                <button
                  class="w-full px-4 py-2 text-left hover:bg-gray-50 text-sm text-red-600"
                  >Sign Out</button
                >
              </div>
            </div>
          {/if}
        </div>
      </div>
    </div>

    <!-- Quick Stats Bar -->
    <div class="mt-4 grid grid-cols-4 gap-4">
      {#each Object.entries(hotelStatus) as [key, value]}
        <div class="bg-gray-50 p-3 rounded-lg">
          <p class="text-sm text-gray-500 capitalize">
            {key.replace(/([A-Z])/g, " $1").trim()}
          </p>
          <p class="text-lg font-semibold">{value}</p>
        </div>
      {/each}
    </div>
  </div>
</header>
