<script lang="ts">
    import "../../app.css";

    import {ChevronUp, Upload, Loader2, ChevronLeft, ChevronRight, Plus, Trash2} from "@lucide/svelte";
    import { Button } from "$lib/components/ui/button/index.js";
    import { Input } from "$lib/components/ui/input/index.js";
    import { Label } from "$lib/components/ui/label/index.js";
    import { Textarea } from "$lib/components/ui/textarea/index.js";
    import * as Drawer from "$lib/components/ui/drawer/index.js";

    import { readTextFile, readPdfFile, readDocxFile } from "$lib/utils";

    /**
     * Uploaded file
     */
    let fileInput: File;

    /**
     * Text to be summarized by the backend.
     */
    let texts: string[] = [""];

    /**
     * Additional Parameters from the user. The Large Language Model will take these into account when generating responses.
     */
    let additionalParams: string = "";

    /**
     * Temperature parameter for LLM responses.
     */
    let llmTemp: number = 0.7;

    /**
     * Number of paragraphs for summary.
     */
    let paragraphs: number = 0;

    /**
     * Number of sentences per paragraph.
     */
    let sentences: number = 0;

    /**
     * Response from LLM to be displayed
     */
    interface Summary {
        topic: string;
        summary: string;
    }
    let summaryResponses: Summary[] = [{
        topic: "",
        summary: ""
    }];

    /**
     * flag for if LLM is processing text
     */
    let isLoading: boolean = false;

    let currentPage: number = 1;
    let totalPages: number = 1;
    let lastSummarizedPage: number = 1;

    /**
     * Send details to backend
     */
    async function send() {
        const formData = new FormData();
        let selectedTexts = texts.slice(lastSummarizedPage, totalPages + 1);
        selectedTexts.forEach((text, index) => {
            formData.append(`texts`, text);
        });
        formData.append("additional_params", additionalParams);
        formData.append("temperature", llmTemp.toString());
        formData.append("paragraphs", paragraphs.toString());
        formData.append("sentences", sentences.toString());

        lastSummarizedPage = totalPages;
        isLoading = true;

        try {
            const response = await fetch('http://127.0.0.1:8000/api/summarize', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // Append each summary in order
            data.results.forEach((result: any) => {
                summaryResponses.push({
                    topic: result.topic,
                    summary: result.summary
                });
            });

        } catch (error) {
            console.error('Error:', error);
            summaryResponses.push({
                topic: "Error",
                summary: error.message
            })
        } finally {
            isLoading = false;
        }
    }


    /**
     * Ensure that temperature is in range and round it off to the nearest hundredths.
     */
    function validateTemp(): void {
        console.log("e")
        llmTemp = Math.max(0, Math.min(2, llmTemp)); // Clamp value between 0 and 2
        llmTemp = Math.round(llmTemp * 100) / 100; // Round to nearest tenth
    }

    /**
     * Get label for temperature UI
     * @param temp
     */
    function getTemperatureLabel(temp: number): string {
        if (temp >= 0.0 && temp <= 0.3) return "Objective";
        if (temp > 0.3 && temp <= 0.7) return "Balanced";
        if (temp > 0.7 && temp <= 1.2) return "Creative";
        return "Chaotic";
    }

    /**
     * Get color for temperature UI
     * @param temp
     */
    function getTempColor(temp: number) {
        if (temp <= 0.3) return "#3b82f6"; // Green (Objective)
        if (temp <= 0.7) return "#22c55e"; // Blue (Balanced)
        if (temp <= 1.2) return "#eab308"; // Yellow (Creative)
        return "#f97316"; // Red (Chaotic)
    }

    /**
     * Open file upload window
     */
    function triggerFileUpload() {
        const fileInput = document.getElementById("text-file");
        if (fileInput) {
            fileInput.click();
        } else {
            console.error("Element with ID 'text-file' not found.");
        }
    }

    /**
     * Upload files and extract text from each
     * @param event
     */
    async function handleFileUpload(event: Event) {
        const input = event.target as HTMLInputElement;
        if (!input.files || input.files.length === 0) return;

        // Process each file sequentially
        for (let i = 0; i < input.files.length; i++) {
            const file = input.files[i];
            const fileType = file.name.split(".").pop()?.toLowerCase();

            if (totalPages > 1 || texts[currentPage]) {
                totalPages += 1;
            }
            currentPage = totalPages;

            try {
                if (fileType === "txt") {
                    texts[currentPage] = await readTextFile(file);
                } else if (fileType === "pdf") {
                    texts[currentPage] = await readPdfFile(file);
                } else if (fileType === "docx") {
                    texts[currentPage] = await readDocxFile(file);
                } else {
                    console.error(`Unsupported file type for ${file.name}`);
                    totalPages -= 1; // Revert the page count for unsupported files
                    continue;
                }
                console.log(`Successfully processed: ${file.name}`);
            } catch (error) {
                console.error(`Error processing file ${file.name}:`, error);
                totalPages -= 1; // Revert the page count for failed files
            }
        }

        fileInput = null;
    }
    // async function handleFileUpload(event: Event): Promise<void> {
    //     const input = event.target as HTMLInputElement;
    //     if (!input.files || input.files.length === 0) return;
    //
    //     const files = Array.from(input.files);
    //     const initialPageCount = totalPages;
    //
    //     try {
    //         await Promise.all(files.map(async (file, index) => {
    //             const fileType = file.name.split(".").pop()?.toLowerCase();
    //             const pageNumber = initialPageCount + index + 1;
    //
    //             if (fileType === "txt") {
    //                 texts[pageNumber] = await readTextFile(file);
    //             } else if (fileType === "pdf") {
    //                 texts[pageNumber] = await readPdfFile(file);
    //             } else if (fileType === "docx") {
    //                 texts[pageNumber] = await readDocxFile(file);
    //             } else {
    //                 console.error(`Unsupported file type for ${file.name}`);
    //                 return;
    //             }
    //             console.log(`Successfully processed: ${file.name}`);
    //         }));
    //
    //         totalPages += files.length;
    //         currentPage = totalPages;
    //     } catch (error) {
    //         console.error("Error processing files:", error);
    //     }
    //
    //     fileInput = null;
    // }

    function addNewPage() {
        texts.push(""); // Add new empty string
        totalPages += 1;
        currentPage = totalPages; // Set to new page index
    }
    function prevPage(): void {
        currentPage -= 1;
    }
    function nextPage(): void {
        currentPage += 1;
    }
    function deleteCurrentPage() {
        totalPages -= 1;
        if (texts.length === 0) return; // Prevent errors if array is empty

        texts.splice(currentPage, 1);
        summaryResponses.splice(currentPage, 1);

        // Adjust currentPage to stay within bounds
        if (currentPage > texts.length) {
            currentPage = Math.max(1, texts.length); // Stay on the last available page
        }
        currentPage -= 1;
        currentPage = Math.max(1, currentPage);
    }
</script>

<div class="flex justify-center items-start gap-25 w-full">
    <div class="w-[90%] md:w-3/7">
        <div class="flex items-center gap-4 mb-4">  <!-- Flex container for all buttons -->
            <!-- Upload File Button (Original) -->
            <div class="w-full">  <!-- Full width container -->
                <!-- Label stays on top -->
                <Label for="picture">Enter Text to be Summarized OR</Label>

                <!-- Full-width flex container for buttons -->
                <div class="flex items-center w-full gap-2 mt-1.5">
                    <!-- Upload File Button - now flex-1 to grow -->
                    <Button variant="default" type="button" class="flex-1 flex items-center justify-center gap-2" onclick={triggerFileUpload}>
                        <Upload class="w-5 h-5" />
                        <span>Upload File</span>
                    </Button>

                    <!-- Arrow Buttons -->
                    <Button variant="outline" size="icon" disabled={currentPage === 1} onclick={prevPage} class="flex-none">
                        <ChevronLeft class="w-4 h-4" />
                    </Button>
                    <div class="text-sm font-medium px-2 py-1 bg-muted rounded-md">
                        Page {currentPage}/{totalPages}
                    </div>
                    <Button variant="outline" size="icon" disabled={currentPage === totalPages} onclick={nextPage} class="flex-none">
                        <ChevronRight class="w-4 h-4" />
                    </Button>

                    <!-- Create/Delete Buttons -->
                    <Button variant="outline" class="flex-1 flex items-center justify-center" onclick={addNewPage}>
                        <Plus class="w-4 h-4 mr-1" /> New Page
                    </Button>
                    <Button variant="outline" class="flex-1 flex items-center justify-center" disabled={totalPages === 1} onclick={deleteCurrentPage}>
                        <Trash2 class="w-4 h-4 mr-1" /> Delete
                    </Button>
                </div>
            </div>
        </div>

        <!-- Hidden File Input & Textarea (Unchanged) -->
        <Input id="text-file" type="file" accept=".docx,.pdf,.txt" multiple class="hidden" bind:value={fileInput} onchange={handleFileUpload} />
        <Textarea
            bind:value={texts[currentPage]}
            class="resize-none w-full h-[calc(100vh-18rem)] p-5"
            placeholder="Type your message here."
            id="message"
        />
    </div>

    <div class="hidden md:block w-[90%] md:w-3/7">
        <div class="flex items-center gap-2 mb-2">
            <div class="text-lg font-semibold">
                {#if summaryResponses && summaryResponses[currentPage]}
                    Summary of {summaryResponses[currentPage].topic}
                {:else}
                    Summary
                {/if}
            </div>
        </div>
        <div class="hidden md:block response-box w-full h-[calc(100vh-15.5rem)] border border-border rounded-md overflow-auto p-5">
            {#if isLoading}
                <span class="animate-pulse text-muted-foreground">Loading summary...</span>
            {:else if summaryResponses && summaryResponses[currentPage]}
                {@html summaryResponses[currentPage].summary.replace(/\n/g, '<br />')}
            {:else}
                Your summary will appear here...
            {/if}
        </div>
    </div>

</div>


<div class="fixed bottom-0 left-0 w-full flex items-center gap-2 p-2 bg-card">
    <div class="hidden md:block">
        <Drawer.Root>
            <div class="fixed bottom-[4.7rem] left-0 w-full flex justify-center">
                <Drawer.Trigger>
                    <Button variant="outline" class="max-w-150 h-7 flex items-center justify-center">
                        <ChevronUp class="w-5 h-5" />{getTemperatureLabel(llmTemp)} ({llmTemp}) |
                            {paragraphs === 0 ? "No Restrictions on Paragraphs" : paragraphs === 1 ? "1 Paragraph" : `${paragraphs} Paragraphs`} |
                            {sentences === 0 ? "No Restrictions on Sentences" : sentences === 1 ? "1 Sentence" : `${sentences} Sentences`}
                        <ChevronUp class="w-5 h-5" />
                    </Button>
                </Drawer.Trigger>
            </div>
            <Drawer.Content class="drawer-content pointer-events-auto bg-primary p-4">
                <div class="grid grid-cols-5 gap-4">
                    <!-- LLM Temperature Slider (3 Columns) -->
                    <div class="col-span-4 flex flex-col gap-2">
                        <label for="llm-temp" class="text-sm font-medium">How would you like your responses?</label>
                        <div class="flex flex-col items-center w-full">
                            <div class="flex justify-between w-full px-2">
                                <span class="font-bold text-sm text-blue-500">Objective</span>
                                <span class="absolute left-[21%] font-bold text-sm text-green-500">Balanced</span>
                                <span class="absolute left-[38.5%] font-bold text-sm text-yellow-500">Creative</span>
                                <span class="text-sm font-bold text-orange-500">Chaotic</span>
                            </div>
                            <Input
                                type="range"
                                id="llm-temp"
                                min="0"
                                max="2"
                                step="0.01"
                                bind:value={llmTemp}
                                class="w-full mt-1"
                                style="accent-color: {getTempColor(llmTemp)};"
                            />
                        </div>


                        <!-- Number Input Below the Slider -->
                        <Input
                            type="number"
                            id="llm-temp"
                            bind:value={llmTemp}
                            min="0"
                            max="2"
                            step="0.01"
                            class="w-full border rounded-md px-2 py-1 text-center"
                            onblur={validateTemp}
                        />
                    </div>

                    <!-- Paragraphs & Sentences Inputs -->
                    <div class="col-span-1 flex flex-col gap-2">
                        <label for="paragraphs" class="text-sm font-medium">Paragraphs (0 for No Restriction)</label>
                        <Input
                            type="number"
                            id="paragraphs"
                            bind:value={paragraphs}
                            min="0"
                            class="border rounded-md px-2 py-1"
                        />
                        <label for="sentences" class="text-sm font-medium">Sentences per Paragraph (0 for No Restriction)</label>
                        <Input
                            type="number"
                            id="sentences"
                            bind:value={sentences}
                            min="0"
                            class="border rounded-md px-2 py-1"
                        />
                    </div>
                </div>
                <Drawer.Footer>
                </Drawer.Footer>
            </Drawer.Content>
        </Drawer.Root>
    </div>
    <Textarea
            bind:value={additionalParams}
            class="flex-1 md:h-14 h-20 resize-none bg-card text-foreground border-border outline-none focus:outline-ring"
            placeholder="Enter additional requests for response (optional)..."
    />
    <Button variant="default" onclick={send} class="flex items-center gap-2" disabled={isLoading}>
        {#if isLoading}
            <Loader2 class="w-5 h-5 animate-spin" />
        {:else}
            Send
        {/if}
    </Button>
</div>