import { backend_port } from "../config.ts";


export const getSimilarManhwa = async (synopsis: string) => {
    const res = await fetch(`${backend_port}/api/search`, {
        method:'post',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ synopsis }) // Pass it as an object
    })
    return await res.json()
} 