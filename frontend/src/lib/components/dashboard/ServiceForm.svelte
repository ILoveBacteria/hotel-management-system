<script lang="ts">
    export let selectedService: string = "";
    export let serviceDate: string = "";
    export let serviceTime: string = "";

    async function handleSubmit(e: Event) {
        e.preventDefault();
        try {
            // Add service booking logic here
            const serviceData = {
                type: selectedService,
                date: serviceDate,
                time: serviceTime,
            };
            // Example: await serviceBooking.create(serviceData);
            alert("Service booked successfully!");
        } catch (error) {
            console.error("Service booking failed:", error);
            alert("Service booking failed. Please try again.");
        }
    }
</script>

<div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
    <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">
        Order Services
    </h2>
    <form class="space-y-4" on:submit|preventDefault={handleSubmit}>
        <div>
            <label
                class="block text-sm font-medium text-gray-700 dark:text-gray-300"
            >
                Service Type
            </label>
            <select
                bind:value={selectedService}
                class="mt-1 block w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                required
            >
                <option value="">Select a service</option>
                <option value="cleaning">Room Cleaning</option>
                <option value="roomService">Room Service</option>
                <option value="maintenance">Maintenance</option>
                <option value="laundry">Laundry</option>
            </select>
        </div>
        <div>
            <label
                class="block text-sm font-medium text-gray-700 dark:text-gray-300"
            >
                Date
            </label>
            <input
                type="date"
                bind:value={serviceDate}
                class="mt-1 block w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                required
            />
        </div>
        <div>
            <label
                class="block text-sm font-medium text-gray-700 dark:text-gray-300"
            >
                Time
            </label>
            <input
                type="time"
                bind:value={serviceTime}
                class="mt-1 block w-full rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                required
            />
        </div>
        <button
            type="submit"
            class="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors"
        >
            Order Service
        </button>
    </form>
</div>
