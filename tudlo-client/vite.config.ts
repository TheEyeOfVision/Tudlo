import { paraglide } from "@inlang/paraglide-sveltekit/vite";
import { svelteTesting } from "@testing-library/svelte/vite";
import tailwindcss from "@tailwindcss/vite";
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import type { ProxyOptions } from 'vite';

export default defineConfig({
    server: {
        proxy: {
            '/api': {
                target: 'http://127.0.0.1:8000',
                changeOrigin: true,
                rewrite: (path: string) => path.replace(/^\/api/, '')
            } as ProxyOptions
        }
    },
    plugins: [tailwindcss(), sveltekit(), paraglide({
        project: "./project.inlang",
        outdir: "./src/lib/paraglide"
    })],

    test: {
        workspace: [{
            extends: "./vite.config.ts",
            plugins: [svelteTesting()],

            test: {
                name: "client",
                environment: "jsdom",
                clearMocks: true,
                include: ['src/**/*.svelte.{test,spec}.{js,ts}'],
                exclude: ['src/lib/server/**'],
                setupFiles: ['./vitest-setup-client.ts']
            }
        }, {
            extends: "./vite.config.ts",

            test: {
                name: "server",
                environment: "node",
                include: ['src/**/*.{test,spec}.{js,ts}'],
                exclude: ['src/**/*.svelte.{test,spec}.{js,ts}']
            }
        }]
    }
});
