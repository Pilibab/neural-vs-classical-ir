import { backend_port } from "../config.ts";

export const getManhwaDetail = async (source: string, sourceId: string) => {
    const res = await fetch(`${backend_port}/api/manhwa/${source}/${sourceId}`);
    return res.json();
}

export const getSimilarManhwa = async (synopsis: string) => {
    const res = await fetch(`${backend_port}/api/search`, {
        method:'post',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ synopsis }) // Pass it as an object
    })
    return await res.json()
} 