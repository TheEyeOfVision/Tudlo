<script lang="ts">
	import { i18n } from "$lib/i18n";
	import { ParaglideJS } from "@inlang/paraglide-sveltekit";
	import '../app.css';
	import {Moon, Sun} from "@lucide/svelte";
	import {Button} from "$lib/components/ui/button";
	let { children } = $props();

	/**
	 * Toggles the dark mode for the website.
	 *
	 * This function switches between light and dark themes by toggling
	 * the "dark" class on the `<html>` element. It also updates the `color-scheme`
	 * for better system compatibility and saves the user's preference in `localStorage`.
	 */
	function toggleMode() {
		const htmlEl = document.documentElement;
		const isDark = htmlEl.classList.toggle("dark"); // Toggles "dark" class

		htmlEl.style.colorScheme = isDark ? "dark" : "light";
		localStorage.setItem("theme", isDark ? "dark" : "light");


	}
</script>

<ParaglideJS {i18n}>
	<!-- Navbar -->
	<header class="w-full p-4">
		<div class="container mx-auto flex items-center justify-between">
			<!-- Logo / Title -->
			<div class="flex items-center gap-6">
				<a href="/" class="text-xl font-semibold">Tudlo</a>
				<a href="/summarizer" class="text-sm font-medium text-foreground hover:underline">Summarizer</a>
			</div>
			<!-- Navigation Button (optional) -->
			<Button onclick={toggleMode} variant="outline" size="icon" class="relative rounded-full transition-colors duration-30 ease-in-out">
				<Sun class="absolute h-[1.2rem] w-[1.2rem] transition-transform duration-300 dark:rotate-90 dark:scale-0 opacity-100 dark:opacity-0" />
				<Moon class="absolute h-[1.2rem] w-[1.2rem] transition-transform duration-300 rotate-90 scale-0 dark:rotate-0 dark:scale-100 opacity-0 dark:opacity-100" />
			</Button>
		</div>
	</header>
	<br>
	{@render children()}
</ParaglideJS>
