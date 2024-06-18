from datetime import datetime

from sqlalchemy import func

from crm.business_service.bases import CustomerBase
from crm.repository.models import CustomerModel, ImageModel, TagModel, NoteModel
from abc import ABC
from crm.repository.repository import Repository


class CustomerRepository(Repository, ABC):
    def __init__(self, session):
        self.session = session

    def list(self, user_id, limit=None, **filters):
        tags = filters.get('tags', [])
        search = filters.get('search', None)
        customers = []
        query = self.session.query(CustomerModel)
        query = query.filter(CustomerModel.owner_id == user_id)
        if tags:
            tags = [tag.lower() for tag in tags]
            query = (query.join(CustomerModel.tags)
                     .filter(func.lower(TagModel.name).in_(tags)))
        if search:
            query = query.filter(CustomerModel.fullname.ilike(f'%{search}%'))

        if limit:
            customers = query.limit(limit).all()
        else:
            customers = query.all()
        return [CustomerBase(**customer.dict()) for customer in customers]

    def _get(self, id, user_id):
        customer = (self.session.query(CustomerModel)
                    .filter(CustomerModel.id == id, CustomerModel.owner_id == user_id)
                    .first())
        if not customer:
            raise ValueError('Customer not found')
        return customer

    def get(self, id, user_id):
        customer = self._get(id, user_id)
        return CustomerBase(**customer.dict(), customer_=customer)

    def add(self, **payload: dict) -> CustomerBase:
        # check if customer phone is already in use
        customer = (self.session.query(CustomerModel)
                    .filter(CustomerModel.mobile_number1 == payload.get('mobile_number1')).first())
        if customer:
            raise ValueError('Customer login is already in use')

        photo = payload.pop('photo', None)
        tags = payload.pop('tags', [])
        notes = payload.pop('notes', [])

        customer = CustomerModel(**payload)

        if photo:
            image = ImageModel(**photo)
            image.main = False
            customer.photo = image

        # add tags
        for tag in tags:
            customer.tags.append(TagModel(**tag))

        # add notes
        for note in notes:
            created_date = note.pop('date', None)
            n = NoteModel(**note)
            n.created_date = created_date
            n.customer = customer
            customer.notes.append(n)

        # set important fields
        customer.status = 1  # active
        customer.date_created = datetime.now()
        self.session.add(customer)
        return CustomerBase(**customer.dict(), customer_=customer)

    def update(self, customer_id, user_id, **payload: dict) -> CustomerBase:
        customer = self._get(customer_id, user_id)

        # Photo:
        # delete photo if new photo is provided
        photo = payload.pop('photo', None)
        if photo:
            if customer.photo and photo.get('id', None):
                self.session.delete(customer.photo)
            image = ImageModel(**photo)
            image.main = False
            customer.photo = image

        # Tags:
        # delete tags that are not in payload
        for tag in customer.tags:
            if tag.id not in [t['id'] for t in payload.get('tags', [])]:
                customer.tags.remove(tag)
        # add new tags
        tags = payload.pop('tags', [])
        for tag in tags:
            if tag['id'] is None:
                customer.tags.append(TagModel(**tag))
            else:
                t = self.session.query(TagModel).filter(TagModel.id == tag['id']).first()
                if t is None:
                    raise ValueError(f'Tag not found with id {tag["id"]} ')
                customer.tags.append(t)

        # Notes:
        # delete notes that are not in payload
        for note in customer.notes:
            if note.id not in [n['id'] for n in payload.get('notes', [])]:
                customer.notes.remove(note)
        # add new notes
        notes = payload.pop('notes', [])
        for note in notes:
            if note['id'] is None:
                created_date = note.pop('date', None)
                n = NoteModel(**note)
                n.created_date = created_date
                n.customer = customer
                customer.notes.append(n)
            else:
                n = self.session.query(NoteModel).filter(NoteModel.id == note['id']).first()
                if n is None:
                    raise ValueError(f'Note not found with id {note["id"]} ')
                customer.notes.append(n)

        # update customer properties:
        for key, value in payload.items():
            setattr(customer, key, value)
        return CustomerBase(**customer.dict(), customer_=customer)

    def delete(self, customer_id):
        customer = self._get(customer_id)
        self.session.delete(customer)
        return None