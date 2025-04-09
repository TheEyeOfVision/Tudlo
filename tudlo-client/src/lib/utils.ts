import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { getDocument, GlobalWorkerOptions } from "pdfjs-dist";
import type { TextItem } from "pdfjs-dist/types/src/display/api";
import pdfWorkerURL from "pdfjs-dist/build/pdf.worker.mjs?url";
import mammoth from "mammoth";

/**
 * Worker source for pdf.js
 */
GlobalWorkerOptions.workerSrc = pdfWorkerURL;


export function cn(...inputs: ClassValue[]) {
	return twMerge(clsx(inputs));
}


// FILE UPLOAD UTILS
/**
 * Reads the contents of a plain text file (.txt) and returns its content as a string.
 *
 * @param {File} file - The text file to read.
 * @returns {Promise<string>} A promise that resolves with the file content as a string.
 *                           If the file is not a valid text file or an error occurs, it rejects with an error message.
 *
 * @example
 * const file = new File(["Hello, world!"], "example.txt", { type: "text/plain" });
 * readTextFile(file).then(console.log).catch(console.error);
 */
export function readTextFile(file: File): Promise<string> {
	return new Promise((resolve, reject) => {
		const reader = new FileReader();

		reader.onload = (e) => {
			const result = e.target?.result;
			if (typeof result === "string") {
				resolve(result);
			} else {
				reject("File is not a text file or is unreadable.");
			}
		};

		reader.onerror = () => reject("Error reading file.");
		reader.readAsText(file);
	});
}

/**
 * Reads and extracts text content from a PDF file.
 *
 * @param {File} file - The PDF file to be read.
 * @returns {Promise<string>} A promise that resolves with the extracted text from the PDF.
 *                           If an error occurs, the promise rejects with an error message.
 *
 * @example
 * const pdfFile = new File([pdfData], "document.pdf", { type: "application/pdf" });
 * readPdfFile(pdfFile).then(console.log).catch(console.error);
 */
export async function readPdfFile(file: File): Promise<string> {
	return new Promise((resolve, reject) => {
		const reader = new FileReader();

		reader.onload = async (e) => {
			if (!e.target?.result) return reject("Failed to read file.");
			const typedArray = new Uint8Array(e.target.result as ArrayBuffer);

			try {
				const pdf = await getDocument({ data: typedArray }).promise;
				let textOutput = "";

				for (let i = 1; i <= pdf.numPages; i++) {
					const page = await pdf.getPage(i);
					const content = await page.getTextContent();

					// ✅ Type guard ensures we only process TextItem objects
					textOutput += content.items
						.filter((item): item is TextItem => "str" in item)
						.map((item) => item.str)
						.join(" ") + "\n";
				}

				resolve(textOutput);
			} catch (error) {
				reject(`Error reading PDF: ${error}`);
			}
		};

		reader.onerror = () => reject("Error loading file.");
		reader.readAsArrayBuffer(file);
	});
}

/**
 * Reads and extracts text content from a DOCX file.
 *
 * @param {File} file - The DOCX file to be read.
 * @returns {Promise<string>} A promise that resolves with the extracted text from the DOCX file.
 *                           If an error occurs, the promise rejects with an error message.
 *
 * @example
 * const docxFile = new File([docxData], "document.docx", { type: "application/vnd.openxmlformats-officedocument.wordprocessingml.document" });
 * readDocxFile(docxFile).then(console.log).catch(console.error);
 */
export async function readDocxFile(file: File): Promise<string> {
	return new Promise((resolve, reject) => {
		const reader = new FileReader();

		reader.onload = async (e) => {
			if (!e.target?.result) {
				return reject("Failed to read file.");
			}

			try {
				const result = await mammoth.extractRawText({
					arrayBuffer: e.target.result as ArrayBuffer
				});

				resolve(result.value.trim()); // Removes any extra spaces
			} catch (error) {
				reject(`Error reading DOCX: ${error}`);
			}
		};

		reader.onerror = () => reject("Error loading file.");
		reader.readAsArrayBuffer(file);
	});
}