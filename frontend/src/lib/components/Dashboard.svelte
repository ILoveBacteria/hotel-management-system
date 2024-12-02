<!-- Dashboard.svelte -->
<script>
    import { onMount } from 'svelte';
  
    // Quick Stats Data
    let stats = [
      { label: 'Available Rooms', value: '12', icon: '🛏️', trend: '+2', color: 'text-green-500' },
      { label: 'Occupied Rooms', value: '45', icon: '🏠', trend: '-1', color: 'text-blue-500' },
      { label: 'Pending Check-ins', value: '8', icon: '✅', trend: '+3', color: 'text-yellow-500' },
      { label: 'Pending Check-outs', value: '6', icon: '🚪', trend: '-2', color: 'text-red-500' }
    ];
  
    // Recent Bookings Data
    let recentBookings = [
      {
        id: 'BK001',
        guestName: 'Alice Johnson',
        roomNumber: '301',
        checkIn: '2024-11-19',
        checkOut: '2024-11-22',
        status: 'Confirmed',
        payment: 'Paid'
      },
      {
        id: 'BK002',
        guestName: 'Robert Smith',
        roomNumber: '205',
        checkIn: '2024-11-20',
        checkOut: '2024-11-25',
        status: 'Pending',
        payment: 'Partial'
      },
      {
        id: 'BK003',
        guestName: 'Emma Davis',
        roomNumber: '401',
        checkIn: '2024-11-19',
        checkOut: '2024-11-21',
        status: 'Checked In',
        payment: 'Paid'
      }
    ];
  
    // Today's Tasks
    let tasks = [
      {
        id: 1,
        title: 'VIP Guest Arrival',
        time: '14:00',
        priority: 'High',
        assigned: 'Front Desk',
        status: 'Pending'
      },
      {
        id: 2,
        title: 'Room 205 Maintenance',
        time: '15:30',
        priority: 'Medium',
        assigned: 'Maintenance',
        status: 'In Progress'
      },
      {
        id: 3,
        title: 'Restaurant Reservation',
        time: '18:00',
        priority: 'Normal',
        assigned: 'Restaurant',
        status: 'Confirmed'
      }
    ];
  
    // Room Status Distribution
    let roomStatus = {
      occupied: 45,
      available: 12,
      maintenance: 3,
      reserved: 5
    };
  
    // Revenue Overview
    let revenueData = {
      daily: '₹12,500',
      weekly: '₹82,300',
      monthly: '₹3,45,000',
      trend: '+12.5%'
    };
  
    // Housekeeping Status
    let housekeepingStatus = [
      { status: 'Cleaned', rooms: ['201', '202', '205', '301'] },
      { status: 'Pending', rooms: ['304', '305'] },
      { status: 'In Progress', rooms: ['401', '402'] }
    ];
  </script>
  
  <div class="space-y-6">
    <!-- Quick Stats Section -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {#each stats as stat}
        <div class="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-4">
              <span class="text-2xl">{stat.icon}</span>
              <div>
                <p class="text-sm text-gray-500">{stat.label}</p>
                <p class="text-2xl font-semibold">{stat.value}</p>
              </div>
            </div>
            <div class={stat.color}>
              {stat.trend}
            </div>
          </div>
        </div>
      {/each}
    </div>
  
    <!-- Main Dashboard Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <!-- Recent Bookings Section -->
      <div class="lg:col-span-2 bg-white p-6 rounded-lg shadow-sm">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold">Recent Bookings</h3>
          <button class="text-blue-600 hover:text-blue-800 text-sm">View All</button>
        </div>
        <div class="overflow-x-auto">
          <table class="min-w-full">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Guest</th>
                <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Room</th>
                <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Check In</th>
                <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              {#each recentBookings as booking}
                <tr class="hover:bg-gray-50">
                  <td class="px-4 py-2 text-sm">{booking.id}</td>
                  <td class="px-4 py-2 text-sm">{booking.guestName}</td>
                  <td class="px-4 py-2 text-sm">{booking.roomNumber}</td>
                  <td class="px-4 py-2 text-sm">{booking.checkIn}</td>
                  <td class="px-4 py-2">
                    <span class="px-2 py-1 text-xs rounded-full
                      {booking.status === 'Confirmed' ? 'bg-green-100 text-green-800' :
                       booking.status === 'Pending' ? 'bg-yellow-100 text-yellow-800' :
                       'bg-blue-100 text-blue-800'}">
                      {booking.status}
                    </span>
                  </td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      </div>
  
      <!-- Today's Tasks Section -->
      <div class="bg-white p-6 rounded-lg shadow-sm">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold">Today's Tasks</h3>
          <button class="text-blue-600 hover:text-blue-800 text-sm">Add Task</button>
        </div>
        <div class="space-y-4">
          {#each tasks as task}
            <div class="p-4 rounded-lg bg-gray-50 hover:bg-gray-100">
              <div class="flex justify-between items-start">
                <div>
                  <h4 class="font-medium">{task.title}</h4>
                  <p class="text-sm text-gray-500">{task.time} - {task.assigned}</p>
                </div>
                <span class="px-2 py-1 text-xs rounded-full
                  {task.priority === 'High' ? 'bg-red-100 text-red-800' :
                   task.priority === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                   'bg-green-100 text-green-800'}">
                  {task.priority}
                </span>
              </div>
            </div>
          {/each}
        </div>
      </div>
    </div>
  
    <!-- Additional Information Section -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <!-- Revenue Overview -->
      <div class="bg-white p-6 rounded-lg shadow-sm">
        <h3 class="text-lg font-semibold mb-4">Revenue Overview</h3>
        <div class="space-y-4">
          <div class="flex justify-between items-center">
            <span class="text-gray-500">Daily Revenue</span>
            <span class="font-semibold">{revenueData.daily}</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-500">Weekly Revenue</span>
            <span class="font-semibold">{revenueData.weekly}</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-500">Monthly Revenue</span>
            <div class="text-right">
              <span class="font-semibold block">{revenueData.monthly}</span>
              <span class="text-sm text-green-500">{revenueData.trend}</span>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Room Status Overview -->
      <div class="bg-white p-6 rounded-lg shadow-sm">
        <h3 class="text-lg font-semibold mb-4">Room Status Overview</h3>
        <div class="space-y-4">
          <div class="flex justify-between items-center">
            <span class="text-gray-500">Occupied</span>
            <span class="font-semibold">{roomStatus.occupied} rooms</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-500">Available</span>
            <span class="font-semibold">{roomStatus.available} rooms</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-500">Maintenance</span>
            <span class="font-semibold">{roomStatus.maintenance} rooms</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-500">Reserved</span>
            <span class="font-semibold">{roomStatus.reserved} rooms</span>
          </div>
        </div>
      </div>
  
      <!-- Housekeeping Status -->
      <div class="bg-white p-6 rounded-lg shadow-sm">
        <h3 class="text-lg font-semibold mb-4">Housekeeping Status</h3>
        <div class="space-y-4">
          {#each housekeepingStatus as status}
            <div class="bg-gray-50 p-3 rounded">
              <div class="flex justify-between items-center mb-2">
                <span class="font-medium">{status.status}</span>
                <span class="text-sm text-gray-500">{status.rooms.length} rooms</span>
              </div>
              <div class="flex flex-wrap gap-2">
                {#each status.rooms as room}
                  <span class="px-2 py-1 bg-white rounded text-sm">{room}</span>
                {/each}
              </div>
            </div>
          {/each}
        </div>
      </div>
    </div>
  </div>