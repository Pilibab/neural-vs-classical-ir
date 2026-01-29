import { backend_port } from "../config";

export const getManhwaDetail = async (source: string, sourceId: string) => {
    const res = await fetch(`${backend_port}/api/manhwa/${source}/${sourceId}`);
    return res.json();
}