export interface Whisky {
    id?: number;
    name: string;
    distillery: string;
    country: string;
    region: string;
    age?: number;
    type: string;
    personal_note?: number;
    comments?: string;
    image?: string;
    date_added?: string;
    purchase_date?: Date;
    price?: number;
    volume: number;
    alcohol_degree: number;
}

// Create a new type for the image field that can be either string or File
type ImageField = string | File;

// Define WhiskyCreateUpdate by picking specific fields and overriding image type
export interface WhiskyCreateUpdate {
    name: string;
    distillery: string;
    country: string;
    region: string;
    age?: number;
    type: string;
    personal_note?: number;
    comments?: string;
    image?: ImageField;
    purchase_date?: Date;
    price?: number;
    volume: number;
    alcohol_degree: number;
}

export interface WhiskyExport {
    whiskies: Whisky[];
}