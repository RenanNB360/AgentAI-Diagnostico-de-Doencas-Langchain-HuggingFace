from fastapi import APIRouter, HTTPException
from add_ons.db import get_patient, create_patient, update_patient, delete_patient, check_date, check_patient
from add_ons.models import User, UserUpdate
from add_ons.agent import get_disease

router = APIRouter()


@router.get('/register/select', response_model= User)
async def get_one_user():
    user_selected = await get_patient()
    if user_selected:
        return user_selected
    raise HTTPException(404, 'Patient not found')

@router.post('/register/create', response_model= User)
async def create_user(user: User):

    user_found = await check_patient(user.name)
    if user_found:
        raise HTTPException(409, 'Patient already have appointment')
    
    user_date = await check_date(user.date, user.time)
    if user_date:
        raise HTTPException(409, 'Appointment already exists')
    
    disease = await get_disease()
    user_data = user.model_dump()
    user_data['disease'] = disease

    create_user, _ = await create_patient(user_data)
    if create_user:
        return create_user
    raise HTTPException(400, 'Somenthing went wrong')

@router.put('/register/update', response_model= User)
async def update_user(user: UserUpdate):
    user_updated = await update_patient(user.model_dump())
    if user_updated:
        return user_updated
    raise HTTPException(404, 'Patient not found')

@router.delete('/register/delete')
async def delete_user():
    var = await delete_patient()
    if var:
        return 'Appointment was canceled'
    raise HTTPException(404, 'Patient not found')