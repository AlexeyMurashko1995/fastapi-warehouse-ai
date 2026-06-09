from sqlmodel import SQLModel, Field, Session, create_engine, Relationship, select, desc
from fastapi import FastAPI, HTTPException, Depends
import httpx
import os
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv('API_KEY')

app = FastAPI()

sql_file_name = 'delivery_service.db'
url = f'sqlite:///{sql_file_name}'

engine = create_engine(url)


class Hub(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    city: str
    parcels: list['Parcel'] = Relationship(back_populates='hub')


class HubRead(SQLModel):
    id: int
    name: str
    city: str


class HubCreate(SQLModel):
    name: str
    city: str


class Parcel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tracking_number: str
    weight: float
    description: str
    category: str | None = None
    hub_id: int = Field(foreign_key='hub.id')
    hub: 'Hub' = Relationship(back_populates='parcels')


class ParcelRead(SQLModel):
    id: int
    tracking_number: str
    weight: float
    description: str
    category: str | None
    hub_id: int


class ParcelCourierRead(SQLModel):
    id: int
    tracking_number: str
    description: str
    hub_id: int


class ParcelCreate(SQLModel):
    tracking_number: str
    weight: float
    description: str
    hub_id: int


def init_db():
    SQLModel.metadata.create_all(engine)
    print('Database created successfully')


def get_session():
    with Session(engine) as session:
        yield session


async def get_ai_category(description: str):
    prompt = f'You are an automated warehouse parcel sorter. Your task is to read the item description and strictly determine its category from the following list: electronics, clothes, food. If the item does not fit any category, return the word unknown. Write ONLY one category name in lowercase letters in the response, without dots, quotes, or any explanations. Item description: {description}'
    payload = {
        'model': 'mistral-small-latest',
        'messages': [
            {
                'role': 'user',
                'content': f'{prompt}'
            }
        ]
    }
    url = 'https://api.mistral.ai/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers, timeout=30.0)

        if response.status_code == 200:
            data = response.json()
            category = data['choices'][0]['message']['content'].strip()
            return category
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return 'unknown'
    except httpx.HTTPError:
        print("Network issue with Mistral API")
        return 'unknown'


@app.get('/hubs', response_model=list[HubRead])
def read_hubs_data(city: str | None=None, limit: int | None = 5, offset: int | None = 0, session: Session = Depends(get_session)):
    query = select(Hub)
    if city is not None:
        query = query.where(Hub.city == city)
    query = query.order_by(Hub.name).limit(limit).offset(offset)
    result = session.exec(query)
    all_hubs = result.all()
    return all_hubs


@app.get('/hubs/{hub_id}', response_model=HubRead)
def read_single_hub(hub_id: int, session: Session = Depends(get_session)):
    target_hub = session.get(Hub, hub_id)
    if target_hub is None:
        raise HTTPException(status_code=404, detail='Hub not found')
    return target_hub


@app.post('/hubs', response_model=HubRead)
def create_hub_endpoint(hub_in: HubCreate, session: Session = Depends(get_session)):
    db_hub = Hub(name=hub_in.name, city=hub_in.city)
    session.add(db_hub)
    session.commit()
    session.refresh(db_hub)
    return db_hub


@app.get('/parcels', response_model=list[ParcelRead])
def read_parcels_data(min_weight: float | None = None, max_weight: float | None = None, limit: int | None = 10, offset: int | None = 0, session: Session = Depends(get_session)):
    query = select(Parcel)
    if min_weight is not None:
        query = query.where(Parcel.weight >= min_weight)
    if max_weight is not None:
        query = query.where(Parcel.weight <= max_weight)
    result = session.exec(query.order_by(desc(Parcel.weight)).limit(limit).offset(offset))
    all_parcels = result.all()
    return all_parcels


@app.get('/parcels/{parcel_id}', response_model=ParcelRead)
def read_single_parcel(parcel_id: int, session: Session = Depends(get_session)):
    target_parcel = session.get(Parcel, parcel_id)
    if target_parcel is None:
        raise HTTPException(status_code=404, detail='Parcel not found')
    return target_parcel


@app.get('/parcels/{parcel_id_courier}/public', response_model=ParcelCourierRead)
def read_single_parcel_courier(parcel_id_courier: int, session: Session = Depends(get_session)):
    target_parcel_courier = session.get(Parcel, parcel_id_courier)
    if target_parcel_courier is None:
        raise HTTPException(status_code=404, detail='Parcel not found')
    return target_parcel_courier


@app.delete('/parcels/{parcel_id}')
def delete_single_parcel(parcel_id: int, session: Session = Depends(get_session)):
    target_parcel = session.get(Parcel, parcel_id)
    if target_parcel:
        session.delete(target_parcel)
        session.commit()
        return {'status': 'success', 'message': f'Parcel {parcel_id} deleted successfully'}
    else:
        raise HTTPException(status_code=404, detail='Parcel not found')


@app.post('/parcels', response_model=ParcelRead)
async def create_parcel_endpoint(parcel_in: ParcelCreate, session: Session = Depends(get_session)):
    parcel_db = Parcel(tracking_number=parcel_in.tracking_number, weight=parcel_in.weight, hub_id=parcel_in.hub_id, description=parcel_in.description)
    parcel_db.category = await get_ai_category(parcel_db.description)
    session.add(parcel_db)
    session.commit()
    session.refresh(parcel_db)
    return parcel_db


if __name__ == '__main__':
    init_db()