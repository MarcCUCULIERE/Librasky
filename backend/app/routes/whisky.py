from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
import base64
import json

from app.database import get_db
from app.models.whisky import Whisky
from app.schemas.whisky import WhiskyCreate, WhiskyUpdate, WhiskyResponse

router = APIRouter(
    prefix="/api/whiskies",
    tags=["whiskies"]
)

@router.get("/", response_model=List[WhiskyResponse])
async def read_whiskies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    whiskies = db.query(Whisky).offset(skip).limit(limit).all()
    return [whisky.to_dict() for whisky in whiskies]

# Ajouter la route d'export AVANT les routes avec paramètres
@router.get("/export", response_class=JSONResponse)
async def export_whiskies(db: Session = Depends(get_db)):
    whiskies = db.query(Whisky).all()
    whisky_list = [whisky.to_dict() for whisky in whiskies]
    
    export_data = {
        "version": "1.0",
        "export_date": str(date.today()),
        "whiskies": whisky_list
    }
    
    headers = {
        'Content-Disposition': 'attachment; filename="whiskies_export.json"'
    }
    
    return JSONResponse(
        content=export_data,
        headers=headers
    )

# Modifiez la route d'import
@router.post("/import")
async def import_whiskies(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        content = await file.read()
        data = json.loads(content.decode())
        
        if not isinstance(data, dict) or "whiskies" not in data:
            raise HTTPException(
                status_code=422,
                detail="Format invalide : le fichier doit contenir une clé 'whiskies'"
            )
        
        imported_count = 0
        for whisky_data in data["whiskies"]:
            # Nettoyage des données
            whisky_data.pop("id", None)
            whisky_data.pop("date_added", None)
            
            # Conversion de l'image base64 en bytes si présente
            if "image" in whisky_data and whisky_data["image"]:
                try:
                    whisky_data["image"] = base64.b64decode(whisky_data["image"])
                except:
                    raise HTTPException(
                        status_code=422,
                        detail=f"Format d'image invalide pour le whisky {imported_count + 1}"
                    )
            
            # Conversion de la date d'achat si présente
            if "purchase_date" in whisky_data and whisky_data["purchase_date"]:
                try:
                    whisky_data["purchase_date"] = datetime.strptime(
                        whisky_data["purchase_date"], 
                        "%Y-%m-%d"
                    ).date()
                except ValueError:
                    raise HTTPException(
                        status_code=422,
                        detail=f"Format de date invalide pour purchase_date: {whisky_data['purchase_date']}"
                    )
            
            try:
                new_whisky = Whisky(**whisky_data)
                db.add(new_whisky)
                imported_count += 1
            except Exception as e:
                raise HTTPException(
                    status_code=422,
                    detail=f"Erreur de validation pour le whisky {imported_count + 1}: {str(e)}"
                )
            
        db.commit()
        
        return {
            "message": f"Import réussi de {imported_count} whiskies",
            "count": imported_count
        }
        
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=422,
            detail="Le fichier n'est pas un JSON valide"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'import: {str(e)}"
        )

# Ensuite les routes avec paramètres
@router.get("/{whisky_id}", response_model=WhiskyResponse)
async def read_whisky(whisky_id: int, db: Session = Depends(get_db)):
    whisky = db.query(Whisky).filter(Whisky.id == whisky_id).first()
    if whisky is None:
        raise HTTPException(status_code=404, detail="Whisky not found")
    return whisky.to_dict()

@router.post("/", response_model=WhiskyResponse)
async def create_whisky(whisky_data: WhiskyCreate, db: Session = Depends(get_db)):
    whisky_dict = whisky_data.dict()
    if whisky_dict.get("image"):
        try:
            whisky_dict["image"] = base64.b64decode(whisky_dict["image"])
        except:
            raise HTTPException(status_code=400, detail="Invalid image format")
    
    whisky = Whisky(**whisky_dict)
    db.add(whisky)
    db.commit()
    db.refresh(whisky)
    return whisky.to_dict()

@router.put("/{whisky_id}", response_model=WhiskyResponse)
async def update_whisky(
    whisky_id: int,
    whisky_update: WhiskyUpdate,
    db: Session = Depends(get_db)
):
    whisky = db.query(Whisky).filter(Whisky.id == whisky_id).first()
    if not whisky:
        raise HTTPException(status_code=404, detail="Whisky not found")

    update_data = whisky_update.dict(exclude_unset=True)
    
    # Log pour déboguer
    print("Received update data:", update_data)
    
    # Assurez-vous que la date est au bon format
    if "purchase_date" in update_data and update_data["purchase_date"]:
        try:
            if isinstance(update_data["purchase_date"], str):
                update_data["purchase_date"] = datetime.strptime(
                    update_data["purchase_date"], 
                    "%Y-%m-%d"
                ).date()
        except ValueError as e:
            raise HTTPException(
                status_code=422, 
                detail=f"Invalid date format. Expected YYYY-MM-DD, got: {update_data['purchase_date']}"
            )

    for key, value in update_data.items():
        setattr(whisky, key, value)

    db.commit()
    db.refresh(whisky)
    return whisky.to_dict()

@router.delete("/{whisky_id}")
async def delete_whisky(whisky_id: int, db: Session = Depends(get_db)):
    whisky = db.query(Whisky).filter(Whisky.id == whisky_id).first()
    if not whisky:
        raise HTTPException(status_code=404, detail="Whisky not found")
    
    db.delete(whisky)
    db.commit()
    return {"message": "Whisky deleted successfully"}