// Définir l'interface pour l'état d'une bouteille
export interface BottleState {
  id: number;
  is_opened: boolean;
  remaining_percentage: number;
}

// Type pour le champ image
type ImageField = string | File;

// Interface de base pour les propriétés communes
export interface WhiskyBase {
  name: string;
  distillery: string;
  country: string;
  region: string;
  age?: number;
  type: string;
  personal_note?: number;
  comments?: string;
  price?: number;
  volume: number;
  alcohol_degree: number;
  quantity?: number;
  bottles?: BottleState[];
  purchase_date?: string | Date;
}

// Interface principale pour un whisky
export interface Whisky extends WhiskyBase {
  id?: number;
  date_added?: string;
  image?: string;
}

// Interface pour la création/mise à jour
export interface WhiskyCreateUpdate extends WhiskyBase {
  image?: ImageField;
}

// Interface pour l'export
export interface WhiskyExport {
  whiskies: Whisky[];
}