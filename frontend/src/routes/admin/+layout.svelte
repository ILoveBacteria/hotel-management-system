<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { PUBLIC_BASE_URL } from "$env/static/public";
  import type { UserProfile } from "$lib/types";
  import AdminLayout from "$lib/components/admin/AdminLayout.svelte";
  import { page } from "$app/stores";

  let user: UserProfile | null = null;
  let isAdminLoginPage = $page.url.pathname == "/admin/login";

  async function checkAdmin() {
    try {
      const response = await fetch(`${PUBLIC_BASE_URL}/users/profile/`, {
        credentials: "include",
      });

      if (!response.ok) {
        goto("/admin/login");
        return;
      }

      const userProfile: UserProfile = await response.json();

      if (!userProfile.is_superuser) {
        goto("/admin/login");
        return;
      }

      user = userProfile;
    } catch (err) {
      goto("/admin/login");
    }
  }

  onMount(() => {
    checkAdmin();
  });
</script>

{#if isAdminLoginPage}
  <slot />
{:else if user}
  <AdminLayout {user}>
    <slot />
  </AdminLayout>
{:else}{/if}
